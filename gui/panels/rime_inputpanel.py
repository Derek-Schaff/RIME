from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog
from pathlib import Path

from gui.panels.rime_editmeta import MetaDataEditWidget
from gui.rime_variables import LABEL_WIDTH
from rime_manager import Manager





class InputPanelWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        '''----------'''
        '''INPUT PAGE'''
        '''----------'''

        '''---Left part - binary input selection---'''
        '''Components of binary selection group'''
        self.binaryFoldersLabel = QtWidgets.QLabel("Binary root directory location:")
        self.binaryFoldersLabel.setMinimumWidth(LABEL_WIDTH)
        self.binaryFoldersButton = QtWidgets.QPushButton("...")
        self.binaryFoldersButton.setObjectName("binaryFolderButton")
        self.binaryFoldersButton.setMinimumWidth(23)
        self.binaryFolders = QtWidgets.QLineEdit()
        self.binaryFolders.setObjectName("binaryFolders")

        '''Horizontal layout for binary selection group'''
        self.inputBinariesLayout = QtWidgets.QHBoxLayout()
        self.inputBinariesLayout.addWidget(self.binaryFoldersLabel)
        self.inputBinariesLayout.addWidget(self.binaryFolders)
        self.inputBinariesLayout.addWidget(self.binaryFoldersButton)
        '''Need to set the layout into a GroupBox so it can be added'''
        self.inputBinariesGroup = QtWidgets.QGroupBox()
        self.inputBinariesGroup.setLayout(self.inputBinariesLayout)

        '''---Left part - metadata input selection---'''
        '''Components of metadata selection group'''
        self.metaDataLabel = QtWidgets.QLabel("Metadata file location:")
        self.metaDataLabel.setMinimumWidth(LABEL_WIDTH)

        self.metaDataButton = QtWidgets.QPushButton("...")
        self.metaDataButton.setObjectName("metaDataButton")
        self.metaDataButton.setMaximumWidth(30)

        self.metaDataEditButton = QtWidgets.QPushButton("Edit")
        self.metaDataEditButton.setObjectName("metaDataEditButton")
        self.metaDataEditButton.setMaximumWidth(30)
        self.metaDataEditButton.setEnabled(False)

        self.metaData = QtWidgets.QLineEdit()
        self.metaData.setObjectName("metaData")

        '''Grid layout for metadata selection group'''
        self.metaDataLayout = QtWidgets.QGridLayout()
        self.metaDataLayout.addWidget(self.metaDataLabel, 0, 0)
        self.metaDataLayout.addWidget(self.metaData, 0, 1)
        self.metaDataLayout.addWidget(self.metaDataButton, 0, 2)
        self.metaDataLayout.addWidget(self.metaDataEditButton, 1, 2)
        '''Need to set the layout into a GroupBox so it can be added'''
        self.metaDataGroup = QtWidgets.QGroupBox()
        self.metaDataGroup.setLayout(self.metaDataLayout)

        '''---Left part - rip input selection---'''
        '''Components of rip selection group'''
        self.ripLabel = QtWidgets.QLabel("RIP file location:")
        self.ripLabel.setMinimumWidth(LABEL_WIDTH)
        self.ripButton = QtWidgets.QPushButton("...")
        self.ripButton.setObjectName("ripButton")
        self.ripButton.setMaximumWidth(30)

        self.ripEditButton = QtWidgets.QPushButton("Edit")
        self.ripEditButton.setObjectName("ripEditButton")
        self.ripEditButton.setMaximumWidth(30)
        self.ripEditButton.setEnabled(False)

        self.ripPathTextBox = QtWidgets.QLineEdit()
        self.ripPathTextBox.setObjectName("rip")

        '''Grid layout for rip selection group'''
        self.ripLayout = QtWidgets.QGridLayout()
        self.ripLayout.addWidget(self.ripLabel, 0, 0)
        self.ripLayout.addWidget(self.ripPathTextBox, 0, 1)
        self.ripLayout.addWidget(self.ripButton, 0, 2)
        self.ripLayout.addWidget(self.ripEditButton, 1, 2)
        '''Need to set the layout into a GroupBox so it can be added'''
        self.ripGroup = QtWidgets.QGroupBox()
        self.ripGroup.setLayout(self.ripLayout)

        '''---Right part - input statistics---'''
        self.sideLayout = QtWidgets.QTextEdit("Statistics...")

        '''---Setup Grid layout of input page---'''
        self.inputPageGrid = QtWidgets.QGridLayout()
        self.inputPageGrid.setObjectName("inputPageLayout")
        self.inputPageGrid.addWidget(self.ripGroup, 0, 0)
        self.inputPageGrid.addWidget(self.metaDataGroup, 1, 0)
        self.inputPageGrid.addWidget(self.inputBinariesGroup, 2, 0)
        self.inputPageGrid.addWidget(self.sideLayout, 0, 1, 3, 1)

        self.setLayout(self.inputPageGrid)

        self.binaryFoldersButton.clicked.connect(self.chooseBinaryPath)
        self.metaDataButton.clicked.connect(self.chooseMetadataFile)
        self.metaDataEditButton.clicked.connect(self.editMetadata)
        self.metaData.textChanged.connect(self.metaDataTextChanged)
        self.ripPathTextBox.textChanged.connect(self.ripTextChanged)
        self.ripButton.clicked.connect(self.chooseripFile)
        self.ripEditButton.clicked.connect(self.editRipData)


    def chooseBinaryPath(self):
        file_path = QFileDialog.getExistingDirectory()
        self.binaryFolders.setText(file_path)
        Manager.getInstance().run_params['binary_path'] = file_path


    def chooseMetadataFile(self):
        file_path = QFileDialog.getOpenFileName()
        self.metaData.setText(file_path[0])
        Manager.getInstance().run_params['metadata_path'] = file_path[0]

    def chooseripFile(self):
        file_path = QFileDialog.getOpenFileName()
        self.ripPathTextBox.setText(file_path[0])
        Manager.getInstance().run_params['rip_path'] = file_path[0]

    def editMetadata(self):
        if Path(self.metaData.text()).is_file():
            self.editMetaWindow = MetaDataEditWidget(self.metaData.text(), "Edit Meta Data File", ",")
            self.editMetaWindow.show()
    '''
    self.ripPathTextBox actually works on the ripPathTextBox file input and edit button.
    We'll need to rework this to make sense at some point
    '''
    def editRipData(self):
        if Path(self.ripPathTextBox.text()).is_file():
            self.editMetaWindow = MetaDataEditWidget(self.ripPathTextBox.text(), "Edit Rip File", "=")
            self.editMetaWindow.show()

    def metaDataTextChanged(self):
        # print(self.metaData.text())
        if self.metaData.text() != "":
            self.metaDataEditButton.setEnabled(True)
        else:
            self.metaDataEditButton.setEnabled(False)

    def ripTextChanged(self):
        if self.ripPathTextBox.text() != "":
            self.ripEditButton.setEnabled(True)
        else:
            self.ripEditButton.setEnabled(False)


