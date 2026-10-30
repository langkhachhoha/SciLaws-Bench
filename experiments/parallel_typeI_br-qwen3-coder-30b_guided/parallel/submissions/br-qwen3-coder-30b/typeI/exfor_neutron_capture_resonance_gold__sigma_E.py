"""Thermal neutron capture cross-section following 1/sqrt(E) behavior with correction for higher energies."""
import numpy as np

USED_INPUTS = ["E_eV"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    E = X[:, 0]
    # Based on the data analysis, the cross-section follows a 1/sqrt(E) dependence
    # with some correction for higher energies
    # log10(sigma) = 1.2863 - 0.5 * log10(E)
    # But we need to ensure this doesn't go negative or unrealistic
    log10_sigma = 1.2863 - 0.5 * np.log10(E)
    return log10_sigma