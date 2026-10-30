"""Power law relationship between porosity and permeability in log-log space."""
import numpy as np

USED_INPUTS = ["phi"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    phi = X[:, 0]
    # Power law fit: log_k = 4.299837 * log10(phi) + 4.998884
    # This corresponds to k = 99743.472526 * phi^4.299837
    return 4.299837 * np.log10(phi) + 4.998884