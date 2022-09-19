from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import LocalClock
from rei.fuzzy.fuzzy_element_factory import FuzzyElementFactory


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
    __temperature_node, __temperature_values = __fuzzy_factory.create_fuzzy_computation_node(
        "temperature__node", [0.0, 0.0, 0.0], battery)
    # Battery static values
    __battery_static_node, __battery_static_values = __fuzzy_factory.create_fuzzy_computation_node(
        "battery_static_node", [0.0, 0.0, 0.0], battery)
    # Battery
    __battery_result_node, __battery_result_value = __fuzzy_factory.create_fuzzy_computation_node(
        "battery_result_node", [], battery)
