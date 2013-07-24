from PySide import QtGui
import sys

__author__ = 'aberg'

class FileBrowser(QtGui.QTreeView):
    def __init__(self):

        # root_path = '/home/aberg/dvdrip-data/film1/avi/'
        # root_path = '/media/aberg/OS/Documents and Settings/Johan/Videos/JOHAN_DVDs/v2/VIDEO_TS'
        root_path = '/home/aberg/PycharmProjects/MovEd/res/mov/'

        super(FileBrowser, self).__init__()
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath('/')
        # view = QtGui.QListView()
        self.setModel(self.model)
        self.setRootIndex(self.model.index(root_path))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    head = FileBrowser()
    head.resize(768, 576)
    head.show()

    sys.exit(app.exec_())