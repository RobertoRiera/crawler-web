import sys
sys.path.insert(0, '/home/roberto/PycharmProjects/utils')

import os
import cv2
from detector_factory import Detector_factory

path_to_photos = os.path.realpath(".") + "/Photos"
print(os.path.join(os.path.split(path_to_photos)[0], 'man'))