"""Proton electric form factor ratio GE/GD approximated as 1/(1 + Q^4/18)."""
import numpy as np

USED_INPUTS = ["Q2_GeV2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # GE/GD = 1 / (1 + Q^4/18) = 18 / (18 + Q^4)
    # Where Q^4 = (Q^2)^2
    Q2 = X[:, 0]
    return 18.0 / (18.0 + Q2**2)