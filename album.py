from bitmath import GiB
from bitmath import MiB


class Album:
    def __init__(self,
                 artist,
                 album,
                 url,
                 band_url='',
                 slug_text='',
                 num_comments=0,
                 tralbum_id=0,
                 art_id=0,
                 genre='',
                 band_id=0,
                 genre_id=0,
                 year=1970,
                 size='0MB',
                 cover_art=''
                 ):

        # Version field for enabling smarter updates
        self.ver = 1

        # Bandcamp Hub API fields
        self.artist = artist
        self.title = album
        self.tralbum_url = url
        self.band_url = band_url
        self.slug_text = slug_text
        self.num_comments = num_comments
        self.tralbum_id = tralbum_id
        self.art_id = art_id  # cover art?
        self.genre = genre
        self.genre_id = genre_id
        self.band_id = band_id
        
        # Custom properties
        self.cover_art = cover_art
        self.size = size
        self.year = year
        self.duration = ''
        self.tracklist = []
        self.tags = []
        self.about = ''
        
        self.is_free = False

    def add_track(self, track_title, track_duration):
        """
        Adds a track to an album, recalculating the duration time
        :param track_title: Track title
        :param track_duration: track is a string in a form hours:mins:secs (1:09:23 or 4:59)
        """
        self.tracklist.append(track_title)

        time = self.duration.split(':') if ':' in self.duration else []
        new_track = track_duration.split(':')
        if len(time) > len(new_track):
            for x in range(0, (len(time) - len(new_track))):
                new_track.insert(0, '00')
        if len(new_track) > len(time):
            for x in range(0, (len(new_track) - len(time))):
                time.insert(0, '00')
        add_one = False
        new_album_time = ''
        for l in range(0, len(time)):
            index = len(time) - l - 1
            additional = 1 if add_one else 0
            add_one = False
            length = int(new_track[index]) + int(time[index]) + additional
            if (l in [0, 1]) and length > 60:
                add_one = True
                length %= 60
            slength = str(length).zfill(2)
            new_album_time = slength + ':' + new_album_time if new_album_time != '' else slength
        self.duration = new_album_time

    def duration_seconds(self):
        seconds = 0
        time = self.duration.split(':') if ':' in self.duration else []
        for i in range(0, len(time)):
            multiply = pow(60, i)
            seconds += int(time[len(time) - i - 1]) * multiply
        return seconds

    def size_bytes(self):
        if 'GB' in self.size:
            return GiB(float(self.size.replace('GB', ''))).bytes
        if 'MB' in self.size:
            return MiB(float(self.size.replace('MB', ''))).bytes
        # for unknown size, let's return some heuristic value based on album duration
        return self.duration_seconds() * 1024 * 100

    def big(self):
        """
        Is the album big?
        :return True if the size of the album is more than 300MB, false otherwise
        """
        return MiB(300).bytes < self.size_bytes()
