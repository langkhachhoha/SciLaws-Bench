"""Period-Luminosity-Metallicity (PLZ) relation for Classical Cepheids: M_W = α*log(P) + γ*[Fe/H] + ZP"""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_P = X[:, 0]
    feh = X[:, 1]
    # Standard PLZ relation: M = α*log(P) + γ*[Fe/H] + ZP
    alpha = -3.14  # PL slope (mag/dex)
    gamma = -0.30  # Metallicity coefficient (mag/dex)
    ZP = -2.95     # Zero point (mag)
    return alpha * log_P + gamma * feh + ZP