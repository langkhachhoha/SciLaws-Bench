"""Linear combination of spatial derivatives of vorticity and deformation fields."""
import numpy as np

USED_INPUTS = ["d_zeta2_dx", "d_zetaD_dx", "d_zetaDtilde_dy"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d_zeta2_dx = X[:, 0]
    d_zetaD_dx = X[:, 1]
    d_zetaDtilde_dy = X[:, 2]
    
    # Based on the discovered relationship from experimental data
    return -3.99e+08 * d_zeta2_dx + 8.88e+08 * d_zetaD_dx - 9.71e+08 * d_zetaDtilde_dy