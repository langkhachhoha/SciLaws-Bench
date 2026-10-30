"""Butler-Volmer equation for HOR/HER on Pt in acidic electrolyte.

j = j0 * P_H2 * exp(Ea/R*(1/298 - 1/T)) * (exp(alpha_a*F*eta/(RT)) - exp(-alpha_c*F*eta/(RT)))
where alpha_c = alpha_c_1 * c_acid^n_acid

Key finding: The cathodic transfer coefficient alpha_c depends on acid concentration.
"""
import numpy as np

USED_INPUTS = ["eta", "T", "P_H2", "c_acid"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    eta = X[:, 0]
    T = X[:, 1]
    P_H2 = X[:, 2]
    c_acid = X[:, 3]
    
    # Physical constants
    F = 96485  # C/mol
    R = 8.314  # J/(mol K)
    T0 = 298.0  # Reference temperature (K)
    
    # Fitted constants (5 total, within limit)
    j0_298 = 209.3  # Exchange current density at T=298K, P_H2=1 (mA/cm2)
    alpha_a = 0.1915  # Anodic transfer coefficient (constant)
    alpha_c_1 = 0.8377  # Cathodic transfer coefficient at c_acid=1
    Ea = 15289.0  # Activation energy (J/mol)
    n_acid = -0.40  # Power for c_acid dependence of alpha_c
    
    # Calculate transfer coefficient (cathodic, depends on acid concentration)
    alpha_c = alpha_c_1 * (c_acid ** n_acid)
    
    # Temperature factor (Arrhenius)
    temp_factor = np.exp(Ea / R * (1.0/T0 - 1.0/T))
    
    # Exchange current density
    j0 = j0_298 * P_H2 * temp_factor
    
    # Butler-Volmer equation
    x = F * eta / (R * T)
    j = j0 * (np.exp(alpha_a * x) - np.exp(-alpha_c * x))
    
    return j