"""Asteroseismic scaling relation: large frequency separation scales as nu_max^0.75."""
import numpy as np

USED_INPUTS = ["nu_max"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    nu_max = X[:, 0]
    return 0.288 * nu_max**0.75