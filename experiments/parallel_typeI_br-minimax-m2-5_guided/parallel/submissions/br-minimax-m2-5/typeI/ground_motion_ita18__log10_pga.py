"""Ground Motion Prediction Equation (GMPE) for log10(PGA).
Format: log10(PGA) = base + site_amplification + faulting_effect
Where base is for rock (ec8_B=1) with neutral faulting."""
import numpy as np

USED_INPUTS = ["Mw", "R_km", "ec8_B", "ec8_C", "ec8_D", "ec8_E", "sof_NF", "sof_TF"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Mw = X[:, 0]  # Moment magnitude
    R = X[:, 1]   # Joyner-Boore distance in km
    ec8_B = X[:, 2]  # Rock site (reference)
    ec8_C = X[:, 3]  # Soft rock
    ec8_D = X[:, 4]  # Stiff soil
    ec8_E = X[:, 5]  # Special soil
    sof_NF = X[:, 6]  # Normal faulting
    sof_TF = X[:, 7]  # Reverse (thrust) faulting
    
    # Base model (for rock site class B with neutral faulting)
    # log10(PGA) = a + b*Mw - c1*log10(R+1) - c2*R
    a = -0.373  # constant
    b = 0.495   # magnitude scaling
    c1 = 0.582  # geometric spreading (log term)
    c2 = 0.0071 # anelastic attenuation (linear term)
    
    base = a + b * Mw - c1 * np.log10(R + 1) - c2 * R
    
    # Site amplification terms (relative to rock ec8_B)
    # Note: ec8_B is the reference (0 contribution)
    SC = 0.15   # ec8_C (soft rock)
    SD = 0.09   # ec8_D (stiff/soft soil)
    SE = 0.19   # ec8_E (special)
    
    site = SC * ec8_C + SD * ec8_D + SE * ec8_E
    
    # Faulting style terms (relative to neutral/strike-slip)
    SNF = 0.14  # Normal faulting (amplification)
    STF = 0.07  # Reverse (thrust) faulting (amplification)
    
    fault = SNF * sof_NF + STF * sof_TF
    
    return base + site + fault