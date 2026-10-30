"""Ground motion prediction equation for peak ground acceleration."""
import numpy as np

USED_INPUTS = ["Mw", "R_km", "ec8_B", "ec8_C", "ec8_D", "ec8_E", "sof_NF", "sof_TF"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Mw = X[:, 0]
    R = X[:, 1]
    ec8_B = X[:, 2]
    ec8_C = X[:, 3]
    ec8_D = X[:, 4]
    ec8_E = X[:, 5]
    sof_NF = X[:, 6]
    sof_TF = X[:, 7]
    
    # GMPE model parameters
    a = 3.82
    b = 0.03
    c = -0.015
    d = -3.42
    e = 0.40
    h = 12.0
    gamma = -0.0045
    
    # Site class coefficients
    sB = -0.10
    sC = 0.10
    sD = 0.13
    sE = 0.19
    
    # Fault type coefficients
    fNF = -0.06
    fTF = -0.18
    
    # Baseline GMPE: magnitude and distance terms
    log10_pga = a + b*Mw + c*Mw**2 + (d + e*Mw)*np.log10(R + h)
    
    # Anelastic attenuation
    log10_pga = log10_pga + gamma*R
    
    # Site class effects
    log10_pga = log10_pga + sB*ec8_B + sC*ec8_C + sD*ec8_D + sE*ec8_E
    
    # Fault type effects
    log10_pga = log10_pga + fNF*sof_NF + fTF*sof_TF
    
    return log10_pga