"""Power law fit for cumulative near-Earth object distribution."""
import numpy as np

USED_INPUTS = ["H_upper"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Based on analysis of the cumulative distribution data
    # N_cum_H = A * H_upper^gamma where A ≈ 2.0e-18 and gamma ≈ 16.82
    # But this leads to numerical issues, so we'll use a more numerically stable form
    # Using the relationship from log-log analysis: N_cum_H = 10^(-17.73) * H_upper^(16.54)
    H_upper = X[:, 0]
    # Numerically stable version: multiply by 10^(-17.73) = 1.86e-18
    return 1.86e-18 * (H_upper ** 16.54)