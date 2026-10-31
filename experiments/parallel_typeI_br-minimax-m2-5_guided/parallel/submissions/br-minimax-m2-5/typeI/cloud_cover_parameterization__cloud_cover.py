"""Cloud cover formula: C = a * (q_c + q_i) * RH * (T_ref - T) + c."""
import numpy as np

USED_INPUTS = ["q_c", "q_i", "RH", "T"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q_c = X[:, 0]
    q_i = X[:, 1]
    RH = X[:, 2]
    T = X[:, 3]
    
    moisture = q_c + q_i
    T_ref = 300.0
    a = 36.9
    c = 0.31
    
    return a * moisture * RH * (T_ref - T) + c