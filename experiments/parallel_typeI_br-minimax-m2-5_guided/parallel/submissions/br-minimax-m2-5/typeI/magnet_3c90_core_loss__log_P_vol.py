"""Steinmetz-type power law for ferrite core losses: log_P = a + alpha*log10(f) + beta*log10(B)"""
import numpy as np

USED_INPUTS = ["f_Hz", "B_peak_T"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    f = X[:, 0]
    B = X[:, 1]
    # log_P = -4.186 + 1.7*log10(f) + 2.4*log10(B)
    return -4.186 + 1.7 * np.log10(f) + 2.4 * np.log10(B)