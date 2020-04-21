from PySide2 import QtWidgets
from PySide2.QtGui import QColor, QTextCursor
from PySide2.QtCore import Slot, Qt

from gui.panels.rime_runprogress import RunProgressWidget
import time

class RunPanelWidget(QtWidgets.QWidget):
    def __init__(self, manager, main_window):
        super().__init__()

        self.manager = manager
        self.runPageProcessBar = QtWidgets.QProgressBar()
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

        for p in self.manager.getInstance().run_params:
            if ((p == 'binary_path' and self.manager.getInstance().run_params[p] == '') or
                (p == 'metadata_path' and self.manager.getInstance().run_params[p] == '') or
                (p == 'rip_path' and self.manager.getInstance().run_params[p] == '') or
                (p == 'output_path' and self.manager.getInstance().run_params[p] == '')):
                self.runPageStatistics.setTextBackgroundColor(QColor(251,115,115))
            else:
                self.runPageStatistics.setTextBackgroundColor(QColor(255, 255, 255))

            self.runPageStatistics.append(p + ": " + str(self.manager.getInstance().run_params[p]) + "\n")

    def validate_forms(self):
        if(self.manager.checkNecessaryInput(self.manager)):
            self.runPageRunButton.setEnabled(True)
            self.runPageRunButton.setToolTip("Start execution")
        else:
            self.runPageRunButton.setEnabled(True)
            self.runPageRunButton.setToolTip("Please set the required input/output parameters!")

    @Slot()
    def runRime(self):
        self.runProgressWindow = RunProgressWidget(self.manager)
        self.runProgressWindow.show()
        # progress = QtWidgets.QProgressDialog("Updates","Some Words",0 , 100,self)
        # progress.setModal(True)
        # progress.show()
        # for i in range(1000):
        #     progress.setLabelText("number: " + str(i))
        #     time.sleep(.01)
        self.runProgressWindow.startRime()


    @Slot(str)
    def appendToStats(self, msg):
        self.runPageStatistics.append(msg)
