import numpy as np

from norm_vec import norm_vec

def canonical_criticality_measure(u_vec, grad_vec, lbu, ubu, mesh_width):
    # Criticality measure for min f(u) subject to lbu <= u <= ubu
    w_vec = u_vec-grad_vec
    proj_w = np.clip(w_vec, lbu, ubu)
    return norm_vec(u_vec-proj_w, mesh_width)
