import h5py
from osgeo import gdal, gdal_array, osr
import numpy as np
from back_end.python import validate


# define factory pattern client
def create(filePath, binary, ripDic, metadataDic, fileFormat):
    converter = get_creator(fileFormat)
    return converter(filePath, binary, ripDic, metadataDic)


def get_creator(format):
    if format == 'HDF5':
        return _create_hdf5
    elif format == 'NETCDF4':
        return _create_netcdf4
    elif format == 'GEOTIFF':
        return _create_geotiff
    else:
        raise ValueError(format)


def _create_hdf5(filePath, binary, ripDic, metadataDict):
    # check that binary is a np array
    validate.validate_np_array(binary)

    # use mode 'w' for write access
    file = h5py.File(filePath, "w")
    file.create_dataset("data", data=binary)

    load_metadata_hdf5(file, metadataDict)

    return file


def _create_netcdf4():
    #TODO
    return


def _create_geotiff(filePath, binary, ripDic, metadataDic):
    x = int(ripDic["FT_DATASET_ROWS"])
    y = int(ripDic["FT_DATASET_COLUMNS"])
    # thirdVal's value in the 'Affine GeoTransform' relationship is multiplied by a coefficient of 0, so we always expect it to be zero. Same with fifthVal
    # In case this ever changes, we set them here rather than using magic numbers
    thirdVal = 0
    fifthVal = 0
    upperLeft = ripDic["FT_DATASET_GRID_UPPER_LEFT_XY"]
    yMax = float(ripDic["FT_DATASET_GEOG_NORTH_BOUND_LATITUDE"])
    yMin = float(ripDic["FT_DATASET_GEOG_SOUTH_BOUND_LATITUDE"])
    xMin = float(ripDic["FT_DATASET_GEOG_WEST_BOUND_LONGITUDE"])
    xMax = float(ripDic["FT_DATASET_GEOG_EAST_BOUND_LONGITUDE"])
    xRes = (xMax - xMin) / float(x)
    yRes = (yMax - yMin) / float(y)
    numberBands = 1
    # EASEGRID Global
    EPSG = 3410

    # create geoTransform in accordance with relationship described at https://gdal.org/user/raster_data_model.html#affine-geotransform
    geoTransform = (xMin, xRes, thirdVal, yMax, fifthVal, -yRes)

    gdalType = gdal_array.NumericTypeCodeToGDALTypeCode(binary.dtype)

    geoTiff = gdal.GetDriverByName('GTiff').Create(filePath, y, x, numberBands, gdalType)
    geoTiff.SetGeoTransform(geoTransform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(EPSG)
    geoTiff.SetProjection(srs.ExportToWkt())
    geoTiff.GetRasterBand(1).WriteArray(binary)
    geoTiff.FlushCache()
    geoTiff = None
    return



def load_metadata_hdf5(file, metadataDic):
    for key in metadataDic.keys():
        # all keys in metaDataDic will be composed of a group path and an attribute name; attr is separated with |
        splitKey = key.split('|')
        groupPath = splitKey[0]
        attrName = splitKey[1]

        # check if group already exists before adding attribute; else, create it
        if groupPath in file:
            group = file[groupPath]
        else:
            group = file.create_group(groupPath)

        group.attrs[attrName] = metadataDic[key]
