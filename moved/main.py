import sys
from moved.widgets.preview import Preview


if __name__ == "__main__":
    from PySide import QtGui

    file_name = "/home/aberg/dvdrip-data/unnamed/vob/001/unnamed-004.vob"
    file_name = '/home/aberg/Downloads/sample_iPod.m4v'
    file_name = '/home/aberg/Downloads/sample_iTunes.mov'

    app = QtGui.QApplication(sys.argv)
    preview = Preview()
    preview.load_movie(file_name)

    preview.resize(768, 576)
    preview.setWindowTitle('Preview')
    preview.show()

    sys.exit(app.exec_())