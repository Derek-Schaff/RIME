import os
from random import randrange

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QFileDialog, QTableWidgetItem
import re

class RunProgressWidget(QtWidgets.QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.resize(525, 300)
        self.setWindowTitle("Run Progress")
        self.runProgressBox = QtWidgets.QTextEdit()
        self.runProgressBox.setReadOnly(True)


        self.runProgressBar = QtWidgets.QProgressBar()
        self.runProgressBar.setObjectName("runProgress")
        self.runProgressBarSpacer = QtWidgets.QSpacerItem(5, 5)
        self.runProgressBarLayout = QtWidgets.QVBoxLayout(self)
        self.runProgressBarLayout.addWidget(self.runProgressBar)
        self.runProgressBarLayout.addSpacerItem(self.runProgressBarSpacer)
        self.runprogressBarLayoutGroup = QtWidgets.QGroupBox(self)
        self.runprogressBarLayoutGroup.setLayout(self.runProgressBarLayout)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setMaximumWidth(60)
        self.cancelButtonLayout = QtWidgets.QHBoxLayout(self)
        self.cancelButtonLayout.addWidget(self.cancelButton, 0, QtCore.Qt.AlignRight)
        self.cancelButtonLayoutGroup = QtWidgets.QGroupBox(self)
        self.cancelButtonLayoutGroup.setLayout(self.cancelButtonLayout)

        self.runProgressGrid = QtWidgets.QGridLayout()
        self.runProgressGrid.setObjectName("runProgressLayout")
        self.runProgressGrid.addWidget(self.runprogressBarLayoutGroup, 0, 0)
        self.runProgressGrid.addWidget(self.runProgressBox, 1, 0)
        self.runProgressGrid.addWidget(self.cancelButtonLayoutGroup, 2, 0)
        self.runProgressGrid.setVerticalSpacing(0)

        self.runProgressGrid.rowStretch(1)

        self.setLayout(self.runProgressGrid)

        self.runProgressBar.setValue(0)

        self.cancelButton.clicked.connect(self.cancelButtonClick)
        # metadataPath, ripPath, outputPath, ignoreWarnings, netcdf4, hdf5, geotiff, checksum, tarNet, tarHdf, tarGeo, tarAll
        # rime = self.manager.getInstance().rimeAccess

        '''
        print(Manager.getInstance().run_params['binary_path'])
        x = int(ripDic["FT_DATASET_ROWS"])
        y = int(ripDic["FT_DATASET_COLUMNS"])
        binList = rime.build_bin_list(Manager.getInstance().run_params['binary_path'])
        ripDic = rime.parse_rip(Manager.getInstance().run_params['rip_path'])
        bin = rime.resolution_reshape(rime.load_binary(binList[0], 'uint8'), x, y)
        metadataDic = rime.parse_metadata(Manager.getInstance().run_params['metadata_path'])
        for i in range(0,10):
          rime.convert_to_hdf5(bin, ripDic, metadataDic, Manager.getInstance().run_params['output_path'], "test_1")
        '''
        #self.manager.getInstance().connectOutput(self.updateProgressBox)
        # args = self.manager.run_params
        # rime.run_rime(args['metadata_path'], args['rip_path'], args['output_path'], args['output_stopwarnings'],
        #               args['output_netcdf4'], args['output_hdf5'], args['output_geotiff'], args['output_option_filehash'],
        #               False, False, False, args['output_compress'], args['binary_path'])

        #self.fakeProgressTimer = QtCore.QTimer(self)
        #self.fakeProgressTimer.setSingleShot(False)
        #self.fakeProgressTimer.timeout.connect(self.fakeProgressUpdate)
        #self.fakeProgressTimer.start(500)

        #self.runProgressBox.append(self.fake_progress_messages[randrange(0, len(self.fake_progress_messages) - 1)] + '\n')
    def fakeProgressUpdate(self):
        amount = randrange(5, 20)

        if amount + self.runProgressBar.value() > 100:
            amount = 100 - self.runProgressBar.value()

        self.runProgressBar.setValue(self.runProgressBar.value() + amount)
        #self.runProgressBox.append(self.fake_progress_messages[randrange(0, len(self.fake_progress_messages) - 1)] + '\n')

        if self.runProgressBar.value() < 100:
          self.fakeProgressTimer.start(2000)
        else:
          self.cancelButton.setText("Success!")
          self.fakeProgressTimer.stop()

    def cancelButtonClick(self):
      if(self.runProgressBar.value() < 100):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setText("Cancel Run")
        msgBox.setInformativeText("Are you sure you want to cancel the run?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)

        choice = msgBox.exec()

        if choice == QtWidgets.QMessageBox.Ok:
          self.fakeProgressTimer.stop()
          self.close()
      else:
        self.close()

    def updateProgressBox(self):
      #self.runProgressBox.append(message)
      message = str(self.process.readAllStandardOutput()).replace('\\n', '\n')
      
      if message != "b''":
        progressText = re.search(r"File Number: (\d*)\s*/\s*(\d*)", message)
        if progressText != None:
          self.runProgressBox.append("TESTTESTTEST" + progressText.group(1))
          self.updateProgBar(int(progressText.group(1)), int(progressText.group(2)))

        self.runProgressBox.append(message)

    def closeEvent(self, event):
        self.manager.getInstance().removeOutput(self.updateProgressBox)
        self.timer.stop()
        return super().closeEvent(event)

    def startRime(self):
        rime = self.manager.getInstance().rimeAccess
        manArgs = self.manager.getInstance().run_params

        self.process = QtCore.QProcess(self)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.updateProgressBox)
        args = " ".join([manArgs['metadata_path'],  manArgs['rip_path'],  manArgs['output_path']]) + " "

        if not manArgs['output_stopwarnings']:
          args += "--ignore_warnings "
        if manArgs['output_netcdf4']:
          args += "--netcdf4 "
        if manArgs['output_hdf5']:
          args += "--hdf5 "
        if manArgs['output_geotiff']:
          args += "--geotiff "
        if manArgs['output_option_filehash']:
          args += "--checksum "
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateProgressBox)
        self.timer.start()
        self.process.start('python3 rime_main.py ' + args)
                
        '''
        rime.run_rime(args['metadata_path'], args['rip_path'], args['output_path'], args['output_stopwarnings'],
                      args['output_netcdf4'], args['output_hdf5'], args['output_geotiff'],
                      args['output_option_filehash'],
                      False, False, False, args['output_compress'], args['binary_path'])'''
    def updateProgBar(self,completed,total):
        self.runProgressBar.setValue((completed/total) * 100.0)
