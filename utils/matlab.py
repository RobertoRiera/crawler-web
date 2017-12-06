__author__ = 'pedro'

# load from matlab file(-v7.3) to numpy array a dataset model
def loadModelSamplesFile_v73(matlab_path):
    import h5py
    import numpy as np
    fd=h5py.File(matlab_path)
    content = fd[fd.keys()[0]]
    return np.array(content)

# Save numpy ndarray to a matlab file a dataset model
def saveModelSamples(file_path, ndarray_vect):
    import scipy.io as io
    import numpy as np
    io.savemat(file_path, dict(modelSamples=np.transpose(ndarray_vect)))