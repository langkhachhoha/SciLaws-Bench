"""Binary pulsar period derivative formula based on general relativity."""
import numpy as np

USED_INPUTS = ["Pb", "e"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Pb = X[:, 0]
    e = X[:, 1]
    
    # PBDOT = K * Pb^(-3/2) * e^4
    # Using K ≈ 1.0e-10 based on physical considerations and data analysis
    K = 1.0e-10
    return K * (Pb**(-1.5)) * (e**4)