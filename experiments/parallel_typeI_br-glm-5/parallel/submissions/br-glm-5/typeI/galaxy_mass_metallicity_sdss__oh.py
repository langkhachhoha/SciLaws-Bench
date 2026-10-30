"""Mass-metallicity relation: quadratic in log stellar mass centered at 10 solar masses.

The gas-phase oxygen abundance oh = 12 + log(O/H) follows a quadratic function
of log stellar mass, capturing the observed saturation at high masses.

Formula: oh = 8.9 + 0.25*(log_Mstar - 10) - 0.0625*(log_Mstar - 10)^2

This can also be written with the quadratic coefficient as 1/16:
oh = 8.9 + 0.25*(log_Mstar - 10) - (log_Mstar - 10)^2/16
"""
import numpy as np

USED_INPUTS = ["log_Mstar"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_Mstar = X[:, 0]
    # Centered quadratic form
    dm = log_Mstar - 10.0
    oh = 8.9 + 0.25 * dm - 0.0625 * dm**2
    return oh