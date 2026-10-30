"""Model based on dominant physical relationships: quadratic Dst dependence, linear Ey and P_dyn dependence."""
import numpy as np

USED_INPUTS = ["Dst", "Ey", "P_dyn"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Dst = X[:, 0]
    Ey = X[:, 1]
    P_dyn = X[:, 2]
    
    # Based on regression analysis, the dominant physical relationships are:
    # - Quadratic dependence on Dst (storm/recovery phase)
    # - Linear dependence on Ey (driving electric field)
    # - Linear dependence on P_dyn (dynamic pressure)
    
    return (0.000125 * Dst**2 - 
            1.4352 * Ey - 
            0.0983 * P_dyn - 
            23.0899)