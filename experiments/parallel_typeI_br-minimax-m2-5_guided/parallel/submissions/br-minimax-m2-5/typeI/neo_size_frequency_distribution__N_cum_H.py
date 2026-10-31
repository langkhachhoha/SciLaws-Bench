"""Log-linear cumulative NEO count: N_cum_H = 10^(0.5*H - 5.819)"""
import numpy as np

USED_INPUTS = ["H_upper"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    H = X[:, 0]
    # log10(N) = 0.5*H + b where b = -5.8191
    return 10**(0.5 * H - 5.8191)