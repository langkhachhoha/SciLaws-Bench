"""Win percentage based on normalized run differential."""
import numpy as np

USED_INPUTS = ["R", "RA", "G"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    R = X[:, 0]
    RA = X[:, 1]
    G = X[:, 2]
    
    # Calculate normalized run differential
    diff = R - RA
    total = R + RA
    
    # Avoid division by zero
    total = np.where(total == 0, 1e-10, total)
    
    normalized_diff = diff / total
    
    # Linear relationship found from data
    # win_pct = 1.2539 * normalized_diff + 0.4976
    win_pct = 1.2539 * normalized_diff + 0.4976
    
    return win_pct