from PySide import QtGui
import os
from time import sleep
from moved.base.mlt_interface import Mlt
from moved.widgets.play_head import PlayHead
from ui.preview import Ui_Form


class Preview(QtGui.QWidget, Ui_Form):
    HEAD_RESOLUTION = 100.0

    def __init__(self, parent=None):
        super(Preview, self).__init__(parent)
        self.setupUi(self)

        # needed for SDL to be used inside an existing Qt widget
        #
        win_id = self.widget.winId()
        os.putenv('SDL_WINDOWID', str(win_id))

        # the mlt class that is actually playing the videos
        self.mlt = Mlt()

        self.play_head = PlayHead()
        self.horizontalLayout.insertWidget(1, self.play_head)

        self.mlt.s_producer_update.connect(self.on_playhead_timer)
        self.mlt.s_play.connect(self.on_s_play)
        self.mlt.s_stop.connect(self.on_s_stop)
        self.mlt.s_seek.connect(self.on_s_seek)

        self.play_head.setMaximum(self.HEAD_RESOLUTION)
        self.play_head.sliderMoved.connect(self.onHeadValueChanged)
        # self.horizontalSlider.valueChanged.connect(self.onHeadValueChanged) # causes stuttering
        self.play_head.sliderPressed.connect(self.onHeadPressed)
        self.play_head.sliderReleased.connect(self.set_play_button_state)

        self.playButton.released.connect(self.onPlay)


    def on_s_seek(self, producer):
        text = self.set_time_label(producer)
        self.play_head.set_head_label(text)

    def set_play_button_state(self):
        if self.mlt.is_playing():
            self.playButton.setChecked(True)
            self.playButton.setDown(True)
        else:
            self.playButton.setChecked(False)
            self.playButton.setDown(False)

    def on_s_stop(self, producer):
        self.set_play_button_state()

    def on_s_play(self, producer):
        self.set_play_button_state()

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
        # print position, length, decimal_position, percent
        return percent

    def set_time_label(self, producer):
        text = '%d/%d' % (producer.position(), producer.get_length())
        self.label.setText(text)
        return text

    def set_playhead(self, producer):
        self.play_head.setValue(self.get_percentage(producer))

    def on_playhead_timer(self, producer):
        self.set_playhead(producer)
        text = self.set_time_label(producer)
        self.play_head.set_head_label(text)

    def onHeadValueChanged(self):
        value = float(self.play_head.value())
        percent = value / self.HEAD_RESOLUTION
        length = self.mlt.producer.get_length()
        frame = length * percent
        self.mlt.refresh()
        self.seek(frame)
        self.mlt.refresh()

    def seek(self, frame_number):
        self.mlt.seek(int(frame_number))

    def onPlay(self):
        if not self.mlt.isRunning():
            self.mlt.start()
            self.play_head.setEnabled(True)
            sleep(.25) #TODO wait for thread to startup, find a better way...

        if not self.mlt.is_playing():
            self.mlt.play()
        else:
            self.mlt.pause()



