"""Maximum power of PV module as linear function of G and G*T."""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_module_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Standard PV model: P = (G/1000) * P_stc * (1 + gamma*(T - 25))
    # Linear form: P = a*G + b*G*T
    # Fitted coefficients from experiments:
    a = 0.218146
    b = -0.00045142
    G = X[:, 0]
    T = X[:, 1]
    return a * G + b * G * T