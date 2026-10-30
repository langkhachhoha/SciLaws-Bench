"""Power law fit for Martian crater size-frequency distribution."""
import numpy as np

USED_INPUTS = ["D_lower_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    D = X[:, 0]
    # Fitted coefficient and exponent from experimental data
    A = 4.072e-03
    gamma = 1.565
    return A * (D ** (-gamma))