"""DNA melting temperature formula based on E, N, and salt concentration."""
import numpy as np

USED_INPUTS = ["E", "N", "salt_M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    E = X[:, 0]
    N = X[:, 1]
    salt_M = X[:, 2]
    
    # Based on the experimental data analysis:
    # Tm = 6.9978*E + 1.0249*N + 4.2118*log(salt_M) + 0.3223
    return 6.9978 * E + 1.0249 * N + 4.2118 * np.log(salt_M) + 0.3223