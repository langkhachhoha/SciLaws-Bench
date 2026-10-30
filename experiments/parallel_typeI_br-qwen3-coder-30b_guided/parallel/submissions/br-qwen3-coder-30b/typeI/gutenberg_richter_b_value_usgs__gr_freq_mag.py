"""Gutenberg-Richter law for earthquake frequency-magnitude distribution."""
import numpy as np

USED_INPUTS = ["M_threshold"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # log10(N) = a - b * M_threshold
    # where a = 8.903589 and b = 1.140272 (from fitting)
    m_threshold = X[:, 0]
    return 8.903589 - 1.140272 * m_threshold