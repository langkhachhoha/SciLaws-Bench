"""Stochastic multiplicative model for N2O emissions."""
import numpy as np

USED_INPUTS = ["GDP", "TP", "AP", "DP", "UR", "AT"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    GDP = X[:, 0]
    TP = X[:, 1]
    AP = X[:, 2]
    DP = X[:, 3]
    UR = X[:, 4]
    AT = X[:, 5]
    
    # Core: NOE ~ TP * GDP^b (Kaya identity style)
    # With small adjustments from other factors
    log_gdp = np.log(GDP)
    
    # Base emission rate per capita as function of GDP
    # EKC-like: quadratic in log(GDP)
    base_factor = 0.05 * np.exp(0.29 * log_gdp + 0.005 * log_gdp**2)
    
    # Adjustments from demographic/environmental factors (small effects)
    ap_adj = 1.0 - 0.2 * (AP - 60) / 100
    dp_adj = 1.0 - 0.3 * np.log(DP / 100 + 1)
    ur_adj = 1.0 - 0.04 * (UR - 50) / 100
    at_adj = 1.0 - 0.35 * (AT - 10) / 10
    
    # Combine adjustments
    adjustment = ap_adj * dp_adj * ur_adj * at_adj
    
    return TP * base_factor * adjustment