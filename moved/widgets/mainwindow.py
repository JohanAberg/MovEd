from PySide import QtGui, QtCore
from moved.widgets.ui.mainwindow import Ui_MainWindow
from moved.widgets.filebrowser import FileBrowser
from moved.widgets.preview import Preview

file_name = "/home/aberg/dvdrip-data/unnamed/vob/001/unnamed-004.vob"
file_name = '/home/aberg/Downloads/sample_iPod.m4v'
file_name = '/home/aberg/Downloads/sample_iTunes.mov'

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('MovEd')

        self.preview = Preview()
        # self.preview.set_movie_path(file_name)
        preview_dock = QtGui.QDockWidget()
        preview_dock.setWidget(self.preview)

        self.file_browser = FileBrowser()
        browser_dock = QtGui.QDockWidget()
        browser_dock.setWidget(self.file_browser)

        self.file_browser.doubleClicked.connect(self.onDoubleClick)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, preview_dock)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, browser_dock)

    def closeEvent(self, event):
        self.preview.close()
        self.preview = None
        del self.preview

    def onDoubleClick(self, index):
        if not self.file_browser.model.isDir(index):
            file_path = self.file_browser.model.filePath(index)
            self.preview.load_movie(file_path)
