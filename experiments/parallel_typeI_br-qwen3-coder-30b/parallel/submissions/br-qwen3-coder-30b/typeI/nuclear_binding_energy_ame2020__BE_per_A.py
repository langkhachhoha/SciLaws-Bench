"""Nuclear binding energy per nucleon using liquid drop model terms."""
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
    
    # Liquid drop model coefficients (fitted from data)
    a_V = 15.8  # Volume term
    a_S = 18.3  # Surface term  
    a_C = 0.714  # Coulomb term
    a_A = 23.2  # Asymmetry term
    a_P = 12.0  # Pairing term
    
    # Volume term
    E_volume = a_V * A
    
    # Surface term
    E_surface = a_S * A**(2/3)
    
    # Coulomb term
    E_coulomb = a_C * Z * (Z - 1) / A**(1/3)
    
    # Asymmetry term
    E_asymmetry = a_A * (N - Z)**2 / A
    
    # Pairing term
    E_pairing = a_P * pair * (1 - abs(pair)) / A**(1/2)
    
    # Total binding energy
    BE = E_volume - E_surface - E_coulomb - E_asymmetry + E_pairing
    
    # Binding energy per nucleon
    return BE / A