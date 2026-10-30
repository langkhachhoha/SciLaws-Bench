"""Delta nu follows a power law with nu_max raised to the 3/4 power."""
import numpy as np

USED_INPUTS = ["nu_max"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    nu_max = X[:, 0]
    # Based on the experimental data and asteroseismological theory,
    # delta_nu ~ 0.2855 * nu_max^(3/4)
    return 0.285476 * (nu_max ** 0.75)