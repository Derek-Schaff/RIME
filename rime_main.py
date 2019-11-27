import sys
from PySide2 import QtWidgets

from gui.rime_mainpanel import MainPanelWidget


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    widget = MainPanelWidget(MainWindow)
    widget.resize(850, 360)
    widget.show()

    sys.exit(app.exec_())
