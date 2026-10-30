"""Ratio of proton electric Sachs form factor to dipole form factor as a function of Q²."""
import numpy as np

USED_INPUTS = ["Q2_GeV2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Q2 = X[:, 0]
    # The ratio G_E/G_D follows the form 1/(1 + Q2)^2
    # This is a standard result in nuclear physics for the ratio of Sachs form factors
    return 1.0 / (1.0 + Q2)**2.0