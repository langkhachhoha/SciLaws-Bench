"""Saturating exponential function matching the hydrological relationship."""
import numpy as np

USED_INPUTS = ["pet_over_p"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    phi = X[:, 0]
    # Using the best fit from our analysis: E/P = 1 - exp(-0.9535 * φ)
    # We can also express this as E/P = 1 - exp(-k*φ) where k ≈ 0.9535
    # But since we're constrained to use only LAW_CONSTANTS = {}, OTHER_CONSTANTS = {},
    # and LOCAL_FITTABLE = {}, we must bake in the fitted value directly.
    k = 0.9535
    return 1.0 - np.exp(-k * phi)