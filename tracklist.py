import sys
import os
import re

full_path = sys.argv[1]

if not os.path.isdir(full_path):
	print('folder expected')
	exit(1)

os.chdir(full_path)
dirname = os.path.basename(full_path)

print('Tracklist: ')
for f in [fl for fl in os.listdir(full_path) if fl.endswith('.flac')]:
	new_name = f.replace(dirname, '')
	new_name = re.sub('([- ])+(?=[0-9])', '', new_name, 1)
	print(new_name.replace('.flac', '', 1))
	os.rename(f, new_name)
