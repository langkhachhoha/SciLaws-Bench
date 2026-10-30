"""Kozeny-Carman permeability-porosity relationship."""
import numpy as np

USED_INPUTS = ["phi"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    phi = X[:, 0]
    # KC form: log10(k) = A + 3*log10(phi) - 2*log10(1-phi)
    # Equivalent to: k ~ phi³/(1-phi)²
    A = 3.05
    log_k = A + 3*np.log10(phi) - 2*np.log10(1 - phi)
    return log_k