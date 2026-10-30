"""Linear fade model for Li-ion battery capacity degradation."""
import numpy as np

USED_INPUTS = ["cycle_index"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = X[:, 0]  # cycle_index
    Q0 = 1.9152  # initial capacity (Ah)
    b = 0.0041   # fade rate per cycle (Ah/cycle)
    return Q0 - b * k