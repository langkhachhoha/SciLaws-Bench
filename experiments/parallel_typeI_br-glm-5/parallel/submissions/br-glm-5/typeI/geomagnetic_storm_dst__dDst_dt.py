"""Burton-type model for Dst index rate of change.

dDst/dt = -a*Dst + b - c*max(Ey, 0) + d*(sqrt(P_dyn) - sqrt(P0))

Where:
- a ≈ 0.05 hr^-1 is the recovery rate
- b is a constant offset
- c ≈ 2.4 (nT/hr)/(mV/m) is the injection efficiency
- d accounts for pressure effects
- Ey is dawn-to-dusk electric field (mV/m)
- P_dyn is solar wind dynamic pressure (nPa)
"""
import numpy as np

USED_INPUTS = ["Dst", "Ey", "P_dyn"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Dst = X[:, 0]
    Ey = X[:, 1]
    P_dyn = X[:, 2]
    
    # Fitted constants
    a = 0.049  # Recovery rate (hr^-1)
    b = 1.5    # Constant offset (nT/hr)
    c = 2.43   # Injection efficiency (nT/hr)/(mV/m)
    d = -0.6   # Pressure coefficient
    
    P0 = 5.0  # Reference pressure
    
    # Model: recovery term + Ey injection + pressure correction
    recovery = -a * Dst
    injection = -c * np.maximum(Ey, 0)
    pressure = d * (np.sqrt(P_dyn) - np.sqrt(P0))
    
    return recovery + b + injection + pressure