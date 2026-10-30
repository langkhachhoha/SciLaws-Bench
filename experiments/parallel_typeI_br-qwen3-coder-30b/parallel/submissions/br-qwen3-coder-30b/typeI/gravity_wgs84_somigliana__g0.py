"""Normal gravity on WGS84 ellipsoid using the International Gravity Formula with fitted coefficients."""
import numpy as np

USED_INPUTS = ["latitude"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    latitude = X[:, 0]
    # Using the fitted coefficients for the International Gravity Formula form:
    # g = A + B*sin²(φ) + C*sin⁴(φ)
    lat_rad = np.radians(latitude)
    sin2 = np.sin(lat_rad)**2
    return 9.78421872 + 0.04065312 * sin2 + 0.00768762 * sin2**2