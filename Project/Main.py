import os
import sys
import cv2
import normalization
import GenderHSNet
import ChictopiaCrawler
from detector_factory import Detector_factory

sys.path.insert(0, '/home/cantim/TFG/utils')


ChictopiaCrawler.ChictopiaCrawler(1, 10)

path_to_photos = os.path.realpath(".") + "/Photos"

for base, dirs, files in os.walk(path_to_photos):
    if files.__len__() != 0:
        for file in files:
            img = cv2.imread(os.path.join(base, file))
            detector_cara = Detector_factory.init()
            womanDir = os.path.join(os.path.split(base)[0], 'woman')
            manDir = os.path.join(os.path.split(base)[0], 'man')
            faces = detector_cara.detect(img)
            if faces.__len__() != 0:
                puntos = detector_cara.predict_points(img, faces[0])
                ojo_dcho = detector_cara.calculate_centroide(puntos, detector_cara.RIGHT_EYE_POINTS)
                ojo_izdo = detector_cara.calculate_centroide(puntos, detector_cara.LEFT_EYE_POINTS)
                p1x = faces[0][0]
                p1y = faces[0][1] - 20
                p2x = faces[0][2]
                p2y = faces[0][3]
                w = p2x - p1x
                h = p2y - p1y
                oix = ojo_izdo[0] - p1x
                oiy = ojo_izdo[1] - p1y
                odx = ojo_dcho[0] - p1x
                ody = ojo_dcho[1] - p1y

                roi_img = img[p1y:p1y + h, p1x:p1x + w]
                roi_gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
                normalizator = normalization.Normalization()
                normalizator.normalize_gray_img(roi_gray, odx, ody, oix, oiy,
                                                normalization.Kind_wraping.HS)

                img_final = cv2.resize(normalizator.norm_image, (227, 227))
                cv2.imwrite('normaHS.jpeg', img_final)
                img2 = cv2.imread('normaHS.jpeg')
                female, male = GenderHSNet.image_gender_classifier("normaHS.jpeg")
                print(os.path.join(base, file))
                if male * 100 > 50:
                    # meter en man
                    os.rename(os.path.join(base, file), os.path.join(manDir, file))
                    print(os.path.join(manDir, file))
                    print('probabilidad de ser hombre', male * 100)
                else:
                    # meter en woman
                    os.rename(os.path.join(base, file), os.path.join(womanDir, file))
                    print(os.path.join(womanDir, file))
                    print("probabilidad de ser mujer", female * 100)

            else:
                # Dejar en undefined
                print('No se encontro ninguna cara')
