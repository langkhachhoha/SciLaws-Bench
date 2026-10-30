"""Fu-Zhang Budyko-type runoff formula with n=2 (no free parameters).

The formula Q = sqrt(P^2 + E_p^2) - E_p derives from the Fu (1981) / Zhang et al. (2004) 
formulation: E = P + E_p - sqrt(P^2 + E_p^2), giving Q = P - E.

This is a physically-based Budyko curve that satisfies:
- Energy limit: E <= E_p when P -> infinity
- Water limit: E <= P when E_p -> infinity
- Q >= 0 always (unlike linear models that can predict negative runoff)
"""
import numpy as np

USED_INPUTS = ["p_mean", "pet_mean"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    P = X[:, 0]  # p_mean
    E_p = X[:, 1]  # pet_mean
    # Fu-Zhang n=2: Q = sqrt(P^2 + E_p^2) - E_p
    return np.sqrt(P**2 + E_p**2) - E_p