"""Metabolic scaling law (Kleiber's law) for basal metabolic rate."""
import numpy as np

USED_INPUTS = ["body_mass_g"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # log(BMR) = 0.759941 * log(M) - 1.712069
    # This is equivalent to BMR = 10^(-1.712069) * M^(0.759941)
    # where M is body mass in grams and BMR is in watts
    mass = X[:, 0]
    return 0.759941 * np.log10(mass) - 1.712069