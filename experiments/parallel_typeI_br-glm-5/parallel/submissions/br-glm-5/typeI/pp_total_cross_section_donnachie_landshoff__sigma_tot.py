"""Total proton-proton cross-section model: σ_tot = A + B*ln²(s) + C*s^(-n)

This matches the PDG parameterization combining:
- Froissart bound behavior at high s: B*ln²(s) asymptotic growth
- Regge behavior at low s: C*s^(-n) fall-off term
"""
import numpy as np

USED_INPUTS = ["s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    s = X[:, 0]
    A = 16.14
    B = 0.2495
    C = 32.48
    n = 0.1418
    return A + B * np.log(s)**2 + C * s**(-n)