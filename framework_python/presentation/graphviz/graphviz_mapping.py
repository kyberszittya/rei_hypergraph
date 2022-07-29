import graphviz

from cognitive.entities.entity.cognitiveentity import CognitiveEntity
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from cognitive.format.hypergraph.foundations.hypergraph_operators import hypergraphedge_2factorization_tree
from physics.kinematics.kinematic_link import KinematicGraph, KinematicJoint


def graphviz_kinematicgraph(kg: KinematicGraph, dot):
    graph = dot
    for v in kg._subsets.values():
        if isinstance(v, HypergraphNode):
            dot.attr('node', color='black', fillcolor="white", style="filled")
            dot.attr('node', shape='ellipse')
            if isinstance(v, KinematicGraph):
                dot.attr('graph', fillcolor='deepskyblue2', style='filled')
                with graph.subgraph(name=f"cluster{v.progenitor_registry.qualified_name}") as c:
                    graphviz_kinematicgraph(v, c)
            else:
                graph.node(v.progenitor_registry.qualified_name, label=v.id_name)
        if isinstance(v, KinematicJoint):
            dot.attr('node', shape='box')
            graph.node(v.progenitor_registry.qualified_name, label=v.id_name)
            res = hypergraphedge_2factorization_tree(v)
            while not res.empty():
                dot.attr('edge', style='solid')
                parent, child = res.get()
                graph.edge(parent.endpoint.progenitor_registry.qualified_name, v.progenitor_registry.qualified_name)
                if isinstance(child.endpoint, KinematicGraph):
                    dot.attr('edge', style='dashed')
                    graph.edge(v.progenitor_registry.qualified_name,
                               head_name=child.endpoint.root_link.progenitor_registry.qualified_name,
                               lhead=f"cluster{child.endpoint.progenitor_registry.qualified_name}")
                else:
                    graph.edge(v.progenitor_registry.qualified_name, child.endpoint.progenitor_registry.qualified_name)


def create_graph_view(sys: HypergraphNode, output_directory: str):
    dot = graphviz.Digraph(comment=f"{sys.id_name} 2-factor graph")
    dot.attr(compund='true')
    for entity in filter(lambda x: CognitiveEntity, sys._subsets.values()):
        for kg in filter(lambda x: KinematicGraph, entity._subsets.values()):
            graphviz_kinematicgraph(kg, dot)
        dot.render(filename=f"{'/'.join([output_directory, entity.id_name])}")