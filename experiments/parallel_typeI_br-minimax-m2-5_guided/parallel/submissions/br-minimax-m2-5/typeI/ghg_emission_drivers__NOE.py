"""National N2O emissions as function of GDP, population, density, temperature, urbanization, and working-age share."""
import numpy as np

USED_INPUTS = ["GDP", "TP", "DP", "AT", "UR", "AP"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    GDP = X[:, 0]
    TP = X[:, 1]
    DP = X[:, 2]
    AT = X[:, 3]
    UR = X[:, 4]
    AP = X[:, 5]
    
    # Fitted power-law model with small corrections
    # NOE ≈ c * GDP^0.24 * TP^0.82 * DP^(-0.28) * exp(-0.039*AT + 0.00096*AT^2 - 0.005*UR - 0.0083*AP)
    c = 18.5
    exponent_GDP = 0.239
    exponent_TP = 0.816
    exponent_DP = -0.284
    
    # Linear corrections (small terms)
    coef_AT = -0.0393
    coef_AT2 = 0.000963
    coef_UR = -0.00503
    coef_AP = -0.00833
    
    NOE = c * (GDP**exponent_GDP) * (TP**exponent_TP) * (DP**exponent_DP) * \
          np.exp(coef_AT * AT + coef_AT2 * AT**2 + coef_UR * UR + coef_AP * AP)
    
    return NOE