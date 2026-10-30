"""Thermocline depth follows a logarithmic relationship with lake surface area.
This is physically motivated: larger lakes have longer wind fetch, leading to
deeper mixing and thermocline. The log form captures the diminishing returns
as fetch effects saturate with increasing area."""
import numpy as np

USED_INPUTS = ["A_s_km2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    A = X[:, 0]
    # z_t = a + b * ln(A), where a ≈ 7.23 m, b ≈ 1.13
    return 7.23 + 1.13 * np.log(A)