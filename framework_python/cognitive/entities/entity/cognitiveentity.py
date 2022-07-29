from cognitive.format.basicelements.concepts.network.base_definitions import NetworkElement, NetworkNode
from cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from physics.kinematics.kinematic_link import KinematicGraph


class ParameterNode(HypergraphNode):

    def __init__(self, name: str, value, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self.value = value



class CognitiveEntity(HypergraphNode):

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        # Attributes
        self.entity_name = name
        # Kinematic graphs
        self.kinematic_graphs = {}
        # Parameter graph
        self.parameter_graph_mapping = {}
        self.parameter_graph = HypergraphNode("parameters", 0)

    def add_kinematic_graph(self, a: KinematicGraph, timestamp: int):
        self.kinematic_graphs[a.id_name] = a
        self.add_subset(a, timestamp)

    def add_kinematic_element(self, el, parent_ctx):
        if str(parent_ctx.parentCtx.graphnode_signature().ID()) in self.kinematic_graphs:
            parent_id = str(parent_ctx.parentCtx.graphnode_signature().ID())
            self.kinematic_graphs[parent_id].add_subset(el, 0)
        else:
            self.add_subset(el, 0)

    def add_parameter(self, parameter: ParameterNode):
        self.parameter_graph_mapping[parameter.id_name] = parameter
        self.parameter_graph.add_subset(parameter, 0)

    def get_parameter(self, id: str):
        return self.parameter_graph_mapping[id]
