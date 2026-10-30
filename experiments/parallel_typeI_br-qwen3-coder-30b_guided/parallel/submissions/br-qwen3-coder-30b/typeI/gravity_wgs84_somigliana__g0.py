"""Normal gravity formula according to WGS84 model."""
import numpy as np

USED_INPUTS = ["latitude"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # WGS84 normal gravity formula
    # g0 = 9.780327 * (1 + 0.00193185265241 * sin²(latitude))
    latitude = X[:, 0]
    lat_rad = np.radians(latitude)
    sin2 = np.sin(lat_rad)**2
    g0 = 9.780327 * (1 + 0.00193185265241 * sin2)
    return g0