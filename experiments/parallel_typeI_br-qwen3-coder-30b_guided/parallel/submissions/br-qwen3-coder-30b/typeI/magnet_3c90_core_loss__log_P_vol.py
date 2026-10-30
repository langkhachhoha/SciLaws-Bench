"""Magnetic core loss scaling law: P ~ f^1.63 * B^2.33"""
import numpy as np

USED_INPUTS = ["f_Hz", "B_peak_T"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    f = X[:, 0]
    B = X[:, 1]
    # From our analysis: log(P) = 1.634 * log(f) + 2.326 * log(B) - 3.838
    # So: P = 10^(-3.838) * f^(1.634) * B^(2.326)
    # Which is approximately: P = 0.000149 * f^(1.634) * B^(2.326)
    return 10**(-3.838) * (f**1.634) * (B**2.326)