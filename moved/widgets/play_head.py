from PySide import QtGui, QtCore
import sys

__author__ = 'aberg'


class PlayHead(QtGui.QWidget):
	def __init__(self):
		super(PlayHead, self).__init__()
		self.setMouseTracking(True)
		self.head_x = 33
		self.fps = 25

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			self.head_x = self.mapFromGlobal(QtGui.QCursor.pos()).x()
		self.update()
		QtGui.QWidget.mouseMoveEvent(self, event)

	def mousePressEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			self.head_x = self.mapFromGlobal(QtGui.QCursor.pos()).x()
			self.update()
		QtGui.QWidget.mousePressEvent(self, event)

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawRectangles(event, qp)
		qp.end()

	def drawRectangles(self, event, qp):
		color = QtGui.QColor(0, 0, 0)

		pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1,
						 QtCore.Qt.SolidLine)
		pen.setWidth(2)
		qp.setPen(pen)

		size = self.size()
		rect = self.rect()

		# qp.setBrush(QtGui.QColor(200, 0, 0))
		margin = 4
		qp.drawRect(rect.left() + margin, rect.top() + margin, rect.width() - margin * 2, rect.height() - margin * 2)

		pen.setWidth(1)
		qp.setPen(pen)
		mark_length = 10
		edge_margin = 4
		for px in range(rect.width()):
			if px % 5 == 0: # every ten pixel
				pen.setWidth(1)
				qp.setPen(pen)
				if px > margin + edge_margin and px < rect.width() - (margin + edge_margin):
					if px % self.fps == 0:
						pen.setWidth(2)
						qp.setPen(pen)
					qp.drawLine(px, margin, px, mark_length)
					qp.drawLine(px, rect.height() - margin, px, rect.height() - mark_length - margin)

		pos = self.mapFromGlobal(QtGui.QCursor.pos())
		qp.drawLine(pos.x(), 0, pos.x(), rect.height())

		pen.setWidth(2)
		qp.setPen(pen)
		qp.drawLine(self.head_x, 0, self.head_x, rect.height())


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	head = PlayHead()
	head.resize(768, 100)
	head.show()

	sys.exit(app.exec_())