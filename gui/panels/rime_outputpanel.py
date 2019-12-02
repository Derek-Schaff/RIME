from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QFileDialog

from rime_manager import Manager


class OutputPanelWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        '''----------'''
        '''INPUT PAGE'''
        '''----------'''

        self.outputLocationBox = QtWidgets.QLineEdit()
        self.outputLocationBox.setObjectName("outputLocationBox")
        self.outputLocationButton = QtWidgets.QPushButton("...")
        self.outputLocationButton.setObjectName("outputLocationButton")
        self.outputLocationButton.setMaximumWidth(30)
        self.outputLocationLabel = QtWidgets.QLabel("Output location:")
        self.outputLocationLabel.setMinimumWidth(350)

        self.outputLocationBoxLayout = QtWidgets.QHBoxLayout()
        self.outputLocationBoxLayout.addWidget(self.outputLocationBox)
        self.outputLocationBoxLayout.addWidget(self.outputLocationButton)
        self.outputLocationBoxLayoutGroup = QtWidgets.QGroupBox()
        self.outputLocationBoxLayoutGroup.setLayout(self.outputLocationBoxLayout)

        self.outputLocationLayout = QtWidgets.QVBoxLayout()
        self.outputLocationLayout.addWidget(self.outputLocationLabel)
        self.outputLocationLayout.addWidget(self.outputLocationBoxLayoutGroup)
        self.outputLocationGroup = QtWidgets.QGroupBox()
        #self.outputLocationGroup.setAlignment()
        self.outputLocationGroup.setLayout(self.outputLocationLayout)

        self.outputPageOptionLabel = QtWidgets.QLabel("Output options:")
        self.outputPageOptionSpacer = QtWidgets.QSpacerItem(5, 30, QtWidgets.QSizePolicy.Expanding)

        self.outputPageOptionCheckSHA = QtWidgets.QCheckBox("Generate SHA256 Checksum")
        self.outputPageOptionCheckSHA.setObjectName("outputPageOptionCheckSHA")

        self.outputPageOptionCompress = QtWidgets.QCheckBox("Compress output")
        self.outputPageOptionCompress.setObjectName("outputPageOptionCompress")

        self.outputPageOptionStop = QtWidgets.QCheckBox("Stop on warnings")
        self.outputPageOptionStop.setObjectName("outputPageOptionStop")

        '''---Setup basic Box layout of output page---'''
        self.outputOptionsLayout = QtWidgets.QVBoxLayout()
        self.outputOptionsLayout.addWidget(self.outputPageOptionLabel)
        self.outputOptionsLayout.addSpacerItem(self.outputPageOptionSpacer)
        self.outputOptionsLayout.addWidget(self.outputPageOptionCheckSHA)
        self.outputOptionsLayout.addWidget(self.outputPageOptionCompress)
        self.outputOptionsLayout.addWidget(self.outputPageOptionStop)
        self.outputOptionsLayout.setAlignment(QtCore.Qt.AlignTop)
        self.outputOptionsGroup = QtWidgets.QGroupBox()
        self.outputOptionsGroup.setLayout(self.outputOptionsLayout)

        self.outputPageOutputLabel = QtWidgets.QLabel("Output formats:")
        self.outputPageOutputSpacer = QtWidgets.QSpacerItem(5, 30, QtWidgets.QSizePolicy.Expanding)

        self.outputPageOutputNetCDF = QtWidgets.QCheckBox("NetCDF4")
        self.outputPageOutputNetCDF.setObjectName("outputPageOutputNetCDF")

        self.outputPageOutputHDF5 = QtWidgets.QCheckBox("HDF5")
        self.outputPageOutputHDF5.setObjectName("outputPageOutputHDF5")

        self.outputPageOutputGeoTIFF = QtWidgets.QCheckBox("GeoTIFF")
        self.outputPageOutputGeoTIFF.setObjectName("outputPageOutputGeoTIFF")

        self.outputOutputLayout = QtWidgets.QVBoxLayout()
        self.outputOutputLayout.addWidget(self.outputPageOutputLabel)
        self.outputOutputLayout.addSpacerItem(self.outputPageOptionSpacer)
        self.outputOutputLayout.addWidget(self.outputPageOutputNetCDF)
        self.outputOutputLayout.addWidget(self.outputPageOutputHDF5)
        self.outputOutputLayout.addWidget(self.outputPageOutputGeoTIFF)
        self.outputOutputLayout.setAlignment(QtCore.Qt.AlignTop)
        self.outputOutputGroup = QtWidgets.QGroupBox()
        self.outputOutputGroup.setLayout(self.outputOutputLayout)

        self.outputLogGroupLabel = QtWidgets.QLabel("Log File Options:")

        # radiobuttons
        self.outputLogFileOptionDefault = QtWidgets.QRadioButton('Default location')
        self.outputLogFileOptionCustom = QtWidgets.QRadioButton('Custom location')
        self.outputLogFileOptionDefault.setChecked(True)  # default option

        # button group
        self.outputLogFileButtonGroup = QtWidgets.QButtonGroup(self)
        self.outputLogFileButtonGroup.addButton(self.outputLogFileOptionDefault, 1)
        self.outputLogFileButtonGroup.addButton(self.outputLogFileOptionCustom, 2)

        self.outputLogfileBox = QtWidgets.QLineEdit()
        self.outputLogfileBox.setObjectName("outputLocationBox")
        self.outputLogfileBoxButton = QtWidgets.QPushButton("...")
        self.outputLogfileBoxButton.setObjectName("outputLocationButton")
        self.outputLogfileBoxButton.setMaximumWidth(30)

        self.outputLogfileBoxLayout = QtWidgets.QHBoxLayout()
        self.outputLogfileBoxLayout.addWidget(self.outputLogfileBox)
        self.outputLogfileBoxLayout.addWidget(self.outputLogfileBoxButton)
        self.outputLogfileBoxLayoutGroup = QtWidgets.QGroupBox()
        self.outputLogfileBoxLayoutGroup.setLayout(self.outputLogfileBoxLayout)

        self.outputLogGroupLayout = QtWidgets.QVBoxLayout()
        self.outputLogGroupLayout.addWidget(self.outputLogGroupLabel)
        self.outputLogGroupLayout.addWidget(self.outputLogFileOptionDefault)
        self.outputLogGroupLayout.addWidget(self.outputLogFileOptionCustom)
        self.outputLogGroupLayout.addWidget(self.outputLogfileBoxLayoutGroup)
        self.outputLogGroup = QtWidgets.QGroupBox()
        self.outputLogGroup.setLayout(self.outputLogGroupLayout)

        self.outputStatistics = QtWidgets.QTextEdit("Output statistics...")

        self.outputPageGrid = QtWidgets.QGridLayout()
        self.outputPageGrid.setObjectName("outputPageLayout")
        self.outputPageGrid.addWidget(self.outputLocationGroup, 0, 0, 1, 4)
        self.outputPageGrid.addWidget(self.outputOptionsGroup, 1, 0, 4, 2)
        self.outputPageGrid.addWidget(self.outputOutputGroup, 1, 2, 4, 2)
        self.outputPageGrid.addWidget(self.outputLogGroup, 0, 4, 2, 5)
        self.outputPageGrid.addWidget(self.outputStatistics, 2, 4, 3, 5)

        self.setLayout(self.outputPageGrid)

        self.outputLocationButton.clicked.connect(self.chooseOutputPath)
        self.outputLogFileButtonGroup.buttonClicked.connect(self.logFileChange)
        self.outputLogfileBoxButton.clicked.connect(self.chooseLogLocation)

        self.outputPageOutputHDF5.stateChanged.connect(self.outputGroupClick)
        self.outputPageOutputNetCDF.stateChanged.connect(self.outputGroupClick)
        self.outputPageOutputGeoTIFF.stateChanged.connect(self.outputGroupClick)

        self.outputPageOptionCheckSHA.stateChanged.connect(self.optionGroupClick)
        self.outputPageOptionStop.stateChanged.connect(self.optionGroupClick)
        self.outputPageOptionCompress.stateChanged.connect(self.optionGroupClick)

        self.outputLogfileBox.setEnabled(False)
        self.outputLogfileBoxButton.setEnabled(False)

    def chooseLogLocation(self):
        if self.outputLogFileButtonGroup.checkedId() == 2:
            file_path = QFileDialog.getExistingDirectory()
            self.outputLogfileBox.setText(file_path)
            Manager.getInstance().run_params['log_path'] = file_path

    def chooseOutputPath(self):
        file_path = QFileDialog.getExistingDirectory()
        self.outputLocationBox.setText(file_path)
        Manager.getInstance().run_params['output_path'] = file_path

    def outputGroupClick(self, box):
        boxChecked = self.sender().text()

        if boxChecked == "HDF5":
            Manager.getInstance().run_params['output_hdf5'] = self.outputPageOutputHDF5.isChecked()
        elif boxChecked == "NetCDF4":
            Manager.getInstance().run_params['output_netcdf4'] = self.outputPageOutputNetCDF.isChecked()
        elif boxChecked == "GeoTIFF":
            Manager.getInstance().run_params['output_geotiff'] = self.outputPageOutputGeoTIFF.isChecked()

    def optionGroupClick(self, box):
        boxChecked = self.sender().text()

        if boxChecked == "Generate SHA256 Checksum":
            Manager.getInstance().run_params['output_option_filehash'] = self.outputPageOptionCheckSHA.isChecked()
        elif boxChecked == "Compress output":
            Manager.getInstance().run_params['output_option_compress'] = self.outputPageOptionCompress.isChecked()
        elif boxChecked == "Stop on warnings":
            Manager.getInstance().run_params['output_option_stopwarn'] = self.outputPageOptionStop.isChecked()

    def logFileChange(self):
        if self.outputLogFileButtonGroup.checkedId() == 2:
            self.outputLogfileBox.setEnabled(True)
            self.outputLogfileBoxButton.setEnabled(True)
        else:
            self.outputLogfileBox.setEnabled(False)
            self.outputLogfileBoxButton.setEnabled(False)
            Manager.getInstance().run_params['log_path'] = "DEFAULT"

