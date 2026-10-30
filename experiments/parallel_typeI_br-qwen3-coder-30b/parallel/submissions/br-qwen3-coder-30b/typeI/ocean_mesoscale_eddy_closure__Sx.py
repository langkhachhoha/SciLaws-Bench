"""Proportional relationship between Sx and sum of inputs with fitted constant."""
import numpy as np

USED_INPUTS = ["d_zeta2_dx", "d_zetaD_dx", "d_zetaDtilde_dy"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Based on the experimental data, Sx appears to be proportional to the sum of inputs
    # with a proportionality constant of approximately 9.6e8
    # Sx = -961650773.7258934 * (d_zeta2_dx + d_zetaD_dx + d_zetaDtilde_dy)
    k = -961650773.7258934
    sum_inputs = X[:, 0] + X[:, 1] + X[:, 2]
    return k * sum_inputs