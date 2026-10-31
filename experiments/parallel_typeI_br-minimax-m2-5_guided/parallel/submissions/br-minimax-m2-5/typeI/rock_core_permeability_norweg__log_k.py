"""Power law relationship: log_k = a + b * phi^0.1 where a and b are fitted constants. This captures the nonlinear relationship between porosity and permeability."""
import numpy as np

USED_INPUTS = ["phi"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return -18.99 + 24.16 * x**0.1