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

    def get_fuzzy_infer_values(self, r: HypergraphRelation):
        v: ValueNode = next(r.endpoint.get_element_by_id_name("values"))
        m: ValueNode = next(r.get_element_by_id_name("membership")).get_values()
        me = next(r.get_element_by_id_name("mbtype")).get_values()
        s_res = []
        # Vectorize input values
        __val = np.array(v.get_values())
        # Iterate over mebership values
        for pi, mu in zip(m, me):
            arg = [__val, *pi]
            # Norm function on node-level
            tau = np.array(mu(*arg))
            s_res.append(tau)
        return np.array(s_res), v

    async def infer_edge(self, edge: HypergraphEdge):
        # Implication
        res = None
        # Get s-norm
        s_norm = next(edge.get_element_by_id_name("snorm")).get_values()[0]
        # Get t-norm
        t_norm = next(edge.get_element_by_id_name("tnorm")).get_values()[0]
        for r in edge.get_incoming_relations():
            s_res, _ = self.get_fuzzy_infer_values(r)
            s_res = await s_norm.execute(s_res)
            if res is None:
                res = s_res
            else:
                res = np.vstack((res, s_res))
        # Update outgoing
        for r in edge.get_outgoing_relations():
            t_res, v = self.get_fuzzy_infer_values(r)
            # Update firing values (for defuzzification)
            # Norm function on node-level
            z = await t_norm.execute(res)
            t_res = np.max(t_res, axis=0)
            next(r.get_element_by_id_name("firevalues")).update_values([t_res])
            v.update_values([z])

    def defuzz(self, node: HypergraphNode):
        for r in filter(lambda x: x.endpoint.direction == EnumRelationDirection.OUTWARDS
                                  or x.endpoint == EnumRelationDirection.BIDIRECTIONAL, node.sub_ports):
            __tau = next(r.endpoint.get_element_by_id_name("firevalues")).get_values()[0]
            __v = next(node.get_element_by_id_name("values")).get_values()[0]
            if __tau.shape==(0,):
                continue
            yield np.sum((__v * __tau)/np.sum(__tau))
        return node.get_element_by_id_name("firevalues")


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
            self, id_name: str, parent: HypergraphNode, tnorm, snorm,
            connections: list[tuple[HypergraphNode, EnumRelationDirection, dict | list, SemanticValueNode | None]]):
        __fhe: HypergraphEdge = self.connect_tuple_nodes(parent, id_name, connections)
        self.create_value(__fhe, "snorm", [snorm])
        self.create_value(__fhe, "tnorm", [tnorm])
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
    __battery_result_node, __battery_result_value = __fuzzy_factory.create_fuzzy_computation_node(
        "battery_result_node", [], battery)
    #
    __battery_infer = __fuzzy_factory.connect_fuzzy_nodes(
        "battery_infer", fuzzy_cogni_sys, no.MinNorm(), no.MaxNorm(), [
            (__battery_dynamic_node, EnumRelationDirection.INWARDS,
                [__fuzzy_factory.create_value(None, "membership", [
                    [0.0, 1.5], [0.0, 1.0, 3.0], [1.0, 4.0, 5.0], [4.0, 6.0, 8.0], [6.0, 12.0]]),
                 __fuzzy_factory.create_value(None, "mbtype", [mb.lamma_v, mb.tri_v, mb.tri_v, mb.tri_v, mb.gamma_v]),
                 ], None),
            (__battery_static_node, EnumRelationDirection.INWARDS,
                 [__fuzzy_factory.create_value(None, "membership", [
                     [0.0, 5.0], [2.0, 10.0, 15.0], [10, 15, 20], [15, 17.5, 22.5], [20, 30]]),
                  __fuzzy_factory.create_value(None, "mbtype", [mb.lamma_v, mb.tri_v, mb.tri_v, mb.tri_v, mb.gamma_v]),
                  ], None),
            (__battery_result_node, EnumRelationDirection.OUTWARDS,
             [__fuzzy_factory.create_value(None, "membership", [
                     [0.0, 0.3], [0.2, 0.5, 0.7], [0.4, 0.6, 0.8], [0.6, 0.85, 0.95], [0.9, 1.0]]),
                 __fuzzy_factory.create_value(None, "mbtype", [mb.lamma_v, mb.tri_v, mb.tri_v, mb.tri_v, mb.gamma_v]),
                 __fuzzy_factory.create_value(None, "firevalues", np.array([0.0, 0.0, 0.0, 0.0, 0.0]))
             ], None)
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
    defuzz = []
    for v in t:
        #
        __lh = 30/(1+np.exp(-v))
        lh.append(__lh)
        __battery_static_values.update_value(0, __lh)

        __lc = 30/(1+np.exp(-0.15*v+ 4))
        lc.append(__lc)
        __battery_static_values.update_value(1, __lc)
        __lrc = 30/(1+np.exp(-0.3*v + 2))
        lrc.append(__lrc)
        __battery_static_values.update_value(2, __lrc)
        # Update dynamic values
        __volt = 12*np.exp(-v) + 0.5
        volt.append(__volt)
        __battery_dynamic_values.update_value(0, __volt)

        __charge = 6*np.exp(-2*v) + 0.7
        charge.append(__charge)
        __battery_dynamic_values.update_value(1, __charge)

        __capacity = 12.0*np.exp(-0.1*v) + 0.1
        capacity.append(__capacity)
        __battery_dynamic_values.update_value(2, __capacity)
        import asyncio
        asyncio.run(engine.infer_edge(__battery_infer))
        z.append(*__battery_result_value._values)
        _v = next(engine.defuzz(__battery_result_node),None)
        defuzz.append(_v)
    plt.subplot(1,2,1)
    plt.plot(t, lh)
    plt.plot(t, lc)
    plt.plot(t, lrc)
    plt.plot(t, volt)
    plt.plot(t, capacity)
    plt.plot(t, charge)
    plt.subplot(1,2,2)
    plt.plot(t, z)
    plt.plot(t, defuzz, linewidth=5)
    # Available energy
    plt.show()


if __name__=="__main__":
    main()
