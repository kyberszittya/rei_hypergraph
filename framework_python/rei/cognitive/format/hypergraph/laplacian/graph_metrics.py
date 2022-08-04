import numpy as np


def laplacian_calc(graph_tensor):
    D_m = np.apply_along_axis(np.sum, 2, graph_tensor[:-1, :-1, :-1], 0)
    d = np.apply_along_axis(np.diag, 1, D_m)
    L_m = d - graph_tensor[:-1, :-1, :-1]
    total_deg = np.sum(d)
    return D_m, L_m, d, total_deg


def entropy_edgewise(L_m, D_m):
    vals = []
    for i,e in enumerate(L_m):
        norm_e = e/np.sum(D_m[i])
        eigval = np.linalg.eig(norm_e)[0]
        eigval[eigval <= 0] = 1
        p = -np.sum(eigval*np.log2(eigval))
        vals.append(p)
    v = np.array(vals)
    return np.sum(v), v


def entropy_projected_laplace(L_m, D_m):
    inv_total = 1.0/np.sum(D_m)
    inv_L = np.sum(L_m, axis=0) * inv_total
    e, w = np.linalg.eig(inv_L)
    e[e <= 0] = 1.0
    entropy = e*np.log2(e)
    return -np.sum(entropy), entropy


def entropy_sum(L_m, D_m):
    degs = np.sum(D_m)
    x = D_m*(1.0/degs)
    x[x <= 0] = 1.0
    entropy = -x*np.log2(x)
    return np.sum(entropy), entropy


def entropy_avg(L_m, D_m):
    v = np.max(np.avg(L_m, axis=0), axis=1)
    entropy = -v*np.log2(v)
    return np.sum(entropy), entropy


def entropy_sum_avg(L_m, D_m):
    rowvise = np.sum(D_m, axis=0)
    x = D_m*(1.0/rowvise)
    x[x <= 0] = 1.0

    v = np.max(np.average(L_m, axis=1), axis=1)
    entropy_avg = -x*np.log2(x/v)
    return np.sum(entropy_avg), entropy_avg