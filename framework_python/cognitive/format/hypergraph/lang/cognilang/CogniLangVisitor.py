# Generated from D:\Haizu\robotics_ws\cogni_ws\rei_ws\rei\framework\cognitive\speclanguage\src\main\antlr4\CogniLang.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CogniLangParser import CogniLangParser
else:
    from CogniLangParser import CogniLangParser

# This class defines a complete generic visitor for a parse tree produced by CogniLangParser.

class CogniLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CogniLangParser#rootnode.
    def visitRootnode(self, ctx:CogniLangParser.RootnodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#entity_subset_elem.
    def visitEntity_subset_elem(self, ctx:CogniLangParser.Entity_subset_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#entity_edges.
    def visitEntity_edges(self, ctx:CogniLangParser.Entity_edgesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#entity_nodes.
    def visitEntity_nodes(self, ctx:CogniLangParser.Entity_nodesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#entity.
    def visitEntity(self, ctx:CogniLangParser.EntityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#parametric.
    def visitParametric(self, ctx:CogniLangParser.ParametricContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#parameter.
    def visitParameter(self, ctx:CogniLangParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphnode.
    def visitGraphnode(self, ctx:CogniLangParser.GraphnodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphnode_expr.
    def visitGraphnode_expr(self, ctx:CogniLangParser.Graphnode_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphnode_body.
    def visitGraphnode_body(self, ctx:CogniLangParser.Graphnode_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphnode_signature.
    def visitGraphnode_signature(self, ctx:CogniLangParser.Graphnode_signatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#common_subset_elem.
    def visitCommon_subset_elem(self, ctx:CogniLangParser.Common_subset_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#field_double.
    def visitField_double(self, ctx:CogniLangParser.Field_doubleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#field_int.
    def visitField_int(self, ctx:CogniLangParser.Field_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#field_string.
    def visitField_string(self, ctx:CogniLangParser.Field_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#field_float_vector.
    def visitField_float_vector(self, ctx:CogniLangParser.Field_float_vectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#parameters.
    def visitParameters(self, ctx:CogniLangParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#param_double.
    def visitParam_double(self, ctx:CogniLangParser.Param_doubleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#param_double_vector.
    def visitParam_double_vector(self, ctx:CogniLangParser.Param_double_vectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#param_int.
    def visitParam_int(self, ctx:CogniLangParser.Param_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#param_string.
    def visitParam_string(self, ctx:CogniLangParser.Param_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#vector_elem.
    def visitVector_elem(self, ctx:CogniLangParser.Vector_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#float_vector.
    def visitFloat_vector(self, ctx:CogniLangParser.Float_vectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#multi_vector.
    def visitMulti_vector(self, ctx:CogniLangParser.Multi_vectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#axis.
    def visitAxis(self, ctx:CogniLangParser.AxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#value.
    def visitValue(self, ctx:CogniLangParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphedge.
    def visitGraphedge(self, ctx:CogniLangParser.GraphedgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphedge_signature.
    def visitGraphedge_signature(self, ctx:CogniLangParser.Graphedge_signatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphedge_expr.
    def visitGraphedge_expr(self, ctx:CogniLangParser.Graphedge_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#graphedge_relation.
    def visitGraphedge_relation(self, ctx:CogniLangParser.Graphedge_relationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#subset_elem.
    def visitSubset_elem(self, ctx:CogniLangParser.Subset_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ref_.
    def visitRef_(self, ctx:CogniLangParser.Ref_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#dir.
    def visitDir(self, ctx:CogniLangParser.DirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#out_dir.
    def visitOut_dir(self, ctx:CogniLangParser.Out_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#in_dir.
    def visitIn_dir(self, ctx:CogniLangParser.In_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#bi_dir.
    def visitBi_dir(self, ctx:CogniLangParser.Bi_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#rigid_transformation.
    def visitRigid_transformation(self, ctx:CogniLangParser.Rigid_transformationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#rotation.
    def visitRotation(self, ctx:CogniLangParser.RotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#kinematic.
    def visitKinematic(self, ctx:CogniLangParser.KinematicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#kinematicnode_body.
    def visitKinematicnode_body(self, ctx:CogniLangParser.Kinematicnode_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#link.
    def visitLink(self, ctx:CogniLangParser.LinkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#linknode_body.
    def visitLinknode_body(self, ctx:CogniLangParser.Linknode_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#inertia_body.
    def visitInertia_body(self, ctx:CogniLangParser.Inertia_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#inertia_vector.
    def visitInertia_vector(self, ctx:CogniLangParser.Inertia_vectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#visual_node.
    def visitVisual_node(self, ctx:CogniLangParser.Visual_nodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#material.
    def visitMaterial(self, ctx:CogniLangParser.MaterialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#collision_node.
    def visitCollision_node(self, ctx:CogniLangParser.Collision_nodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#geometry_body.
    def visitGeometry_body(self, ctx:CogniLangParser.Geometry_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#geometries.
    def visitGeometries(self, ctx:CogniLangParser.GeometriesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#cylinder_geometry.
    def visitCylinder_geometry(self, ctx:CogniLangParser.Cylinder_geometryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#polyhedron_geometry.
    def visitPolyhedron_geometry(self, ctx:CogniLangParser.Polyhedron_geometryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ellipsoid_geometry.
    def visitEllipsoid_geometry(self, ctx:CogniLangParser.Ellipsoid_geometryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#mesh_geometry.
    def visitMesh_geometry(self, ctx:CogniLangParser.Mesh_geometryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#joint.
    def visitJoint(self, ctx:CogniLangParser.JointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#joint_body.
    def visitJoint_body(self, ctx:CogniLangParser.Joint_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#joint_relation.
    def visitJoint_relation(self, ctx:CogniLangParser.Joint_relationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#joint_type.
    def visitJoint_type(self, ctx:CogniLangParser.Joint_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#geometrictemplate.
    def visitGeometrictemplate(self, ctx:CogniLangParser.GeometrictemplateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#geometricoperation.
    def visitGeometricoperation(self, ctx:CogniLangParser.GeometricoperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#geometricmirror.
    def visitGeometricmirror(self, ctx:CogniLangParser.GeometricmirrorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#templateoperations.
    def visitTemplateoperations(self, ctx:CogniLangParser.TemplateoperationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#template_instantiation.
    def visitTemplate_instantiation(self, ctx:CogniLangParser.Template_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ambient.
    def visitAmbient(self, ctx:CogniLangParser.AmbientContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ambient_element_signature.
    def visitAmbient_element_signature(self, ctx:CogniLangParser.Ambient_element_signatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ambient_graph_body.
    def visitAmbient_graph_body(self, ctx:CogniLangParser.Ambient_graph_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ambient_element.
    def visitAmbient_element(self, ctx:CogniLangParser.Ambient_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#actuator.
    def visitActuator(self, ctx:CogniLangParser.ActuatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#sensor.
    def visitSensor(self, ctx:CogniLangParser.SensorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#sensor_basic_definition.
    def visitSensor_basic_definition(self, ctx:CogniLangParser.Sensor_basic_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#sensor_basic_definition_parameters.
    def visitSensor_basic_definition_parameters(self, ctx:CogniLangParser.Sensor_basic_definition_parametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#precision_parameter.
    def visitPrecision_parameter(self, ctx:CogniLangParser.Precision_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#accuracy_parameter.
    def visitAccuracy_parameter(self, ctx:CogniLangParser.Accuracy_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#variance_parameter.
    def visitVariance_parameter(self, ctx:CogniLangParser.Variance_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#sensor_type.
    def visitSensor_type(self, ctx:CogniLangParser.Sensor_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ambience_relation.
    def visitAmbience_relation(self, ctx:CogniLangParser.Ambience_relationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#element_placement_relation.
    def visitElement_placement_relation(self, ctx:CogniLangParser.Element_placement_relationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#geom_relation.
    def visitGeom_relation(self, ctx:CogniLangParser.Geom_relationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#proprioceptive_sensor.
    def visitProprioceptive_sensor(self, ctx:CogniLangParser.Proprioceptive_sensorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#prop_sensor_type.
    def visitProp_sensor_type(self, ctx:CogniLangParser.Prop_sensor_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#exteroceptive_sensor.
    def visitExteroceptive_sensor(self, ctx:CogniLangParser.Exteroceptive_sensorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ext_sensor_type.
    def visitExt_sensor_type(self, ctx:CogniLangParser.Ext_sensor_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#communication_elements.
    def visitCommunication_elements(self, ctx:CogniLangParser.Communication_elementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#communication_type.
    def visitCommunication_type(self, ctx:CogniLangParser.Communication_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#communication_connection_msg.
    def visitCommunication_connection_msg(self, ctx:CogniLangParser.Communication_connection_msgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ambient_signal.
    def visitAmbient_signal(self, ctx:CogniLangParser.Ambient_signalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CogniLangParser#ambient_stream.
    def visitAmbient_stream(self, ctx:CogniLangParser.Ambient_streamContext):
        return self.visitChildren(ctx)



del CogniLangParser