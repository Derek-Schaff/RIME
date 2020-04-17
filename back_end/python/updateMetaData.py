import fileinput
import sys


class updateMetaData():

    def update(file, field, newVal, delim):
        for line in fileinput.input(file, inplace=1):
            if line.startswith(field):
                if delim == '=':
                    delim = "= "
                sys.stdout.write(field + delim + newVal + "\n")
            else:
                sys.stdout.write(line)

