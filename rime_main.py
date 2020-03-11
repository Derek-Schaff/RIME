import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"back_end/python/"))
from back_end.python import rime

from PySide2 import QtWidgets
from gui.rime_mainpanel import MainPanelWidget

def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget = MainPanelWidget(MainWindow)

    MainWindow.setCentralWidget(widget)
    MainWindow.setWindowTitle("Rime")
    MainWindow.resize(850, 375)
    MainWindow.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__),"back_end/python/"))

    for arg in sys.argv:
        if arg == "--gui":
            print("Starting GUI...")
            run()

    sys.stdout = sys.__stdout__
    print("Starting CLI...")
    rime.main()
        
