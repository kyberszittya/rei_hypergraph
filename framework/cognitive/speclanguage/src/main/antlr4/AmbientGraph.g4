grammar AmbientGraph;

import HypergraphBasicElements, GeometryElements;

// Ambient elements
ambient: 'ambient' graphnode_signature ambient_graph_body;
ambient_element_signature: ID;
// Ambient body
ambient_graph_body: '{' (ambient_element)* '}';
// Ambient elements
ambient_element: actuator | sensor | ambient | ambience_edge | kinematic | port | sensor_placement;
// Derived ambient elements
// Actuators
actuator: 'actuator' ambient_element_signature '{'
    (parameters_=parameters)*
'}';
// Sensors
sensor: 'sensor' ambient_element_signature sensor_type '{'
    (parameters_=parameters)*
'}';
ambience_edge: 'ambience' graphedge_signature ambience_edge_body (',' ambience_edge_body)*;
ambience_edge_body: (communication_connections)+;
sensor_placement: 'placement' graphedge_signature '{' (ambience_placement_element)* '}';
ambience_placement_element: ambience_base_reference|element_placement_relation|ambience_placement_reference_port;
ambience_placement_reference_port: 'port' direction=('->'|'--'|'<-') port_ref_=ref_;
ambience_base_reference: 'ambience' direction_='->' ambience_base_=ref_;

sensor_basic_definition: sensor_type (sensor_basic_definition_parameters)*;
sensor_basic_definition_parameters: precision_parameter|accuracy_parameter|variance_parameter;
precision_parameter: 'precision' field_double;
accuracy_parameter: 'accuracy' field_double;
variance_parameter: 'variance' field_double;
sensor_type: proprioceptive_sensor | exteroceptive_sensor;

element_placement_relation: geom_relation;
geom_relation: 'at' direction=('->'|'<-'|'--') referenced_element_=ref_ (transformation_=rigid_transformation)?;

// Proprioceptive sensor can be assigned to a specific ambience relation of the system
proprioceptive_sensor: prop_sensor_type;
prop_sensor_type: 'imu'|'encoder'|'force'|STRING;
// Exteroceptive sensor obtains data outside the context of the system
exteroceptive_sensor: ext_sensor_type;
ext_sensor_type: 'gnss'|matrix_sensor|STRING;
matrix_sensor: 'visual'|'laserarray'|'mat' matrix_sensor_type_=STRING;
// Communication port elements
communication_connections: (optype=graphedge_relation_optype)? 'comm' direction=('->'|'<-'|'--') comm_type=communication_type ref_;
communication_type: ambient_signal | ambient_stream;
communication_connection_msg: STRING;
ambient_signal: 'signal';
ambient_stream: 'stream';
// Communication port (node)
port_signature: 'port' graphnode_signature ':' topic_name=STRING '(' msg=communication_connection_msg ')' ;
port: port_signature '{' (parameters_=parameters)*  '}';

//
