"""Commuting flow model with origin-destination interaction and intervening opportunities."""
import numpy as np

USED_INPUTS = ["m_i", "m_j", "s_ij"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    m_i = X[:, 0]
    m_j = X[:, 1]
    s_ij = X[:, 2]
    
    # Compute the product of origin and destination populations
    m_product = m_i * m_j
    
    # Apply the fitted model:
    # log10(Tij) = 0.646 * log10(m_i * m_j) - 0.264 * log10(s_ij + 1) - 2.583
    log_m_product = np.log10(m_product)
    log_s_plus_1 = np.log10(s_ij + 1)
    
    # Fitted coefficients from experimental data analysis
    a = 0.646
    b = -0.264
    c = -2.583
    
    return a * log_m_product + b * log_s_plus_1 + c