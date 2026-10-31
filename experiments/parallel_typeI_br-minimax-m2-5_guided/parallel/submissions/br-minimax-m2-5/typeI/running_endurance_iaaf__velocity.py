"""Power-law velocity formula: v = a * d^(-0.1) * (1 + 0.1*sex_M)

The velocity decreases with distance as a power law (d^-0.1), and males
run approximately 10% faster than females (factor of 1.1 when sex_M=1)."""
import numpy as np

USED_INPUTS = ["distance_m", "sex_M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]  # distance in meters
    sex_M = X[:, 1]  # 0=female, 1=male
    a = 14.53  # fitted prefactor
    return a * np.power(d, -0.1) * (1 + 0.1 * sex_M)