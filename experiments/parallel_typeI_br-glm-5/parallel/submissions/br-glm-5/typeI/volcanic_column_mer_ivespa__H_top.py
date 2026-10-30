"""Quarter-power scaling law for eruption column height.

Classical volcanological model: H = a * MER^(1/4) + b
Based on buoyant plume rise theory (Morton et al. 1956, Sparks 1986).
The 1/4 exponent arises from dimensional analysis of plume rise in a stratified atmosphere.
The intercept b represents a minimum height offset (lava fountaining, observation threshold).
"""
import numpy as np

USED_INPUTS = ["MER_kg_per_s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    MER = X[:, 0]
    a = 0.198
    b = 1.0
    H = a * MER**0.25 + b
    return H