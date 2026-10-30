"""Gutenberg-Richter law for earthquake frequency-magnitude distribution."""
import numpy as np

USED_INPUTS = ["M_threshold"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Gutenberg-Richter law: log10(N) = a - b*M
    # Where N is the cumulative number of earthquakes with magnitude >= M
    # a and b are constants determined from the data
    
    # Fitted parameters from the data:
    # a = 8.737231
    # b = 1.113999
    
    M = X[:, 0]
    a = 8.737231
    b = 1.113999
    
    return a - b * M