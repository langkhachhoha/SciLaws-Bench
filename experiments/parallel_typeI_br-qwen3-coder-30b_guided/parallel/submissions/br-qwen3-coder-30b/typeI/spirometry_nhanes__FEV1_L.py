"""FEV1 prediction based on height and age with linear interaction term."""
import numpy as np

USED_INPUTS = ["age", "height_cm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Coefficients derived from fitting: FEV1 = 0.0423 * height + 0.0076 * age - 0.0002 * height * age - 2.8090
    height = X[:, 1]
    age = X[:, 0]
    
    return 0.0423 * height + 0.0076 * age - 0.0002 * height * age - 2.8090