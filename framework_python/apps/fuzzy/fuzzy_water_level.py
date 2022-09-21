import numpy as np

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import LocalClock
from rei.fuzzy.fuzzy_element_factory import FuzzyElementFactory

import rei.fuzzy.membership_functions as mb


from rei.hypergraph.common_definitions import EnumRelationDirection


def main():
    __time = LocalClock()
    __factory = HypergraphFactory("fuzzy_sys_factory", __time)
    cogni_sys = __factory.generate_node("fuzzy_sys_cogni")
    ambient_sys = __factory.generate_node("ambient_sys")
    # Factory
    __fuzzy_factory = FuzzyElementFactory("fuzzy_factory", __time)
    engine = __fuzzy_factory.create_fuzzy_engine("water_engine")
    # Physical values
    __water_sensor = __factory.generate_node("water_sensor", ambient_sys)
    __wl = __factory.create_value(__water_sensor, "water_level", [2.0])
    __wr = __factory.create_value(__water_sensor, "water_rate", [0.1])

    # Fuzzy value
    __li = __fuzzy_factory.generate_fuzzy_linguistic_nodes(cogni_sys, [
        ("water_level", ["LOW", "MID", "HI"]),
        ("water_rate", ["LOW", "MID", "HI"]),
        ("water_cmd", ["CLOSEFAST", "CLOSESLOW", "STANDBY", "OPENSLOW", "OPENFAST"])
    ])
    ling_water_level, ling_water_rate, ling_water_cmd = __li
    # Fuzzy cmd
    fuzz_water_level, fuzz_water_rate, fuzz_water_cmd = __fuzzy_factory.generate_fuzzifier_nodes(cogni_sys, [
        ("water_level_fuzzy", [mb.lamma_v, mb.tri_v, mb.gamma_v], [[-0.7, -0.4], [-0.5, 0.0, 0.5], [0.4, 0.7]]),
        ("water_rate_fuzzy", [mb.lamma_v, mb.tri_v, mb.gamma_v], [[-0.7, -0.4], [-0.5, 0.0, 0.5], [0.4, 0.7]]),
        ("water_cmd_fuzzy", [mb.tri_v, mb.tri_v, mb.tri_v, mb.tri_v, mb.tri_v],
         [[-1.0, -0.7, -0.3], [-0.45, -0.2, 0.0], [-0.5, 0.0, 0.5], [0.0, 0.2, 0.45], [0.4, 0.7, 1.0]])
    ])
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_water_level, fuzz_water_level, EnumRelationDirection.INWARDS,
                                           __water_sensor, ["water_level"], [0.0, 20.0])
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_water_rate, fuzz_water_rate, EnumRelationDirection.INWARDS,
                                           __water_sensor, ["water_rate"], [-2.0, 2.0])
    # Command values
    __wcmd = __factory.create_value(ling_water_cmd, "water_cmd", [0.0])
    __wcmd_raw = __factory.create_value(ling_water_cmd, "raw_water_cmd", [0.0])
    # Connect linguistic node with command output
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_water_cmd, fuzz_water_cmd, EnumRelationDirection.OUTWARDS,
                                           cogni_sys, ["water_cmd"], [-1.0, 1.0])
    # Computation edge
    #__he = __fuzzy_factory.create_computation_edge("water_control", cogni_sys,
    #                                               [fuzz_water_level, fuzz_water_rate],
    #                                               [fuzz_water_cmd], [ling_water_cmd])
    # Rules
    #_r1 = __fuzzy_factory.create_rule(
    #    "R01", __he, [fuzz_water_level, fuzz_water_cmd], [('water_level', ["LOW"])], [("water_cmd", ["CLOSEFAST"])])
    #_r2 = __fuzzy_factory.create_rule(
    #    "R02", __he, [fuzz_water_level, fuzz_water_cmd], [('water_level', ["HI"])], [("water_cmd", ["OPENFAST"])])
    __he = __fuzzy_factory.generate_fuzzy_ruleset_edge(
        "water_control", cogni_sys, [fuzz_water_level, fuzz_water_rate], [fuzz_water_cmd], [ling_water_cmd],
        [
            ("R0", [('water_level', ["LOW"])], [("water_cmd", ["CLOSEFAST"])]),
            ("R1", [('water_level', ["HI"])], [("water_cmd", ["OPENFAST"])]),
            ("R2", [('water_level', ["MID"])], [("water_cmd", ["STANDBY"])])
        ]
    )
    # Endpoints
    import matplotlib.pyplot as plt
    wf = np.linspace(0, 20, 100)
    __wl.update_values(wf)
    wr = np.linspace(-2, 2, 100)
    __wr.update_values(wr)
    # Water
    fuzz_water_level.fuzzify()
    fuzz_water_rate.fuzzify()
    # Plot results
    plt.gcf().canvas.get_renderer()
    # Plot membership
    plt.subplot(2,1,1)
    for _v in next(fuzz_water_level.get_values("values")).get_values():
        plt.plot(wf, _v)
    plt.plot(wf, np.max(next(fuzz_water_level.get_values("values")).get_values(), axis=0), linestyle='--')
    plt.subplot(2,1,2)
    for _v in next(fuzz_water_rate.get_values("values")).get_values():
        plt.plot(wr, _v)
    plt.show()
    __he.eval()
    plt.figure()
    plt.subplot(3,1,1)
    _y = next(ling_water_cmd.get_values("water_cmd")).get_values()
    _y_raw = next(ling_water_cmd.get_values("water_cmd")).get_values()
    plt.plot(_y)
    fuzz_water_cmd.fuzzify()
    plt.subplot(3,1,2)
    __tau = next(fuzz_water_cmd.get_values("values")).get_values()
    for _v in __tau:
        plt.plot(_v)
    # Summarizing
    plt.subplot(3,1,3)
    plt.plot(np.sum(__tau, axis=0) * _y/ (
            (np.sum(__tau)/np.count_nonzero(__tau))*(np.sum(_y)/np.count_nonzero(__tau))))
    plt.show()


if __name__=="__main__":
    main()
