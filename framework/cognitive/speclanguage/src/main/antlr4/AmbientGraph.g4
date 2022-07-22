grammar AmbientGraph;

import HypergraphBasicElements, GeometryElements;

// Ambient elements
ambient: 'ambient' graphnode_signature ambient_graph_body;
ambient_element_signature: ID;
// Ambient body
ambient_graph_body: '{' (ambient_element)* '}';
// Ambient elements
ambient_element: actuator | sensor | ambient | ambience_relation | kinematic;
// Derived ambient elements
// Actuators
actuator: 'actuator' ambient_element_signature OUT_DIR joint_ref=ref_ '{'
    (communication_elements)*
'}';
// Sensors
sensor: 'sensor' ambient_element_signature OUT_DIR link_ref=ref_ '{'
    sensor_basic_definition (communication_elements)*
'}';

sensor_basic_definition: sensor_type (sensor_basic_definition_parameters)*;
sensor_basic_definition_parameters: precision_parameter|accuracy_parameter|variance_parameter;
precision_parameter: 'precision' field_double;
accuracy_parameter: 'accuracy' field_double;
variance_parameter: 'variance' field_double;
sensor_type: proprioceptive_sensor | exteroceptive_sensor;

ambience_relation: 'ambience' graphedge_signature (element_placement_relation)*;
element_placement_relation: geom_relation;
geom_relation: 'link' ref_;

// Proprioceptive sensor can be assigned to a specific ambience relation of the system
proprioceptive_sensor: prop_sensor_type IN_DIR ID;
prop_sensor_type: 'imu'|'encoder'|'force';
// Exteroceptive sensor obtains data outside the context of the system
exteroceptive_sensor: ext_sensor_type;
ext_sensor_type: 'gnss'|matrix_sensor;
matrix_sensor: 'visual'|'laserarray';
// Communication port elements
communication_elements: comm_type=communication_type graphedge_signature dir topic_name=STRING msg=communication_connection_msg;
communication_type: ambient_signal | ambient_stream;
communication_connection_msg: ':' STRING;
ambient_signal: 'signal';
ambient_stream: 'stream';