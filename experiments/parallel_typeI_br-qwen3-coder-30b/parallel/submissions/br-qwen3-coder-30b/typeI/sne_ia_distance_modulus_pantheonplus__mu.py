"""Distance modulus for Type Ia supernovae as a function of redshift, using a log-linear model."""
import numpy as np

USED_INPUTS = ["z_hd"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    z = X[:, 0]
    # Coefficients determined from fitting the simulator data
    # mu = A*z + B*log(1+z) + C
    return -14.374623 * z + 36.587256 * np.log(1 + z) + 34.009945