"""Carbon dioxide emissions model with multiplicative environmental factors.

Structure: CDE = a * TP * GDP * exp(-b*GDP) * exp(c*|AP-55|) * 
           exp(-(DP-200)²/(2*500²)) * exp(-(UR-60)²/(2*70²)) * exp(-(AT-9)²/(2*15²))

Key mechanisms:
- GDP: Environmental Kuznets Curve (inverted U-shape, peak at ~41,500)
- AP : V-shaped minimum at AP=55 (working-age share)
- DP, UR, AT: Bell curves centered at optimal values
"""
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
    
    # Fitted constants (7 total)
    a = 0.42          # scale factor
    b = 2.4e-5        # GDP decay rate
    c = 0.048         # AP growth rate
    AP_min = 55.0     # AP minimum location
    DP_opt = 200.0    # DP optimal location
    sDP = 500.0       # DP width
    UR_opt = 60.0     # UR optimal location
    sUR = 70.0        # UR width
    AT_opt = 9.0      # AT optimal location
    sAT = 15.0        # AT width
    
    # Environmental Kuznets Curve for GDP
    f_gdp = GDP * np.exp(-b * GDP)
    
    # V-shaped effect for active population (minimum at AP_min)
    f_ap = np.exp(c * np.abs(AP - AP_min))
    
    # Bell curve effects for DP, UR, AT
    f_dp = np.exp(-(DP - DP_opt)**2 / (2 * sDP**2))
    f_ur = np.exp(-(UR - UR_opt)**2 / (2 * sUR**2))
    f_at = np.exp(-(AT - AT_opt)**2 / (2 * sAT**2))
    
    return a * TP * f_gdp * f_ap * f_dp * f_ur * f_at