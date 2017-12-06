__author__ = 'javier'

import cv2
import cv2.cv as cv
import numpy as np
from skimage import transform
from skimage.feature import hog


class Cara:
    # tipo de detector
    tipo_detector = 0  # indica que metodo usamos para detectar las caras: opencv, encara, dario.

    # tamanyo imagen cabeza
    size_cabeza = 48

    # numero elementos de la rejilla
    num_rejilla = 3

    def __init__(self):
        # inicializa el detector cara
        self.detector_cara = self.inicializa_detector(
            '/home/javier/FuenteOpenCV/opencv-2.4.13/data/haarcascades/haarcascade_frontalface_alt.xml')

        # inicializa detectores de ojos
        self.detector_ojo_dcho = self.inicializa_detector(
            '/home/javier/FuenteOpenCV/opencv-2.4.13/data/haarcascades/haarcascade_mcs_righteye.xml')

        self.detector_ojo_izdo = self.inicializa_detector(
            '/home/javier/FuenteOpenCV/opencv-2.4.13/data/haarcascades/haarcascade_mcs_lefteye.xml')

        self.tipo_detector = 1

    def inicializa_detector(self, modelo):
        return cv2.CascadeClassifier(modelo)

    # devuelve la posicion de la cara como un rectangulo [x1,y1,x2,y2]
    def detect(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                         flags=cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        # pasa de x1,y1,w,h a x1,y1,x2,y2
        rects[:, 2:] += rects[:, :2]
        return rects

    def busca_mayor(self, rects):
        mayor = 0
        for r in rects:
            x1, y1, x2, y2 = r
            area = (x2 - x1) * (y2 - y1)
            if area > mayor:
                mayor = area
                rmayor = r

        return rmayor

    def detecta_con_opencv(self, imagen):
        # convierte a grises y ecualiza
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # detecta caras en la imagen
        rects = self.detect(gray, self.detector_cara)

        # busca la cara mayor
        if len(rects) > 0:
            max_rect = self.busca_mayor(rects)
            x1, y1, x2, y2 = max_rect

            # busca ojos en la cara
            roi_gray = gray[y1:y2, x1:x2]

            ojo_dcho = self.detector_ojo_dcho.detectMultiScale(roi_gray)
            ojo_izdo = self.detector_ojo_izdo.detectMultiScale(roi_gray)

            # visualiza la cara
            # vis = imagen.copy()
            # roi_color = vis[y1:y2, x1:x2]
            # cv2.rectangle(vis, (x1, y1), (x2, y2), (255,0,0), 2)
            # for (ex,ey,ew,eh) in ojo_dcho:
            #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            # for (ex,ey,ew,eh) in ojo_izdo:
            #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            # cv2.imshow('cara', vis)
            # cv2.waitKey(25)

            if len(ojo_dcho) < 1 or len(ojo_dcho) < 1:
                max_rect = []

        else:
            max_rect = []

        return max_rect

    def detecta_cara(self, imagen):
        if self.tipo_detector == 1:  # detectar usando opencv
            rect = self.detecta_con_opencv(imagen)

        return rect

    def calcula_hog(self, imagen):
        # convierte a niveles de gris
        imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        # reescala imagen
        imagen_gray = transform.resize(imagen_gray, (self.size_cabeza, self.size_cabeza))

        # valor de epsilon para evitar ceros
        eps = 0.00000001

        # calcula el HOG para cada elemento de la rejilla y concatena
        hog_histo = []
        pixels_rejilla = self.size_cabeza / self.num_rejilla
        for f in range(self.num_rejilla):
            for c in range(self.num_rejilla):
                tmp_image = imagen_gray[f * pixels_rejilla:(f + 1) * pixels_rejilla,
                            c * pixels_rejilla:(c + 1) * pixels_rejilla]
                # print tmp_image
                tmp_histo = hog(tmp_image, orientations=9, pixels_per_cell=(8, 8),
                                cells_per_block=(2, 2), visualise=False)

                # add epsilon para evitar ceros y normaliza
                tmp_histo = tmp_histo + eps
                tmp_histo = tmp_histo / np.linalg.norm(tmp_histo, ord=1)

                hog_histo.append(tmp_histo)

        return np.concatenate(hog_histo)
