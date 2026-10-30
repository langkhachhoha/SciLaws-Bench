"""Power law fit for Martian crater size-frequency distribution."""
import numpy as np

USED_INPUTS = ["D_lower_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    D = X[:, 0]
    # Fitted constants from experimental data analysis
    K = 0.003198
    alpha = 1.7245
    return K * (D ** (-alpha))