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
        self.binaryFoldersLabel = QtWidgets.QLabel("Binaries location:")
        self.binaryFoldersLabel.setMinimumWidth(LABEL_WIDTH)
        self.binaryFoldersButton = QtWidgets.QPushButton("...")
        self.binaryFoldersButton.setObjectName("binaryFoldersButton")
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

        '''---Left part - catalog input selection---'''
        '''Components of catalog selection group'''
        self.catalogLabel = QtWidgets.QLabel("Catalog file location:")
        self.catalogLabel.setMinimumWidth(LABEL_WIDTH)
        self.catalogButton = QtWidgets.QPushButton("...")
        self.catalogButton.setObjectName("CatalogButton")
        self.catalogButton.setMaximumWidth(30)

        self.catalogEditButton = QtWidgets.QPushButton("Edit")
        self.catalogEditButton.setObjectName("catalogEditButton")
        self.catalogEditButton.setMaximumWidth(30)
        self.catalogEditButton.setEnabled(False)

        self.catalog = QtWidgets.QLineEdit()
        self.catalog.setObjectName("Catalog")

        '''Grid layout for catalog selection group'''
        self.catalogLayout = QtWidgets.QGridLayout()
        self.catalogLayout.addWidget(self.catalogLabel, 0, 0)
        self.catalogLayout.addWidget(self.catalog, 0, 1)
        self.catalogLayout.addWidget(self.catalogButton, 0, 2)
        self.catalogLayout.addWidget(self.catalogEditButton, 1, 2)
        '''Need to set the layout into a GroupBox so it can be added'''
        self.catalogGroup = QtWidgets.QGroupBox()
        self.catalogGroup.setLayout(self.catalogLayout)

        '''---Right part - input statistics---'''
        self.sideLayout = QtWidgets.QTextEdit("Statistics...")

        '''---Setup Grid layout of input page---'''
        self.inputPageGrid = QtWidgets.QGridLayout()
        self.inputPageGrid.setObjectName("inputPageLayout")
        self.inputPageGrid.addWidget(self.inputBinariesGroup, 0, 0)
        self.inputPageGrid.addWidget(self.metaDataGroup, 1, 0)
        self.inputPageGrid.addWidget(self.catalogGroup, 2, 0)
        self.inputPageGrid.addWidget(self.sideLayout, 0, 1, 3, 1)

        self.setLayout(self.inputPageGrid)

        self.binaryFoldersButton.clicked.connect(self.chooseBinaryPath)
        self.metaDataButton.clicked.connect(self.chooseMetadataFile)
        self.metaDataEditButton.clicked.connect(self.editMetadata)
        self.metaData.textChanged.connect(self.metaDataTextChanged)
        self.catalog.textChanged.connect(self.catalogTextChanged)
        self.catalogButton.clicked.connect(self.chooseCatalogFile)


    def chooseBinaryPath(self):
        file_path = QFileDialog.getOpenFileName()
        self.binaryFolders.setText(file_path[0])
        Manager.getInstance().run_params['binary_path'] = file_path[0]


    def chooseMetadataFile(self):
        file_path = QFileDialog.getOpenFileName()
        self.metaData.setText(file_path[0])
        Manager.getInstance().run_params['metadata_path'] = file_path[0]

    def chooseCatalogFile(self):
        file_path = QFileDialog.getOpenFileName()
        self.catalog.setText(file_path[0])
        Manager.getInstance().run_params['catalog_path'] = file_path[0]

    def editMetadata(self):
        if Path(self.metaData.text()).is_file():
            self.editMetaWindow = MetaDataEditWidget(self.metaData.text())
            self.editMetaWindow.show()

    def metaDataTextChanged(self):
        # print(self.metaData.text())
        if self.metaData.text() != "":
            self.metaDataEditButton.setEnabled(True)
        else:
            self.metaDataEditButton.setEnabled(False)

    def catalogTextChanged(self):
        if self.catalog.text() != "":
            self.catalogEditButton.setEnabled(True)
        else:
            self.catalogEditButton.setEnabled(False)


