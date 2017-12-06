__author__ = 'pedro'

#hist-> NUMPY ndarray
def normalizar(hist, eps = 0.000001):
    import numpy as np
    hist = hist + eps
    hist = hist / np.linalg.norm(hist, ord=1)
    return hist