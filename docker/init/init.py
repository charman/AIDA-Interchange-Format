import os
import logging
import boto3
import tarfile
import zipfile
import glob
import logging
import uuid
import shutil
from pathlib import Path
from enum import Enum
from botocore.exceptions import ClientError

class Task(Enum):
	one = 1
	two = 2
	three = 3

def download_and_extract_submission_from_s3(session, submission):
	"""Downloads submission from s3 and extracts contents to the working directory.
	Submissions must be an archive of .zip, .tar.gz, or .tgz.

	:param Session session: The boto3 session 
	:param str submission: The path of the submission on s3
	:raises ClientError: SQS client exception
	:raises Exception: No turtle (TTL) files extracted from s3 submission
	:returns: The directory of the extracted content
	:rtype: str
	"""
	s3_bucket, s3_object, file_name, file_ext = get_submission_paths(submission)

	uid = str(uuid.uuid4())

	# create directory for output
	if not os.path.exists(uid):
	    os.makedirs(uid)

	s3_client = session.client('s3')

	try:
	    logging.info("Downloading %s from bucket %s", s3_object, s3_bucket)
	    s3_client.download_file(s3_bucket, s3_object, file_name)
	    logging.info("Extracting %s", file_name)

	    # extract files
	    if file_ext == '.tgz' or file_ext == '.tar.gz':
	        # extract the contents of the .tar.gz
	        with tarfile.open(file_name) as tar:
	            tar.extractall(uid)
	    elif(file_ext == '.zip'):
	        zip_ref = zipfile.ZipFile(file_name, 'r')
	        zip_ref.extractall(uid)
	        zip_ref.close()

	    ttls_paths = (glob.glob(uid + '/**/*.ttl', recursive=True))
	    ttls = [ Path(x).name for x in ttls_paths ]

	    # if no ttl files extracted raise an exception
	    if len(ttls) <= 0 :
	        err = "No files with .ttl extension found in S3 submission {0}".format(file_name)
	        raise ValueError(err)

	    # check for duplicates
	    #if len(ttls) != len(set(ttls)):
	    #    err = "Duplicate files with .ttl extension found in S3 submission {0}".format(file_name)
	    #    raise ValueError(err)

	    return uid

	except ClientError as e:
	    logging.error(e)
	    raise
	except ValueError as e:
	    logging.error(e)
	    raise


def upload_file_to_s3(session, filepath, bucket, prefix=None):
    """Helper function to upload single file to S3 bucket with specified prefix

    :param str filepath: The local path of the file to be uploaded
    :param str bucket: The S3 bucket to upload file to
    :param str prefix: The prefix to be added to the file name
    :raises ClientError: S3 client exception
    """
    s3_client = session.client('s3')

    try:
        if prefix is not None:
            s3_object = '/'.join([prefix, Path(filepath).name])
        else:
            s3_object = Path(filepath).name

        logging.info("Uploading %s to bucket %s with prefix", s3_object, bucket)
        s3_client.upload_file(str(filepath), bucket, s3_object)

    except ClientError as e:
        logging.error(e)


def get_submission_paths(submission):
    """Helper function to extract s3 and file path information from s3 submission 
    path.

    :returns: 
        - s3_bucket - the extracted S3 bucket
        - s3_object - the extracted s3 object
        - file_name - the extracted file name including extension
        - file_ext - the extracted file extension
    :rtype: (str, str, str, str)
    """
    path = Path(submission)
    s3_bucket = path.parts[0]          
    s3_object = '/'.join(path.parts[1:])   
    file_name = path.name
    suffixes = path.suffixes
    file_ext = get_submission_extension(submission)

    return s3_bucket, s3_object, file_name, file_ext


def get_submission_extension(submission):
	"""Helper function to get the extension of the submission

	:param str submission: The full path of the submission on s3
	:returns: The submission extension
	:rtype: str
	"""
	path = Path(submission)
	suffixes = path.suffixes

	if len(suffixes) > 1 and suffixes[-1] == '.gz':
	    file_ext = "".join([suffixes[-2], suffixes[-1]])
	elif len(suffixes) > 1:
	    file_ext = suffixes[-1]
	elif len(suffixes) == 1:
	    file_ext = suffixes[0]

	return file_ext


def check_submission_extension(submission):
    """Helper function that checks the submission extension is valid before
    downloading archive from S3. Valid submissions can be archived as .tar.gz, 
    .tgz, or .zip. 

	:param str submission: The path of the submission
	:raises ValueError: The submission extension type is invalid
    """
    file_ext = get_submission_extension(submission)
    valid_ext = [".tar.gz", ".tgz", ".zip"]

    try:
        logging.info("Checking if submission %s is a valid archive type", submission)
        if file_ext not in valid_ext:
            raise ValueError("Submission {0} is not a valid archive type".format(submission))
    except ValueError as e:
        logging.error(e)
        raise


def get_submission_stem(submission):
	"""Function will return the stem of the submission accounting for the
	extension .tar.gz.

	:param str submission: The path of the submission on s3
	:returns: The stem of the submission
	:rtype: str
	"""
	path = Path(submission)
	stem = path.stem

	if get_submission_extension(submission) == '.tar.gz':
		return Path(stem).stem
	else:
		return stem


def get_task_type(stem):
	"""Function will determine the task type of the submission based on the naming 
	convention of the stem.

	:param str stem: The stem of the submission
	:returns The task type enum of the submission stems
	:rtype: Enum
	"""
	delim_count = stem.count('.')

	if delim_count == 0:
		return Task.one
	elif delim_count == 1:
		return Task.two
	elif delim_count == 2:
		return Task.three
	else:
		raise ValueError("Invalid submission format. Could not extract task type with submission stem %s", stem) 


def validate_and_upload(session, directory, task, bucket, prefix):
	"""Validates directory structure of task type and then uploads contents to s3. Will return a dictionary
	of the jobs that need to be executed on batch with their corresponding s3 locations.

	:param Session session: The boto3 session
	:param str directory: The local directory containing the donwloaded contents of
		the submission
	:param Task task: The task enum that representing the task type of the submission
	:param str bucket: The S3 bucket
	:param str prefix: The prefix to append to all objects uploaded to the S3 bucket
	:returns: List of dictionary objects representing the aws batch jobs that need to be executed
	:rtype: List
	"""
	logging.info("Validating submission as task type %s", task.value)
	task_type = str(task.value)
	jobs = []

	if task == Task.one or task == Task.two:

		# NIST direcotry required, do not upload INTER-TA if NIST does not exist
		if not check_nist_directory(directory):
			logging.error("Task 1 submission format is invalid. Could not locate NIST directory")
		else:
			jobs.append(upload_formatted_submission(session, directory, bucket, prefix, 'NIST'))

			# INTER-TA directory **not required**
			if check_inter_ta_directory(directory):
				jobs.append(upload_formatted_submission(session, directory, bucket, prefix, 'INTER-TA'))

		logging.info("AWS Batch jobs to be submitted: %s", jobs)
		return jobs

	elif task == Task.three:
		pass

	else:
		logging.error("Could not validate submission structure for invalid task %s", task)


def upload_formatted_submission(session, directory, bucket, prefix, validation_type):
	"""
	"""
	job = {}
	bucket_prefix = prefix + '-' + validation_type + '/UNPROCESSED'
	logging.info("Task 1 submission %s directory exists. Uploading .ttl files to %s", 
		validation_type, bucket + '/' + bucket_prefix)

	ttl_paths = (glob.glob(directory + '/' + validation_type + '/*.ttl', recursive=True))

	ttl_count = 0
	for path in ttl_paths:
		upload_file_to_s3(session, path, bucket, bucket_prefix)
		ttl_count = ttl_count + 1

	if ttl_count == 0:
		logging.error("No .ttl files found in Task 1 submission %s directory", validation_type)

	# create the batch job information
	job['validation_flag'] = validation_type
	job['count'] = ttl_count
	job['path'] = bucket + '/' + bucket_prefix
	return job
		


def check_nist_directory(directory):
	"""Helper function that will determine if NIST directory exists as an 
	immediate subdirectory of the passed in directory.

	:param str directory: The directory to validate against
	"""
	return os.path.exists(directory + "/NIST")


def check_inter_ta_directory(directory):
	"""Helper function that will determine if INTER-TA directory exists as
	an immediate subdirectory of the passed in directory.

	:param str directory: The directory to validate against
	"""
	return os.path.exists(directory + "/INTER-TA")

def main():

	# variables 
	aws_region = 'us-east-1'
	aws_bucket = 'aida-validation'

	# set logging to info
	logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

	submission = 'aida-validation/archives/NextCentury_1.zip'

	session = boto3.session.Session(region_name=aws_region)

	check_submission_extension(submission)
	stem = get_submission_stem(submission)
	logging.info("File stem for submission %s is %s", submission, stem)

	task = get_task_type(stem)
	staging_dir = download_and_extract_submission_from_s3(session, submission)

	# validate structure of submission and upload to S3 
	validate_and_upload(session, staging_dir, task, aws_bucket, stem)

	# remove staing directory and downloaded submission
	os.remove(Path(submission).name)
	shutil.rmtree(staging_dir)


if __name__ == "__main__": main()
