from music21 import *
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# import music21

class PathGrabber:
    def __init__(self):
        self.path = None

    def set_path(self, path):
        self.path = path


c_minor = chord.Chord(['C4', 'G4', 'E-5'])
c_minor.duration.type = 'whole'
print(c_minor.pitchedCommonName)

n1 = note.Note('C4', quarterLength=1)
n2 = note.Note('A4', quarterLength=1)
s = stream.Stream()
s.append(n1)
s.append(n2)
# s.show('lily.svg')
# s.write('', fp='/Users/macbook/programming/python/music_theory/')
path_grabber = PathGrabber()
c_minor.show('lily.png', my_show=False, my_path_grabber=path_grabber)
# c_minor.show('test.svg')


im = Image.open(path_grabber.path)
x = np.array(im)
plt.figure()
plt.imshow(x)
plt.show()

def get_random_chord():
    return None

exit = False
while not exit:
    chord = get_random_chord()