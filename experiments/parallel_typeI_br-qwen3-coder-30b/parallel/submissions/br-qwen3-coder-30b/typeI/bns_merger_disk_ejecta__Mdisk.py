"""Power law relationship between disk mass and compactness."""
import numpy as np

USED_INPUTS = ["C1"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    C1 = X[:, 0]
    # Based on empirical fitting of the simulator data
    # Mdisk = 2.054619 * (1 - C1)^19
    return 2.054619 * np.power((1 - C1), 19)