import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"back_end/python/"))
from back_end.python import rime

from PySide2 import QtWidgets, QtCore

from gui.rime_mainpanel import MainPanelWidget
from queue import Queue

'''
# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)
'''
class WriteStream(object):
    """ Redirects sys.stdout to a thread-safe Queue

    Arguments:
        object {object} -- base class
    """
    def __init__(self, queue):
        self.queue = queue

    def write(self, msg):
        self.queue.put(msg)

    def flush(self):
        """ Passing to create non-blocking stream (?!)
            https://docs.python.org/3/library/io.html#io.IOBase.flush
        """
        pass

def run():
    # create Queue to be passed to WriteStream and WriteStreamListener
    queue = Queue()
    # redirect stdout to WriteStream()
    sys.stdout = WriteStream(queue)
    print("Redirected sys.stdout to WriteStream")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # Create Queue and redirect sys.stdout to this queue
    #queue = Queue()
    #sys.stdout = WriteStream(queue)
    
    # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
    #thread = QtCore.QThread()

    #widget = MainPanelWidget(MainWindow, thread, queue)
    widget = MainPanelWidget(MainWindow, queue)
    MainWindow.setCentralWidget(widget)
    MainWindow.setWindowTitle("Rime")
    MainWindow.resize(850, 375)
    MainWindow.show()
    
    #thread.exit()
    sys.exit(app.exec_())

    @QtCore.Slot(str)
    def onUpdateText(self, text):
        print(text)


if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "--gui":
            print("Starting GUI...")
            run()
            #break

    os.chdir(os.path.join(os.path.dirname(__file__),"back_end/python/"))
    rime.main()
        
