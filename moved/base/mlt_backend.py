from time import sleep

__author__ = 'aberg'
import mlt

class Mlt(object):

	def __init__(self):
		self.consumer = None
		self.factory = None
		self.producer = None

	def setup(self):

		file_name = "/home/aberg/dvdrip-data/unnamed/vob/001/unnamed-003.vob"

		self.factory = mlt.Factory().init()
		profile = mlt.Profile("DV/DVD PAL")

		self.producer = mlt.Producer(profile, file_name)

		# self.filter = mlt.Filter(profile, "greyscale")
		# self.filter.connect(producer)

		self.consumer = mlt.Consumer()
		self.consumer.connect(self.producer)
		# self.consumer.connect(filter)
		self.consumer.set("real_time", 1)

		self.consumer.start()
		self.pause()

		while not self.consumer.is_stopped():
		# while True:
			sleep(0.1)

		self.consumer.stop()
		mlt.Factory.close()

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

	def stop(self):
		self.producer.set_speed(0)

	def pause(self):
		self.producer.pause()

	def start_player(self):
		self.consumer.start()
		# self.producer.set_speed(1)

	def stop_player(self):
		self.consumer.stop()

	def refresh(self):
		self.consumer.set("refresh", 1)


if __name__ == "__main__":
	m = Mlt()
	m.setup()
	# m.start_player()
