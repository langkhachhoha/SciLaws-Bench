"""Win percentage based on run differential ratio."""
import numpy as np

USED_INPUTS = ["R", "RA"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    R = X[:, 0]
    RA = X[:, 1]
    # Using the relationship: win_pct = 1.005975 * (R-RA)/(R+RA) + 0.502678
    # Rounded to reasonable precision for the final formula
    return 1.006 * (R - RA) / (R + RA) + 0.503