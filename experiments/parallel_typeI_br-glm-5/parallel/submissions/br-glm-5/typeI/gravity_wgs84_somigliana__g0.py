"""WGS84 Somigliana formula for normal gravity.

γ(φ) = γ_e * (1 + k * sin²(φ)) / sqrt(1 - e² * sin²(φ))

Standard WGS84 constants based on the reference ellipsoid definition.
"""
import numpy as np

USED_INPUTS = ["latitude"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # WGS84 Somigliana formula constants
    gamma_e = 9.7803253359      # Equatorial normal gravity (m/s²)
    k = 0.00193185265241       # Somigliana's constant
    e2 = 0.00669437999014      # First eccentricity squared
    
    # Convert latitude from degrees to radians
    lat_deg = X[:, 0]
    lat_rad = np.radians(lat_deg)
    
    # Compute sin²(latitude)
    sin2 = np.sin(lat_rad) ** 2
    
    # Somigliana formula
    y_pred = gamma_e * (1 + k * sin2) / np.sqrt(1 - e2 * sin2)
    
    return y_pred