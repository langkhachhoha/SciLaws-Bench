"""DNA melting temperature (Tm) model based on nearest-neighbor thermodynamics.

Formula: Tm = a + b*E + c*N + d*sqrt(salt_M) + e*ln(C_DNA)

Where:
- E: DNA strength parameter per base (encodes stacking and hydrogen bonding)
- N: Sequence length in base pairs
- salt_M: Sodium ion concentration (screening of DNA backbone)
- C_DNA: Total nucleotide strand concentration (affects duplex stability)
"""
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
    return -4.88 + 6.62 * E + 1.25 * N + 20.87 * np.sqrt(salt_M) + 1.48 * np.log(dna_conc_M)