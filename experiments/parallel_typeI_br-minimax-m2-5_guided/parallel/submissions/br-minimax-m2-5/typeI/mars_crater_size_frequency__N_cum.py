"""Crater size-frequency distribution: quadratic in log-log space (diameter-dependent power law index)."""
import numpy as np

USED_INPUTS = ["D_lower_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    D = X[:, 0]
    # log10(N) = c + b*log10(D) + a*log10(D)^2
    # with a = -0.4658, b = -0.4786, c = -2.8011
    log_D = np.log10(D)
    log_N = -2.8011 + (-0.4786) * log_D + (-0.4658) * (log_D ** 2)
    return 10 ** log_N