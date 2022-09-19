import numpy as np

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import LocalClock
from rei.fuzzy.fuzzy_element_factory import FuzzyElementFactory

import rei.fuzzy.membership_functions as mb
import rei.fuzzy.norm_functions as no

import matplotlib.pyplot as plt

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
    ling_water_level = __fuzzy_factory.create_linguistic_node("water_level", cogni_sys, ["LOW","MID","HI"])
    ling_water_rate = __fuzzy_factory.create_linguistic_node("water_rate", cogni_sys, ["LOW","MID","HI"])
    # Fuzzy cmd
    ling_water_cmd = __fuzzy_factory.create_linguistic_node(
        "water_cmd", cogni_sys, ["CLOSEFAST", "CLOSESLOW", "STANDBY", "OPENSLOW", "OPENFAST"])
    #
    fuzz_water_level = __fuzzy_factory.create_fuzzifier_node(
        "water_level_fuzzy", cogni_sys, [mb.lamma_v, mb.tri_v, mb.gamma_v],
        [[-0.7, -0.4], [-0.5, 0.0, 0.5], [0.4, 0.7]])
    fuzz_water_rate = __fuzzy_factory.create_fuzzifier_node(
        "water_rate_fuzzy", cogni_sys, [mb.lamma_v, mb.tri_v, mb.gamma_v],
        [[-0.7, -0.4], [-0.5, 0.0, 0.5], [0.4, 0.7]])
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_water_level, fuzz_water_level, __water_sensor,
                                           ["water_level"], [0.0, 20.0])
    __fuzzy_factory.connect_fuzzifier_node(cogni_sys, ling_water_rate, fuzz_water_rate, __water_sensor,
                                           ["water_rate"], [-2.0, 2.0])
    # Control
    fuzz_water_cmd = __fuzzy_factory.create_fuzzifier_node(
        "water_cmd_fuzzy", cogni_sys, [mb.tri_v, mb.tri_v, mb.tri_v, mb.tri_v, mb.tri_v],
        [[-1.0, -0.7, -0.3], [-0.45, -0.2, 0.0], [-0.5, 0.0, 0.5], [0.0, 0.2, 0.45], [0.4, 0.7, 1.0]])
    __he = __fuzzy_factory.create_computation_edge("water_control", cogni_sys,
                                                   [fuzz_water_level, fuzz_water_rate],
                                                   [fuzz_water_cmd], [ling_water_cmd])
    _r = __fuzzy_factory.create_rule(
        "R01", __he, [fuzz_water_level], [('water_level', ["LOW"])], [("water_cmd", ["CLOSEFAST"])])
    # Endpoints
    import matplotlib.pyplot as plt
    wf = np.linspace(0, 20, 100)
    __wl.update_values(wf)
    wr = np.linspace(-2, 2, 100)
    __wr.update_values(wr)
    # Water
    fuzz_water_level.fuzzify()
    fuzz_water_rate.fuzzify()
    __he.eval()
    # Plot results
    plt.subplot(2,1,1)
    for _v in next(fuzz_water_level.get_values("values")).get_values():
        plt.plot(wf, _v)
    plt.plot(wf, np.max(next(fuzz_water_level.get_values("values")).get_values(), axis=0), linestyle='--')
    plt.subplot(2,1,2)
    for _v in next(fuzz_water_rate.get_values("values")).get_values():
        plt.plot(wr, _v)
    plt.show()


if __name__=="__main__":
    main()
