"""Liquid Drop Model with modified asymmetry and pairing terms."""
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
    
    # Fitted parameters
    a_V = 14.166     # Volume coefficient (MeV)
    a_S = 13.910     # Surface coefficient (MeV)
    a_C = 0.5724     # Coulomb coefficient (MeV)
    a_A = 17.370     # Asymmetry coefficient (MeV)
    a_P = 3.410      # Pairing coefficient (MeV)
    
    # Liquid Drop Model:
    # BE/A = a_V - a_S*A^(-1/3) - a_C*Z^2/A^(4/3) - a_A*(N-Z)^2/A^2 + a_P*pair/A
    y_pred = (a_V 
              - a_S * np.power(A, -1.0/3.0) 
              - a_C * Z**2 / np.power(A, 4.0/3.0) 
              - a_A * NZ_diff**2 / A**2 
              + a_P * pair / A)
    
    return y_pred