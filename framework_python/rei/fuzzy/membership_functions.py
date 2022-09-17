import numpy as np


def gamma(x, alpha: float, beta: float):
    return (np.clip(x, alpha, beta) - alpha)/(beta - alpha)


def gamma_v(*args):
    return (np.clip(args[0], args[1], args[2]) - args[1])/(args[2] - args[1])


def lamma(x, alpha: float, beta: float):
    return 1.0 - (np.clip(x, alpha, beta) - alpha)/(beta - alpha)


def lamma_v(*args):
    return 1.0 - (np.clip(args[0], args[1], args[2]) - args[1])/(args[2] - args[1])


def tri(x, alpha: float, beta: float, c: float):
    return gamma(x, alpha, beta) - gamma(x, beta, c)


def tri_v(*args):
    return gamma(args[0], args[1], args[2]) - gamma(args[0], args[2], args[3])


def trap(x, a: float, b: float, c: float, d: float):
    return gamma(x, a, b) - gamma(x, c, d)


def trap_v(*args):
    return gamma(args[0], args[1], args[2]) - gamma(args[0], args[2], args[3])
