import queue
from enum import IntEnum

from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphEdge


class EnumFactorizationMode(IntEnum):
    TREE_FACTORIZATION = 0,
    PAIRING_FACTORIZATION = 1,
    RECURRENCE_FACTORIZATION = 2


def hypergraphedge_2factorization_tree(edge: HypergraphEdge, self_loops: bool = False):
    incoming_edges = []
    outgoing_edges = []
    for e in edge.subrelations:
        match e.direction:
            case EnumRelationDirection.INWARDS:
                incoming_edges.append(e)
            case EnumRelationDirection.OUTWARDS:
                outgoing_edges.append(e)
            case EnumRelationDirection.UNDIRECTED:
                outgoing_edges.append(e)
                incoming_edges.append(e)
    # Descartes combination
    res = queue.Queue()
    for c0 in incoming_edges:
        for c1 in outgoing_edges:
            if self_loops:
                res.put((c0, c1))
            else:
                if c0 is not c1:
                    res.put((c0, c1))
    return res


def hypergraphedge_2factorization_pairing(edge: HypergraphEdge):
    # TODO: think through
    pass


def hypergraphedge_2factorization(edge: HypergraphEdge,
                                  mode: EnumFactorizationMode = EnumFactorizationMode.TREE_FACTORIZATION):
    match mode:
        case EnumFactorizationMode.TREE_FACTORIZATION:
            return hypergraphedge_2factorization_tree(edge)
        case EnumFactorizationMode.PAIRING_FACTORIZATION:
            pass
        case EnumFactorizationMode.RECURRENCE_FACTORIZATION:
            hypergraphedge_2factorization_tree(edge, True)
