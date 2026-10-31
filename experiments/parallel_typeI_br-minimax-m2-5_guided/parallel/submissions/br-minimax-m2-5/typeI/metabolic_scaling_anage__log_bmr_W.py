"""Kleiber's law: BMR scales as M^0.75 (log10 space: slope = 0.75)"""
import numpy as np

USED_INPUTS = ["body_mass_g"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # log_bmr_W = 0.75 * log10(body_mass_g) - 1.723
    log_mass = np.log10(X[:, 0])
    return 0.75 * log_mass - 1.723