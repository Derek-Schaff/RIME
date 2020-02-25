import numpy as np


def validate_np_array(array):

    if type(array) == np.ndarray:
        return
    else:
        raise TypeError
