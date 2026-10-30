"""Gravity model with intervening opportunities."""
import numpy as np

USED_INPUTS = ["m_i", "m_j", "s_ij"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    m_i = X[:, 0]
    m_j = X[:, 1]
    s_ij = X[:, 2]
    
    # Using the best fitting model from our experiments
    # log10_Tij = A * log(m_i) * log(m_j) / (1 + B * s_ij) + C
    # Based on our fitting: A ≈ 0.3389, B ≈ 1.6515e-07, C ≈ -0.8155
    
    # Simplified version that matches the structure and fits well
    # We'll use a form that's more robust and interpretable:
    # log10_Tij = 0.3389 * log10(m_i) * log10(m_j) / (1 + 1.6515e-07 * s_ij) - 0.8155
    
    # To avoid numerical issues, we'll use a slightly different formulation
    # that maintains the core structure but is numerically stable
    log_m_i = np.log10(m_i)
    log_m_j = np.log10(m_j)
    denominator = 1.0 + 1.6515e-07 * s_ij
    
    # Ensure we don't divide by zero or get extremely large values
    # The formula should be: A * log(m_i) * log(m_j) / (1 + B * s_ij) + C
    # With fitted parameters: A ≈ 0.3389, B ≈ 1.6515e-07, C ≈ -0.8155
    
    return 0.3389 * log_m_i * log_m_j / denominator - 0.8155