import sys
import os

full_path = sys.argv[1]

if not os.path.isdir(full_path):
	print 'folder expected'
	exit(1)

os.chdir(full_path)
dirname = os.path.basename(full_path)

print 'Tracklist: '
for f in os.listdir(full_path):
	if not dirname in f:
		print 'skipped %s' % f
	new_name = f.replace(dirname, '')
	if new_name.startswith(' - '):
		new_name = new_name.replace(' - ', '', 1)
	print new_name.replace('.flac', '', 1)
	os.rename(f, new_name)
print 'Done'
