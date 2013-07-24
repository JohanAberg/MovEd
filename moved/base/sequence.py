import mlt
from time import sleep


class Sequence(object):
    def __init__(self):
        mlt.Factory.init()
        prof_name = "DV/DVD PAL"
        self.profile = mlt.Profile()

    def create_tractor(self):
        tractor = mlt.Tractor()
        # tractor.mark_in = 0
        # tractor.mark_out = 22
        return tractor

    def connect_playlist_to_multi_track(self, multi_track, playlist):
        multi_track.connect(playlist, 0)

    def create_multi_track(self, tractor):
        multi_track = tractor.multitrack()
        return multi_track

    def create_playlist(self):
        playlist = mlt.Playlist()
        playlist.id = 234
        return playlist

    def create_producer(self, file_path):
        producer = mlt.Producer(self.profile, file_path)
        producer.id = file_path
        # producer.set_in_and_out(11, 22)
        # producer.clip_in = 1 # inclusive. -1 == not set
        # producer.clip_out = 11 # inclusive, -1 == not set
        print 'fps', producer.get_fps()
        return producer


if __name__ == "__main__":

    """
    basic usage of a mlt tractor
    """

    file_name = '/home/aberg/PycharmProjects/MovEd/res/mov/wheel.mov'
    file_name2 = '/home/aberg/PycharmProjects/MovEd/res/mov/wheel2.mov'

    # m = Mlt()
    seq = Sequence()

    tractor = seq.create_tractor()
    multi_track = seq.create_multi_track(tractor)
    playlist = seq.create_playlist()

    producer = seq.create_producer(file_name)
    producer2 = seq.create_producer(file_name2)
    playlist.append(producer, 44, 88)
    playlist.append(producer2, 22, 66)

    seq.connect_playlist_to_multi_track(multi_track, playlist)

    consumer = mlt.Consumer()
    consumer.purge()
    consumer.set("real_time", 1)
    consumer.connect(tractor)

    # producer.seek(1)
    # producer.set_speed(1)
    consumer.start()

    while not consumer.is_stopped():
        sleep(.25)
