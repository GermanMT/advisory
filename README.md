# Advisory
Una herramienta para el análisis de vulnerabilidades en proyectos software **open-source**.

## Entorno de instalación
Para obtener la herramienta podemos descargar el comprimido de alguna de las realeases disponibles en el repositorio o bien clonar el código de la rama **main** con el comando *git clone*.

Una vez obtenida, necesitamos tener instalado Python versión 3.9.12 de forma local o en un entorno virtual. Y utilizar el comando *pip install -r requirements.txt* desde el directorio ráiz del proyecto para instalar las dependencias necesarias.

En este [link](https://docs.python.org/3/library/venv.html) puede obtener informacion de como crear un entorno virtual con Python.

## Uso de la herramienta
Una vez tengamos configurado el entorno podremos hacer uso de la herramienta editando el fichero main.py añadiendo el repositorio del proyecto software que queremos y ejecutando el comando *python main.py*, si estamos en el entorno virtual o *python3.9 main.py* si estamos en local.

También podemos ejecutar los experimentos con el comando *python/python3.9 experimentation/run.py*, se recomienda modificar el archivo run.py para correr cada experimento individualmente, ya que son pesados. En la carpeta de *../experiments/results/* se encuentran los ficheros generados la última vez que se ejecutaron los experimentos.