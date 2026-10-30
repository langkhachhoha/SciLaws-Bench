"""Logarithmic relationship between GDP per capita and life expectancy."""
import numpy as np

USED_INPUTS = ["gdppc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Using the fitted coefficients from the data analysis
    # e0 = 5.0420 + 9.0863 * log(gdppc)
    gdppc = X[:, 0]
    return 5.0420 + 9.0863 * np.log(gdppc)