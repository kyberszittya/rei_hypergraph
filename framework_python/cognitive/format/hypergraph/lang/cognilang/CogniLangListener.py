# Generated from D:\Haizu\robotics_ws\cogni_ws\rei_ws\rei\framework\cognitive\speclanguage\src\main\antlr4\CogniLang.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CogniLangParser import CogniLangParser
else:
    from CogniLangParser import CogniLangParser

# This class defines a complete listener for a parse tree produced by CogniLangParser.
class CogniLangListener(ParseTreeListener):

    # Enter a parse tree produced by CogniLangParser#rootnode.
    def enterRootnode(self, ctx:CogniLangParser.RootnodeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#rootnode.
    def exitRootnode(self, ctx:CogniLangParser.RootnodeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#entity_subset_elem.
    def enterEntity_subset_elem(self, ctx:CogniLangParser.Entity_subset_elemContext):
        pass

    # Exit a parse tree produced by CogniLangParser#entity_subset_elem.
    def exitEntity_subset_elem(self, ctx:CogniLangParser.Entity_subset_elemContext):
        pass


    # Enter a parse tree produced by CogniLangParser#entity_edges.
    def enterEntity_edges(self, ctx:CogniLangParser.Entity_edgesContext):
        pass

    # Exit a parse tree produced by CogniLangParser#entity_edges.
    def exitEntity_edges(self, ctx:CogniLangParser.Entity_edgesContext):
        pass


    # Enter a parse tree produced by CogniLangParser#entity_nodes.
    def enterEntity_nodes(self, ctx:CogniLangParser.Entity_nodesContext):
        pass

    # Exit a parse tree produced by CogniLangParser#entity_nodes.
    def exitEntity_nodes(self, ctx:CogniLangParser.Entity_nodesContext):
        pass


    # Enter a parse tree produced by CogniLangParser#entity.
    def enterEntity(self, ctx:CogniLangParser.EntityContext):
        pass

    # Exit a parse tree produced by CogniLangParser#entity.
    def exitEntity(self, ctx:CogniLangParser.EntityContext):
        pass


    # Enter a parse tree produced by CogniLangParser#parametric.
    def enterParametric(self, ctx:CogniLangParser.ParametricContext):
        pass

    # Exit a parse tree produced by CogniLangParser#parametric.
    def exitParametric(self, ctx:CogniLangParser.ParametricContext):
        pass


    # Enter a parse tree produced by CogniLangParser#parameter.
    def enterParameter(self, ctx:CogniLangParser.ParameterContext):
        pass

    # Exit a parse tree produced by CogniLangParser#parameter.
    def exitParameter(self, ctx:CogniLangParser.ParameterContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphnode.
    def enterGraphnode(self, ctx:CogniLangParser.GraphnodeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphnode.
    def exitGraphnode(self, ctx:CogniLangParser.GraphnodeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphnode_expr.
    def enterGraphnode_expr(self, ctx:CogniLangParser.Graphnode_exprContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphnode_expr.
    def exitGraphnode_expr(self, ctx:CogniLangParser.Graphnode_exprContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphnode_body.
    def enterGraphnode_body(self, ctx:CogniLangParser.Graphnode_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphnode_body.
    def exitGraphnode_body(self, ctx:CogniLangParser.Graphnode_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphnode_signature.
    def enterGraphnode_signature(self, ctx:CogniLangParser.Graphnode_signatureContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphnode_signature.
    def exitGraphnode_signature(self, ctx:CogniLangParser.Graphnode_signatureContext):
        pass


    # Enter a parse tree produced by CogniLangParser#common_subset_elem.
    def enterCommon_subset_elem(self, ctx:CogniLangParser.Common_subset_elemContext):
        pass

    # Exit a parse tree produced by CogniLangParser#common_subset_elem.
    def exitCommon_subset_elem(self, ctx:CogniLangParser.Common_subset_elemContext):
        pass


    # Enter a parse tree produced by CogniLangParser#field_double.
    def enterField_double(self, ctx:CogniLangParser.Field_doubleContext):
        pass

    # Exit a parse tree produced by CogniLangParser#field_double.
    def exitField_double(self, ctx:CogniLangParser.Field_doubleContext):
        pass


    # Enter a parse tree produced by CogniLangParser#field_int.
    def enterField_int(self, ctx:CogniLangParser.Field_intContext):
        pass

    # Exit a parse tree produced by CogniLangParser#field_int.
    def exitField_int(self, ctx:CogniLangParser.Field_intContext):
        pass


    # Enter a parse tree produced by CogniLangParser#field_string.
    def enterField_string(self, ctx:CogniLangParser.Field_stringContext):
        pass

    # Exit a parse tree produced by CogniLangParser#field_string.
    def exitField_string(self, ctx:CogniLangParser.Field_stringContext):
        pass


    # Enter a parse tree produced by CogniLangParser#field_float_vector.
    def enterField_float_vector(self, ctx:CogniLangParser.Field_float_vectorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#field_float_vector.
    def exitField_float_vector(self, ctx:CogniLangParser.Field_float_vectorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#parameters.
    def enterParameters(self, ctx:CogniLangParser.ParametersContext):
        pass

    # Exit a parse tree produced by CogniLangParser#parameters.
    def exitParameters(self, ctx:CogniLangParser.ParametersContext):
        pass


    # Enter a parse tree produced by CogniLangParser#param_double.
    def enterParam_double(self, ctx:CogniLangParser.Param_doubleContext):
        pass

    # Exit a parse tree produced by CogniLangParser#param_double.
    def exitParam_double(self, ctx:CogniLangParser.Param_doubleContext):
        pass


    # Enter a parse tree produced by CogniLangParser#param_double_vector.
    def enterParam_double_vector(self, ctx:CogniLangParser.Param_double_vectorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#param_double_vector.
    def exitParam_double_vector(self, ctx:CogniLangParser.Param_double_vectorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#param_int.
    def enterParam_int(self, ctx:CogniLangParser.Param_intContext):
        pass

    # Exit a parse tree produced by CogniLangParser#param_int.
    def exitParam_int(self, ctx:CogniLangParser.Param_intContext):
        pass


    # Enter a parse tree produced by CogniLangParser#param_string.
    def enterParam_string(self, ctx:CogniLangParser.Param_stringContext):
        pass

    # Exit a parse tree produced by CogniLangParser#param_string.
    def exitParam_string(self, ctx:CogniLangParser.Param_stringContext):
        pass


    # Enter a parse tree produced by CogniLangParser#vector_elem.
    def enterVector_elem(self, ctx:CogniLangParser.Vector_elemContext):
        pass

    # Exit a parse tree produced by CogniLangParser#vector_elem.
    def exitVector_elem(self, ctx:CogniLangParser.Vector_elemContext):
        pass


    # Enter a parse tree produced by CogniLangParser#float_vector.
    def enterFloat_vector(self, ctx:CogniLangParser.Float_vectorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#float_vector.
    def exitFloat_vector(self, ctx:CogniLangParser.Float_vectorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#multi_vector.
    def enterMulti_vector(self, ctx:CogniLangParser.Multi_vectorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#multi_vector.
    def exitMulti_vector(self, ctx:CogniLangParser.Multi_vectorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#axis.
    def enterAxis(self, ctx:CogniLangParser.AxisContext):
        pass

    # Exit a parse tree produced by CogniLangParser#axis.
    def exitAxis(self, ctx:CogniLangParser.AxisContext):
        pass


    # Enter a parse tree produced by CogniLangParser#value.
    def enterValue(self, ctx:CogniLangParser.ValueContext):
        pass

    # Exit a parse tree produced by CogniLangParser#value.
    def exitValue(self, ctx:CogniLangParser.ValueContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphedge.
    def enterGraphedge(self, ctx:CogniLangParser.GraphedgeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphedge.
    def exitGraphedge(self, ctx:CogniLangParser.GraphedgeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphedge_signature.
    def enterGraphedge_signature(self, ctx:CogniLangParser.Graphedge_signatureContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphedge_signature.
    def exitGraphedge_signature(self, ctx:CogniLangParser.Graphedge_signatureContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphedge_expr.
    def enterGraphedge_expr(self, ctx:CogniLangParser.Graphedge_exprContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphedge_expr.
    def exitGraphedge_expr(self, ctx:CogniLangParser.Graphedge_exprContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphedge_relation.
    def enterGraphedge_relation(self, ctx:CogniLangParser.Graphedge_relationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphedge_relation.
    def exitGraphedge_relation(self, ctx:CogniLangParser.Graphedge_relationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#graphedge_relation_optype.
    def enterGraphedge_relation_optype(self, ctx:CogniLangParser.Graphedge_relation_optypeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#graphedge_relation_optype.
    def exitGraphedge_relation_optype(self, ctx:CogniLangParser.Graphedge_relation_optypeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#subset_elem.
    def enterSubset_elem(self, ctx:CogniLangParser.Subset_elemContext):
        pass

    # Exit a parse tree produced by CogniLangParser#subset_elem.
    def exitSubset_elem(self, ctx:CogniLangParser.Subset_elemContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ref_.
    def enterRef_(self, ctx:CogniLangParser.Ref_Context):
        pass

    # Exit a parse tree produced by CogniLangParser#ref_.
    def exitRef_(self, ctx:CogniLangParser.Ref_Context):
        pass


    # Enter a parse tree produced by CogniLangParser#dir.
    def enterDir(self, ctx:CogniLangParser.DirContext):
        pass

    # Exit a parse tree produced by CogniLangParser#dir.
    def exitDir(self, ctx:CogniLangParser.DirContext):
        pass


    # Enter a parse tree produced by CogniLangParser#out_dir.
    def enterOut_dir(self, ctx:CogniLangParser.Out_dirContext):
        pass

    # Exit a parse tree produced by CogniLangParser#out_dir.
    def exitOut_dir(self, ctx:CogniLangParser.Out_dirContext):
        pass


    # Enter a parse tree produced by CogniLangParser#in_dir.
    def enterIn_dir(self, ctx:CogniLangParser.In_dirContext):
        pass

    # Exit a parse tree produced by CogniLangParser#in_dir.
    def exitIn_dir(self, ctx:CogniLangParser.In_dirContext):
        pass


    # Enter a parse tree produced by CogniLangParser#bi_dir.
    def enterBi_dir(self, ctx:CogniLangParser.Bi_dirContext):
        pass

    # Exit a parse tree produced by CogniLangParser#bi_dir.
    def exitBi_dir(self, ctx:CogniLangParser.Bi_dirContext):
        pass


    # Enter a parse tree produced by CogniLangParser#rigid_transformation.
    def enterRigid_transformation(self, ctx:CogniLangParser.Rigid_transformationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#rigid_transformation.
    def exitRigid_transformation(self, ctx:CogniLangParser.Rigid_transformationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#rotation.
    def enterRotation(self, ctx:CogniLangParser.RotationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#rotation.
    def exitRotation(self, ctx:CogniLangParser.RotationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#kinematic.
    def enterKinematic(self, ctx:CogniLangParser.KinematicContext):
        pass

    # Exit a parse tree produced by CogniLangParser#kinematic.
    def exitKinematic(self, ctx:CogniLangParser.KinematicContext):
        pass


    # Enter a parse tree produced by CogniLangParser#kinematicnode_body.
    def enterKinematicnode_body(self, ctx:CogniLangParser.Kinematicnode_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#kinematicnode_body.
    def exitKinematicnode_body(self, ctx:CogniLangParser.Kinematicnode_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#link.
    def enterLink(self, ctx:CogniLangParser.LinkContext):
        pass

    # Exit a parse tree produced by CogniLangParser#link.
    def exitLink(self, ctx:CogniLangParser.LinkContext):
        pass


    # Enter a parse tree produced by CogniLangParser#linknode_body.
    def enterLinknode_body(self, ctx:CogniLangParser.Linknode_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#linknode_body.
    def exitLinknode_body(self, ctx:CogniLangParser.Linknode_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#inertia_body.
    def enterInertia_body(self, ctx:CogniLangParser.Inertia_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#inertia_body.
    def exitInertia_body(self, ctx:CogniLangParser.Inertia_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#inertia_vector.
    def enterInertia_vector(self, ctx:CogniLangParser.Inertia_vectorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#inertia_vector.
    def exitInertia_vector(self, ctx:CogniLangParser.Inertia_vectorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#visual_node.
    def enterVisual_node(self, ctx:CogniLangParser.Visual_nodeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#visual_node.
    def exitVisual_node(self, ctx:CogniLangParser.Visual_nodeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#material.
    def enterMaterial(self, ctx:CogniLangParser.MaterialContext):
        pass

    # Exit a parse tree produced by CogniLangParser#material.
    def exitMaterial(self, ctx:CogniLangParser.MaterialContext):
        pass


    # Enter a parse tree produced by CogniLangParser#collision_node.
    def enterCollision_node(self, ctx:CogniLangParser.Collision_nodeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#collision_node.
    def exitCollision_node(self, ctx:CogniLangParser.Collision_nodeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#geometry_body.
    def enterGeometry_body(self, ctx:CogniLangParser.Geometry_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#geometry_body.
    def exitGeometry_body(self, ctx:CogniLangParser.Geometry_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#geometries.
    def enterGeometries(self, ctx:CogniLangParser.GeometriesContext):
        pass

    # Exit a parse tree produced by CogniLangParser#geometries.
    def exitGeometries(self, ctx:CogniLangParser.GeometriesContext):
        pass


    # Enter a parse tree produced by CogniLangParser#cylinder_geometry.
    def enterCylinder_geometry(self, ctx:CogniLangParser.Cylinder_geometryContext):
        pass

    # Exit a parse tree produced by CogniLangParser#cylinder_geometry.
    def exitCylinder_geometry(self, ctx:CogniLangParser.Cylinder_geometryContext):
        pass


    # Enter a parse tree produced by CogniLangParser#polyhedron_geometry.
    def enterPolyhedron_geometry(self, ctx:CogniLangParser.Polyhedron_geometryContext):
        pass

    # Exit a parse tree produced by CogniLangParser#polyhedron_geometry.
    def exitPolyhedron_geometry(self, ctx:CogniLangParser.Polyhedron_geometryContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ellipsoid_geometry.
    def enterEllipsoid_geometry(self, ctx:CogniLangParser.Ellipsoid_geometryContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ellipsoid_geometry.
    def exitEllipsoid_geometry(self, ctx:CogniLangParser.Ellipsoid_geometryContext):
        pass


    # Enter a parse tree produced by CogniLangParser#mesh_geometry.
    def enterMesh_geometry(self, ctx:CogniLangParser.Mesh_geometryContext):
        pass

    # Exit a parse tree produced by CogniLangParser#mesh_geometry.
    def exitMesh_geometry(self, ctx:CogniLangParser.Mesh_geometryContext):
        pass


    # Enter a parse tree produced by CogniLangParser#joint.
    def enterJoint(self, ctx:CogniLangParser.JointContext):
        pass

    # Exit a parse tree produced by CogniLangParser#joint.
    def exitJoint(self, ctx:CogniLangParser.JointContext):
        pass


    # Enter a parse tree produced by CogniLangParser#joint_body.
    def enterJoint_body(self, ctx:CogniLangParser.Joint_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#joint_body.
    def exitJoint_body(self, ctx:CogniLangParser.Joint_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#joint_relation.
    def enterJoint_relation(self, ctx:CogniLangParser.Joint_relationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#joint_relation.
    def exitJoint_relation(self, ctx:CogniLangParser.Joint_relationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#joint_type.
    def enterJoint_type(self, ctx:CogniLangParser.Joint_typeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#joint_type.
    def exitJoint_type(self, ctx:CogniLangParser.Joint_typeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#geometrictemplate.
    def enterGeometrictemplate(self, ctx:CogniLangParser.GeometrictemplateContext):
        pass

    # Exit a parse tree produced by CogniLangParser#geometrictemplate.
    def exitGeometrictemplate(self, ctx:CogniLangParser.GeometrictemplateContext):
        pass


    # Enter a parse tree produced by CogniLangParser#geometricoperation.
    def enterGeometricoperation(self, ctx:CogniLangParser.GeometricoperationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#geometricoperation.
    def exitGeometricoperation(self, ctx:CogniLangParser.GeometricoperationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#geometricmirror.
    def enterGeometricmirror(self, ctx:CogniLangParser.GeometricmirrorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#geometricmirror.
    def exitGeometricmirror(self, ctx:CogniLangParser.GeometricmirrorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#templateoperations.
    def enterTemplateoperations(self, ctx:CogniLangParser.TemplateoperationsContext):
        pass

    # Exit a parse tree produced by CogniLangParser#templateoperations.
    def exitTemplateoperations(self, ctx:CogniLangParser.TemplateoperationsContext):
        pass


    # Enter a parse tree produced by CogniLangParser#template_instantiation.
    def enterTemplate_instantiation(self, ctx:CogniLangParser.Template_instantiationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#template_instantiation.
    def exitTemplate_instantiation(self, ctx:CogniLangParser.Template_instantiationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambient.
    def enterAmbient(self, ctx:CogniLangParser.AmbientContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambient.
    def exitAmbient(self, ctx:CogniLangParser.AmbientContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambient_element_signature.
    def enterAmbient_element_signature(self, ctx:CogniLangParser.Ambient_element_signatureContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambient_element_signature.
    def exitAmbient_element_signature(self, ctx:CogniLangParser.Ambient_element_signatureContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambient_graph_body.
    def enterAmbient_graph_body(self, ctx:CogniLangParser.Ambient_graph_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambient_graph_body.
    def exitAmbient_graph_body(self, ctx:CogniLangParser.Ambient_graph_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambient_element.
    def enterAmbient_element(self, ctx:CogniLangParser.Ambient_elementContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambient_element.
    def exitAmbient_element(self, ctx:CogniLangParser.Ambient_elementContext):
        pass


    # Enter a parse tree produced by CogniLangParser#actuator.
    def enterActuator(self, ctx:CogniLangParser.ActuatorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#actuator.
    def exitActuator(self, ctx:CogniLangParser.ActuatorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#sensor.
    def enterSensor(self, ctx:CogniLangParser.SensorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#sensor.
    def exitSensor(self, ctx:CogniLangParser.SensorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambience_edge.
    def enterAmbience_edge(self, ctx:CogniLangParser.Ambience_edgeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambience_edge.
    def exitAmbience_edge(self, ctx:CogniLangParser.Ambience_edgeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambience_edge_body.
    def enterAmbience_edge_body(self, ctx:CogniLangParser.Ambience_edge_bodyContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambience_edge_body.
    def exitAmbience_edge_body(self, ctx:CogniLangParser.Ambience_edge_bodyContext):
        pass


    # Enter a parse tree produced by CogniLangParser#sensor_basic_definition.
    def enterSensor_basic_definition(self, ctx:CogniLangParser.Sensor_basic_definitionContext):
        pass

    # Exit a parse tree produced by CogniLangParser#sensor_basic_definition.
    def exitSensor_basic_definition(self, ctx:CogniLangParser.Sensor_basic_definitionContext):
        pass


    # Enter a parse tree produced by CogniLangParser#sensor_basic_definition_parameters.
    def enterSensor_basic_definition_parameters(self, ctx:CogniLangParser.Sensor_basic_definition_parametersContext):
        pass

    # Exit a parse tree produced by CogniLangParser#sensor_basic_definition_parameters.
    def exitSensor_basic_definition_parameters(self, ctx:CogniLangParser.Sensor_basic_definition_parametersContext):
        pass


    # Enter a parse tree produced by CogniLangParser#precision_parameter.
    def enterPrecision_parameter(self, ctx:CogniLangParser.Precision_parameterContext):
        pass

    # Exit a parse tree produced by CogniLangParser#precision_parameter.
    def exitPrecision_parameter(self, ctx:CogniLangParser.Precision_parameterContext):
        pass


    # Enter a parse tree produced by CogniLangParser#accuracy_parameter.
    def enterAccuracy_parameter(self, ctx:CogniLangParser.Accuracy_parameterContext):
        pass

    # Exit a parse tree produced by CogniLangParser#accuracy_parameter.
    def exitAccuracy_parameter(self, ctx:CogniLangParser.Accuracy_parameterContext):
        pass


    # Enter a parse tree produced by CogniLangParser#variance_parameter.
    def enterVariance_parameter(self, ctx:CogniLangParser.Variance_parameterContext):
        pass

    # Exit a parse tree produced by CogniLangParser#variance_parameter.
    def exitVariance_parameter(self, ctx:CogniLangParser.Variance_parameterContext):
        pass


    # Enter a parse tree produced by CogniLangParser#sensor_type.
    def enterSensor_type(self, ctx:CogniLangParser.Sensor_typeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#sensor_type.
    def exitSensor_type(self, ctx:CogniLangParser.Sensor_typeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#element_placement_relation.
    def enterElement_placement_relation(self, ctx:CogniLangParser.Element_placement_relationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#element_placement_relation.
    def exitElement_placement_relation(self, ctx:CogniLangParser.Element_placement_relationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#geom_relation.
    def enterGeom_relation(self, ctx:CogniLangParser.Geom_relationContext):
        pass

    # Exit a parse tree produced by CogniLangParser#geom_relation.
    def exitGeom_relation(self, ctx:CogniLangParser.Geom_relationContext):
        pass


    # Enter a parse tree produced by CogniLangParser#proprioceptive_sensor.
    def enterProprioceptive_sensor(self, ctx:CogniLangParser.Proprioceptive_sensorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#proprioceptive_sensor.
    def exitProprioceptive_sensor(self, ctx:CogniLangParser.Proprioceptive_sensorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#prop_sensor_type.
    def enterProp_sensor_type(self, ctx:CogniLangParser.Prop_sensor_typeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#prop_sensor_type.
    def exitProp_sensor_type(self, ctx:CogniLangParser.Prop_sensor_typeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#exteroceptive_sensor.
    def enterExteroceptive_sensor(self, ctx:CogniLangParser.Exteroceptive_sensorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#exteroceptive_sensor.
    def exitExteroceptive_sensor(self, ctx:CogniLangParser.Exteroceptive_sensorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ext_sensor_type.
    def enterExt_sensor_type(self, ctx:CogniLangParser.Ext_sensor_typeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ext_sensor_type.
    def exitExt_sensor_type(self, ctx:CogniLangParser.Ext_sensor_typeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#matrix_sensor.
    def enterMatrix_sensor(self, ctx:CogniLangParser.Matrix_sensorContext):
        pass

    # Exit a parse tree produced by CogniLangParser#matrix_sensor.
    def exitMatrix_sensor(self, ctx:CogniLangParser.Matrix_sensorContext):
        pass


    # Enter a parse tree produced by CogniLangParser#communication_connections.
    def enterCommunication_connections(self, ctx:CogniLangParser.Communication_connectionsContext):
        pass

    # Exit a parse tree produced by CogniLangParser#communication_connections.
    def exitCommunication_connections(self, ctx:CogniLangParser.Communication_connectionsContext):
        pass


    # Enter a parse tree produced by CogniLangParser#communication_type.
    def enterCommunication_type(self, ctx:CogniLangParser.Communication_typeContext):
        pass

    # Exit a parse tree produced by CogniLangParser#communication_type.
    def exitCommunication_type(self, ctx:CogniLangParser.Communication_typeContext):
        pass


    # Enter a parse tree produced by CogniLangParser#communication_connection_msg.
    def enterCommunication_connection_msg(self, ctx:CogniLangParser.Communication_connection_msgContext):
        pass

    # Exit a parse tree produced by CogniLangParser#communication_connection_msg.
    def exitCommunication_connection_msg(self, ctx:CogniLangParser.Communication_connection_msgContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambient_signal.
    def enterAmbient_signal(self, ctx:CogniLangParser.Ambient_signalContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambient_signal.
    def exitAmbient_signal(self, ctx:CogniLangParser.Ambient_signalContext):
        pass


    # Enter a parse tree produced by CogniLangParser#ambient_stream.
    def enterAmbient_stream(self, ctx:CogniLangParser.Ambient_streamContext):
        pass

    # Exit a parse tree produced by CogniLangParser#ambient_stream.
    def exitAmbient_stream(self, ctx:CogniLangParser.Ambient_streamContext):
        pass


    # Enter a parse tree produced by CogniLangParser#port_signature.
    def enterPort_signature(self, ctx:CogniLangParser.Port_signatureContext):
        pass

    # Exit a parse tree produced by CogniLangParser#port_signature.
    def exitPort_signature(self, ctx:CogniLangParser.Port_signatureContext):
        pass


    # Enter a parse tree produced by CogniLangParser#port.
    def enterPort(self, ctx:CogniLangParser.PortContext):
        pass

    # Exit a parse tree produced by CogniLangParser#port.
    def exitPort(self, ctx:CogniLangParser.PortContext):
        pass



del CogniLangParser