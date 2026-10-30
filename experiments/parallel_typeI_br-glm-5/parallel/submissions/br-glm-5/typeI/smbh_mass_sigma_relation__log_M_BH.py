"""Linear scaling relation between supermassive black hole mass and host spheroid mass.

Physical interpretation: log_M_BH scales approximately linearly with log_M_sph,
with slope slightly above 1, indicating more massive spheroids host proportionally
more massive black holes. This is consistent with the observed M_BH-M_sph relation."""
import numpy as np

USED_INPUTS = ["log_M_sph"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_M_sph = X[:, 0]
    # Linear scaling: log(M_BH/M_sun) = alpha + beta * log(M_sph/M_sun)
    alpha = -3.24  # intercept
    beta = 1.08    # slope
    return alpha + beta * log_M_sph