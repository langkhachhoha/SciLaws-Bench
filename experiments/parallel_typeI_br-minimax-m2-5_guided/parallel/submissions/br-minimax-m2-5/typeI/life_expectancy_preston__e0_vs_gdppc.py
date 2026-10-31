"""Preston curve: e0 = a - b * exp(-c * gdppc), a classic demographic relationship between life expectancy and GDP per capita."""
import numpy as np

USED_INPUTS = ["gdppc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    gdppc = X[:, 0]
    a = 72.21    # Asymptotic maximum life expectancy (years)
    b = 63.62    # Range of life expectancy gain
    c = 0.0106   # Diminishing returns parameter (per USD)
    return a - b * np.exp(-c * gdppc)