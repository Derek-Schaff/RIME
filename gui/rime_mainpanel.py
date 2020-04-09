from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot

from gui.panels.rime_inputpanel import InputPanelWidget
from gui.panels.rime_outputpanel import OutputPanelWidget
from gui.panels.rime_runpanel import RunPanelWidget

import os
import sys
   
class MainPanelWidget(QtWidgets.QWidget):
    def __init__(self, main_window, manager):
        super(MainPanelWidget, self).__init__()
        self.mainWindow = main_window
        self.manager = manager

        ''' Create main container (QToolBox) for dropdown style panels'''
        self.panels = QtWidgets.QToolBox()
        self.panels.setObjectName("MainPanel")

        '''Create different 'pages' for dropdown panels'''
        self.inputPage = InputPanelWidget()
        self.inputPage.setObjectName("inputPage")

        self.outputPage = OutputPanelWidget(self.manager)
        self.outputPage.setObjectName("outputPage")

        self.runPage = RunPanelWidget(self.manager)
        self.runPage.setObjectName("runPage")

        self.panels.addItem(self.inputPage, "Input")
        self.panels.addItem(self.outputPage, "Output")
        self.panels.addItem(self.runPage, "Run")

        self.warningIcon = QtGui.QIcon()
        self.warningIcon.addPixmap(QtGui.QPixmap("gui/img/warning.png"), QtGui.QIcon.Normal)
        self.panels.setItemIcon(1, self.warningIcon)
        self.panels.setItemIcon(2, self.warningIcon)

        self.menuBar = QtWidgets.QMenuBar(self.mainWindow)  # requires parent
        self.menu = QtWidgets.QMenu(self)
        self.menu.setTitle("File")
        self.menuBar.addMenu(self.menu)
        self.menu.addAction("Load Preset")
        self.menu.addAction("Save Preset")
        self.menu.addAction("Quit")
        self.menu.triggered[QtWidgets.QAction].connect(self.MenuAction)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.panels)
        self.layout.setMenuBar(self.menuBar)
        self.setLayout(self.layout)

        self.panels.currentChanged.connect(self.panelChange)

        self.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Rime", None, -1))

        style_file = os.path.dirname(__file__) + "/styles/rime_styles.qss"
        with open(style_file, "r") as styles:
            self.setStyleSheet(styles.read())
        

    def MenuAction(self, q):
        print("Menu action: " + q.text() + "\n")

    def panelChange(self, panelID):
        if panelID == 2:
            self.runPage.update_statistics()
            self.runPage.validate_forms()
            self.manager.getInstance().connectOutput(self.runPage.appendToStats)