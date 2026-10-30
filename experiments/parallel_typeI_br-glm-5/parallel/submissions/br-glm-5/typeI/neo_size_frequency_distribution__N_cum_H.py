"""Cumulative NEO count follows exponential law in magnitude: N = A * 10^(α*H)"""
import numpy as np

USED_INPUTS = ["H_upper"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    H = X[:, 0]
    # Fitted exponential: N = A * 10^(α * H)
    # α = 0.4840555478, A = 2.560989412185e-06
    A = 2.560989412185e-06
    alpha = 0.4840555478
    N_cum_H = A * 10**(alpha * H)
    return N_cum_H