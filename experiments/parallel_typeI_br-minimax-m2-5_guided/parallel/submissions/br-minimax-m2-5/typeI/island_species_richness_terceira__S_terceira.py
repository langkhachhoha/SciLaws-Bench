"""Power-law decay: S = 517 * d^(-3/2). Species richness decreases as the 3/2 power of the habitat-modification index."""
import numpy as np

USED_INPUTS = ["d"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]
    return 517 * np.power(d, -1.5)