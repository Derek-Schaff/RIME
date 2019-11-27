from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog


class RunPanelWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.runPageProcessBar = QtWidgets.QProgressBar()

        self.runPageGrid = QtWidgets.QGridLayout()
        self.runPageGrid.setObjectName("runPageLayout")
        self.runPageGrid.addWidget(self.runPageProcessBar, 0, 0)#

        self.setLayout(self.runPageGrid)