"""Terminal velocity of dynamical ejecta from neutron star mergers: vej = C * q^(-2/3) * Lambda_tilde^(-1/10)."""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    Lambda_tilde = X[:, 1]
    return 0.453 * q**(-2/3) * Lambda_tilde**(-1/10)