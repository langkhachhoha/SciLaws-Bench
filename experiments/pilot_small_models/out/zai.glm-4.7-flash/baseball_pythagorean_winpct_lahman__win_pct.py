"""Win percentage is a function of run differential per game."""
import numpy as np

USED_INPUTS = ["R", "RA", "G"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    R = X[:, 0]
    RA = X[:, 1]
    G = X[:, 2]
    
    # Calculate Run Differential per Game
    # The mechanism is Win % = 0.5 + (RD/G) / (1 + (RD/G)^2)
    # This models a logistic relationship between run differential and winning percentage.
    rd = R - RA
    rd_per_g = rd / G
    
    # Logistic function: 0.5 + x / (1 + x^2)
    # This ensures the win percentage is bounded between 0 and 1.
    # When RD/G = 0, Win % = 0.5.
    # As RD/G -> infinity, Win % -> 1.
    # As RD/G -> -infinity, Win % -> 0.
    win_pct = 0.5 + rd_per_g / (1 + rd_per_g**2)
    
    return win_pct