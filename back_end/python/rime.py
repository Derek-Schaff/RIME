import argparse
# import convert
# import validate
# import numpy as np
# import h5py
import time
import sys
from ctypes import *
from ctypes.util import find_library
#import rime_main
import os
from os import path
import subprocess


# this class will store data in a struct
class BinStruct(Structure):
    # does some black magic. Describe struct fields and their data types
    _fields_ = [('files', c_char_p),
                ('numFiles', c_int)]


# create parser object, which handles commandline arguments
def parse_args(sysArgs):
    parser = argparse.ArgumentParser(sysArgs)
    # options without -- are required and positional
    parser.add_argument("catalog", help="")
    parser.add_argument("rip", help="")
    parser.add_argument("output", help="")
    # options with -- are optional and can occur in any order. If a type isn't explicitly defined, they are assumed to be booleans that are set to true when enabled
    parser.add_argument("--ignore_warnings", "-i", action="store_true", help="Instead of stopping on warnings, ignore and continue")
    parser.add_argument("--netcdf4", "-n", action="store_true", help="Store output in NetCDF4 file format. Any combination of output format options can be specified simultaneously")
    parser.add_argument("--gui", "-gu", action="store_true", help="Launch RIME GUI")
    parser.add_argument("--hdf5", "-hd", action="store_true", help="Store output in HDF5 file format. Any combination of output format options can be specified simultaneously")
    parser.add_argument("--geotiff", "-g", action="store_true", help="Store output in GeoTIFF file format. Any combination of output format options can be specified simultaneously")
    parser.add_argument("--checksum", "-c", action="store_true", help="")
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
                raise FileNotFoundError()

    return binList


def load_binary(binaryPath, dataType):
    binary = np.fromfile(binaryPath, dataType)

    return binary


# def resolution_reshape(array, x, y):
#     validate.validate_np_array(array)
#     array = np.reshape(array, (x,y))
#
#     return array


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
                    splitLine = line.split('=')
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
                splitLine = line.split(',')
                key = splitLine[0].strip()
                value = splitLine[1].strip()

                # ensure that key doesn't exist so we don't accidentally overwrite a value we want
                if key in metadataDic:
                    print("Key %s already exists in metadataDic!" % key)
                    raise KeyError

                # now that we've split the line, make sure we get rid of trailing whitespace
                metadataDic[key] = value

    return metadataDic


def update_status(updateString, log):
    #TODO
    return


if __name__ == "__main__":
    # get commandline args
    args = parse_args(sys.argv[1:])
    catalogPath = args.catalog
    ripPath = args.rip
    outputPath = args.output
    ignoreWarnings = args.ignore_warnings
    netcdf4 = args.netcdf4
    gui = args.gui
    hdf5 = args.hdf5
    geotiff = args.geotiff
    checksum = args.checksum
    tarNet = args.tar_netcdf4
    tarHdf = args.tar_hdf5
    tarGeo = args.tar_geotiff
    tarAll = args.tar_all



    '''
    # load C .so library to get access to parseDir()
    parseLib = CDLL('../c/parserlib.so')
    # debug print statement.. delete me later!
    print(parseLib)
    # specify C types of input args and return value
    parseLib.parseDir.argtypes = [c_wchar_p]
    parseLib.parseDir.restypes = [c_void_p]

    # the C function returns a struct- throw it into a class with the same values and print to see if it's right
    p1 = BinStruct.from_address(parseLib.parseDir('.'))
    print(p1.files)
    '''
    netCDF = CDLL("/home/turkishdisko/RIME/back_end/c/dum.so")
    ripDic = parse_rip("test/test_rip.txt")
    metadataDic = parse_metadata("test/test_metadata.txt")

    if gui:
        netCDF.conv_netCDF()
        #rime_main.run()
        None


    else:
        args = parse_args(sys.argv[1:])
        catalogPath = args.catalog
        ripPath = args.rip
        outputPath = args.output
        ignoreWarnings = args.ignore_warnings
        netcdf4 = args.netcdf4
        #gui = args.gui
        hdf5 = args.hdf5
        geotiff = args.geotiff
        checksum = args.checksum
        tarNet = args.tar_netcdf4
        tarHdf = args.tar_hdf5
        tarGeo = args.tar_geotiff
        tarAll = args.tar_all

        '''
        # load C .so library to get access to parseDir()
        parseLib = CDLL('../c/parserlib.so')
        # debug print statement.. delete me later!
        print(parseLib)
        # specify C types of input args and return value
        parseLib.parseDir.argtypes = [c_wchar_p]
        parseLib.parseDir.restypes = [c_void_p]

        # the C function returns a struct- throw it into a class with the same values and print to see if it's right
        p1 = BinStruct.from_address(parseLib.parseDir('.'))
        print(p1.files)
        '''
        # x = int(ripDic["FT_DATASET_ROWS"])
        # y = int(ripDic["FT_DATASET_COLUMNS"])
        # binList = read_catalog("test/test_catalog.txt")
        # bin = resolution_reshape(load_binary(binList[0], 'uint8'), x, y)
        #
        # if tarAll:
        #     None
        # else:
        #     if tarNet:
        #         None
        #     if tarGeo:
        #         None
        #     if tarHdf:
        #         None
        #
        # if checksum:
        #     None
        #     #checksum stuff
        #
        # # BELOW IS SPOOFING FOR USER TESTING
        # '''
        # if badMetadata and badCatalog:
        #     if not ignoreWarnings:
        #         # TODO
        #         if badMetadata:
        #             #TODO
        #         elif badCatalog:
        #             #TODO
        # '''
        #
        # if netcdf4 and hdf5 and geotiff:
        #     #TODO
        #     if tarAll:
        #         None
        #         # TODO
        # elif netcdf4:
        #     None
        #     #TODO
        #     if tarNet:
        #         None
        #         #TODO
        # elif hdf5:
        #     for i in range(0,10):
        #         testOutput = 'test1/'
        #         if not path.isdir(testOutput):
        #             command = "mkdir %s" % testOutput
        #             subprocess.run(command.split())
        #
        #         spoofPath = '%s/output%d.h5' % (testOutput, i)
        #
        #         start = time.time()
        #         print("Beginning conversion of bin%d" % i)
        #         test_hdf5 = convert.create(spoofPath, bin, ripDic, metadataDic, "HDF5")
        #         end = time.time()
        #         print("bin%d conversion to HDF5 complete. Total time elapsed: %f seconds" % (i, end - start))
        #
        #     if tarHdf:
        #         None
        #         #TODO
        # elif geotiff:
        #     None
        #         # TODO
        #     if tarGeo:
        #         None
        #         #TODO
        #
        #
        # hdf5 = convert.create("path.h5", bin, ripDic, metadataDic, "HDF5")
        # GTIFF = convert.create("path.gtif", bin, ripDic, metadataDic, "GEOTIFF")
        # # print(h5py.is_hdf5(hdf5.filename))
        # # print(hdf5.keys())
        # hdf5.close()
