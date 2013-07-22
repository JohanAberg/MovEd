from PySide import QtGui
import os
from PySide.QtCore import QTimer, QThread
from moved.base.mlt_backend import Mlt
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
		self.mlt = MltThread()

		self.playhead_timer = QTimer()
		self.playhead_timer.setInterval(70)
		self.playhead_timer.timeout.connect(self.on_playhead_timer)

		self.horizontalSlider.setMaximum(self.HEAD_RESOLUTION)
		self.horizontalSlider.sliderReleased.connect(self.onHeadValueChanged)

		self.playButton.pressed.connect(self.onPlay)

	def __del__(self):
		pass
		# self.mlt.stop_player()
		# self.mlt.mlt.Factory.close()

	def get_percentage(self):
		position = float(self.mlt.mlt.producer.position())
		length = float(self.mlt.mlt.producer.get_length())
		decimal_position = position / length
		percent = decimal_position * self.HEAD_RESOLUTION
		return percent

	def set_time_label(self):
		self.label.setText('%d/%d' % (self.get_percentage(), self.mlt.mlt.producer.get_length()))

	def set_playhead(self):
		self.horizontalSlider.setValue(self.get_percentage())

	def on_playhead_timer(self):
		self.set_time_label()
		self.set_playhead()

	def onHeadValueChanged(self):
		value = self.horizontalSlider.value()
		decimal = (value*self.HEAD_RESOLUTION)/self.mlt.mlt.producer.get_length()

		self.mlt.mlt.refresh()
		self.seek(decimal)
		self.mlt.mlt.refresh()
		print decimal

	def seek(self, frame_number):
		# self.mlt.producer.pause()
		print self.mlt.mlt.producer.seek(int(frame_number))

	def onPlay(self):
		if self.mlt.mlt.is_stopped():
			# self.mlt.start_player()
			self.mlt.start()
			self.playButton.setChecked(False)
			self.playhead_timer.start(70)
		else:
			self.playButton.setChecked(True)
			self.mlt.mlt.stop_player()
			self.playhead_timer.stop()

		self.set_playhead()


