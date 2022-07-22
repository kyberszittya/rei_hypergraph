grammar GeometryElements;

import HypergraphBasicElements;


// Rigid Transformation:
rigid_transformation: '[' float_vector (',')?  rotation?']';  // Rotation
rotation: (rot_type=('d'|'r'))?(float_vector);
// Kinematic node
kinematic: 'kinematic' graphnode_signature kinematicnode_body;
// Body of each kinematic element
kinematicnode_body: '{' (link|joint|kinematic|geometrictemplate|geometricoperation)* '}';
// Derived kinematic elements
// Link
link: (root_link='root')?'link' graphnode_signature ('@' pose=rigid_transformation)? (linknode_body)?;
linknode_body: '{' inertia_body (visual_node|collision_node)* '}';
// Inertia element
inertia_body: 'inertia' '{' 'mass' mass=FLOAT (inertia_vector)? '}';
inertia_vector: 'inertia' inertia_vector_=field_float_vector;
// Link elements (geometry)
visual_node: 'visual' (ID)? material? geometry_body;
material: '(' 'material' material_name=ID ')';
collision_node: 'collision' (ID)? geometry_body;
// Link elements (geometry body)
geometry_body: '{' geometries '}';
// Geometry types
geometries: cylinder_geometry | polyhedron_geometry | mesh_geometry | ellipsoid_geometry | ref_;
cylinder_geometry: 'cylinder' (ID)? field_float_vector;
polyhedron_geometry: 'polyhedron' (ID)? field_float_vector;
ellipsoid_geometry: 'ellipsoid' (ID)? field_float_vector;
mesh_geometry: 'mesh' (ID)? field_float_vector;
// Joint
joint: 'joint' graphedge_signature joint_body;
joint_body: (joint_relation)+;
joint_relation: type=joint_type direction=('->'|'<-'|'--') ref_ rigid_transformation? axis?;
joint_type: value_=('fix'|'rev'|'tr');
// Templating (as an edge operation)
geometrictemplate: graphedge_signature ref_ joint_relation;
// Different geometric operations
geometricoperation: geometricmirror;

geometricmirror: 'mirror' graphedge_signature ref_ OUT_DIR ref_;