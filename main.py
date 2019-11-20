# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Wed Nov 20 15:09:00 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 401, 262))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtWidgets.QToolBox(self.verticalLayoutWidget)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 399, 152))
        self.page.setObjectName("page")
        self.frame = QtWidgets.QFrame(self.page)
        self.frame.setGeometry(QtCore.QRect(-1, 0, 401, 151))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.spinBox = QtWidgets.QSpinBox(self.frame)
        self.spinBox.setGeometry(QtCore.QRect(140, 60, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(30, 30, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.toolBox.addItem(self.page, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.toolBox.addItem(self.page_5, "")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.toolBox.addItem(self.page_6, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 399, 152))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")
        self.verticalLayout.addWidget(self.toolBox)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuRIME = QtWidgets.QMenu(self.menuBar)
        self.menuRIME.setObjectName("menuRIME")
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionLoad_Preset = QtWidgets.QAction(MainWindow)
        self.actionLoad_Preset.setObjectName("actionLoad_Preset")
        self.actionSave_Preset = QtWidgets.QAction(MainWindow)
        self.actionSave_Preset.setObjectName("actionSave_Preset")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuRIME.addAction(self.actionLoad_Preset)
        self.menuRIME.addAction(self.actionSave_Preset)
        self.menuRIME.addAction(self.actionExit)
        self.menuBar.addAction(self.menuRIME.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtWidgets.QApplication.translate("MainWindow", "Input", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), QtWidgets.QApplication.translate("MainWindow", "Output", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_6), QtWidgets.QApplication.translate("MainWindow", "Run", None, -1))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtWidgets.QApplication.translate("MainWindow", "Page 2", None, -1))
        self.menuRIME.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuAbout.setTitle(QtWidgets.QApplication.translate("MainWindow", "About", None, -1))
        self.actionLoad_Preset.setText(QtWidgets.QApplication.translate("MainWindow", "Load Preset", None, -1))
        self.actionSave_Preset.setText(QtWidgets.QApplication.translate("MainWindow", "Save Preset", None, -1))
        self.actionExit.setText(QtWidgets.QApplication.translate("MainWindow", "Exit", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

