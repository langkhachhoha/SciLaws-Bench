"""Parker spiral interplanetary magnetic field model.

The azimuthal component B_phi is related to the radial component B_r by:
B_phi = -B_r * Omega * r / v_sw

where Omega is the solar rotation angular velocity and r is heliocentric distance.
At 1 AU, Omega * r ≈ 278 km/s from the fitted data.
"""
import numpy as np

USED_INPUTS = ["B_r_nT", "v_sw_km_s", "r_AU"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    B_r = X[:, 0]      # radial field component (nT)
    v_sw = X[:, 1]     # solar wind speed (km/s)
    r_AU = X[:, 2]     # heliocentric distance (AU)
    
    # Parker spiral coefficient fitted from data
    k = 277.7697  # km/s (effective Omega * r at 1 AU)
    
    # B_phi = -B_r * k * r / v_sw
    B_phi = -B_r * k * r_AU / v_sw
    
    return B_phi