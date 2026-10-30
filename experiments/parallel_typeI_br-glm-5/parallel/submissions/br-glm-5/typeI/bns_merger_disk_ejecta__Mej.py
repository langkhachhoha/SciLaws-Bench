"""Dynamical ejecta mass from neutron star mergers.

Mej = asymmetric component (depends on mass ratio) + symmetric base component.
- Asymmetric: A*(1-q)^p * Lambda^3 * exp(-Lambda/Lambda0) 
- Base: C * Lambda^2 * exp(-Lambda/Lambda1)

At q=1, the asymmetric term vanishes, leaving only the baseline ejecta from 
neutrino-driven winds and other mechanisms in symmetric mergers.
"""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    lam = X[:, 1]
    
    # Fitted constants
    A = 4.2e-13        # amplitude of asymmetric term
    p = 3.0            # power of (1-q) asymmetry
    Lambda0 = 400      # decay scale for asymmetric term
    C = 1.2e-6         # amplitude of base term  
    Lambda1 = 500      # decay scale for base term
    
    # Asymmetric ejecta (vanishes when q=1)
    asym_term = A * np.power(np.maximum(1-q, 1e-6), p) * np.power(np.maximum(lam, 1), 3) * np.exp(-lam/Lambda0)
    
    # Base ejecta (exists even for symmetric q=1 mergers)
    base_term = C * np.power(np.maximum(lam, 1), 2) * np.exp(-lam/Lambda1)
    
    return asym_term + base_term