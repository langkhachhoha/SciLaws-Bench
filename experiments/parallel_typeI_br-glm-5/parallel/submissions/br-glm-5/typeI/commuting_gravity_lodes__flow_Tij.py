"""Radiation-type commuting flow model: T_ij proportional to m_i * m_j / (s_ij + m_j)"""
import numpy as np

USED_INPUTS = ["m_i", "m_j", "s_ij"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    m_i = X[:, 0]
    m_j = X[:, 1]
    s_ij = X[:, 2]
    
    # Fitted constant: alpha = -1.2311
    alpha = -1.2311
    
    # Avoid log(0) when s_ij + m_j = 0 (shouldn't happen with valid data)
    denominator = np.maximum(s_ij + m_j, 1)
    
    # log10(T_ij + 1) = log10(m_i) + log10(m_j) - log10(s_ij + m_j) + alpha
    log_T = np.log10(m_i) + np.log10(m_j) - np.log10(denominator) + alpha
    
    return log_T