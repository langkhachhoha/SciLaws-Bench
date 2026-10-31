"""Mass-metallicity relation: exponential saturation form."""
import numpy as np

USED_INPUTS = ["log_Mstar"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # oh = oh_sat - a * exp(-b * log_Mstar)
    # Exponential saturation: metallicity increases with mass then saturates
    oh_sat = 9.2942
    a = 120.398
    b = 0.5744
    return oh_sat - a * np.exp(-b * x)