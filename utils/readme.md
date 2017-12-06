#Estándares:

##Ejecucción desde terminal

Para que funcione correctamente desde terminal hay que añadir el path de trabajo. En el caso del usuario "pedro" con sus proyectos en "caffe/examples", export PYTHONPATH=/home/pedro/caffe/examples:$PYTHONPATH Dentro de "examples" (en mi caso) están todos los proyectos.

##Configuración del entorno
###XML
Tiene que estar ubicado un nivel superior al del proyecto, para que todos los proyectos lo compartan. Generalmente el nombre del fichero es Config.xml porque ya hay utilidades implementadas con este fichero de configuración. Con un navegador web puedes observar la composición del fichero xml. 
###configuration.py
Módulo que gestiona las lecturas del fichero xml.
####Leer

    conf = Configuration(os.path.dirname(__file__)+'/../Config.xml')
    ruta_dlib_landmarks = conf.get_value([conf.RUTAS_DETECTORES, conf.DLIB_FACE_LANDMARKS]))

El método "get_value" recorre los tag del xml en profundidad, por parámetro se le pasa un vector con el nombre de los tag necesarios para obtener el valor deseado.
####Proceso para añadir un tag al xml
1. Se añade el tag correspondiente en el xml
2. Se crea una constante en el módulo configuration.py con valor del nombre del tag
##Descargar el shape_predictor_68_face_landmarks.dat:
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
##Commits:
[ADD] Añadir funcionalidad
[FIX] Solucionar incidencia

