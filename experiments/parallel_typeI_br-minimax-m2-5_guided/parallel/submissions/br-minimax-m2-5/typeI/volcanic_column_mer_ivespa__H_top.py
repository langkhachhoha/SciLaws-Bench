"""Power law: eruption column height proportional to MER^0.2."""
import numpy as np

USED_INPUTS = ["MER_kg_per_s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    MER = X[:, 0]
    # H_top = 0.52 * MER^0.2
    return 0.52 * np.power(MER, 0.2)