from PySide import QtCore
from moved.base.mlt_backend import Mlt


class MltThread(QtCore.QThread):
	def __init__(self):
		super(MltThread, self).__init__()
		self.mlt = Mlt()
		self.mlt.setup()

	def run(self):
		self.mlt.start_player()
