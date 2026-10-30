"""Steinmetz equation for soft ferrite core loss: P_vol = K * f^a * B^b"""
import numpy as np

USED_INPUTS = ["f_Hz", "B_peak_T"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    f = X[:, 0]  # f_Hz
    B = X[:, 1]  # B_peak_T
    
    # Fitted parameters
    K = 8.2158e-05
    a = 1.6856
    b = 2.4333
    
    # Steinmetz equation in log form
    log_P_vol = np.log10(K) + a * np.log10(f) + b * np.log10(B)
    
    return log_P_vol