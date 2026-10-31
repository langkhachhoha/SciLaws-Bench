"""Physical model of Dst tendency: relaxation + solar wind electric field injection.

The tendency dDst/dt is governed by:
- Relaxation term: -alpha * Dst (ring current decays toward zero)
- Injection term: -beta * max(0, Ey) (dawn-to-dusk electric field drives ring current)

Where max(0, Ey) implements the asymmetry: only dawn-to-dusk (positive Ey) 
convective electric field injects particles into the ring current; dusk-to-dawn 
(negative Ey) has minimal effect at these energies.

Fitted coefficients from experimental data: alpha ≈ 1/21 per hour, beta ≈ -2.5 nT/hr per mV/m.
"""
import numpy as np

USED_INPUTS = ["Dst", "Ey"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Dst = X[:, 0]
    Ey = X[:, 1]
    
    # Relaxation: ring current decays toward baseline
    # When Dst < 0 (storm), this term is positive -> recovery
    # When Dst > 0, this term is negative -> decay
    alpha = 0.047
    relaxation = alpha * Dst
    
    # Injection: only positive (dawn-to-dusk)Ey drives ring current
    beta = 2.49
    injection = beta * np.maximum(Ey, 0)
    
    # Net tendency
    dDst_dt = relaxation - injection
    return dDst_dt