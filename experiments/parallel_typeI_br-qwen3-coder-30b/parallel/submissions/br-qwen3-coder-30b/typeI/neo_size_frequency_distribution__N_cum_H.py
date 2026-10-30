"""Cumulative near-Earth object distribution following power law with exponent ~2."""
import numpy as np

USED_INPUTS = ["H_upper"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    H_upper = X[:, 0]
    # Based on the observed linear relationship in log space: 
    # log10(N_cum_H) = 0.5007 * H_upper - 5.8650
    # Therefore: N_cum_H = 10^(-5.8650) * 10^(0.5007 * H_upper)
    # Which simplifies to: N_cum_H = 1.36e-6 * (3.16)^H_upper
    return 1.36e-6 * (3.16 ** H_upper)