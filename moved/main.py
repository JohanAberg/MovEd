#!/usr/bin/env python

import sys
from PySide import QtGui, QtCore
from moved.widgets.mainwindow import MainWindow


if __name__ == "__main__":


    app = QtGui.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.resize(768, 900)
    main_window.show()

    sys.exit(app.exec_())