from rdflib import URIRef
from rdflib.namespace import ClosedNamespace

# TODO: change the ontology namespace to match the nist.gov ones in seedling-ontology.ttl
# TODO: temporarily extend these to include all ColdStart entity types - #2
# TODO: long-term, we need to make the program ontology configurable
"""
The domain ontology.

For the moment, this is hard-coded to match ColdStart
"""
AIDA_PROGRAM_ONTOLOGY = ClosedNamespace(
    uri=URIRef("http://nist.gov/ontologies/ColdstartOntology#"),
    terms=["Person", "Organization", "Location", "Facility", "GeopoliticalEntity", "String",
           # realis types
           "Actual", "Generic", "Other",
           # relation types
           "CONFLICT.ATTACK", "CONFLICT.DEMONSTRATE",
           "CONTACT.BROADCAST", "CONTACT.CONTACT", "CONTACT.CORRESPONDENCE", "CONTACT.MEET",
           "JUSTICE.ARREST-JAIL", "LIFE.DIE", "LIFE.INJURE", "MANUFACTURE.ARTIFACT",
           "MOVEMENT.TRANSPORT-ARTIFACT", "MOVEMENT.TRANSPORT-PERSON", "PERSONNEL.ELECT",
           "PERSONNEL.END-POSITION", "PERSONNEL.START-POSITION", "TRANSACTION.TRANSACTION",
           "TRANSACTION.TRANSFER-MONEY", "TRANSACTION.TRANSFER-OWNERSHIP", "children",
           "parents", "other_family", "parents", "children", "siblings", "spouse",
           "employee_or_member_of", "employees_or_members", "schools_attended", "students",
           "city_of_birth", "births_in_city", "stateorprovince_of_birth",
           "births_in_stateorprovince", "country_of_birth", "births_in_country",
           "cities_of_residence", "residents_of_city",
           "statesorprovinces_of_residence", "residents_of_stateorprovince",
           "countries_of_residence", "residents_of_country",
           "city_of_death", "deaths_in_city",
           "stateorprovince_of_death", "deaths_in_stateorprovince",
           "country_of_death", "deaths_in_country",
           "shareholders", "holds_shares_in",
           "founded_by", "organizations_founded",
           "top_members_employees", "top_member_employee_of",
           "members", "member_of", "subsidiaries",
           "city_of_headquarters", "headquarters_in_city",
           "stateorprovince_of_headquarters", "headquarters_in_stateorprovince",
           "country_of_headquarters", "headquarters_in_country",
           "alternate_names", "alternate_names", "date_of_birth",
           "political_religious_affiliation", "age", "number_of_employees_members",
           "origin", "date_founded", "date_of_death", "date_dissolved",
           "cause_of_death", "website", "title", "religion", "charges"])

AIDA_PROGRAM_ONTOLOGY_LUT = {
    "PER": AIDA_PROGRAM_ONTOLOGY.Person, "ORG": AIDA_PROGRAM_ONTOLOGY.Organization,
    "GPE": AIDA_PROGRAM_ONTOLOGY.GeopoliticalEntity, "LOC": AIDA_PROGRAM_ONTOLOGY.Location,
    "FAC": AIDA_PROGRAM_ONTOLOGY.Facility, "STRING": AIDA_PROGRAM_ONTOLOGY.String,
    "String": AIDA_PROGRAM_ONTOLOGY.String,
    # relations
    "age": AIDA_PROGRAM_ONTOLOGY.age,
    "alternate_names": AIDA_PROGRAM_ONTOLOGY.alternate_names,
    "births_in_city": AIDA_PROGRAM_ONTOLOGY.births_in_city,
    "births_in_country": AIDA_PROGRAM_ONTOLOGY.births_in_country,
    "births_in_stateorprovince": AIDA_PROGRAM_ONTOLOGY.births_in_stateorprovince,
    "cause_of_death": AIDA_PROGRAM_ONTOLOGY.cause_of_death,
    "charges": AIDA_PROGRAM_ONTOLOGY.charges,
    "children": AIDA_PROGRAM_ONTOLOGY.children,
    "cities_of_residence": AIDA_PROGRAM_ONTOLOGY.cities_of_residence,
    "city_of_birth": AIDA_PROGRAM_ONTOLOGY.city_of_birth,
    "city_of_death": AIDA_PROGRAM_ONTOLOGY.city_of_death,
    "city_of_headquarters": AIDA_PROGRAM_ONTOLOGY.city_of_headquarters,
    "CONFLICT.ATTACK": AIDA_PROGRAM_ONTOLOGY['CONFLICT.ATTACK'],
    "CONFLICT.DEMONSTRATE": AIDA_PROGRAM_ONTOLOGY['CONFLICT.DEMONSTRATE'],
    "CONTACT.BROADCAST": AIDA_PROGRAM_ONTOLOGY['CONTACT.BROADCAST'],
    "CONTACT.CONTACT": AIDA_PROGRAM_ONTOLOGY['CONTACT.CONTACT'],
    "CONTACT.CORRESPONDENCE": AIDA_PROGRAM_ONTOLOGY['CONTACT.CORRESPONDENCE'],
    "CONTACT.MEET": AIDA_PROGRAM_ONTOLOGY['CONTACT.MEET'],
    "countries_of_residence": AIDA_PROGRAM_ONTOLOGY.countries_of_residence,
    "country_of_birth": AIDA_PROGRAM_ONTOLOGY.country_of_birth,
    "country_of_death": AIDA_PROGRAM_ONTOLOGY.country_of_death,
    "country_of_headquarters": AIDA_PROGRAM_ONTOLOGY.country_of_headquarters,
    "date_dissolved": AIDA_PROGRAM_ONTOLOGY.date_dissolved,
    "date_founded": AIDA_PROGRAM_ONTOLOGY.date_founded,
    "date_of_birth": AIDA_PROGRAM_ONTOLOGY.date_of_birth,
    "date_of_death": AIDA_PROGRAM_ONTOLOGY.date_of_death,
    "deaths_in_city": AIDA_PROGRAM_ONTOLOGY.deaths_in_city,
    "deaths_in_country": AIDA_PROGRAM_ONTOLOGY.deaths_in_country,
    "deaths_in_stateorprovince": AIDA_PROGRAM_ONTOLOGY.deaths_in_stateorprovince,
    "employee_or_member_of": AIDA_PROGRAM_ONTOLOGY.employee_or_member_of,
    "employees_or_members": AIDA_PROGRAM_ONTOLOGY.employees_or_members,
    "founded_by": AIDA_PROGRAM_ONTOLOGY.founded_by,
    "headquarters_in_city": AIDA_PROGRAM_ONTOLOGY.headquarters_in_city,
    "headquarters_in_country": AIDA_PROGRAM_ONTOLOGY.headquarters_in_country,
    "headquarters_in_stateorprovince": AIDA_PROGRAM_ONTOLOGY.headquarters_in_stateorprovince,
    "holds_shares_in": AIDA_PROGRAM_ONTOLOGY.holds_shares_in,
    "JUSTICE.ARREST-JAIL": AIDA_PROGRAM_ONTOLOGY['JUSTICE.ARREST-JAIL'],
    "LIFE.DIE": AIDA_PROGRAM_ONTOLOGY['LIFE.DIE'],
    "LIFE.INJURE": AIDA_PROGRAM_ONTOLOGY['LIFE.INJURE'],
    "MANUFACTURE.ARTIFACT": AIDA_PROGRAM_ONTOLOGY['MANUFACTURE.ARTIFACT'],
    "member_of": AIDA_PROGRAM_ONTOLOGY.member_of,
    "members": AIDA_PROGRAM_ONTOLOGY.members,
    "MOVEMENT.TRANSPORT-ARTIFACT": AIDA_PROGRAM_ONTOLOGY['MOVEMENT.TRANSPORT-ARTIFACT'],
    "MOVEMENT.TRANSPORT-PERSON": AIDA_PROGRAM_ONTOLOGY['MOVEMENT.TRANSPORT-PERSON'],
    "number_of_employees_members": AIDA_PROGRAM_ONTOLOGY.number_of_employees_members,
    "organizations_founded": AIDA_PROGRAM_ONTOLOGY.organizations_founded,
    "origin": AIDA_PROGRAM_ONTOLOGY.origin,
    "other_family": AIDA_PROGRAM_ONTOLOGY.other_family,
    "parents": AIDA_PROGRAM_ONTOLOGY.parents,
    "PERSONNEL.ELECT": AIDA_PROGRAM_ONTOLOGY['PERSONNEL.ELECT'],
    "PERSONNEL.END-POSITION": AIDA_PROGRAM_ONTOLOGY['PERSONNEL.END-POSITION'],
    "PERSONNEL.START-POSITION": AIDA_PROGRAM_ONTOLOGY['PERSONNEL.START-POSITION'],
    "political_religious_affiliation": AIDA_PROGRAM_ONTOLOGY.political_religious_affiliation,
    "religion": AIDA_PROGRAM_ONTOLOGY.religion,
    "residents_of_city": AIDA_PROGRAM_ONTOLOGY.residents_of_city,
    "residents_of_country": AIDA_PROGRAM_ONTOLOGY.residents_of_country,
    "residents_of_stateorprovince": AIDA_PROGRAM_ONTOLOGY.residents_of_stateorprovince,
    "schools_attended": AIDA_PROGRAM_ONTOLOGY.schools_attended,
    "shareholders": AIDA_PROGRAM_ONTOLOGY.shareholders,
    "siblings": AIDA_PROGRAM_ONTOLOGY.siblings,
    "spouse": AIDA_PROGRAM_ONTOLOGY.spouse,
    "stateorprovince_of_birth": AIDA_PROGRAM_ONTOLOGY.stateorprovince_of_birth,
    "stateorprovince_of_death": AIDA_PROGRAM_ONTOLOGY.stateorprovince_of_death,
    "stateorprovince_of_headquarters": AIDA_PROGRAM_ONTOLOGY.stateorprovince_of_headquarters,
    "statesorprovinces_of_residence": AIDA_PROGRAM_ONTOLOGY.statesorprovinces_of_residence,
    "students": AIDA_PROGRAM_ONTOLOGY.students,
    "subsidiaries": AIDA_PROGRAM_ONTOLOGY.subsidiaries,
    "title": AIDA_PROGRAM_ONTOLOGY.title,
    "top_member_employee_of": AIDA_PROGRAM_ONTOLOGY.top_member_employee_of,
    "top_members_employees": AIDA_PROGRAM_ONTOLOGY.top_members_employees,
    "TRANSACTION.TRANSACTION": AIDA_PROGRAM_ONTOLOGY['TRANSACTION.TRANSACTION'],
    "TRANSACTION.TRANSFER-MONEY": AIDA_PROGRAM_ONTOLOGY['TRANSACTION.TRANSFER-MONEY'],
    "TRANSACTION.TRANSFER-OWNERSHIP": AIDA_PROGRAM_ONTOLOGY['TRANSACTION.TRANSFER-OWNERSHIP'],
    "website": AIDA_PROGRAM_ONTOLOGY.website}

AIDA_ANNOTATION = ClosedNamespace(
    uri=URIRef("http://www.isi.edu/aida/interchangeOntology#"),
    terms=[
      # Classes
      'AudioJustification',
      'BoundingBox',
      'ClusterMembership',
      'Confidence',
      'Entity',
      'Event',
      'Hypothesis',
      'ImageJustification',
      'KeyFrameVideoJustification',
      'LinkAssertion',
      'MutualExclusion',
      'MutualExclusionAlternative',
      'PrivateData',
      'SameAsCluster',
      'ShotVideoJustification',
      'Subgraph',
      'System',
      'TextJustification',
      # Properties
      'alternativeGraph',
      'alternative',
      'boundingBox',
      'boundingBoxUpperLeftX',
      'boundingBoxUpperLeftY',
      'boundingBoxLowerRightX',
      'boundingBoxLowerRightY',
      'cluster',
      'clusterMember',
      'confidence',
      'confidenceValue',
      'dependsOnHypothesis',
      'endOffsetInclusive',
      'endTimestamp',
      'subgraphContains',
      'hypothesisContent',
      'jsonContent',
      'justifiedBy',
      'keyFrame',
      'link',
      'linkTarget',
      'noneOfTheAbove',
      'privateData',
      'prototype',
      'shot',
      'source',
      'startOffset',
      'startTimestamp',
      'subgraphContains',
      'system'])
