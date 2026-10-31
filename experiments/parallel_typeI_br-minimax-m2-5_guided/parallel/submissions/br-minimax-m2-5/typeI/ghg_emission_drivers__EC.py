"""Energy consumption as GDP^0.61 * TP * (AP/100)^3.68 * (UR/100)^0.47 * exp(-0.017*AT) * (100/DP)^0.07"""
import numpy as np

USED_INPUTS = ["GDP", "TP", "AP", "UR", "AT", "DP"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    GDP = X[:, 0]
    TP = X[:, 1]
    AP = X[:, 2]
    UR = X[:, 3]
    AT = X[:, 4]
    DP = X[:, 5]
    
    # Formula: EC = GDP^0.61 * TP * (AP/100)^3.68 * (UR/100)^0.47 * exp(-0.017*AT) * (100/DP)^0.07 * C
    C = 0.000162
    
    EC = (GDP**0.61) * TP * ((AP/100)**3.68) * ((UR/100)**0.47) * np.exp(-0.017 * AT) * ((100/DP)**0.07) * C
    
    return EC