from PySide import QtGui, QtCore
import sys
from PySide.QtCore import QPointF

__author__ = 'aberg'


class PlayHead(QtGui.QWidget):
    sliderMoved = QtCore.Signal(object)
    sliderPressed = QtCore.Signal(object)
    sliderReleased = QtCore.Signal(object)

    def __init__(self):
        super(PlayHead, self).__init__()
        self.setMouseTracking(True)
        self.head_x = 0.0
        self._value = 0.0
        self.max = 100.0
        self.fps = 25
        self.setEnabled(False)
        self.head_label = ""

    def set_head_label(self, label):
        self.head_label = label
        self.update()

    def setMaximum(self, value):
        self.max = value

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = float(value)
        fraction = self._value / self.max
        self.head_x = float(self.width()) * fraction
        self.update()

    def getValue(self):
        return self.head_x

    def sizeHint(self):
        return QtCore.QSize(9999999.0, 125.0)

    def from_screen_to_value(self, widget_value):
        fraction = widget_value / float(self.width())
        local_value = fraction * self.max
        return local_value

    def from_value_to_screen(self, value):
        return value

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.head_x = self.mapFromGlobal(QtGui.QCursor.pos()).x()
            self._value = self.from_screen_to_value(self.head_x)
            self.sliderMoved.emit(None)
        self.update()
        QtGui.QWidget.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.head_x = self.mapFromGlobal(QtGui.QCursor.pos()).x()
            self._value = self.from_screen_to_value(self.head_x)
            self.sliderPressed.emit(None)
            self.sliderMoved.emit(None)
        self.update()
        QtGui.QWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.sliderReleased.emit(None)
        self.sliderMoved.emit(None)
        self.update()
        QtGui.QWidget.mouseReleaseEvent(self, event)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        # qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.drawRectangles(event, qp)
        qp.end()

    def drawRectangles(self, event, qp):
        color = QtGui.QColor(0, 0, 0)

        pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1,
                         QtCore.Qt.SolidLine)
        pen.setWidth(1)
        qp.setPen(pen)

        size = self.size()
        rect = self.rect()

        # qp.setBrush(QtGui.QColor(200, 0, 0))
        margin = 2.0
        qp.drawRect(rect.left() + margin, rect.top() + margin, rect.width() - margin * 2, rect.height() - margin * 2)

        pen.setWidth(1)
        qp.setPen(pen)
        mark_length = 10.0
        edge_margin = 0.0
        for px in range(rect.width()):
            if px % 5 == 0: # every ten pixel
                pen.setWidth(1)
                qp.setPen(pen)
                if px > margin + edge_margin and px < rect.width() - (margin + edge_margin):
                    if px % self.fps == 0:
                        pen.setWidth(2)
                        qp.setPen(pen)
                    qp.drawLine(px, margin * 2, px, mark_length)
                    qp.drawLine(px, rect.height() - margin * 2, px, rect.height() - mark_length + (margin * 1))


        # preview line
        pos = self.mapFromGlobal(QtGui.QCursor.pos())
        qp.drawLine(pos.x(), 0, pos.x(), rect.height())

        # main head line
        pen.setWidth(1)
        qp.setPen(pen)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.drawLine(QPointF(self.head_x, 0.0), QPointF(self.head_x, rect.height()))

        qp.setRenderHint(QtGui.QPainter.Antialiasing, False)
        fm = QtGui.QFontMetricsF(qp.font())
        rect = fm.boundingRect(self.head_label)
        qp.setBrush(QtGui.QColor(200, 210, 210))
        qp.drawRect(self.head_x - rect.center().x() - 3,
                    (rect.height() - rect.height() / 2) + 4,
                    rect.width() + 6,
                    rect.height() + 3)
        qp.drawText(self.head_x - rect.center().x(), self.height() / 2 + 5, self.head_label)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    head = PlayHead()
    head.resize(768, 100)
    head.show()

    sys.exit(app.exec_())