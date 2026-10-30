"""Power law fit for basal metabolic rate: log(BMR) = log(A) + b * log(M)"""
import numpy as np

USED_INPUTS = ["body_mass_g"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract body mass
    mass = X[:, 0]
    
    # Parameters from fitting: 
    # log(BMR) = -1.8038 + 0.7801 * log10(mass)
    # So BMR = 10^(-1.8038) * mass^(0.7801)
    # Which means BMR = 0.0158 * mass^(0.7801)
    
    # Using the fitted parameters from our analysis
    log_bmr = -1.8038 + 0.7801 * np.log10(mass)
    
    return log_bmr