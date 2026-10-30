"""PFAS solid-liquid partition coefficient model.

Kd = Koc * foc where Koc = a * Kow^0.5

This gives: log10(Kd) = log10(a) + 0.5*log_Kow + b*log10(foc)

The coefficient for foc is fitted as a separate parameter,
reflecting potential non-ideal sorption behavior.
"""
import numpy as np

USED_INPUTS = ["log_Kow", "foc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_Kow = X[:, 0]
    foc = X[:, 1]
    
    # log_kd = 0.5 * log_Kow + a * log10(foc) + b
    # Fitted: a = 0.5677, b = -0.4885
    log_kd = 0.5 * log_Kow + 0.5677 * np.log10(foc) - 0.4885
    
    return log_kd