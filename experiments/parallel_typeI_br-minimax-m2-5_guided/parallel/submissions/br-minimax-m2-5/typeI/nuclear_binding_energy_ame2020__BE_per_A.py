"""Nuclear binding energy per nucleon using the Semi-Empirical Mass Formula (SEMF).

BE/A = a_v - a_s * A^(-1/3) - a_c * Z*(Z-1) / A^(4/3) - a_a * (NZ_diff)^2 / A^2 + a_p * pair / A

where:
- a_v: volume term (~15.6 MeV)
- a_s: surface term (~18.4 MeV)
- a_c: Coulomb term (~0.68 MeV)
- a_a: asymmetry term (~21.1 MeV)
- a_p: pairing term (~11.8 MeV)
"""
import numpy as np

USED_INPUTS = ["Z", "N", "A", "NZ_diff", "pair"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Z = X[:, 0]
    N = X[:, 1]
    A = X[:, 2]
    NZ_diff = X[:, 3]
    pair = X[:, 4]
    
    # SEMF parameters (fitted to simulator data)
    a_v = 15.5782
    a_s = 18.3935
    a_c = 0.6811
    a_a = 21.1171
    a_p = 11.7959
    
    # Volume term: a_v * A / A = a_v
    volume = a_v
    
    # Surface term: a_s * A^(2/3) / A = a_s * A^(-1/3)
    surface = a_s * A**(-1/3)
    
    # Coulomb term: a_c * Z*(Z-1) / A^(4/3)
    coulomb = a_c * Z * (Z - 1) / A**(4/3)
    
    # Asymmetry term: a_a * (A-2Z)^2 / A^2 = a_a * (NZ_diff)^2 / A^2
    asymmetry = a_a * NZ_diff**2 / A**2
    
    # Pairing term: delta / A where delta = +a_p for even-even, 0 for odd-mass, -a_p for odd-odd
    delta = np.where(pair == 1, a_p, np.where(pair == -1, -a_p, 0))
    pairing = delta / A
    
    # Total binding energy per nucleon
    BE_per_A = volume - surface - coulomb - asymmetry + pairing
    
    return BE_per_A