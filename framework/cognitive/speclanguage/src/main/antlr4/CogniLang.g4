grammar CogniLang;

import HypergraphBasicElements, GeometryElements, HypergraphTemplates, AmbientGraph;

rootnode: entity;

entity_subset_elem: entity_edges | entity_nodes | common_subset_elem | template_instantiation | graphnode | graphedge;

entity_edges: joint;
entity_nodes: ambient | kinematic | parametric;
// Cognitive entity with ambient and physical description
entity: 'entity' graphnode_signature '{' (entity_subset_elem)* '}';
// Parametric
parametric: 'parameters' '{' parameter* '}';
parameter: name=ID '=' parameter_value=(ID|FLOAT|INT);
