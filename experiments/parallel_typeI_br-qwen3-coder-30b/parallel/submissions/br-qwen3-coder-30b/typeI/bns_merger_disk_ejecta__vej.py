"""Velocity of dynamical ejecta from neutron star mergers, based on mass ratio and tidal deformability."""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    Lambda_tilde = X[:, 1]
    
    # Best-fit model from experimental data analysis
    # vej = 0.4371 / (q * (Lambda_tilde)^0.0697)
    return 0.4371 / (q * (Lambda_tilde)**0.0697)