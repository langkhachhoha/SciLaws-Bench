"""GE/GD = 1 - a*Q² - b*Q⁴: Polynomial form for proton electric Sachs form factor ratio."""
import numpy as np

USED_INPUTS = ["Q2_GeV2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Q2 = X[:, 0]
    return 1 - 0.074 * Q2 - 0.008 * Q2**2