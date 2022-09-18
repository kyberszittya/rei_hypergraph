import numpy as np

from rei.hypergraph.base_elements import HypergraphNode, HypergraphRelation, HypergraphEdge
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.value_node import ValueNode


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



