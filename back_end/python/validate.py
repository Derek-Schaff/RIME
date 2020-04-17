import numpy as np
import os.path as path
import subprocess


def validate_cf_conventions(netCDFPath, logFile):
    try:
        # runs cfchecks, a tool that checks if metadata in a NetCDF4 program meets CF conventions
        command = "cfchecks %s" % netCDFPath
        # will raise CalledProcessError if subprocess failed
        process = subprocess.check_output(command.split())
        return

    except subprocess.CalledProcessError as e:
        errorStr = "Warning: CF Metadata Convention check raised error code %d:\n%s" % (e.returncode, e.output.decode('utf-8'))
        print(errorStr)
        logFile.write(errorStr)
        exit()


def validate_np_array(array):
    valid = False
    if isinstance(array, np.ndarray):
        valid = True

    return valid


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
