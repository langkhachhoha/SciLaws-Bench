"""Power law relationship between river main-stem length and drainage area (Hack's law).
L = 1.76 * A^0.55 where L is main-stem river length (km) and A is drainage area (km^2)."""
import numpy as np

USED_INPUTS = ["upland_area_skm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    A = X[:, 0]  # drainage area in km^2
    return 1.76 * (A ** 0.55)