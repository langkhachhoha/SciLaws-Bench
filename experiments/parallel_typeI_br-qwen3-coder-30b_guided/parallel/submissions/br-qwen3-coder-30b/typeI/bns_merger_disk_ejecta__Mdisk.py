"""Disk mass as a function of compactness, using a power-law form with physical motivation."""
import numpy as np

USED_INPUTS = ["C1"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Using a physically motivated power law form
    # Mdisk = A * (1 - C1)^B where A and B are fitted constants
    # Based on the data analysis, we expect a strong inverse relationship
    # with a steep decline for higher compactness values
    
    c1 = X[:, 0]
    
    # The relationship appears to be approximately Mdisk = 0.26 * (1 - C1)^8.5
    # This captures both the rapid decrease for small C1 values 
    # and the very small values for large C1 values
    
    return 0.26 * np.power((1.0 - c1), 8.5)