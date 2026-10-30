"""Black hole mass scaling relation with stellar spheroid mass."""
import numpy as np

USED_INPUTS = ["log_M_sph"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Based on the experimental data, the relationship is:
    # log(M_BH) = 1.1 * log(M_sph) - 3.4
    # where M_BH is in solar masses and M_sph is in solar masses
    x = X[:, 0]
    return 1.1 * x - 3.4