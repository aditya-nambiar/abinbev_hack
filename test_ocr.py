from os import listdir
from os.path import isfile, join
from ocr import get_text

onlyfiles = [f for f in listdir('/Users/nambiar/Documents/code/abinbev/ocr/a') if isfile(join('/Users/nambiar/Documents/code/abinbev/ocr/a', f))]

for f in onlyfiles :
	print f
	get_text(f)