"""Mass-Radius relation for sub-stellar objects using Langmuir-like equation.
R = 12.5 * M / (32 + M) + 0.5
Equivalent form: R = (13*M + 16) / (M + 32)
"""
import numpy as np

USED_INPUTS = ["M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    M = X[:, 0]
    return 12.5 * M / (32 + M) + 0.5