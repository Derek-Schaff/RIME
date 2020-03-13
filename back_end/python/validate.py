import numpy as np
import os.path as path


def validate_np_array(array):
    if isinstance(array, np.ndarray):
        return
    else:
        raise TypeError


def validate_binary_file(filePath):
    valid = False

    if path.exists(filePath) and path.isfile(filePath):
        valid = True

    return valid


def validate_dir(dirPath):
    valid = False

    if path.exists(dirPath) and path.isdir(dirPath):
        valid = True

    return valid