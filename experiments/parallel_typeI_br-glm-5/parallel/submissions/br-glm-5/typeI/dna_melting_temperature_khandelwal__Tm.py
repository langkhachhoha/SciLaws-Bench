"""DNA melting temperature model: linear additive form with log-scaled salt and DNA concentration."""
import numpy as np

USED_INPUTS = ["E", "N", "salt_M", "dna_conc_M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    E = X[:, 0]
    N = X[:, 1]
    salt_M = X[:, 2]
    dna_conc_M = X[:, 3]
    
    # Additive model: Tm = a*E + b*N + c*log10(salt) + d*log10(dna) + e
    a = 7.657
    b = 0.978
    c = 13.297
    d = 4.570
    e = 19.342
    
    Tm = a * E + b * N + c * np.log10(salt_M) + d * np.log10(dna_conc_M) + e
    
    return Tm