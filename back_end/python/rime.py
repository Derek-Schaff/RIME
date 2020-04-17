import argparse
import back_end.python.convert as convert
import back_end.python.validate as validate
import numpy as np
import h5py
import time
import sys
from ctypes import *
from ctypes.util import find_library
#import rime_main
import os
from os import path
import subprocess
import back_end.python.statusUpdate as statusUpdate
from back_end.python.checkSum import generate_chk_sum
import unittest



# this class will store data in a struct
class BinStruct(Structure):
    # does some black magic. Describe struct fields and their data types
    _fields_ = [('files', c_char_p),
                ('numFiles', c_int)]


# create parser object, which handles commandline arguments
def parse_args(sysArgs):
    parser = argparse.ArgumentParser(sysArgs)
    # options without -- are required and positional
    parser.add_argument("metadata", help="File containing metadata necessary for file conversion. Must meet EASEGRID 2.0 standards")
    parser.add_argument("rip", help="Read Input Parameter file containing necessary information for file conversion")
    parser.add_argument("output", help="Desired output directory")
    # options with -- are optional and can occur in any order. If a type isn't explicitly defined, they are assumed to be booleans that are set to true when enabled
    parser.add_argument("--ignore_warnings", "-i", action="store_true", help="Instead of stopping on warnings, ignore and continue")
    parser.add_argument("--gui", "-gu", action="store_true", help="Launch RIME GUI. GUI currently inoperable")
    parser.add_argument("--netcdf4", "-n", action="store_true", help="Store output in NetCDF4 file format. Any combination of output format options can be specified simultaneously")
    parser.add_argument("--hdf5", "-hd", action="store_true", help="Store output in HDF5 file format. Any combination of output format options can be specified simultaneously")
    parser.add_argument("--geotiff", "-g", action="store_true", help="Store output in GeoTIFF file format. Any combination of output format options can be specified simultaneously")
    parser.add_argument("--checksum", "-c", action="store_true", help="Generate file checksum value")
    parser.add_argument("--tar_netcdf4", "-tn", action="store_true", help="Automatically compress output NetCDF4 files. --netcdf4 must be enabled")
    parser.add_argument("--tar_hdf5", "-th", action="store_true", help="Automatically compress output HDF5 files. --hdf5 must be enabled")
    parser.add_argument("--tar_geotiff", "-tg", action="store_true", help="Automatically compress output GeoTIFF files. --geotiff must be enabled")
    parser.add_argument("--tar_all", "-ta", action="store_true", help="Automatically compress output for all specified output types")
    # example of specifying type and default value: parser.add_argument("--", type=float, default=1e-5, help="")

    return parser.parse_args()




# reads lines from catalog file, which contains paths to input binaries
def read_catalog(filePath):
    binList = []

    with open(filePath) as catalog:
        for binPath in catalog:
            binPath = binPath.strip()

            if os.path.exists(binPath):
                binList.append(binPath)
            else:
                raise FileNotFoundError(binPath)

    return binList


def load_binary(binaryPath, dataType):
    binary = np.fromfile(binaryPath, dataType)

    return binary


def create_output_dir(dirPath):
    command = "mkdir %s" % dirPath
    subprocess.run(command.split())

    validate.validate_dir(dirPath)


def resolution_reshape(array, x, y):
    if validate.validate_np_array(array):
        try:
            array = np.reshape(array, (x,y))
        except ValueError as e:
            raise ValueError("Array cannot be reshaped to %d x %d" % (x, y))
    else:
        raise TypeError("Input array is not a Numpy array")

    return array


def parse_rip(filePath):
    ripDic = {}  # type: Dict[str, str]

    # use open convention that helps avoid weird issues if the program crashes with file open:
    with open(filePath) as paramFile:
        for line in paramFile:
            # skip comments starting with #. Otherwise, remove whitespace and split using '=' as delimiter
            if line[0] != '#':
                line = line.strip()
                # skip empty lines
                if line:
                    # line structure should be key = value, so we split on '=' and set dict[key] = value
                    splitLine = line.split('=', 1) #split at only the first instance of the delimiter
                    ripDic[splitLine[0].strip()] = splitLine[1].strip()

    return ripDic


# hey dummy, combine metadata and rip parse into a single method because they're super similar. Maybe make them one of
# those fancy factory things
def parse_metadata(filePath):
    metadataDic = {} # type: Dict[str, str]

    with open(filePath) as metadataFile:
        for line in metadataFile:
            # remove any extra whitespace
            line = line.strip()
            # skip comments and empty strings
            if line and line[0] != '#':
                splitLine = line.split(',', 1) #split at only the first instance of the delimiter
                key = splitLine[0].strip()
                value = splitLine[1].strip()

                # ensure that key doesn't exist so we don't accidentally overwrite a value we want
                if key in metadataDic:
                    print("Key %s already exists in metadataDic!" % key)
                    raise KeyError

                # now that we've split the line, make sure we get rid of trailing whitespace
                metadataDic[key] = value

    return metadataDic


# validate that all .bins in binDir exist and append them to list
def build_bin_list(binDir):
    binList = []

    for root, dirs, files in os.walk(binDir):
        for file in files:
            if file.endswith(".bin"):
                binPath = os.path.join(root, file)
                validate.validate_binary_file(binPath)
                binList.append(binPath)

    return binList


def update_status(updateString, log):
    print(updateString)
    log.write(updateString)

def gen_checksum(filePath, outputPath, logFile):
    update_status("Generating checksum for %s..." % filePath, logFile)
    checkFile = open(outputPath + "/../check_sums.txt", 'a+')
    checkFile.write(outputPath + ": " + generate_chk_sum(filePath) + "\n")
    checkFile.close()

def run_rime(metadataPath, ripPath, outputPath, ignoreWarnings, netcdf4, hdf5, geotiff, checksum, tarNet, tarHdf, tarGeo, tarAll, binRoot=None):
    metadataDic = parse_metadata(metadataPath)
    ripDic = parse_rip(ripPath)
    times = []
    x = int(ripDic["FT_DATASET_ROWS"])
    y = int(ripDic["FT_DATASET_COLUMNS"])
    datatype = ripDic["FT_DATASET_DATATYPE_FOR_STATUS"]
    logPath = os.getcwd() + "/log.txt" #%slog.txt" % ripDic["FT_OUTPUT_LOG_DIR"]
    if ripDic["FT_BINARY_ROOT_DIR"]:
        binDir = ripDic["FT_BINARY_ROOT_DIR"]
    else:
        binDir = binRoot

    # automatically detects all .bin files, validates they exist
    binList = build_bin_list(binDir)
    numBins = len(binList)

    # open logfile
    with open(logPath, "a+") as logFile:
        update_status("Loading binary files....", logFile)
        for currentBinNum, binFile in enumerate(binList):
            validate.validate_binary_file(binFile)
            update_status("Current file: %s\nFile Number: %d / %d" % (binFile, currentBinNum, numBins), logFile)

            binData = resolution_reshape(load_binary(binFile, datatype), x, y)
            binBaseName = path.basename(os.path.splitext(binFile)[0])
            validateCFInterval = 50

            if hdf5:
                hdfOutputDir = "%s/HDF5" % outputPath
                hdfOutputFile = ("%s/%s.h5" % (hdfOutputDir, binBaseName))

                # if output HDF5 dir doesn't exist, try to make it
                if not validate.validate_dir(hdfOutputDir):
                    create_output_dir(hdfOutputDir)

                start = time.time()
                hdfFile = convert.create(hdfOutputFile, binData, ripDic, metadataDic, "HDF5")
                h5py.is_hdf5(hdfFile.filename) #TODO: Make this a validate method
                hdfFile.close()
                end = time.time()

                updateString = "%s HDF5 conversion time: %f" % (binFile, end - start)
                times.append([end-start])
                update_status(updateString, logFile)

            if geotiff:
                gtifOutputDir = "%s/GEOTIFF" % outputPath
                gtifOutputFile = ("%s/%s.h5" % (gtifOutputDir, binBaseName))

                # if output Geotiff dir doesn't exist, try to make it
                if not validate.validate_dir(gtifOutputDir):
                    create_output_dir(gtifOutputDir)

                GTIFFOutput = ("%s/GEOTIFF/%s.gtif" % (outputPath, binBaseName))
                start = time.time()
                GTIFF = convert.create(GTIFFOutput, binData, ripDic, metadataDic, "GEOTIFF")
                end = time.time()

                updateString = "%s GEOTIFF conversion time: %f" % (binFile, end - start)
                times.append([end-start])
                update_status(updateString, logFile)

            if netcdf4:

                ncdfOutputDir = "%s/NETCDF4" % outputPath
                ncdfOutputFile = ("%s/%s.nc" % (ncdfOutputDir, binBaseName))

                # if output netCDF dir doesn't exist, try to make it
                if not validate.validate_dir(ncdfOutputDir):
                    create_output_dir(ncdfOutputDir)

                ncdfOutput = ("%s/NETCDF4/%s.nc" % (outputPath, binBaseName))
                start = time.time()
                ncdf = convert.create(ncdfOutput, load_binary(binFile, datatype), ripDic, metadataDic, "NETCDF4")
                end = time.time()
                times.append([end-start])


                validate.validate_cf_conventions(ncdfOutput, logFile)

                updateString = "%s NETCDF4 conversion time: %f" % (binFile, end - start)
                update_status(updateString, logFile)

            # The CF metadata validation package we use only works on NetCDF4 files, so to check metadata validity in
            # cases where we aren't creating
            elif currentBinNum % validateCFInterval == 0:
                tempDir = "%s/temp" % outputPath
                if not validate.validate_dir(tempDir):
                    create_output_dir(tempDir)

                ncdfOutput = "%s/temp/temp.nc" % outputPath
                start = time.time()
                ncdf = convert.create(ncdfOutput, load_binary(binFile, datatype), ripDic, metadataDic, "NETCDF4")
                end = time.time()

                #validate.validate_cf_conventions(ncdfOutput, logFile)

            update_status("Conversions on file %s complete" % binBaseName, logFile)
            update_status("Remaining conversions ETA: %d minutes" % (np.average(times) * (numBins - currentBinNum) / 60.0), logFile)

        update_status("All conversions complete!", logFile)

        # remove temporary netCDF4 CF metadata validation dir
        if not netcdf4:
            command = "rm -rf %s/temp" % outputPath
            subprocess.check_output(command.split())

        if tarAll or checksum:
            try:
                outputName = os.path.basename(outputPath)
                command = "tar -czf %s.tgz %s" % (outputName, outputPath)
                update_status("Compressing all output files...", logFile)
                subprocess.check_output(command.split())

                if checksum:
                    gen_checksum("%s.tgz" % outputName, outputPath, logFile)

            except subprocess.CalledProcessError as e:
                print("Unable to tar %s: %s") % (outputPath, e.output)

        else:
            if tarGeo:
                try:
                    outputName = os.path.basename(outputPath)
                    command = "tar -czf %s.tgz %s" % outputName
                    subprocess.check_output(command.split())
                    statusUpdate.update_status("compressing all GEOTIFF files", logFile)

                    if checksum:
                        gen_checksum("%s.tgz" % outputName, outputPath, logFile)

                except subprocess.CalledProcessError as e:
                    print("Unable to tar %s: %s") % (outputPath, e.output)

            if tarHdf:
                try:
                    outputName = os.path.basename(outputPath)
                    statusUpdate.update_status("compressing all HDF5 files", logFile)
                    command = "tar -czf %s.tgz %s" % (outputName, outputPath)
                    subprocess.check_output(command.split())

                    if checksum:
                        gen_checksum("%s.tgz" % outputName, outputPath, logFile)

                except subprocess.CalledProcessError as e:
                    print("Unable to tar %s: %s") % (outputPath, e.output)

                if tarNet:
                    try:
                        outputName = os.path.basename(outputPath)
                        statusUpdate.update_status("compressing all NETCDF4 files", logFile)
                        command = "tar -czf %s.tgz %s" % outputName
                        subprocess.check_output(command.split())

                        if checksum:
                            gen_checksum("%s.tgz" % outputName, outputPath, logFile)

                    except subprocess.CalledProcessError as e:
                        print("Unable to tar %s: %s") % (outputName, e.output)

    # if checksum:
    #     checkFile = open(outputPath + "/check_sums.txt", 'w+')
    #
    #     if geotiff:
    #         checkFile.write("--geotiff checksums--\n\n")
    #         for filename in os.listdir(gtifOutputDir):
    #             checkFile.write(filename + ": " + generate_chk_sum(gtifOutputDir + "/" + filename) + "\n")
    #         checkFile.write("\n")
    #
    #     if hdf5:
    #         checkFile.write("--hdf5 checksums--\n\n")
    #         for filename in os.listdir(hdfOutputDir):
    #             checkFile.write(filename + ": " + generate_chk_sum(hdfOutputDir + "/" + filename) + "\n")
    #         checkFile.write("\n")
    #     if netcdf4:
    #         checkFile.write("--netcdf4 checksums--\n\n")
    #         for filename in os.listdir(ncdfOutputDir):
    #             checkFile.write(filename + ": " + generate_chk_sum(ncdfOutputDir + "/" + filename) + "\n")
    #         checkFile.write("\n")
    #
    #     statusUpdate.update_status("generating MD5 checksums", temp_logPath)
    #     checkFile.close()


if __name__ == "__main__":
    #get commandline args
    args = parse_args(sys.argv[1:])
    metadataPath = args.metadata
    ripPath = args.rip
    outputPath = args.output
    ignoreWarnings = args.ignore_warnings
    gui = args.gui
    netcdf4 = args.netcdf4
    hdf5 = args.hdf5
    geotiff = args.geotiff
    checksum = args.checksum
    tarNet = args.tar_netcdf4
    tarHdf = args.tar_hdf5
    tarGeo = args.tar_geotiff
    tarAll = args.tar_all

    run_rime(metadataPath, ripPath, outputPath, ignoreWarnings, netcdf4, hdf5, geotiff, checksum, tarNet, tarHdf, tarGeo, tarAll)