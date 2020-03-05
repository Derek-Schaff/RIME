from PySide2 import QtWidgets, QtGui
#from PySide2.QtWidgets import QAction
from PySide2 import QtCore
from queue import Queue

from gui.panels.rime_inputpanel import InputPanelWidget
from gui.panels.rime_outputpanel import OutputPanelWidget
from gui.panels.rime_runpanel import RunPanelWidget
import os
import sys
'''
# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal 
class MyReceiver(QtCore.QObject):
    mysignal = QtCore.Signal(str)

    def __init__(self,queue,*args,**kwargs):
        QtCore.QObject.__init__(self,*args,**kwargs)
        self.queue = queue

    @QtCore.Slot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)
'''
class WriteStreamThread(QtCore.QThread):
    queue_updated = QtCore.Signal(str)

    def __init__(self, queue):
        super(WriteStreamThread, self).__init__()
        self.stop = False
        self.queue = queue

    def set_stop(self):
        self.stop = True
        self.wait() # waits till finished signal has been emitted

    def run(self):
        while not self.stop:    # i guess this is blocking
            try:
                msg = self.queue.get(block=False)
            except:
                #msg = "No items in message queue, sleeping..."
                self.sleep(0.2)   # if commented out, app crashes
            
            if(msg != "\n"):
                self.queue_updated.emit(msg)
        self.finished.emit()
        
class MainPanelWidget(QtWidgets.QWidget):
    def __init__(self, main_window, queue):
        super(MainPanelWidget, self).__init__()
        self.mainWindow = main_window
        #self.thread = thread
        #self.queue = queue
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
        

        self.listener_thread = WriteStreamThread(queue)
        self.listener_thread.queue_updated.connect(self._log_to_qtextedit)
        self.listener_thread.start()

    @QtCore.Slot(str)
    def _log_to_qtextedit(self, msg):
        self.inputPage.sideLayout.insertPlainText(msg)

        '''
        my_receiver = MyReceiver(self.queue)
        my_receiver.mysignal.connect(self.append_text)
        my_receiver.moveToThread(self.thread)
        thread.started.connect(my_receiver.run)
        thread.start()
        '''

    def MenuAction(self, q):
        print("Menu action: " + q.text())

    def panelChange(self, panelID):
        if panelID == 2:
            self.runPage.update_statistics()
            self.runPage.validate_forms()

    def onUpdateText(self, text):
        print("WORK")
        #cursor = self.inputPage.sideLayout.textCursor()
        #cursor.movePosition(QtGui.QTextCursor.End)
        #cursor.insertText(text)
        #self.inputPage.sideLayout.setTextCursor(cursor)
        #self.process.ensureCursorVisible()