# coding=UTF-8

__author__ = 'javier'

# Programa para crear almacenar las imágenes contenidas en las carpetas de un directorio en una base de datos HDF5. Reescala
# las imágenes al ancho y algo indicado y opcionalmente las convierte a niveles de grises

#
import os
import sys
import h5py
import argparse
import numpy as np
import cv2
import glob




# h5f = h5py.File('data.h5', 'w')
# h5f.create_dataset('cifar10_X', data=X)
# h5f.create_dataset('cifar10_Y', data=Y)
# h5f.create_dataset('cifar10_X_test', data=X_test)
# h5f.create_dataset('cifar10_Y_test', data=Y_test)
# h5f.close()
#
# # Load hdf5 dataset
# h5f = h5py.File('data.h5', 'r')
# X = h5f['cifar10_X']
# Y = h5f['cifar10_Y']
# X_test = h5f['cifar10_X_test']
# Y_test = h5f['cifar10_Y_test']
#
# h5f.close()


# función para analizar la linea de comandos
def analiza_argumentos(args):
    parser = argparse.ArgumentParser(description='Almacenar imágenes en base de datos HDF5')

    parser.add_argument('-g', '--grayscale', help='Para convertir las imágenes en escala de grises',
                        action="store_true")
    parser.add_argument('-f', '--folder', help='Carpeta donde están los ficheros', required='True')
    parser.add_argument('-o', '--output', help='Base de datos de salida', required='True')
    parser.add_argument('-wi', '--width', help='Nuevo ancho de las imágenes', required='True')
    parser.add_argument('-he', '--height', help='Nuevo alto de las imágenes', required='True')
    parser.add_argument('-p', '--proportion', help='Proporción de datos en el conjunto train')

    # argumentos = vars(parser.parse_args()) # para convertir la salida en un diccionario en lugar de un namespace
    argumentos = parser.parse_args()

    return argumentos


def crearBaseDeDatosTrainTest(dir, h5file, w, h, grises=False, proporcion=0.66, patron='*.png'):
    print ('OPCION DE TRAIN Y TEST NO IMPLEMENTADO')


def crearBaseDeDatosFullNoIter(dir, h5file, w, h, grises=False, patron='*.png'):
    print ('************ Creación NO iterativa de la base de datos')

    # obtiene el número de clases
    nombre_clases = glob.glob(os.path.join(dir, '*'))
    num_clases = len(nombre_clases)
    print ('numero de clases: {} -> {}'.format(num_clases, nombre_clases))

    # calcula el número total de ficheros
    clase_idx = 0
    total_num_ficheros = 0

    for folder in nombre_clases:
        # obtiene el número de ficheros por clase
        carpeta = os.path.join(folder, patron)
        ficheros = glob.glob(carpeta)
        nficheros = len(ficheros)

        total_num_ficheros += nficheros

        print ('clase: {} -> {}\n'.format(folder, nficheros))

    print ('numero total de ficheros: {}\n'.format(total_num_ficheros))
    print ('numero total de clases: {}\n'.format(num_clases))

    # reserva espacio para las imágenes y clases
    if grises:
        X = np.zeros([total_num_ficheros, w, h, 1], np.float32)
    else:
        X = np.zeros([total_num_ficheros, w, h, 3], np.uint8)

    Y = np.zeros([total_num_ficheros], np.uint8)

    # lectura de las imágenes y carga en el array
    img_idx = 0
    for clase_idx in range(num_clases):
        # obtiene el número de ficheros por clase
        folder = nombre_clases[clase_idx]
        carpeta = os.path.join(folder, patron)
        ficheros = glob.glob(carpeta)
        nficheros = len(ficheros)

        for i in range(nficheros):
            if img_idx % 500 == 0:
                print ('Leyendo fichero ({}/{}): {}'.format(img_idx, total_num_ficheros, ficheros[i]))
            img = cv2.imread(ficheros[i])

            # print(ficheros[i])
            img_resized = cv2.resize(img, (w, h))
            if grises:
                img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
                X[img_idx, :, :, 0] = img_resized
            else:
                X[img_idx, :, :, :] = img_resized

            # guarda imagen y clase
            Y[img_idx] = clase_idx

            img_idx += 1

    h5f.create_dataset('X', data=X)
    h5f.create_dataset('Y', data=Y)

    return

def crearBaseDeDatosFull(dir, h5file, w, h, grises=False, patron='*.png'):
    print ('************ Creación ITERATIVA de la base de datos')
    # obtiene el número de clases
    nombre_clases = glob.glob(os.path.join(dir, '*'))
    num_clases = len(nombre_clases)
    print ('numero de clases: {} -> {}'.format(num_clases, nombre_clases))

    # calcula el número total de ficheros
    clase_idx = 0
    total_num_ficheros = 0

    for folder in nombre_clases:
        # obtiene el número de ficheros por clase
        carpeta = os.path.join(folder, patron)
        ficheros = glob.glob(carpeta)
        nficheros = len(ficheros)

        total_num_ficheros += nficheros

        print ('clase: {} -> {}\n'.format(folder, nficheros))

    print ('numero total de ficheros: {}\n'.format(total_num_ficheros))
    print ('numero total de clases: {}\n'.format(num_clases))

    # reserva espacio para las imágenes y clases
    if grises:
        X = h5file.create_dataset('X', shape = [total_num_ficheros, w, h, 1], dtype = np.float32)
    else:
        X = h5file.create_dataset('X', shape = [total_num_ficheros, w, h, 3], dtype = np.float32)

    Y = h5file.create_dataset('Y', shape=[total_num_ficheros, 1], dtype=np.uint8)

    # lectura de las imágenes y carga en el array
    img_idx = 0
    for clase_idx in range(num_clases):
        # obtiene el número de ficheros por clase
        folder = nombre_clases[clase_idx]
        carpeta = os.path.join(folder, patron)
        ficheros = glob.glob(carpeta)
        nficheros = len(ficheros)

        for i in range(nficheros):
            if img_idx % 500 == 0:
                print ('Leyendo fichero ({}/{}): {}'.format(img_idx, total_num_ficheros, ficheros[i]))
            img = cv2.imread(ficheros[i])

            # print(ficheros[i])
            img_resized = cv2.resize(img, (w, h))
            if grises:
                img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
                img_resized = img_resized.astype(np.float32)
                img_resized = img_resized * (1./255.)
                X[img_idx, :, :, 0] = img_resized
            else:
                img_resized = img_resized.astype(np.float32)
                img_resized = img_resized * (1./255.)
                X[img_idx, :, :, :] = img_resized

            # guarda imagen y clase
            Y[img_idx] = clase_idx

            img_idx += 1

    return

# programa principal
if __name__ == '__main__':
    # analiza argumentos de entrada
    argumentos = analiza_argumentos(sys.argv[1:])

    carpeta = argumentos.folder # nombre de la carpeta donde leer las imágenes
    basedatos = argumentos.output # nombre de la base de datos HDF5 donde se escribem
    w = int(argumentos.width) # nuevo ancho de las imágenes
    h = int(argumentos.height) # nuevo alto de las imágenes

    if argumentos.grayscale:
        gris = True # se convierte a niveles de gris las imágenes
    else:
        gris = False # se mantienen en color las imágenes

    prop = argumentos.proportion # proporción de las imágenes que se usan para entrenamiento

    # creación de la base de datos
    h5f = h5py.File(basedatos, 'w')

    if prop == None:
        crearBaseDeDatosFull(carpeta, h5f, w, h, gris)
    else:
        crearBaseDeDatosTrainTest(carpeta, h5f, w, h, prop, gris)

    # print X.shape
    # print Y.shape

    # cerrar la base de datos
    h5f.close()
