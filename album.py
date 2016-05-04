from bitmath import GiB
from bitmath import MiB

class Album:
	def __init__(self, artist, album, year, url, size):
		self.artist = artist
		self.album = album
		self.year = year
		self.url = url
		self.size = size
		self.duration = ''

	def add_track(self, track):
		"""
		Adds a track to an album, recalculating the duration time
		:param track: track is a string in a form hours:mins:secs (1:09:23 or 4:59)
		"""
		time = self.duration.split(':') if ':' in self.duration else []
		new_track = track.split(':')
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

	def to_str(self):
		return ', '.join([self.album, self.artist, str(self.year), self.duration, self.size, self.url])
