import sys
import os
import runpy
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"back_end/python/"))
#from back_end.python import rime
import back_end.python.rime as rime
from rime_manager import Manager

from PySide2 import QtWidgets
from gui.rime_mainpanel import MainPanelWidget

def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget = MainPanelWidget(MainWindow, Manager)

    MainWindow.setCentralWidget(widget)
    MainWindow.setWindowTitle("Rime")
    MainWindow.resize(850, 375)
    MainWindow.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    #os.chdir(os.path.join(os.path.dirname(__file__),"back_end/python/"))

    for arg in sys.argv:
        if arg == "--gui":
            print("Starting GUI...")
            Manager.getInstance().rimeAccess = rime
            Manager.getInstance().connectOutput(sys.stdout.write)
            run()

    sys.stdout = sys.__stdout__
    print("Starting CLI...")
    '''
    args = rime.parse_args(sys.argv[1:])
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

    rime.run_rime(metadataPath, ripPath, outputPath, ignoreWarnings, netcdf4, hdf5, geotiff, checksum, tarNet, tarHdf, tarGeo, tarAll)
    '''
    runpy.run_module("rime", run_name='__main__')
        
