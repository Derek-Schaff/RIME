from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog

from gui.panels.rime_runprogress import RunProgressWidget
from rime_manager import Manager


class RunPanelWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #self.runPageProcessBar = QtWidgets.QProgressBar()
        self.runPageStatistics = QtWidgets.QTextEdit()
        self.runPageStatistics.setReadOnly(True)

        self.runPageRunButton = QtWidgets.QPushButton("Run")
        self.runPageRunButton.setObjectName("runButton")

        self.runPageGrid = QtWidgets.QGridLayout()
        self.runPageGrid.setObjectName("runPageLayout")
        self.runPageGrid.addWidget(self.runPageStatistics, 0, 0)
        self.runPageGrid.addWidget(self.runPageRunButton, 1, 0)
        self.runPageGrid.rowStretch(0)

        self.setLayout(self.runPageGrid)

        self.runPageRunButton.clicked.connect(self.runRime)

    def update_statistics(self):
        self.runPageStatistics.clear()

        for p in Manager.getInstance().run_params:
            self.runPageStatistics.append(p + ": " + str(Manager.getInstance().run_params[p]) + "\n")

    def runRime(self):
        self.runProgressWindow = RunProgressWidget()
        self.runProgressWindow.show()