from ctypes import *
import os


def update_status(updateMessage,logPath):
    status_update = CDLL(os.path.dirname(__file__) + "/../c/status_updater.so")
    status_update.statusUpdate.argtypes = [c_char_p, c_char_p]
    b_logPath = logPath.encode('utf-8')
    b_updateMessage = updateMessage.encode('utf-8')

    status_update.statusUpdate(b_updateMessage, b_logPath)

    return


# if __name__ == "__main__":
#     update_status("Yo", "../upTest.txt")
