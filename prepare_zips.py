import os, sys
import subprocess
from zipfile import ZipFile

folder = sys.argv[1]
if not folder or not os.path.isdir(folder):
	print('Folder containing zip files expected')
	exit(1)
print('Processing albums from %s' % folder)

files = os.listdir(folder)
zips = (f for f in files if f.endswith('.zip'))
for z in zips:
	print('Extracting from %s' % z)
	fullpath = folder + '/' + z.replace(".zip", "")
	ZipFile(folder + '/' + z).extractall(path=fullpath)
	output = subprocess.check_output(["python", "tracklist.py", fullpath])
	print(output)
	os.rename(fullpath, fullpath + " [FLAC]")
