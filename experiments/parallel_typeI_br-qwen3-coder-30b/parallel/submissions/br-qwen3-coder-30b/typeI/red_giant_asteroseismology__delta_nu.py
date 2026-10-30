"""Delta nu follows a square root relationship with nu_max."""
import numpy as np

USED_INPUTS = ["nu_max"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    nu_max = X[:, 0]
    # Based on the data analysis, delta_nu ~ 0.9257 * sqrt(nu_max)
    # However, since we need to match the functional form exactly according to 
    # the simulator's internal mechanism, let's use a simpler form that captures
    # the essential physics relationship observed in asteroseismology
    return 0.925707 * np.sqrt(nu_max)