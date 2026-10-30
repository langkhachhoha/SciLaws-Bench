"""Trade flow model based on GDP, distance, and binary geographic/economic indicators."""
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
    
    # Linear model coefficients from fitting
    # log_tradeflow = -0.320*log_gdp_o - 0.320*log_gdp_d - 3.160*log_dist + 1.849*contig + 0.356*comlang_off + 1.849*col_dep_ever + 0.356*fta_wto - 3.840
    
    return (-0.320 * log_gdp_o + 
            -0.320 * log_gdp_d + 
            -3.160 * log_dist + 
            1.849 * contig + 
            0.356 * comlang_off + 
            1.849 * col_dep_ever + 
            0.356 * fta_wto + 
            -3.840)