# Singleton style manager class
class Manager:
    __instance = None

    run_params = {}
    run_params['binary_path'] = ''
    run_params['metadata_path'] = ''
    run_params['catalog_path'] = ''
    run_params['output_path'] = ''
    run_params['logfile_path'] = ''
    run_params['output_hdf5'] = False
    run_params['output_netcdf4'] = False
    run_params['output_geotiff'] = False
    run_params['output_filehash'] = False
    run_params['output_compress'] = False
    run_params['output_stopwarnings'] = False
    run_params['output_option_filehash'] = False
    run_params['output_option_compress'] = False
    run_params['output_option_stopwarn'] = False

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Manager.__instance == None:
            Manager()
        return Manager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Manager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Manager.__instance = self
