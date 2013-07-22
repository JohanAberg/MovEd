from PySide import QtGui
import os
from time import sleep
from moved.base.mlt_interface import Mlt
from ui.preview import Ui_Form


class Preview(QtGui.QWidget, Ui_Form):
	HEAD_RESOLUTION = 10000

	def __init__(self, parent=None):
		super(Preview, self).__init__(parent)
		self.setupUi(self)

		win_id = self.widget.winId()
		os.putenv('SDL_WINDOWID', str(win_id))

		self.mlt = Mlt()
		self.playing = False

		self.mlt.producer_update.connect(self.on_playhead_timer)

		self.horizontalSlider.setMaximum(self.HEAD_RESOLUTION)
		self.horizontalSlider.sliderReleased.connect(self.onHeadValueChanged)
		self.horizontalSlider.sliderPressed.connect(self.onHeadPressed)

		self.playButton.pressed.connect(self.onPlay)

	def onHeadPressed(self):
		self.mlt.pause()

	def load_movie(self, file_name):
		self.mlt.set_movie(file_name)

	def closeEvent(self, *args, **kwargs):
		self.mlt.stop_player()
		self.mlt.close()
		self.mlt.quit()
		self.mlt.wait()


	def get_percentage(self, producer):
		position = float(producer.position())
		length = float(producer.get_length())
		decimal_position = position / length
		percent = decimal_position * self.HEAD_RESOLUTION
		return percent

	def set_time_label(self, producer):
		self.label.setText('%d/%d' % (self.get_percentage(producer), producer.get_length()))

	def set_playhead(self, producer):
		self.horizontalSlider.setValue(self.get_percentage(producer))

	def on_playhead_timer(self, producer):
		self.set_time_label(producer)
		self.set_playhead(producer)

	def onHeadValueChanged(self):
		value = self.horizontalSlider.value()
		decimal = (value * self.HEAD_RESOLUTION) / self.mlt.producer.get_length()
		self.mlt.refresh()
		self.seek(decimal)
		self.mlt.refresh()

	def seek(self, frame_number):
		# self.mlt.producer.pause()
		self.mlt.producer.seek(int(frame_number))

	def onPlay(self):
		if not self.mlt.isRunning():
			self.mlt.start()
			sleep(.25) #TODO wait for thread to startup

		if not self.playing:
			self.mlt.play()
			self.playButton.setChecked(False)
			self.playing = True
		else:
			self.playButton.setChecked(True)
			self.mlt.pause()
			self.playing = False

		# self.set_playhead()


