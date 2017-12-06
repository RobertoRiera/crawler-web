__author__ = 'pedro'

from configuration import Configuration
import dlib
import os
import numpy as np

DLIB = 1
OPENCV = 0


class Detector_factory(object):
    def init(type_detector=DLIB):
        if type_detector == DLIB:
            return Dlib_face_detector()
        if type_detector == OPENCV:
            # implementar
            pass

    init = staticmethod(init)

    def detect(self, image_RGB):
        pass


class Dlib_face_detector(Detector_factory):
    # DLIB_FACE_LANDMARS CONSTANTS
    FACE_POINTS = list(range(17, 68))
    MOUTH_POINTS = list(range(48, 61))
    RIGHT_BROW_POINTS = list(range(17, 22))
    LEFT_BROW_POINTS = list(range(22, 27))
    RIGHT_EYE_POINTS = range(42, 48)
    LEFT_EYE_POINTS = range(36, 42)
    NOSE_POINTS = list(range(27, 35))
    JAW_POINTS = list(range(0, 17))
    CHIN_POINTS = list(range(6, 11))

    def __init__(self):
        self.conf = Configuration(os.path.dirname(__file__) + '/../Config.xml')
        self.face_detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            self.conf.get_value([self.conf.RUTAS_DETECTORES, self.conf.DLIB_FACE_LANDMARKS]))

    def detect(self, image_RGB, param=1):
        recs = self.face_detector(image_RGB, param)
        result = []
        for rec in recs:
            result.append([rec.left(), rec.top(), rec.right(), rec.bottom()])
        return result

    def predict_points(self, image_RGB, rect):
        drec = dlib.rectangle(left=rect[0], top=rect[1], right=rect[2], bottom=rect[3])
        main_points = self.predictor(image_RGB, drec).parts()
        result = []
        for point in main_points:
            result.append([point.x, point.y])
        return result

    def calculate_centroide(self, points, POINTS):
        media = np.mean(points[min(POINTS):max(POINTS)], 0)
        return media[0], media[1]
