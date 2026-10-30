"""Red giant nu_max scales as rational function of delta_nu.

The rational form captures the transition from quadratic scaling 
at low delta_nu (d << b) to linear scaling at high delta_nu (d >> b).

nu_max = a * delta_nu^2 / (b + delta_nu)
- At low d: nu_max ~ (a/b) * d^2
- At high d: nu_max ~ a * d
"""
import numpy as np

USED_INPUTS = ["delta_nu"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]
    a = 15.27
    b = 2.94
    return a * d**2 / (b + d)