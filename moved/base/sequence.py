import mlt


class Sequence(object):

    def __init__(self):
        self.profile = mlt.Profile("DV/DVD PAL")

    def create_tractor(self):
        tractor = mlt.Tractor()
        # tractor.mark_in = -1
        # tractor.mark_out = -1
        return tractor

    def connect_track_to_multi_track(self, multi_track, track):
        multi_track.connect(track, len([]))

    def create_multi_track(self, tractor):
        multi_track = tractor.multitrack()
        return multi_track

    def create_playlist(self):
        new_track = mlt.Playlist()
        return new_track

    def create_producer(self, file_path):
        producer = mlt.Producer(self.profile, file_path)
        return producer