import numpy as np


def compute_bfd(fragments):
    result = [0] * 256
    for byte in fragments:
        result[int(byte)] += 1
    return np.asarray(result)
