"""Power-law scaling: M_BH ∝ M_sph^1.09 (the M-sphere relation)."""
import numpy as np

USED_INPUTS = ["log_M_sph"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 1.0945 * x - 3.3954