"""Classical gravity model of bilateral trade flows."""
import numpy as np

USED_INPUTS = ["log_gdp_o", "log_gdp_d", "log_dist", "contig", "comlang_off", "col_dep_ever", "fta_wto"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_gdp_o = X[:, 0]
    log_gdp_d = X[:, 1]
    log_dist = X[:, 2]
    contig = X[:, 3]
    comlang_off = X[:, 4]
    col_dep_ever = X[:, 5]
    fta_wto = X[:, 6]
    
    # Gravity model: log_tradeflow = α + β₁*ln(Y_i) + β₂*ln(Y_j) - θ*ln(d_ij) + binary effects
    y_pred = (-16.66 
              + 1.07 * log_gdp_o 
              + 0.86 * log_gdp_d 
              - 1.21 * log_dist 
              + 0.73 * contig 
              + 0.82 * comlang_off 
              + 1.30 * col_dep_ever 
              + 1.04 * fta_wto)
    
    return y_pred