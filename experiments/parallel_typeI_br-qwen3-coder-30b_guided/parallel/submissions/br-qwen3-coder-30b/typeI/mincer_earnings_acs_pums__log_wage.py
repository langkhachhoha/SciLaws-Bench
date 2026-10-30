"""Linear model with schooling and experience effects."""
import numpy as np

USED_INPUTS = ["SCHL_years", "exp"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Coefficients derived from fitting the data
    # log_wage = 0.1146 * SCHL_years + 0.0168 * exp + 8.7051
    s = X[:, 0]  # SCHL_years
    e = X[:, 1]  # exp
    return 0.11464765132763564 * s + 0.016848136485028156 * e + 8.70508752866054