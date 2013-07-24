from PySide import QtCore
from time import sleep
import mlt
from PySide.QtCore import QTimer


class Mlt(QtCore.QThread):
    s_producer_update = QtCore.Signal(object)
    s_play = QtCore.Signal(object)
    s_stop = QtCore.Signal(object)
    s_seek = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(Mlt, self).__init__()
        self.parent = parent
        self.consumer = None
        self.producer = None
        self.movie_file = None
        self.profile = None

        self.position_timer = QTimer()
        self.position_timer.setInterval(125)
        self.position_timer.timeout.connect(self.onPositionTimeout)

    def onPositionTimeout(self):
        self.s_producer_update.emit(self.producer)

    def run(self):
        """
        starts thread
        """
        try:
            self.setup()
        except RuntimeError, err:
            print 'ERROR: Mlt.run: starting thread:', err
            self.quit()

    def set_filter(self, filter_name):
        filter = mlt.Filter(self.profile, filter_name)
        filter.connect(self.producer)
        self.consumer.connect(filter)

    def setup(self):

        self.load_new_movie()

        self.consumer = mlt.Consumer()
        if self.parent:
            win_id = self.parent.widget.winId()
            self.consumer.set("window_id", int(win_id))

        self.consumer.connect(self.producer)
        self.consumer.set("real_time", 1)
        self.consumer.set("rescale", "nearest")
        self.consumer.set("resize", 1)
        self.consumer.set("progressive", 1)

        self.consumer.start()
        # self.pause()

        try:
            while not self.consumer.is_stopped():
                sleep(0.25)
        except AttributeError, err:
            print 'closing...\n\n'
            mlt.Factory.close()

    def load_new_movie(self):
        mlt.Factory.init()
        # self.profile = mlt.Profile("DV/DVD PAL")
        self.profile = mlt.Profile()
        # self.movie_file = 'xml:/tmp/mlt_tractor.xml'
        print self.profile.description(), self.movie_file
        self.producer = mlt.Producer(self.profile, self.movie_file)
        if not self.producer.is_valid():
            self.producer = None
            self.profile = None
            raise RuntimeError('Movie file not valid')
        if self.consumer:
            # print 'purging'
            # self.consumer.purge()
            self.consumer.connect(self.producer)
            self.producer.set_speed(0)
            self.consumer.start()
            # self.stop()
            # self.consumer.connect(self.producer)

        # self.stop()
        # self.consumer.connect(self.producer)
        # if self.consumer.is_stopped:
        #     self.consumer.start()

    def set_movie(self, file_path):
        self.movie_file = file_path

    def close(self):
        mlt.Factory.close()

    def get_version(self):
        major = mlt.mlt_version_get_major()
        minor = mlt.mlt_version_get_minor()
        revision = mlt.mlt_version_get_revision()
        print "%02d%02d%02d" % (major, minor, revision)
        return (major, minor, revision)

    def is_stopped(self):
        if not self.consumer:
            return True
        return self.consumer.is_stopped()

    def play(self):
        if self.producer:
            self.producer.set_speed(1)
            self.s_play.emit(self.producer)

    def stop(self):
        self.producer.set_speed(0)
        self.position_timer.stop()
        self.s_stop.emit(self.producer)

    def pause(self):
        self.stop()

    # self.producer.pause()

    def start_player(self):
        self.consumer.start()


    def stop_player(self):
        self.consumer.stop()


    def refresh(self):
        if not self.consumer:
            return
        self.consumer.set("refresh", 1)

    def is_playing(self):
        if self.producer and self.producer.get_speed() > 0:
            return True
        return False

    def seek(self, frame):
        self.producer.seek(frame)
        self.s_seek.emit(self.producer)


if __name__ == "__main__":
    m = Mlt()
    m.set_movie('/home/aberg/PycharmProjects/MovEd/res/mov/wheel.mov')
    m.setup()