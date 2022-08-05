import numpy as np

from rei.cognitive.format.hypergraph.laplacian.graph_metrics import entropy_sum, entropy_projected_laplace


def laplacian_calc(M):
    D_m = np.sum(M, axis=0)
    L_m = np.diag(D_m) - M
    deg = np.sum(D_m)
    return D_m, L_m, deg


def laplacian_calc_tensor(A):
    total_deg = 0
    Ds = []
    Ls = []
    degs = []
    for e in A:
        D, L, deg = laplacian_calc(e)
        Ds.append(D)
        Ls.append(L)
        degs.append(deg)
        total_deg += deg
    return np.array(Ds), np.array(Ls), total_deg


# Entropy calculations
def graph_bound_entropy(A):
    _, Ls, total_deg = laplacian_calc_tensor(A)
    total_entropy = 0.0
    for L in Ls:
        tr = np.trace(L)
        norm_tr = tr / total_deg
        total_entropy -= norm_tr*np.log2(norm_tr)
    return total_entropy


def laplacian_calc_vector(M):
    D_m = np.sum(M, 1)
    d = np.apply_along_axis(np.diag, 1, D_m)
    L_m = d - M
    deg = np.sum(np.abs(D_m))
    return d, L_m, deg



