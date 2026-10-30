"""Melt pool depth proportional to laser power divided by scan velocity and beam diameter."""
import numpy as np

USED_INPUTS = ["laser_power_W", "scan_velocity_mm_per_s", "beam_diameter_um"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    P = X[:, 0]
    V = X[:, 1]
    D = X[:, 2]
    # Constant determined from experimental data: ~25942
    return 25942.0 * P / (V * D)