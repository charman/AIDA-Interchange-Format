package com.ncc.aif;

import org.apache.jena.rdf.model.Resource;

import java.util.Set;

import javafx.util.Pair;

/**
 * A domain ontology.
 */
interface OntologyMapping {
    Set<String> entityShortNames();
    Resource entityType(String ontology_type);

    Resource relationType(String relationName);
    Resource eventType(String eventName);
    Resource eventArgumentType(String argName);
    /**
     * Given a relation, get its two argument types in the same order as in LDC annotation.
     */
    Pair<Resource, Resource> relationArgumentTypes(Resource relation);

    /**
     * Is an object of this type allowed to have a name property?
     */
    boolean typeAllowedToHaveAName(Resource type);
    boolean typeAllowedToHaveTextValue(Resource type);
    boolean typeAllowedToHaveNumericValue(Resource type);
}