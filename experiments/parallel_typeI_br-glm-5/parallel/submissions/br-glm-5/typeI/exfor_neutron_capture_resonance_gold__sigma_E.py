"""Au-197 neutron capture cross section with single resonance.

Single-level Breit-Wigner formula:
σ(E) = A_bg/√E + A_res/√E / ((E - E_r)² + (Γ/2)²)
log10(σ) = log10(σ_background + σ_resonance)

This captures the 1/v thermal behavior and the prominent resonance at ~4.9 eV.
"""
import numpy as np

USED_INPUTS = ["E_eV"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    E = X[:, 0]
    # Fitted constants (4 total)
    A_bg = 3.3453      # Background amplitude
    A_res = 302.4007   # Resonance amplitude  
    E_r = 4.8754       # Resonance energy (eV)
    gamma = 0.1107     # Resonance width (eV)
    
    # Background: 1/v law (σ ~ 1/√E)
    sigma_bg = A_bg / np.sqrt(E)
    
    # Resonance: Breit-Wigner single level
    sigma_res = A_res / np.sqrt(E) / ((E - E_r)**2 + (gamma/2)**2)
    
    # Total cross section and log transform
    sigma_total = sigma_bg + sigma_res
    return np.log10(sigma_total)