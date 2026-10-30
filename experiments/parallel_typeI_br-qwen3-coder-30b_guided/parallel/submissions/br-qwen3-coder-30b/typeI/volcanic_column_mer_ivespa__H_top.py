"""Power law relationship between mass eruption rate and eruption column height."""
import numpy as np

USED_INPUTS = ["MER_kg_per_s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Fitted constants from experimental data
    A = 0.4549
    b = 0.2110
    mer = X[:, 0]
    return A * (mer ** b)