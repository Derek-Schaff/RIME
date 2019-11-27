from PySide2 import QtWidgets

from gui.panels.rime_inputpanel import InputPanelWidget
from gui.panels.rime_outputpanel import OutputPanelWidget
from gui.panels.rime_runpanel import RunPanelWidget


class MainPanelWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mainWindow = main_window

        # self.text.setAlignment(QtCore.Qt.AlignCenter)

        ''' Create main container (QToolBox) for dropdown style panels'''
        self.panels = QtWidgets.QToolBox()
        self.panels.setObjectName("MainPanel")

        '''Create different 'pages' for dropdown panels'''
        self.inputPage = InputPanelWidget()
        self.inputPage.setObjectName("inputPage")

        self.outputPage = OutputPanelWidget()
        self.outputPage.setObjectName("outputPage")

        self.runPage = RunPanelWidget()
        self.runPage.setObjectName("runPage")

        self.panels.addItem(self.inputPage, "Input")
        self.panels.addItem(self.outputPage, "Output")
        self.panels.addItem(self.runPage, "Run")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.panels)
        self.setLayout(self.layout)

        self.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Rime", None, -1))

        style_file = "gui/styles/rime_styles.qss"
        with open(style_file, "r") as fh:
            self.setStyleSheet(fh.read())
        '''
        self.panels.setItemText(self.panels.indexOf(self.inputPage),
                                QtWidgets.QApplication.translate("MainWindow", "Input", None, -1))
        self.panels.setItemText(self.panels.indexOf(self.outputPage),
                                QtWidgets.QApplication.translate("MainWindow", "Output", None, -1))
        '''

