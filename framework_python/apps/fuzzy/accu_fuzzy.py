import typing

import numpy as np

from rei.factories.abstract_factory import AbstractElementFactory
from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import LocalClock, MetaClock
from rei.fuzzy.norm_functions import SNorm
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge, HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection

import rei.fuzzy.membership_functions as mb
import rei.fuzzy.norm_functions as no

import matplotlib.pyplot as plt

from rei.hypergraph.value_node import ValueNode, SemanticValueNode


class FuzzyEngine(HypergraphNode):

    def get_fuzzy_elements_from_node(self, rel: HypergraphRelation):
        r: HypergraphRelation
        v: ValueNode = next(rel.get_element_by_id_name("values"))
        m: ValueNode = next(rel.get_element_by_id_name("membership"))
        me: typing.Callable = next(rel.get_element_by_id_name("mbtype")).get_values()[0]
        arg = [np.array(v.get_values()), *m.get_values()]
        return me, arg

    async def infer_edge(self, edge: HypergraphEdge):
        # Implication
        res = None
        for r in edge.get_incoming_relations():
            r: HypergraphRelation
            v: ValueNode = next(r.endpoint.get_element_by_id_name("values"))
            m: ValueNode = next(r.get_element_by_id_name("membership"))
            me = next(r.get_element_by_id_name("mbtype")).get_values()[0]
            arg = [np.array(v.get_values()), *m.get_values()]
            # Get s-norm
            node_norm = next(r.get_element_by_id_name("norm")).get_values()[0]
            # Norm function on node-level
            z = await node_norm.execute(np.array(me(*arg)))
            if res is None:
                res = z
            else:
                res = np.vstack((res, z))
        for r in edge.get_outgoing_relations():
            r: HypergraphRelation
            v: ValueNode = next(r.endpoint.get_element_by_id_name("values"))
            # Get t-norm
            node_norm = next(edge.get_element_by_id_name("norm")).get_values()[0]
            # Norm function on node-level
            z = await node_norm.execute(res)
            v.update_values(z)


class FuzzyElementFactory(HypergraphFactory):

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__(factory_name, clock)

    def create_fuzzy_engine(self, id_name: str, parent: HypergraphNode = None) -> FuzzyEngine:
        if parent is not None:
            uid = self.unique_identifier.generate_uid('/'.join([parent.qualified_name, id_name]))
        else:
            uid = self.unique_identifier.generate_uid(id_name)
        node = FuzzyEngine(id_name, uid, '/'.join([self._factory_name, self.get_qualified_name(id_name)]),
                           self._clock, parent)
        return node

    def create_fuzzy_computation_node(self, id_name: str,
                                      values: list,
                                      parent: HypergraphNode = None):
        __node = self.generate_node(id_name, parent)
        __values = self.create_value(__node, "values", values)
        return __node, __values

    def connect_fuzzy_nodes(
            self, id_name: str, parent: HypergraphNode, norm,
            connections: list[tuple[HypergraphNode, EnumRelationDirection, dict | list, SemanticValueNode | None]]):
        __fhe: HypergraphEdge = self.connect_tuple_nodes(parent, id_name, connections)
        self.create_value(__fhe, "norm", [norm])
        return __fhe


def main():
    __time = LocalClock()
    __factory = HypergraphFactory("fuzzy_sys_factory", __time)
    fuzzy_cogni_sys = __factory.generate_node("fuzzy_sys_cogni")
    # Factory
    __fuzzy_factory = FuzzyElementFactory("fuzzy_factory", __time)
    engine = __fuzzy_factory.create_fuzzy_engine("battery_engine")
    # Endpoints
    # Battery
    battery = __factory.generate_node("battery_node", fuzzy_cogni_sys)
    # Battery dynamic values
    __battery_dynamic_node, __battery_dynamic_values = __fuzzy_factory.create_fuzzy_computation_node(
        "battery_dynamic_node", [0.0, 0.0, 0.0], battery)
    # Battery static values
    __battery_static_node, __battery_static_values = __fuzzy_factory.create_fuzzy_computation_node(
        "battery_static_node", [0.0, 0.0, 0.0], battery)
    # Battery
    __battery_result_node = __factory.generate_node("battery_result", battery)
    __battery_result_value = __factory.create_value(__battery_result_node, "values", [])
    #
    __battery_infer = __fuzzy_factory.connect_fuzzy_nodes(
        "battery_infer", fuzzy_cogni_sys, no.MinNorm(), [
            (__battery_dynamic_node, EnumRelationDirection.INWARDS,
                [__fuzzy_factory.create_value(None, "membership", [1.0, 2.0, 3.0]),
                 __fuzzy_factory.create_value(None, "mbtype", [mb.tri_v]),
                 __fuzzy_factory.create_value(None, "norm", [no.MaxNorm()]),
                 ], None),
            (__battery_static_node, EnumRelationDirection.INWARDS,
                 [__fuzzy_factory.create_value(None, "membership", [5.0, 10.0, 20.0, 30.0]),
                  __fuzzy_factory.create_value(None, "mbtype", [mb.trap_v]),
                  __fuzzy_factory.create_value(None, "norm", [no.MaxNorm()]),
                  ], None),
            (__battery_result_node, EnumRelationDirection.OUTWARDS, [], None)
        ]
    )
    #
    t = np.linspace(0, 10, 100)
    # Exterior effects
    __exterior_node = __factory.generate_node("external_effects")
    lh = []
    lc = []
    lrc = []

    volt = []
    capacity = []
    charge = []

    z = []
    for v in t:
        #
        __lh = 10 - np.exp(-v)
        lh.append(__lh)
        __battery_static_values.update_value(0, __lh)

        __lc = 10 - np.exp(-v)
        lc.append(__lc)
        __battery_static_values.update_value(1, __lc)
        __lrc = 10 - np.exp(-v)
        lrc.append(__lrc)
        __battery_static_values.update_value(2, __lrc)
        # Update dynamic values
        __volt = 3*np.exp(-v) + 0.1
        volt.append(__volt)
        __battery_dynamic_values.update_value(0, __volt)

        __charge = 2*np.exp(-2*v) + 0.1
        charge.append(__charge)
        __battery_dynamic_values.update_value(1, __charge)

        __capacity = 2.76*np.exp(-0.1*v) + 0.1
        capacity.append(__capacity)
        __battery_dynamic_values.update_value(2, __capacity)
        import asyncio
        asyncio.run(engine.infer_edge(__battery_infer))
        z.append(__battery_result_value._values)

    plt.plot(t, lh)
    plt.plot(t, lc)
    plt.plot(t, lrc)
    plt.plot(t, volt)
    plt.plot(t, capacity)
    plt.plot(t, charge)
    plt.plot(t, z, linewidth=5)
    # Available energy
    plt.show()
    print(z)


if __name__=="__main__":
    main()
