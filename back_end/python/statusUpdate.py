from ctypes import *
import os
import time
from gui.panels.rime_runprogress import RunProgressWidget


def update_status(progress_window,updateMessage, logPath):
    if (updateMessage == None):
        print("No message passed")
        return

    message = time.strftime("%x - %I:%M:%S %p: ", time.localtime()) + updateMessage
    # print status to command line
    print(message)

    # append to log
    logFile = open(logPath, "a+")
    logFile.write(message + "\n")
    logFile.close()

    # push to GUI)
    progress_window.updateProgressBox(message)

    # status_update = CDLL(os.path.dirname(__file__) + "/../c/status_updater.so")
    # status_update.statusUpdate.argtypes = [c_char_p, c_char_p]
    # b_logPath = logPath.encode('utf-8')
    # b_updateMessage = updateMessage.encode('utf-8')
    # status_update.statusUpdate(b_updateMessage, b_logPath)
    # return

# if __name__ == "__main__":
