"""Classic gravity model of trade: log_tradeflow = const + log_gdp_o + log_gdp_d - log_dist + binary effects."""
import numpy as np

USED_INPUTS = ["log_gdp_o", "log_gdp_d", "log_dist", "contig", "comlang_off", "col_dep_ever", "fta_wto"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs in order: log_gdp_o, log_gdp_d, log_dist, contig, comlang_off, col_dep_ever, fta_wto
    log_gdp_o = X[:, 0]
    log_gdp_d = X[:, 1]
    log_dist = X[:, 2]
    contig = X[:, 3]
    comlang_off = X[:, 4]
    col_dep_ever = X[:, 5]
    fta_wto = X[:, 6]
    
    # Classic gravity model: 
    # log(X_ij) = -18.86 + log(Y_i) + log(Y_j) - log(d_ij) + δ*Z_ij
    # with estimated binary coefficients
    return (-18.86 + 
            log_gdp_o + 
            log_gdp_d - 
            log_dist + 
            1.41 * contig + 
            0.85 * comlang_off + 
            1.35 * col_dep_ever + 
            0.78 * fta_wto)