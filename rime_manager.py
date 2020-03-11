import helpers
from queue import Queue
import sys
from PySide2 import QtCore
from back_end.python.rime import *

# Singleton style manager class
class Manager:
    __instance = None

    # create Queue to be passed to WriteStream and WriteStreamListener
    queue = Queue()
    # redirect stdout to WriteStream()
    sys.stdout = helpers.WriteStream(queue)

    # create a thread that is connected to the queue which can be freely
    # forwarded to any function
    listener_thread = helpers.WriteStreamThread(queue)
    listener_thread.start()
    print("Redirected sys.stdout to WriteStream")

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

    listeners = []

    def checkNecessaryInput(self):
        inputCheck = False
        outputCheck = False

        if self.run_params['binary_path'] != '' and self.run_params['metadata_path']  != '' and self.run_params['catalog_path'] != '':
           inputCheck = True

        if self.run_params['output_hdf5'] or self.run_params['output_netcdf4'] or self.run_params['output_geotiff']:
            outputCheck = True

        return inputCheck and outputCheck

    def connectOutput(self, output_method):
        output_method_name = output_method.__name__
        
        if output_method_name not in self.listeners:
            self.listeners.append(output_method_name)
            self.listener_thread.queue_updated.connect(output_method)
        else:
            pass

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
    
    def __del__(self):
        self.listener_thread.exit()

