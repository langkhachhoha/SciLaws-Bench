"""Power law background + Breit-Wigner resonance for Au-197 neutron capture."""
import numpy as np

USED_INPUTS = ["E_eV"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Model: sigma = A * E^(-0.75) + C * Er^2 * Gamma^2 / ((E - Er)^2 + Gamma^2/4)
    # Background: A * E^(-3/4) - power law with exponent 0.75
    # Resonance: Breit-Wigner form centered at Er with width Gamma
    A = 3.6911
    n = 0.75
    Er = 4.8688
    Gamma = 0.1262
    C = 369.6273
    
    sigma_bg = A * (x ** (-n))
    sigma_bw = C * (Er**2 * Gamma**2) / ((x - Er)**2 + Gamma**2/4)
    sigma = sigma_bg + sigma_bw
    
    # Return log10 of sigma
    return np.log10(sigma)