"""Power law relationship with sex-dependent amplitude factor."""
import numpy as np

USED_INPUTS = ["distance_m", "sex_M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    distance_m = X[:, 0]
    sex_M = X[:, 1]
    
    # Base amplitude for women (or when sex_M = 0)
    A_base = 13.83
    # Exponent (approximately the same for both sexes)
    B = 0.092
    # Sex effect factor (men are ~6.9% faster)
    sex_factor = 0.069
    
    # Apply the power law with sex correction
    return A_base * (distance_m ** (-B)) * (1 + sex_factor * sex_M)