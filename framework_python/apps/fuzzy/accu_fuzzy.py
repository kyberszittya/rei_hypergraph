from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import LocalClock
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge
from rei.hypergraph.common_definitions import EnumRelationDirection


def main():
    __time = LocalClock()
    __factory = HypergraphFactory("fuzzy_sys_factory", __time)
    fuzzy_cogni_sys = __factory.generate_node("fuzzy_sys_cogni")
    # Endpoints
    # Battery
    battery = __factory.generate_node("battery_node", fuzzy_cogni_sys)
    # Battery dynamic values
    __battery_dynamic_node = __factory.generate_node("battery_dynamic_node", battery)
    __battery_dynamic_values = __factory.create_value(__battery_dynamic_node, "values", [0.0, 0.0, 0.0])
    __battery_dynamic_memberships = __factory.create_value(__battery_dynamic_node, "membership", [1.0, 1.0, 1.0])
    # Battery static values
    __battery_static_node = __factory.generate_node("battery_static_node", battery)
    __battery_static_values = __factory.create_value(__battery_static_node, "values", [0.0, 0.0, 0.0])
    __battery_static_memberships = __factory.create_value(__battery_static_node, "membership", [1.0, 1.0, 1.0])
    # Battery
    __battery_result_node = __factory.generate_node("battery_result")
    __battery_result_value = __factory.create_value(__battery_result_node, "battery_result_value", [])
    __battery_infer: HypergraphEdge = __factory.connect_tuple_nodes(
        fuzzy_cogni_sys, "battery_infer",
        [(__battery_dynamic_node, EnumRelationDirection.INWARDS, None, None),
         (__battery_static_node, EnumRelationDirection.INWARDS, None, None),
         (__battery_result_node, EnumRelationDirection.OUTWARDS, None, None)])
    # Exterior effects
    exterior = __factory.generate_node("external_effects")
    print(list(__battery_infer.get_incoming_relations()))
    # Available energy


if __name__=="__main__":
    main()
