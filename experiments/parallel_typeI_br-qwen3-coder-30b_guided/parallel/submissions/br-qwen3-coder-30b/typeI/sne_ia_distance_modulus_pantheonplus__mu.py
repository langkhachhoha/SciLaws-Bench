"""Distance modulus for Type Ia supernovae as a function of redshift."""
import numpy as np

USED_INPUTS = ["z_hd"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    z = X[:, 0]
    # Based on the analysis of the simulator behavior, the relationship appears to be:
    # mu = A * log10(1+z)^2 + B * log10(1+z) + C
    # where A=-106.427612, B=80.064546, C=32.074642
    log1pz = np.log10(1 + z)
    return -106.427612 * log1pz**2 + 80.064546 * log1pz + 32.074642