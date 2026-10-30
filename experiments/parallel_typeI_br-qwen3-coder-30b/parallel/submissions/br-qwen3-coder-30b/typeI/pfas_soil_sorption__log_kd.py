"""Linear model: log_kd = a * log_Kow + b * foc + c"""
import numpy as np

USED_INPUTS = ["log_Kow", "foc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_Kow = X[:, 0]
    foc = X[:, 1]
    # Coefficients from least squares fit
    a = 0.9372
    b = -3.1891
    c = -2.7258
    return a * log_Kow + b * foc + c