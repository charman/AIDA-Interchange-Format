# AIDA Interchange Format (AIF)

This repository contains resources to support the AIDA Interchange Format (AIF).  It consists of:

*    a formal representation of the format in terms of an OWL ontology in `src/main/resources/com/ncc/aif/ontologies/InterchangeOntology`.
     This ontology can be validated using the SHACL constraints file in
     `src/main/resources/com/ncc/aif/aida_ontology.shacl`.

*    utilities to make it easier to work with this format.  Java utilities are
     in `src/main/java/com/ncc/aif/AIFUtils.java`, which can be used by adding
     a Maven dependency on `com.ncc:aida-interchange:1.0.0-SNAPSHOT`.  A
     Python translation of these utilities is in
     `python/aida_interchange/aifutils.py`.
	 
*    examples of how to use AIF. These are given in Java in the unit tests under
     `src/test/java/com/ncc/aif/ExamplesAndValidationTests`.  A Python
     translation of these examples is in `python/tests/Examples.py`.  If you run either set of
     examples, the corresponding Turtle output will be dumped.
	 
We recommend using Turtle format for AIF when working with single document files (for
readability) but N-Triples for working with large KBs (for speed).

# Installation

* To install the Java code, do `mvn install` from the root of this repository using Apache Maven.
Repeat this if you pull an updated version of the code. You can run the tests,
which should output the examples, by doing `mvn test`.
* The Python code is not currently set up for installation; just add `AIDA-Interchange-Format/python` to your `PYTHONPATH`.

# Using the AIF Library

To use the library in Java, include the library generated by the
installation above into your build script or tool.  For gradle, for
example, include the following in the dependencies in your `build.gradle` file:

`dependencies {
    compile 'com.ncc:aida-interchange:1.0-SNAPSHOT'
}`

In your code, import classes from the `com.ncc.aif` package.
Then, create a model, add entities, relations, and events to the
model, and then write the model out.

The file `src/test/java/com/ncc/aif/ExamplesAndValidationTests.java`
has a series of examples showing how to add things to the model.  The
`src/text/java/com/ncc/aif/ScalingTest.java` file has examples of how
to write the model out.

# The AIF Validator
The AIF validator is an extension of the validator written by Ryan Gabbard (USC ISI)
and converted to Java by Next Century.  This version of the validator accepts multiple
ontology files, can validate against NIST requirements (restricted AIF), and can
validate N files or all files in a specified directory.

### Running the AIF validator
To run the validator from the command line, run `target/appassembler/bin/validateAIF`
with a series of command-line arguments (in any order) honoring the following usage:  <br>
Usage:  <br>
`validateAIF { --ldc | --program | --ont FILE ...} [--nist] [--nist-ta3] [-o] [-h | --help] [--abort [num]] {-f FILE ... | -d DIRNAME}`  <br>

| Switch | Description |
| ----------- | ----------- |
|`--ldc`    | validate against the LDC ontology |
|`--program`| validate against the program ontology |
|`--ont FILE ...` | validate against the OWL-formatted ontolog(ies) at the specified filename(s) |
|`--nist` | validate against the NIST restrictions |
|`--nist-ta3` | validate against the NIST hypothesis restrictions (implies `--nist`) |
|`-o` | Save validation report model to a file.  `KB.ttl` would result in `KB-report.txt`. Output defaults to stderr. |
|`-h, --help` | This help and usage text |
|`--abort [num]` | Abort validation after `[num]` SHACL violations (num > 2), or three violations if `[num]` is omitted. |
|`-f FILE ...` | validate the specified file(s) with a `.ttl` suffix |
|`-d DIRNAME` | validate all `.ttl` files in the specified directory |

Either a file (-f) or a directory (-d) must be specified (but not both).  <br>
Exactly one of --ldc, --program, or --ont must be specified.  <br>
Ontology files can be found in `src/main/resources/com/ncc/aif/ontologies`:
- LDC (LO): `LDCOntology`
- Program (AO): `EntityOntology`, `EventOntology`, `RelationOntology`

### Validator return values
Return values from the command-line validator are as follows:
* `0 (Success)`.  There were no validation (or any other) errors.
* `1 (Validation Error)`.	All specified files were validated but at least one failed validation.  Supersedes a File Error.
* `2 (Usage Error)`.  There was a problem interpreting command-line arguments.  No validation was performed.
* `3 (File Error)`.  A file was rejected or couldn't be validated, either due to an I/O error, a validation engine error,
  or because it didn't meet certain criteria.  Logging indicates the nature of the problem(s).  Validation may
  have been performed on a subset of specified KBs.  If there is an error loading any ontologies or SHACL files,
  then no validation is performed.

### Running the validator in code
To run the validator programmatically in Java code, first use one of the public `ValidateAIF.createXXX()`
methods to create a validator object, then call one of the public `validateKB()` methods.
`createForLDCOntology()` and `createForProgramOntology()` are convenience wrappers for `create()`, which
is flexible enough to take a Set of ontologies.  All creation methods accept a flag for validating
against restricted AIF.  See the JavaDocs.

Note: the original `ValidateAIF.createForDomainOntologySource()` method remains for backward compatibility.

### Failing fast

The AIF Validator can be told to "fail fast," that is, exit as soon as a few SHACL violations are found in
the specified KB.  On the command-line, use the `--abort` option to have the validator exit after three
violations.  Specify a number after the `--abort` flag to exit after that number of violations.  The validation
summary will display the number of aborted validations-- but if your file has the exact number of violations as
the threshold, it will still be counted as an aborted validation.

**NOTE**: As of this writing, if you set the threshold too low (less than 3), the validator might erroneously return
that your KB is *valid*.  This appears to be a current bug or limitation in the TopBraid shacl library snapshot.
Consequently, the command-line validator will reject thresholds less than 3.

Without the `--abort` option, the entire KB will be validated with full output of all violations.

To fail fast when using the validator programmatically, use `ValidateAIF.setAbortThreshold()` to set an error
threshold.

# Running the Ontology Resource Generator

To generate the resource variables from a particular ontology file, please refer to 
the README located at `src/main/java/com/ncc/aif/ont2javagen/README.md`.

# Additional Information about Individual Ontologies

There is another README located at `src/main/resources/com/ncc/aif/ontologies/README.md` that gives a description about each of the ontology files currently available in AIF.

# Developing

If you need to edit the Java code:
 1. Install IntelliJ IDEA.
 2. "Import Project from Existing Sources"
 3. Choose the `pom.xml` for this repository and accept all defaults.

You should now be ready to go.

# Documentation

### Java

To generate the javadoc documentation, navigate to the top level directory in the AIDA-Interchange-Format project. Run the following command:

```bash
$ javadoc -d build/docs/javadoc/ src/main/java/com/ncc/aif/*.java
```
This script will generate documentation in the form of HTML and place it within the `build/docs/javadoc` folder.

### Python

The python project uses [Sphinx](http://www.sphinx-doc.org/en/master/) for generating documentation. To generate the documentation, navigate to the `python/docs` directory and run the `update_documentation.sh` script.

```bash
$ ./update_documentation.sh
```
This script will generate documentation in the form of HTML and place it within the `python/docs/build/html` folder. 

# FAQ

Please see `FAQ.md` for frequently asked questions.

# Contact

AIF was designed by Ryan Gabbard (gabbard@isi.edu) and Pedro Szekely
(pszekeley@isi.edu) of USC ISI.  Gabbard also wrote the initial
implementations of the associated tools.  The tools are now supported
and extended by Eddie Curley (eddie.curley@nextcentury.com), Bao Pham
(bao.pham@nextcentury.com), Craig Warsaw (craig.warsaw@nextcentury.com),
and Darren Gemoets (darren.gemoets@nextcentury.com) of Next Century.

The open repository will support an open NIST evaluation. For
questions related to this evaluation, please contact Hoa Dang
(hoa.dang@nist.gov).

# Legal Stuff

This material is based on research sponsored by DARPA under agreement
number FA8750-18- 2-0014 and FA875018C0010-HR0011730814.  The
U.S. Government is authorized to reproduce and distribute reprints for
Governmental purposes notwithstanding any copyright notation thereon.

The views and conclusions contained herein are those of the authors
and should not be interpreted as necessarily representing the official
policies or endorsements, either expressed or implied, of DARPA or the
U.S. Government.

The AIF repository has been approved by DARPA for public release under
Distribution Statement "A" (Approved for Public Release, Distribution
Unlimited).
