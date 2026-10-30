"""Mass-luminosity relation for main-sequence stars in eclipsing binaries.
The cubic form captures the varying mass-luminosity exponent:
log_L = log_M * (a + b*log_M + c*log_M^2) + d
where the effective exponent α = a + 2b*log_M + 3c*log_M^2 varies with mass.

Physics: Low-mass stars (M<0.5) have lower α due to convection;
Intermediate mass (~1-5 Msun) have α~4 (radiative envelope);
High-mass stars show reduced α due to Eddington limit effects."""
import numpy as np

USED_INPUTS = ["log_M_Msun"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]  # log_M_Msun
    # Cubic polynomial in log space
    # log_L = a*x + b*x^2 + c*x^3 + d
    # Best fit coefficients from current data
    a = 4.5
    b = 0.6
    c = -1.0
    d = 0.0
    
    log_L = a * x + b * x**2 + c * x**3 + d
    return log_L