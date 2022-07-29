grammar HypergraphBasicElements;


// Graph node expr
graphnode: 'node' graphnode_expr;
graphnode_expr: graphnode_signature (graphnode_body)?;
graphnode_body: '{' subset_elem* '}';
graphnode_signature: ID;

common_subset_elem: parameters;

// Fields
field_double: FLOAT | ref_;
field_int: INT | ref_;
field_string: STRING | ref_;
field_float_vector: float_vector|ref_;
// Parameter subset
parameters: param_double | param_int | param_string | param_double_vector;
param_double:           ('double' ID '=' FLOAT);
param_double_vector:    ('vec' ID '=' float_vector);
param_int:              'int' ID '=' value_=INT;
param_string:           'string' ID '=' STRING;
vector_elem: float_vector | ref_;
float_vector:  '[' value ((',')? value)* ']';
multi_vector: '[' vector_elem ((',')? vector_elem)* ']';
// Axis
axis: '|' axis_=float_vector;

value: (ref_|FLOAT);

// Graph edge
graphedge: 'edge' graphedge_expr;
graphedge_signature: ID ':';
graphedge_expr: graphedge_signature '{' graphedge_relation (',' graphedge_relation)*'}';
graphedge_relation: (dir ref_ (optype=graphedge_relation_optype)?);
graphedge_relation_optype: (op='pairwise'|'single'|'full'|'union');

// Graph node body
subset_elem: graphnode | graphedge | common_subset_elem;

ref_     : '{' ID '}';
dir     : (out_dir OUT_DIR | in_dir IN_DIR | bi_dir BI_DIR);
out_dir : OUT_DIR;
OUT_DIR : '->';
in_dir: IN_DIR;
IN_DIR  : '<-';
bi_dir  : BI_DIR;
BI_DIR  : '--';


DECIMALS: [0-9]+;
ID      : [a-zA-Z_/]+DECIMALS*ID*;
INT     : [-]?DECIMALS+;
FLOAT   : [-]?DECIMALS+('.'DECIMALS)+?;
STRING  : '"'[a-zA-Z_/'-'0-9]*'"';

COMMENT : '//' .*? [\n] -> skip;
COMMENT_LONG: '/*' .*? '*/' -> skip;
// No regard of whitespace
WS      : [ \t\n\r]+ -> skip;