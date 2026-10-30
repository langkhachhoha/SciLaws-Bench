"""Hydrogen oxidation/evolution reaction current density with Tafel, pressure, and temperature dependencies."""
import numpy as np

USED_INPUTS = ["eta", "T", "P_H2", "c_acid"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {"R": 8.31446261815324, "F": 96485.33212331001, "A": 1.0, "Ea": 50000.0}
LOCAL_FITTABLE = {}

def predict(X):
    eta = X[:, 0]
    T = X[:, 1]
    P_H2 = X[:, 2]
    c_acid = X[:, 3]
    
    # Constants
    R = OTHER_CONSTANTS["R"]  # J/mol/K
    F = OTHER_CONSTANTS["F"]  # C/mol
    A = OTHER_CONSTANTS["A"]  # Scaling factor
    Ea = OTHER_CONSTANTS["Ea"]  # Activation energy (J/mol)
    
    # Tafel-like behavior with exponential dependence on eta
    # j = A * (exp(η) - exp(-η)) * sqrt(P_H2) * exp(-Ea/(R*T))
    j = A * (np.exp(eta) - np.exp(-eta)) * np.sqrt(P_H2) * np.exp(-Ea/(R * T))
    
    return j