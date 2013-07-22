__author__ = 'aberg'
import mlt

class Mlt(object):

	def setup(self):

		file_name = "/home/aberg/dvdrip-data/unnamed/vob/001/unnamed-004.vob"

		self.factory = mlt.Factory().init()
		profile = mlt.Profile("DV/DVD PAL")

		self.producer = mlt.Producer(profile, file_name)

		# self.filter = mlt.Filter(profile, "greyscale")
		# self.filter.connect(producer)

		self.consumer = mlt.Consumer()
		self.consumer.connect(self.producer)
		# self.consumer.connect(filter)
		# self.consumer.set("real_time", 1)

		major = mlt.mlt_version_get_major()
		minor = mlt.mlt_version_get_minor()
		revision = mlt.mlt_version_get_revision()
		print "%02d%02d%02d" % (major, minor, revision)

		# self.consumer.start()

	# while not consumer.is_stopped():
	# 	sleep(0.25)
	#
	# consumer.stop()
	# mlt.Factory.close()

	def is_stopped(self):
		return self.consumer.is_stopped()

	def start_player(self):
		self.consumer.start()
		self.producer.set_speed(1)

	def stop_player(self):
		self.consumer.stop()

	def refresh(self):
		self.consumer.set("refresh", 1)
