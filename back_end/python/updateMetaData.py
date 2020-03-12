import fileinput
import sys


class updateMetaData():

    def update(file, field, newVal):
        for line in fileinput.input(file, inplace=1):
            if line.startswith(field):
                sys.stdout.write(field + " = " + newVal + "\n")
            else:
                sys.stdout.write(line)

