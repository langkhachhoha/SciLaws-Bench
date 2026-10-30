"""Power law relationship between mass eruption rate and eruption column height."""
import numpy as np

USED_INPUTS = ["MER_kg_per_s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract MER values
    mer = X[:, 0]
    
    # Power law relationship: H_top = A * MER^B
    # From our analysis, A ≈ 0.5645 and B ≈ 0.1924
    A = 0.5645
    B = 0.1924
    
    return A * (mer ** B)