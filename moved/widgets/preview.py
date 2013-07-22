from PySide import QtGui
import os
from time import sleep
from PySide.QtCore import QTimer, QThread
from moved.base.mlt_thread import MltThread
from ui.preview import Ui_Form


class Preview(QtGui.QWidget, Ui_Form):

	HEAD_RESOLUTION = 10000

	def __init__(self, parent=None):
		super(Preview, self).__init__(parent)
		self.setupUi(self)
		win_id = self.widget.winId()
		os.putenv('SDL_WINDOWID', str(win_id))
		# self.mlt = Mlt()
		self.mlt_thread = MltThread()
		self.playing = False

		self.playhead_timer = QTimer()
		self.playhead_timer.setInterval(70)
		self.playhead_timer.timeout.connect(self.on_playhead_timer)

		self.horizontalSlider.setMaximum(self.HEAD_RESOLUTION)
		self.horizontalSlider.sliderReleased.connect(self.onHeadValueChanged)

		self.playButton.pressed.connect(self.onPlay)

	def closeEvent(self, *args, **kwargs):
		self.mlt_thread.mlt.stop_player()
		self.mlt_thread.mlt.close()
		self.mlt_thread.quit()
		self.mlt_thread.wait()

	# def __del__(self):
	# 	pass
		# self.mlt.stop_player()
		# self.mlt.mlt.Factory.close()

	def get_percentage(self):
		position = float(self.mlt_thread.mlt.producer.position())
		length = float(self.mlt_thread.mlt.producer.get_length())
		decimal_position = position / length
		percent = decimal_position * self.HEAD_RESOLUTION
		return percent

	def set_time_label(self):
		self.label.setText('%d/%d' % (self.get_percentage(), self.mlt_thread.mlt.producer.get_length()))

	def set_playhead(self):
		self.horizontalSlider.setValue(self.get_percentage())

	def on_playhead_timer(self):
		self.set_time_label()
		self.set_playhead()

	def onHeadValueChanged(self):
		value = self.horizontalSlider.value()
		decimal = (value*self.HEAD_RESOLUTION)/self.mlt_thread.mlt.producer.get_length()
		self.mlt_thread.mlt.refresh()
		self.seek(decimal)
		self.mlt_thread.mlt.refresh()

	def seek(self, frame_number):
		# self.mlt.producer.pause()
		self.mlt_thread.mlt.producer.seek(int(frame_number))

	def onPlay(self):
		if not self.mlt_thread.isRunning():
			self.mlt_thread.start()
			sleep(.25) #TODO wait for thread to startup

		if not self.playing:
			self.mlt_thread.mlt.play()
			self.playButton.setChecked(False)
			self.playhead_timer.start()
			self.playing = True
		else:
			self.playButton.setChecked(True)
			self.mlt_thread.mlt.pause()
			self.playhead_timer.stop()
			self.playing = False

		# self.set_playhead()


