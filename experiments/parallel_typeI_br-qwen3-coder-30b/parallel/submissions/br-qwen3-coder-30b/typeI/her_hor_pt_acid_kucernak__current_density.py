"""Butler-Volmer type equation with Tafel-like behavior and pressure dependence."""
import numpy as np

USED_INPUTS = ["eta", "T", "P_H2", "c_acid"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {
    "F": 96485.33212,  # Faraday constant (C/mol)
    "R": 8.314462618,  # Gas constant (J/mol/K)
    "alpha": 0.5,      # Transfer coefficient (assumed symmetric)
    "j0_ref": 1.0      # Reference exchange current density (A/cm²)
}
LOCAL_FITTABLE = {}

def predict(X):
    eta = X[:, 0]
    T = X[:, 1]
    P_H2 = X[:, 2]
    c_acid = X[:, 3]
    
    F = OTHER_CONSTANTS["F"]
    R = OTHER_CONSTANTS["R"]
    alpha = OTHER_CONSTANTS["alpha"]
    j0_ref = OTHER_CONSTANTS["j0_ref"]
    
    # Calculate the exchange current density with dependencies
    # j0 = j0_ref * sqrt(P_H2) * exp(-Ea/(R*T)) * c_acid^F
    # For simplicity, we'll assume a basic form that captures the physics
    j0 = j0_ref * np.sqrt(P_H2) * np.exp(-10000.0 / (R * T)) * (c_acid ** 0.5)
    
    # Butler-Volmer equation: j = j0 * (exp(alpha*F*eta/(R*T)) - exp(-(1-alpha)*F*eta/(R*T)))
    # For symmetric transfer coefficient (alpha = 0.5), this simplifies to:
    # j = j0 * sinh(F*eta/(2*R*T))
    sinh_arg = F * eta / (2 * R * T)
    j = j0 * np.sinh(sinh_arg)
    
    return j