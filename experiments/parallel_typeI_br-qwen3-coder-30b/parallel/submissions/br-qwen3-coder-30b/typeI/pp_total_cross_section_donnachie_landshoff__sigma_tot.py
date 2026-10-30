"""Cross-section model with logarithmic and exponential terms."""
import numpy as np

USED_INPUTS = ["s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    s = X[:, 0]
    # Model based on observed behavior: logarithmic growth with saturation
    # sigma_tot = 40 + 10 * log(s) + 5 * (1 - exp(-0.00001 * s))
    return 40 + 10 * np.log(s) + 5 * (1 - np.exp(-0.00001 * s))