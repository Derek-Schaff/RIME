# Singleton style manager class
class Manager:
    __instance = None

    #expanded on multiple lines for clarity
    run_params = {}
    run_params['binary_path'] = ''
    run_params['metadata_path'] = ''
    run_params['catalog_path'] = ''
    run_params['output_path'] = ''
    run_params['logfile_path'] = 'DEFAULT'
    run_params['output_hdf5'] = False
    run_params['output_netcdf4'] = False
    run_params['output_geotiff'] = False
    run_params['output_filehash'] = False
    run_params['output_compress'] = False
    run_params['output_stopwarnings'] = False
    run_params['output_option_filehash'] = False
    run_params['output_option_compress'] = False
    run_params['output_option_stopwarn'] = False

    def checkNecessaryInput(self):
        inputCheck = False
        outputCheck = False

        if self.run_params['binary_path'] != '' and self.run_params['metadata_path']  != '' and self.run_params['catalog_path'] != '':
           inputCheck = True

        if self.run_params['output_hdf5'] or self.run_params['output_netcdf4'] or self.run_params['output_geotiff']:
            outputCheck = True

        return inputCheck and outputCheck




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
