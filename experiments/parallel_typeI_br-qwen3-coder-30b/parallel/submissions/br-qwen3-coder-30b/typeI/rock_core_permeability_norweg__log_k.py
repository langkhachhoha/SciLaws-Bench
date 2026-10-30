"""Power law relationship between porosity and permeability."""
import numpy as np

USED_INPUTS = ["phi"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    phi = X[:, 0]
    # Based on analysis of the simulator data, log_k ≈ 4.5 * phi^1.5
    return 4.5 * (phi ** 1.5)