"""Distance modulus for Type Ia supernovae in flat Lambda-CDM cosmology.

mu = 5 * log10(d_L / 10 pc), where d_L is the luminosity distance.
d_L = (c/H0) * (1+z) * integral_0^z dz'/E(z')
E(z) = sqrt(Om*(1+z)^3 + Ol), with Ol = 1 - Om for flat universe.

Fitted parameters: H0 ≈ 75 km/s/Mpc, Om ≈ 1/3 (Ω_Λ ≈ 2/3).
"""
import numpy as np
from scipy import integrate

USED_INPUTS = ["z_hd"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    z = X[:, 0]
    
    # Cosmological parameters (fitted)
    H0 = 75.0        # Hubble constant in km/s/Mpc
    Om = 1/3         # Matter density parameter (Omega_m)
    Ol = 1 - Om      # Dark energy density (Omega_Lambda) for flat universe
    
    c = 299792.458   # Speed of light in km/s
    
    # E(z) = sqrt(Om*(1+z)^3 + Ol)
    def E(z):
        return np.sqrt(Om * (1 + z)**3 + Ol)
    
    # Compute distance modulus for each z
    z = np.atleast_1d(z)
    mu = np.zeros_like(z, dtype=float)
    
    for i, zi in enumerate(z):
        if zi > 0:
            # Integrate 1/E(z) from 0 to z
            integral, _ = integrate.quad(lambda zp: 1.0 / E(zp), 0, zi)
        else:
            integral = 0
        
        # Luminosity distance in Mpc
        d_L = (c / H0) * (1 + zi) * integral
        
        # Convert to pc and compute distance modulus
        d_L_pc = d_L * 1e6  # in parsecs
        mu[i] = 5 * np.log10(d_L_pc / 10.0)
    
    return mu