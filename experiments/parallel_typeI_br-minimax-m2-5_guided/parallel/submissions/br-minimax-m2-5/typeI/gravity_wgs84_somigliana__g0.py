"""WGS84 Normal Gravity (Somigliana formula): γ = γₑ*(1 + k*sin²φ)/√(1 - e²*sin²φ)"""
import numpy as np

USED_INPUTS = ["latitude"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # WGS84 normal gravity formula
    lat_rad = np.radians(X[:, 0])
    sin_sq = np.sin(lat_rad) ** 2
    
    # WGS84 ellipsoid constants
    gamma_e = 9.7803253359   # gravity at equator (m/s²)
    k = 0.00193185265241    # form factor
    e2 = 0.00669437999014   # first eccentricity squared
    
    # Somigliana closed-form formula
    gamma = gamma_e * (1 + k * sin_sq) / np.sqrt(1 - e2 * sin_sq)
    return gamma