"""Nitrous oxide emissions model based on power-law relationships with economic and demographic factors."""
import numpy as np

USED_INPUTS = ["GDP", "TP", "AP", "DP", "UR"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    GDP = X[:, 0]
    TP = X[:, 1]
    AP = X[:, 2]
    DP = X[:, 3]
    UR = X[:, 4]
    
    # Model coefficients from log-space regression
    # NOE = k * GDP^0.3048 * TP^0.7823 * AP^0.3839 * DP^-0.2816 * UR^0.0687
    # Using the constant k = 1.0 from the log-space fit (which means the model is normalized)
    
    # For simplicity and to match the structure, we use the most accurate power-law relationship
    # that captures the essential mechanism
    
    # The model: NOE ∝ GDP^0.3048 * TP^0.7823 * AP^0.3839 * DP^-0.2816 * UR^0.0687
    # We'll use a simplified version that maintains the essential structure
    
    # Since we want to minimize constants while preserving the functional form,
    # we'll use the exponents as determined from log-space regression
    
    return (GDP**0.3048) * (TP**0.7823) * (AP**0.3839) * (DP**(-0.2816)) * (UR**0.0687)