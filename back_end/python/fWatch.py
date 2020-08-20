import os
import sys
import time
from gui.panels.rime_runprogress import RunProgressWidget


class Watcher(object):
    running = True
    #refresh_delay_secs = 1

    # Constructor
    def __init__(self, watch_file):
        self._cached_stamp = 0
        self.filename = watch_file

    # Look for changes
    def look(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            with open(self.filename) as myfile:
                message = list(myfile)[-1]
            # put gui status updater here with argument (message)
            #if theres a better python way to get the last line plz fix
            RunProgressWidget.updateProgressBox(message)

    # Keep watching in a loop
    def watch(self):
        while self.running:
            try:
                # Look for changes
                #time.sleep(self.refresh_delay_secs)
                self.look()
            # except KeyboardInterrupt:
            #     print('\nDone')
            #     break
            except FileNotFoundError:
                # Action on file not found
                pass
            except:
                print('Unhandled error: %s' % sys.exc_info()[0])

# watch_file = '/home/turkishdisko/CLionProjects/RIME/back_end/c/t.txt'
# watcher = Watcher(watch_file)  # simple
# watcher.watch()  # start the watch going