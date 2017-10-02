import datetime
from os.path import join
import sys
import pygame

def logout(s, tag=""):
	sys.stdout.write("[{:%Y-%m-%d %H:%M:%S} {}] {}\n".format(datetime.datetime.now(), tag, s))

def logerr(s, tag=""):
	sys.stderr.write("[{:%Y-%m-%d %H:%M:%S} {}] {}\n".format(datetime.datetime.now(), tag, s))

def load_image(filename):
	path = join("assets", filename)
	try:
		image = pygame.image.load(path)
	except:
		logerr("ERROR: Image '{}' not found".format(filename), "load_image")
		sys.exit(-1)
	#try:
	if image.get_alpha() is None:
		image = image.convert()
	else:
		image = image.convert_alpha()
	#except:
	#	logerr("ERROR: Image '{}' not converted".format(filename))
	return image