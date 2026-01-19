import numpy as np

def calculate_eoq(D, S, H):
    return np.sqrt((2 * D * S) / H)
