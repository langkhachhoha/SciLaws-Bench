"""Battery capacity degradation following exponential decay model."""
import numpy as np

USED_INPUTS = ["cycle_index"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Parameters obtained from fitting the exponential decay model
    # capacity = A * exp(-k * cycle) + C_min
    A = 1.8843
    k = 0.003467
    C_min = 1.1789
    
    cycle_index = X[:, 0]
    return A * np.exp(-k * cycle_index) + C_min