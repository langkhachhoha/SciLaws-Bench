"""Nuclear binding energy per nucleon formula based on Weizsäcker semi-empirical formula."""
import numpy as np

USED_INPUTS = ["Z", "N", "A", "NZ_diff", "pair"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Z = X[:, 0]
    N = X[:, 1] 
    A = X[:, 2]
    NZ_diff = X[:, 3]
    pair = X[:, 4]
    
    # Weizsäcker semi-empirical formula components
    # BE/A = a1 - a2*A^(-1/3) - a3*(A-2Z)^2/A^2 + a4*NZ_diff + a5*pair
    
    # Using approximate constants based on nuclear physics
    # These values are chosen to reproduce the general behavior observed:
    # - Large A -> constant binding energy (~8.5 MeV)
    # - Small A -> stronger A^(-1/3) dependence
    # - NZ_diff effect is positive (more neutrons improve binding)
    # - Pair effect is small but present
    
    a1 = 15.8  # Binding energy constant (MeV)
    a2 = 18.3  # Volume term coefficient
    a3 = 0.71  # Surface term coefficient  
    a4 = 0.02  # Asymmetry term coefficient
    a5 = 0.01  # Pairing term coefficient
    
    # Calculate individual terms
    volume_term = a1
    surface_term = a2 / (A ** (1/3))
    asymmetry_term = a3 * ((A - 2*Z)**2) / (A**2)
    nz_diff_term = a4 * NZ_diff
    pairing_term = a5 * pair
    
    # Combine terms
    be_per_a = volume_term - surface_term - asymmetry_term + nz_diff_term + pairing_term
    
    return be_per_a