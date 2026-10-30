"""Basal metabolic rate as linear plus surface-area scaling: BMR = a*M + b*M^(2/3)

This combines tissue mass metabolism (linear term) with surface-area dependent 
heat loss (M^(2/3) term), providing a physiologically interpretable formula.
"""
import numpy as np

USED_INPUTS = ["body_mass_g"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    M = X[:, 0]  # body_mass_g
    a = 0.0005   # W/g linear coefficient
    b = 0.025    # W/g^(1/3) surface-area coefficient
    bmr_W = a * M + b * M**(2/3)
    return np.log10(bmr_W)