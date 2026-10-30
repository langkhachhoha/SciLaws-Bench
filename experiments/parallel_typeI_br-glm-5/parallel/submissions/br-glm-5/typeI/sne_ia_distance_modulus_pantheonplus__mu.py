"""Flat LCDM cosmological model for Type Ia supernova distance modulus.
mu = M + 5*log10(d_L) where d_L is the luminosity distance.
For a flat universe: d_L = (1+z) * integral(0 to z) dx/sqrt(Omega_m*(1+x)^3 + Omega_Lambda)
with Omega_Lambda = 1 - Omega_m."""
import numpy as np
from scipy.integrate import quad

USED_INPUTS = ["z_hd"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

# Fitted constants
M = 43.05
OMEGA_M = 0.33
OMEGA_L = 1 - OMEGA_M

def predict(X):
    z = X[:, 0]
    results = []
    for zi in z:
        integral, _ = quad(lambda x: 1/np.sqrt(OMEGA_M*(1+x)**3 + OMEGA_L), 0, zi)
        d_L = (1 + zi) * integral
        mu = M + 5 * np.log10(d_L)
        results.append(mu)
    return np.array(results)