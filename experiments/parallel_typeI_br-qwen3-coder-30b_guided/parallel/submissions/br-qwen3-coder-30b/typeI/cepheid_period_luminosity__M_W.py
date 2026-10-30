"""Cepheid absolute Wesenheit magnitude relation with period and metallicity dependence."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_P = X[:, 0]
    feh = X[:, 1]
    # Based on the fitted model: M_W = A * log_P + B + C * feh + D * log_P * feh
    # Using coefficients from the best fit (interaction model)
    return -3.1241 * log_P + -2.9622 + 0.8656 * feh + -0.6768 * log_P * feh