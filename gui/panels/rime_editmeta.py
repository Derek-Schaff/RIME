import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QFileDialog, QTableWidgetItem


class MetaDataEditWidget(QtWidgets.QWidget):
    def __init__(self, path):
        super().__init__()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setObjectName("editMetaDataPanel")
        self.resize(525, 300)

        self.metaTable = QtWidgets.QTableWidget(0, 2)
        self.metaTable.setColumnWidth(0, 250)
        self.metaTable.setColumnWidth(1, 200)
        self.metaTable.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.metaTable.setHorizontalHeaderItem(1, QTableWidgetItem("Value"))
        self.layout.addWidget(self.metaTable)
        self.setLayout(self.layout)

        self.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Edit Metadata", None, -1))

        metadata_file = path
        with open(metadata_file, "r") as meta:
            content = meta.readlines()

            for line in content:
                line.strip()
                if not line.startswith('#') and len(line) > 1:
                    temp = line.strip().split('=')

                    self.metaTable.insertRow(self.metaTable.rowCount())
                    self.metaTable.setItem(self.metaTable.rowCount()-1, 0,  QTableWidgetItem(temp[0]))
                    self.metaTable.setItem(self.metaTable.rowCount()-1, 1,  QTableWidgetItem(temp[1]))
