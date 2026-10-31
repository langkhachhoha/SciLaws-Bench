"""Butler-Volmer equation for HOR/HER on Pt: j = A * P_H2 * c_acid^(-m) * exp(-Ea/(R*T)) * (exp(alpha_a*eta*F/(R*T)) - exp(-alpha_c*eta*F/(R*T)))"""
import numpy as np

USED_INPUTS = ["eta", "T", "P_H2", "c_acid"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {"F": 96485.0, "R": 8.314}
LOCAL_FITTABLE = {}

def predict(X):
    eta = X[:, 0]
    T = X[:, 1]
    P_H2 = X[:, 2]
    c_acid = X[:, 3]
    
    F = 96485.0  # Faraday constant, C/mol
    R = 8.314    # Gas constant, J/(mol·K)
    
    # Fitted constants
    A = 94688.0        # Pre-exponential factor
    Ea = 15261.0       # Activation energy, J/mol
    alpha_a = 0.138    # Anodic transfer coefficient
    alpha_c = 1.077    # Cathodic transfer coefficient  
    m = 0.160          # Acid concentration exponent
    
    # Butler-Volmer with Arrhenius temperature dependence
    k = A * (c_acid ** (-m)) * np.exp(-Ea / (R * T))
    
    return k * P_H2 * (np.exp(alpha_a * eta * F / (R * T)) - np.exp(-alpha_c * eta * F / (R * T)))