"""Linear subgrid-scale momentum closure: zonal eddy momentum forcing
is a linear combination of enstrophy gradient and vorticity-deformation gradients."""
import numpy as np

USED_INPUTS = ["d_zeta2_dx", "d_zetaD_dx", "d_zetaDtilde_dy"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x1 = X[:, 0]  # d_zeta2_dx
    x2 = X[:, 1]  # d_zetaD_dx
    x3 = X[:, 2]  # d_zetaDtilde_dy
    
    c1 = -5.3938e+08
    c2 = 9.5629e+08
    c3 = -1.0787e+09
    
    return c1 * x1 + c2 * x2 + c3 * x3