"""FVC = a + b*height² + c*age: Linear in age with quadratic height term."""
import numpy as np

USED_INPUTS = ["age", "height_cm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    age = X[:, 0]
    height_cm = X[:, 1]
    # FVC = a + b*height² + c*age
    # Coefficients fitted from NHANES adolescent male spirometry data
    a = -1.791254
    b = 0.0001669244
    c = 0.108243
    return a + b * (height_cm ** 2) + c * age