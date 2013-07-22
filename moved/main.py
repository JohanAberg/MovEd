import os
from moved.widgets.preview import Preview

__author__ = 'aberg'

if __name__ == "__main__":

	import sys
	from PySide import QtGui, QtCore

	app = QtGui.QApplication(sys.argv)
	preview = Preview()

	preview.resize(768, 576)
	preview.setWindowTitle('Preview')
	preview.show()

	sys.exit(app.exec_())