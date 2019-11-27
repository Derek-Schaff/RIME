from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QFileDialog

from gui.rime_editmeta import MetaDataEditWidget
from gui.rime_variables import LABEL_WIDTH

import PySide2.QtPositioning

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

        self.outputLogFileButtonGroup.buttonClicked.connect(self.logFileChange)

        self.outputLogfileBox.setEnabled(False)
        self.outputLogfileBoxButton.setEnabled(False)

    def logFileChange(self):
        if self.outputLogFileButtonGroup.checkedId() == 2:
            self.outputLogfileBox.setEnabled(True)
            self.outputLogfileBoxButton.setEnabled(True)
        else:
            self.outputLogfileBox.setEnabled(False)
            self.outputLogfileBoxButton.setEnabled(False)

