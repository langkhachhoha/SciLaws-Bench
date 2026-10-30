"""Mass-averaged terminal velocity of dynamical ejecta follows a power-law scaling."""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    L = X[:, 1]
    return 0.587 / np.sqrt(q) / (L ** (1/7))