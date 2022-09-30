import numpy as np

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import LocalClock
from rei.fuzzy.fuzzy_element_factory import FuzzyElementFactory
from rei.hypergraph.common_definitions import EnumRelationDirection

import rei.fuzzy.membership_functions as mb
import rei.fuzzy.norm_functions as no

import matplotlib.pyplot as plt


def main():
    __time = LocalClock()
    __factory = HypergraphFactory("fuzzy_sys_factory", __time)
    cogni_sys = __factory.generate_node("fuzzy_sys_cogni")
    # Factory
    __fuzzy_factory = FuzzyElementFactory("fuzzy_factory", __time)
    engine = __fuzzy_factory.create_fuzzy_engine("battery_engine")
    # Endpoints
    # Battery
    # Physical values
    battery = __factory.generate_node("battery_node", cogni_sys)
    __battery_lhc = __factory.create_value(battery, "battery_lhc", [2.0])
    __battery_lc = __factory.create_value(battery, "battery_lc", [0.1])
    __battery_lrc = __factory.create_value(battery, "battery_lrc", [0.1])
    # Fuzzy value
    __li = __fuzzy_factory.generate_fuzzy_linguistic_nodes(cogni_sys, [
        ("battery_voltage", ["LOW", "MID", "HI"]),
        ("battery_capacity", ["LOW", "MID", "HI"]),
        ("battery_cmd", ["CLOSEFAST", "CLOSESLOW", "STANDBY", "OPENSLOW", "OPENFAST"])
    ])
    # Linguistic values
    ling_battery_voltage, ling_battery_capacity, ling_battery_cmd = __li
    # Fuzzy cmd
    fuzz_water_level, fuzz_water_rate, fuzz_water_cmd = __fuzzy_factory.generate_fuzzifier_nodes(cogni_sys, [
        ("battery_voltage_fuzzy", [mb.lamma_v, mb.tri_v, mb.gamma_v], [[-0.7, -0.4], [-0.5, 0.0, 0.5], [0.4, 0.7]]),
        ("battery_capacity_fuzzy", [mb.lamma_v, mb.tri_v, mb.gamma_v], [[-0.7, -0.4], [-0.5, 0.0, 0.5], [0.4, 0.7]]),
        ("battery_cmd_fuzzy", [mb.tri_v, mb.tri_v, mb.tri_v, mb.tri_v, mb.tri_v],
         [[-1.0, -0.7, -0.3], [-0.45, -0.2, 0.0], [-0.5, 0.0, 0.5], [0.0, 0.2, 0.45], [0.4, 0.7, 1.0]])
    ])
    # Fuzzy membership nodes
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_battery_voltage, fuzz_water_level, EnumRelationDirection.INWARDS,
                                           battery, ["battery_voltage"], [0.0, 20.0])
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_battery_capacity, fuzz_water_rate, EnumRelationDirection.INWARDS,
                                           battery, ["battery_capacity"], [-2.0, 2.0])
    # Command values
    __wcmd = __factory.create_value(ling_battery_cmd, "battery_cmd", [0.0])
    __wcmd_raw = __factory.create_value(ling_battery_cmd, "raw_battery_cmd", [0.0])
    # Connect linguistic node with command output
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_battery_cmd, fuzz_water_cmd, EnumRelationDirection.OUTWARDS,
                                           cogni_sys, ["battery_cmd"], [-1.0, 1.0])
    # Computation edge
    __he = __fuzzy_factory.generate_fuzzy_ruleset_edge(
        "battery_computation_edge", cogni_sys, [fuzz_water_level, fuzz_water_rate], [fuzz_water_cmd], [ling_battery_cmd],
        [
            ("R0", [('battery_voltage', ["LOW"])], [("battery_cmd", ["CLOSEFAST"])]),
            ("R1", [('battery_voltage', ["HI"])], [("battery_cmd", ["OPENFAST"])]),
            ("R2", [('battery_voltage', ["MID"])], [("battery_cmd", ["STANDBY"])])
        ]
    )
    # Battery dynamic values

    # Computation edge
    __he = __fuzzy_factory.generate_fuzzy_ruleset_edge(
        "water_control", cogni_sys, [fuzz_water_level, fuzz_water_rate], [fuzz_water_cmd], [ling_battery_cmd],
        [
            ("R0", [('battery_voltage', ["LOW"])], [("battery_cmd", ["CLOSEFAST"])]),
            ("R1", [('battery_voltage', ["HI"])], [("battery_cmd", ["OPENFAST"])]),
            ("R2", [('battery_voltage', ["MID"])], [("battery_cmd", ["STANDBY"])])
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
        __battery_lhc.update_value(0, __lh)

        __lc = 30/(1+np.exp(-0.15*v+ 4))
        lc.append(__lc)
        __battery_lhc.update_value(1, __lc)
        __lrc = 30/(1+np.exp(-0.3*v + 2))
        lrc.append(__lrc)
        __battery_lrc.update_value(2, __lrc)
        # Update dynamic values
        __volt = 12*np.exp(-v) + 0.5
        volt.append(__volt)
        #__battery_dynamic_values.update_value(0, __volt)

        __charge = 6*np.exp(-2*v) + 0.7
        charge.append(__charge)
        #__battery_dynamic_values.update_value(1, __charge)

        __capacity = 12.0*np.exp(-0.1*v) + 0.1
        capacity.append(__capacity)
        #__battery_dynamic_values.update_value(2, __capacity)
        import asyncio
        #asyncio.run(engine.infer_edge(__battery_infer))
        #z.append(*__battery_result_value._values)
        #_v = next(engine.defuzz(__battery_result_node),None)
        #defuzz.append(_v)
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
    # Decision space

    # Available energy
    plt.show()


if __name__=="__main__":
    main()
