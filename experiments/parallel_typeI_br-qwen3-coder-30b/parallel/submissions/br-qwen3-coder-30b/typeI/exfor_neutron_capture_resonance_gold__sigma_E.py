"""Neutron capture cross section model based on 1/sqrt(E) behavior at low energies."""
import numpy as np

USED_INPUTS = ["E_eV"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    E = X[:, 0]
    # Model: log10(sigma) = A / sqrt(E) + B
    # Based on fitting the data, A ≈ 0.1003, B ≈ 0.9749
    return 0.1003 / np.sqrt(E) + 0.9749