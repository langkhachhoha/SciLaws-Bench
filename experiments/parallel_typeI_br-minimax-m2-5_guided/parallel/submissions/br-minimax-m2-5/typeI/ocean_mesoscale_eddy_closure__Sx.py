"""Subgrid-scale zonal eddy momentum forcing: Sx = k * (-5*d_zeta2_dx + 11*d_zetaD_dx - 12*d_zetaDtilde_dy)"""
import numpy as np

USED_INPUTS = ["d_zeta2_dx", "d_zetaD_dx", "d_zetaDtilde_dy"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = 8.062e7
    d_zeta2_dx = X[:, 0]
    d_zetaD_dx = X[:, 1]
    d_zetaDtilde_dy = X[:, 2]
    return k * (-5 * d_zeta2_dx + 11 * d_zetaD_dx - 12 * d_zetaDtilde_dy)