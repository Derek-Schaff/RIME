import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QFileDialog

from rime_editmeta import MetaDataEditWidget

LABEL_WIDTH = 120


class MainPanelWidget(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow

        #self.text.setAlignment(QtCore.Qt.AlignCenter)

        ''' Create main container (QToolBox) for dropdown style panels'''
        self.panels = QtWidgets.QToolBox()
        self.panels.setObjectName("mainPanel")

        '''Create different 'pages' for dropdown panels'''
        self.inputPage = QtWidgets.QWidget()
        self.inputPage.setObjectName("inputPage")

        self.outputPage = QtWidgets.QWidget()
        self.outputPage.setObjectName("outputPage")

        '''----------'''
        '''INPUT PAGE'''
        '''----------'''

        '''---Left part - binary input selection---'''
        '''Components of binary selection group'''
        self.binaryFoldersLabel = QtWidgets.QLabel("Binaries location:")
        self.binaryFoldersLabel.setMinimumWidth(LABEL_WIDTH)
        self.binaryFoldersButton = QtWidgets.QPushButton("...")
        self.binaryFoldersButton.setObjectName("binaryFoldersButton")
        self.binaryFoldersButton.setMaximumWidth(30)
        self.binaryFolders = QtWidgets.QLineEdit()
        self.binaryFolders.setObjectName("binaryFolders")

        '''Horizontal layout for binary selection group'''
        self.inputBinariesLayout = QtWidgets.QHBoxLayout()
        self.inputBinariesLayout.addWidget(self.binaryFoldersLabel)
        self.inputBinariesLayout.addWidget(self.binaryFolders)
        self.inputBinariesLayout.addWidget(self.binaryFoldersButton)
        '''Need to set the layout into a GroupBox so it can be added'''
        inputBinariesGroup = QtWidgets.QGroupBox()
        inputBinariesGroup.setLayout(self.inputBinariesLayout)

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
        metaDataGroup = QtWidgets.QGroupBox()
        metaDataGroup.setLayout(self.metaDataLayout)

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
        catalogGroup = QtWidgets.QGroupBox()
        catalogGroup.setLayout(self.catalogLayout)

        '''---Right part - input statistics---'''
        self.sideLayout = QtWidgets.QTextEdit("Statistics...")

        '''---Setup Grid layout of input page---'''
        self.inputPageGrid = QtWidgets.QGridLayout(self.inputPage)
        self.inputPageGrid.setObjectName("inputPageLayout")
        self.inputPageGrid.addWidget(inputBinariesGroup, 0, 0)
        self.inputPageGrid.addWidget(metaDataGroup, 1, 0)
        self.inputPageGrid.addWidget(catalogGroup, 2, 0)
        self.inputPageGrid.addWidget(self.sideLayout, 0, 1, 3, 1)

#        self.inputPageGrid.addWidget(self.pushButton, 0, 1)
        self.outputLocationLabel = QtWidgets.QLabel("Output location:")
        self.outputLocationLabel.setMinimumWidth(LABEL_WIDTH)

        self.outputLocationBox = QtWidgets.QLineEdit()
        self.outputLocationBox.setObjectName("outputLocationBox")
        self.outputLocationButton = QtWidgets.QPushButton("...")
        self.outputLocationButton.setObjectName("outputLocationButton")
        self.outputLocationButton.setMaximumWidth(30)

        self.outputLocationBoxLayout = QtWidgets.QHBoxLayout()
        self.outputLocationBoxLayout.addWidget(self.outputLocationBox)
        self.outputLocationBoxLayout.addWidget(self.outputLocationButton)
        outputLocationBoxLayoutGroup = QtWidgets.QGroupBox()
        outputLocationBoxLayoutGroup.setLayout(self.outputLocationBoxLayout)

        self.outputLocationLayout = QtWidgets.QVBoxLayout()
        self.outputLocationLayout.addWidget(self.outputLocationLabel)
        self.outputLocationLayout.addWidget(outputLocationBoxLayoutGroup)
        outputLocationGroup = QtWidgets.QGroupBox()
        outputLocationGroup.setLayout(self.outputLocationLayout)

        self.outputPageOptionCheckSHA = QtWidgets.QCheckBox("Generate SHA256 Checksum")
        self.outputPageOptionCheckSHA.setObjectName("outputPageOptionCheckSHA")

        self.outputPageOptionCompress = QtWidgets.QCheckBox("Compress output")
        self.outputPageOptionCompress.setObjectName("outputPageOptionCompress")

        self.outputPageOptionStop = QtWidgets.QCheckBox("Stop on warnings")
        self.outputPageOptionStop.setObjectName("outputPageOptionStop")

        '''---Setup basic Box layout of output page---'''
        self.outputOptionsLayout = QtWidgets.QVBoxLayout()
        self.outputOptionsLayout.addWidget(self.outputPageOptionCheckSHA)
        self.outputOptionsLayout.addWidget(self.outputPageOptionCompress)
        self.outputOptionsLayout.addWidget(self.outputPageOptionStop)
        outputOptionsGroup = QtWidgets.QGroupBox()
        outputOptionsGroup.setLayout(self.outputOptionsLayout)

        self.outputPageOutputNetCDF = QtWidgets.QCheckBox("NetCDF4")
        self.outputPageOutputNetCDF.setObjectName("outputPageOutputNetCDF")

        self.outputPageOutputHDF5 = QtWidgets.QCheckBox("HDF5")
        self.outputPageOutputHDF5.setObjectName("outputPageOutputHDF5")

        self.outputPageOutputGeoTIFF = QtWidgets.QCheckBox("GeoTIFF")
        self.outputPageOutputGeoTIFF.setObjectName("outputPageOutputGeoTIFF")



        self.outputOutputLayout = QtWidgets.QVBoxLayout()
        self.outputOutputLayout.addWidget(self.outputPageOutputNetCDF)
        self.outputOutputLayout.addWidget(self.outputPageOutputHDF5)
        self.outputOutputLayout.addWidget(self.outputPageOutputGeoTIFF)
        outputOutputGroup = QtWidgets.QGroupBox()
        outputOutputGroup.setLayout(self.outputOutputLayout)

        self.outputPageGrid = QtWidgets.QGridLayout(self.outputPage)
        self.outputPageGrid.setObjectName("outputPageLayout")
        self.outputPageGrid.addWidget(outputLocationGroup, 0, 0, 1, 2)
        self.outputPageGrid.addWidget(outputOptionsGroup, 1, 0)
        self.outputPageGrid.addWidget(outputOutputGroup, 1, 1)

        self.panels.addItem(self.inputPage, "")
        self.panels.addItem(self.outputPage, "")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.panels)
        self.setLayout(self.layout)

        self.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Rime", None, -1))

        self.panels.setItemText(self.panels.indexOf(self.inputPage), QtWidgets.QApplication.translate("MainWindow", "Input", None, -1))
        self.panels.setItemText(self.panels.indexOf(self.outputPage), QtWidgets.QApplication.translate("MainWindow", "Output", None, -1))

        self.binaryFoldersButton.clicked.connect(self.chooseBinaryPath)
        self.metaDataButton.clicked.connect(self.chooseMetadataFile)
        self.metaDataEditButton.clicked.connect(self.editMetadata)
        self.metaData.textChanged.connect(self.metaDataTextChanged)
        self.catalog.textChanged.connect(self.catalogTextChanged)
        self.catalogButton.clicked.connect(self.chooseCatalogFile)

    def chooseBinaryPath(self):
        filePath=QFileDialog.getExistingDirectory()
        self.binaryFolders.setText(filePath)

    def chooseMetadataFile(self):
        filePath=QFileDialog.getOpenFileName()
        self.metaData.setText(filePath[0])

    def chooseCatalogFile(self):
        filePath=QFileDialog.getOpenFileName()
        self.catalog.setText(filePath[0])

    def editMetadata(self):
        self.editMetaWindow = MetaDataEditWidget(self.MainWindow)
        self.editMetaWindow.show()

    def metaDataTextChanged(self):
        #print(self.metaData.text())
        if self.metaData.text() != "":
            self.metaDataEditButton.setEnabled(True)
        else:
            self.metaDataEditButton.setEnabled(False)

    def catalogTextChanged(self):
        if self.catalog.text() != "":
            self.catalogEditButton.setEnabled(True)
        else:
            self.catalogEditButton.setEnabled(False)

'''
   label = new QLabel("foo");
    button = new QPushButton("Browse");
    connect(button, SIGNAL(clicked()), SLOT(browse()));
    layout = new QHorizontalLayout();
    layout->addWidget(label);
    layout->addWidget(button);
    setLayout(layout);
void MyMainWindow::browse()
{
    QString directory = QFileDialog::getExistingDirectory(this,
                            tr("Find Files"), QDir::currentPath());

    if (!directory.isEmpty()) {
        if (directoryComboBox->findText(directory) == -1)
            directoryComboBox->addItem(directory);
        directoryComboBox->setCurrentIndex(directoryComboBox->findText(directory));
    }
}'''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    widget = MainPanelWidget(MainWindow)
    widget.resize(850, 400)
    widget.show()

    sys.exit(app.exec_())
