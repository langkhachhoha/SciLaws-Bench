"""Michaelis-Menten (saturation) model for life expectancy vs GDP per capita.

The Preston curve in development literature relates life expectancy to economic 
development. This Michaelis-Menten form captures the saturating relationship:
- At low GDP, e0 increases roughly linearly with GDP
- At high GDP, e0 approaches a maximum asymptote (~74 years)
- The half-saturation point (where e0 = Vmax/2 = 37) occurs at K≈50 USD

e0 = Vmax * gdppc / (K + gdppc)

With Vmax = 74 and K = 50:
- e0(50) = 37 (half saturation)
- e0 → 74 as gdppc → ∞
"""
import numpy as np

USED_INPUTS = ["gdppc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    gdppc = X[:, 0]
    Vmax = 74
    K = 50
    return Vmax * gdppc / (K + gdppc)