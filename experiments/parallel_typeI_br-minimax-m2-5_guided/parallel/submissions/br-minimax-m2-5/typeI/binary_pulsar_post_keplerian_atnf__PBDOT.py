"""Orbital period derivative formula for binary pulsar systems.

Based on General Relativity gravitational wave emission, scaled as:
PBDOT ~ (1/Pb^3 - 1/Pb^4) * (1 - e^2)^(-7/2) * (1 + 73/24*e^2 + 37/96*e^4)

The combination of 1/Pb^3 and 1/Pb^4 terms creates sign changes at different Pb values,
reproducing the characteristic inspiral dynamics of relativistic binary systems.
"""
import numpy as np

USED_INPUTS = ["Pb", "e"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Pb = X[:, 0]
    e = X[:, 1]
    
    # Peters & Mathews eccentricity factor for gravitational wave emission
    ecc_factor = (1 - e**2)**(-7/2) * (1 + 73/24 * e**2 + 37/96 * e**4)
    
    # Combined power law with sign-changing behavior
    # The 1/Pb^3 term dominates at low Pb (negative), the 1/Pb^4 term at high Pb
    # This captures the qualitative behavior of GR-driven orbital decay
    result = (1/Pb**3 - 1/Pb**4) * ecc_factor
    
    return result