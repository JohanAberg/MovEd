from PySide import QtCore
from time import sleep
import mlt
from PySide.QtCore import QTimer


class Mlt(QtCore.QThread):

	producer_update = QtCore.Signal(object)

	def __init__(self):
		super(Mlt, self).__init__()
		self.consumer = None
		self.factory = None
		self.producer = None
		self.movie_file = None

		self.position_timer = QTimer()
		self.position_timer.setInterval(70)
		self.position_timer.timeout.connect(self.onPositionTimeout)

	def onPositionTimeout(self):
		self.producer_update.emit(self.producer)

	def run(self):
		self.setup()

	def setup(self):

		self.factory = mlt.Factory().init()
		profile = mlt.Profile("DV/DVD PAL")

		self.producer = mlt.Producer(profile, self.movie_file)
		if not self.producer.is_valid():
			raise RuntimeError('Movie file not valid')

		# self.filter = mlt.Filter(profile, "greyscale")
		# self.filter.connect(producer)

		self.consumer = mlt.Consumer()
		self.consumer.connect(self.producer)
		# self.consumer.connect(filter)
		self.consumer.set("real_time", 1)

		self.consumer.start()
		self.pause()

		while not self.consumer.is_stopped():
			sleep(0.1)

		self.consumer.stop()
		mlt.Factory.close()

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
		self.producer.set_speed(1)
		self.position_timer.start()

	def stop(self):
		self.producer.set_speed(0)
		self.position_timer.stop()

	def pause(self):
		self.producer.pause()

	def start_player(self):
		self.consumer.start()


	def stop_player(self):
		self.consumer.stop()

	def refresh(self):
		self.consumer.set("refresh", 1)


if __name__ == "__main__":
	m = Mlt()
	m.set_movie('/home/aberg/dvdrip-data/unnamed/vob/001/unnamed-003.vob')
	m.setup()
# m.start_player()
