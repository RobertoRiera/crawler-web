__author__ = 'pedroamarinreyes'
import xml.etree.ElementTree as ET
import copy


class Configuration:
    RUTA_FICHERO_SALIDA = 'ruta_fichero_salida'
    RUTA_FICHERO_TIPO_CLASIFICADOR = 'ruta_fichero_tipo_clasificador'
    RUTAS_DETECTORES = 'rutas_detectores'
    CARA = 'cara'
    OJO_DERECHO = 'ojo_derecho'
    OJO_IZQUIERDO = 'ojo_izquierdo'
    BOCA = 'boca'
    HOMBRO_CABEZA_HOMBRO = 'hombro_cabeza_hombro'
    DLIB_FACE_LANDMARKS = 'dlib_face_landmarks'

    RUTAS_TIPOSPLANOS_CNN = 'rutas_tiposPlanos_CNN'
    RUTAS_SEXOS_CNN = 'rutas_sexos_CNN'
    MODELO = 'modelo'
    PESOS = 'pesos'
    PROMEDIO = 'promedio'

    def __init__(self, path):
        self.root = ET.parse(path).getroot()

    # ejemplo: labels->[rutas_detectores, cara] se obtendria la ruta del detector de cara
    def get_value(self, labels):
        aux = self.root
        for label in labels:
            aux = aux.find(label)
        return aux.text

# ejempolo de uso
# a = Configuracion('../Config.xml')
# print a.get_value([a.RUTAS_SEXOS_CNN,a.MODELO])
