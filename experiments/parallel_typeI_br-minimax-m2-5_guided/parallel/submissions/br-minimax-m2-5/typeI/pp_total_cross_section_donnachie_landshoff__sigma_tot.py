"""Total proton-proton cross-section with Froissart-logarithmic scaling: sigma_tot = a + b*log(s) + c*log²(s)."""
import numpy as np

USED_INPUTS = ["s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    s = X[:, 0]
    log_s = np.log(s)
    # Froissart behavior: sigma_tot ≈ a + b*ln(s) + c*ln²(s)
    return 47.833779 - 3.606373 * log_s + 0.363254 * log_s**2