from PySide2 import QtCore
from queue import Queue

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
            msg = None
            try:
                msg = self.queue.get(block=False)
            except:
                self.sleep(0.2)   # if commented out, app crashes            
            if(msg):
                self.queue_updated.emit(msg)
        self.finished.emit()
   