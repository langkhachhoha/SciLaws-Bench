"""Cepheid Period-Luminosity relation with metallicity dependence and interaction term."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_P = X[:, 0]
    feh = X[:, 1]
    # M_W = a*log_P + b + c*feh + d*log_P*feh
    # where a ≈ -3.23 (PL slope), b ≈ -2.80 (intercept), 
    # c ≈ 0.63 (metallicity term), d ≈ -0.70 (interaction)
    a = -3.23
    b = -2.80
    c = 0.63
    d = -0.70
    return a * log_P + b + c * feh + d * log_P * feh