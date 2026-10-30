"""Accretion luminosity scaling law for T Tauri stars.
L_acc ~ L_star^1.5 (physically motivated scaling relation)
logL_acc = 1.5 * logL_star - 1.37 + noise"""

import numpy as np

USED_INPUTS = ["logL_star"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    logL_star = X[:, 0]
    logL_acc = 1.5 * logL_star - 1.37
    return logL_acc