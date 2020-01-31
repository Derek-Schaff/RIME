import argparse
import sys
from ctypes import *
from ctypes.util import find_library

# this class will store data in a struct
class BinStruct(Structure):
    # does some black magic. Describe struct fields and their data types
    _fields_ = [('files', c_char_p),
                ('numFiles', c_int)]

# create parser object, which handles commandline arguments
def parseArgs(sysArgs):
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


if __name__ == "__main__":
    # get commandline args
    args = parseArgs(sys.argv[1:])

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
