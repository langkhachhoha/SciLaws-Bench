"""Geomagnetic Dst index tendency model based on physical relationships."""
import numpy as np

USED_INPUTS = ["Dst", "Ey", "P_dyn"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    Dst = X[:, 0]
    Ey = X[:, 1] 
    P_dyn = X[:, 2]
    
    # Fitted coefficients from experimental data analysis
    # dDst_dt = -0.0581*Dst - 1.4521*Ey + 0.2562/P_dyn - 6.5271
    return -0.058065 * Dst - 1.452084 * Ey + 0.256221 / P_dyn - 6.527052