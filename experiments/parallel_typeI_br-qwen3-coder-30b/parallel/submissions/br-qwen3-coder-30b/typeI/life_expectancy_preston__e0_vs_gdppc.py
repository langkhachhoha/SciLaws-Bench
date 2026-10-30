"""Life expectancy as a function of GDP per capita using a saturation model."""
import numpy as np

USED_INPUTS = ["gdppc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract GDP per capita
    gdppc = X[:, 0]
    
    # Apply saturation model: e0 = A * (1 - exp(-B * ln(gdppc))) + C
    # Fitted parameters from experimental data
    A = 375.3554
    B = 0.578465
    C = -298.3483
    
    # Compute natural logarithm of GDP per capita
    log_gdppc = np.log(gdppc)
    
    # Apply the saturation function
    y_pred = A * (1 - np.exp(-B * log_gdppc)) + C
    
    return y_pred