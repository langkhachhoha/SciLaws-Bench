"""Linear model of trade flows based on GDP, distance, and geographic/cultural factors."""
import numpy as np

USED_INPUTS = ["log_gdp_o", "log_gdp_d", "log_dist", "contig", "comlang_off", "col_dep_ever", "fta_wto"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    log_gdp_o = X[:, 0]
    log_gdp_d = X[:, 1]
    log_dist = X[:, 2]
    contig = X[:, 3]
    comlang_off = X[:, 4]
    col_dep_ever = X[:, 5]
    fta_wto = X[:, 6]
    
    # Linear combination with fitted coefficients
    # ln(X_ij) = 1.1385 * ln(Y_i) + 0.8854 * ln(Y_j) - 1.0559 * ln(d_ij) + 0.8207*contig + 1.2155*comlang_off + 1.2230*col_dep_ever + 0.8207*fta_wto - 18.9543
    return (1.1385 * log_gdp_o + 
            0.8854 * log_gdp_d - 
            1.0559 * log_dist + 
            0.8207 * contig + 
            1.2155 * comlang_off + 
            1.2230 * col_dep_ever + 
            0.8207 * fta_wto - 
            18.9543)