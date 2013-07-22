from PySide import QtCore
from moved.base.mlt_interface import Mlt


class MltThread(QtCore.QThread):
    def __init__(self):
        super(MltThread, self).__init__()
        self.mlt = Mlt()

    def run(self):
        self.mlt.setup()