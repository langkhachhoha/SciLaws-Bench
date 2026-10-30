"""Linear relationship between log10_F_1p3_Jy and log10_M_star_SDF00."""
import numpy as np

USED_INPUTS = ["log10_M_star_SDF00"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Based on the linear fit: y = 0.7158 * x - 1.4147
    return 0.7158 * x - 1.4147