"""Energy consumption model with EKC, demographic, climate, and density effects."""
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
    
    # Fitted constants
    a = 8.21e-13
    b = 2.08
    c = 0.845
    d = 0.0378
    p = 0.102
    q = 0.00036
    r = 2.38
    s = 0.000098
    t = 0.051
    
    # Model: EC = a * TP^b * GDP * exp(-c*GDP/50000) * exp(-d*AT) 
    #            * (p + q*(AP-60)^2) * (r + s*(UR-60)^2) * DP^t
    
    tp_eff = TP ** b
    gdp_eff = GDP * np.exp(-c * GDP / 50000)
    at_eff = np.exp(-d * AT)
    ap_eff = p + q * (AP - 60) ** 2
    ur_eff = r + s * (UR - 60) ** 2
    dp_eff = DP ** t
    
    y_pred = a * tp_eff * gdp_eff * at_eff * ap_eff * ur_eff * dp_eff
    
    return y_pred