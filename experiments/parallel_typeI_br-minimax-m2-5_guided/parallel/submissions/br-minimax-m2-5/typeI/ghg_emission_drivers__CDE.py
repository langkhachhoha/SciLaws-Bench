"""National CO2 emissions from fossil fuel combustion and industrial processes.

CDE = K * GDP^0.75 * TP^1 * AP^3.5 * UR^0.5 * (AT+10)^-0.25 * DP^-0.125
where:
- GDP: GDP per capita (USD)
- TP: Total population
- AP: Working-age population share (%)
- UR: Urban population share (%)
- AT: Annual mean temperature (°C)
- DP: Population density (persons/km²)
"""
import numpy as np

USED_INPUTS = ["GDP", "TP", "AP", "UR", "AT", "DP"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    GDP = X[:, 0]
    TP = X[:, 1]
    AP = X[:, 2]
    UR = X[:, 3]
    AT = X[:, 4]
    DP = X[:, 5]
    
    K = 7.655574623744291e-07
    return K * (GDP**0.75) * TP * (AP**3.5) * (UR**0.5) * ((AT + 10)**-0.25) * (DP**-0.125)