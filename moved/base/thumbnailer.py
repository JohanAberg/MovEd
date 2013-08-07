from PySide import QtCore

__author__ = 'aberg'

class Thumber(QtCore.QThread):
    def __init__(self):
        super(Thumber, self).__init__()


    def run(self):
        print 'go! thumber'
