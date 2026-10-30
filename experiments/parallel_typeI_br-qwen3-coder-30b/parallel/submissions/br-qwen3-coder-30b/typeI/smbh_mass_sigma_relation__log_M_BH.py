"""Power law relationship between supermassive black hole mass and galaxy spheroid mass."""
import numpy as np

USED_INPUTS = ["log_M_sph"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Based on fitted power law: log_M_BH = 0.260980 * (log_M_sph)^1.4577
    return 0.260980 * (x ** 1.4577)