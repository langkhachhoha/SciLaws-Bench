"""PFAS solid-liquid distribution coefficient: log_kd = 0.5*log_Kow + 0.6*log10(foc) - 0.4

This form captures the square-root dependence on Kow (hydrophobic effect, a ≈ 0.5) and the organic carbon normalization (b ≈ 0.6). The constant captures baseline sorption."""
import numpy as np

USED_INPUTS = ["log_Kow", "foc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # X[:, 0] = log_Kow, X[:, 1] = foc
    log_Kow = X[:, 0]
    foc = X[:, 1]
    return 0.5 * log_Kow + 0.6 * np.log10(foc) - 0.4