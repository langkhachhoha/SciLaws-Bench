"""Power law model for magnetic core loss: log_P_vol = A + alpha*log10(f) + beta*log10(B)"""
import numpy as np

USED_INPUTS = ["f_Hz", "B_peak_T"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    f = X[:, 0]
    B = X[:, 1]
    # Coefficients determined from experimental data
    A = -3.1364
    alpha = 1.4934
    beta = 2.3053
    return A + alpha * np.log10(f) + beta * np.log10(B)