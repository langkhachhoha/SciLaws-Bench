"""DNA melting temperature formula based on linear combination of inputs."""
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
    
    # Coefficients derived from fitting the data
    # Tm = 5.340*E + 2.395*N - 1.573*salt_M + 2.275*log(dna_conc_M) + 0.335
    return 5.340 * E + 2.395 * N + (-1.573) * salt_M + 2.275 * np.log(dna_conc_M) + 0.335