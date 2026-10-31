"""Commuting flow model: log10(m_i * m_j / (m_i + m_j + s_ij) + 1)."""
import numpy as np

USED_INPUTS = ["m_i", "m_j", "s_ij"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mi = X[:, 0]
    mj = X[:, 1]
    sij = X[:, 2]
    return np.log10(mi * mj / (mi + mj + sij) + 1)