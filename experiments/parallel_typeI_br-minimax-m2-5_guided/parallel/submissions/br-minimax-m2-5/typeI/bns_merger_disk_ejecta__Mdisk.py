"""Mdisk = a * (C1_crit - C1)^(2/3) for C1 < C1_crit, else 0.

This represents a threshold power law: when the lighter neutron star's compactness
exceeds the critical value C1_crit ≈ 0.173, the accretion disk mass drops to zero.
The exponent 2/3 (cubic root of squared difference) is characteristic of this mechanism."""
import numpy as np

USED_INPUTS = ["C1"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    C1 = X[:, 0]
    a = 1.614           # coefficient
    C1_crit = 0.173     # critical compactness threshold
    exponent = 2/3      # power law exponent
    
    # Apply threshold: only positive values contribute
    diff = C1_crit - C1
    diff = np.maximum(diff, 0)
    return a * (diff ** exponent)