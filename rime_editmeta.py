import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QFileDialog

LABEL_WIDTH = 120


class MetaDataEditWidget(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow

        #self.text.setAlignment(QtCore.Qt.AlignCenter)

        ''' Create main container (QToolBox) for dropdown style panels'''
        self.layout = QtWidgets.QGridLayout()
        self.layout.setObjectName("editMetaDataPanel")

        self.metaTable = QtWidgets.QTableWidget(10, 2)

        self.layout.addWidget(self.metaTable)
        self.setLayout(self.layout)

        self.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Edit Metadata", None, -1))

