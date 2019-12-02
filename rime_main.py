import sys
from PySide2 import QtWidgets

from gui.rime_mainpanel import MainPanelWidget


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    widget = MainPanelWidget(MainWindow)
    MainWindow.setCentralWidget(widget)
    MainWindow.setWindowTitle("Rime")
    MainWindow.resize(850, 375)
    MainWindow.show()

    sys.exit(app.exec_())
