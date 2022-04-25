# Advisory
Una herramienta para el análisis de vulnerabilidades en proyectos software **open-source**.

[![DOI](https://zenodo.org/badge/484736338.svg)](https://zenodo.org/badge/latestdoi/484736338)

## Entorno de desarrollo
1. Debes tener [git](https://git-scm.com/) instalado localmente. 

2. Debes tener instalado Python versión 3.9.12 de forma local y crear un entorno virtual para el mismo.

    1. Para crear un entorno virtual usaremos el comando *python3.9 -m venv advisory-env*.

    2. Para activar el entorno virtual se usa el comando *source advisory-env/bin/activate* en sistemas Linux o Mac o *advisory-env\Scripts\activate.bat* en windows.

    En este [link](https://docs.python.org/3/library/venv.html) puede obtener más información de como crear un entorno virtual con Python.

4. Adicionalmente sería recomendable utilizar un editor de código de su preferencia.

## Variables de entorno

1. Para configurar las variables de entorno debes crear un fichero *.env* en la raiz del proyecto con la siguiente estructura:
   ```
    # environment variables defined inside a .env file
    GIT_GRAPHQL_API_KEY = 'YOUR_GIT_API_KEY'
    NVD_API_KEY = 'YOUR_NVD_API_KEY'
   ```
    Y sustiturir ambas variables por sus API KEY.

2. Para conseguir una KEY de la API GraphQL de github debe estar registrado y entrar [aquí](https://github.com/settings/tokens). Debe darle todos los permisos.

3. Para conseguir una KEY de la API de NVD debe entrar [aquí](https://nvd.nist.gov/developers/request-an-api-key) y seguir los pasos.

## Uso de la herramienta
1. Obtener la herramienta: podemos descargar el comprimido de alguna de las realeases disponibles en el repositorio o bien clonar el código de la rama **main** con el comando *git clone https://github.com/GermanMT/advisory.git*.

2. Utilizar el comando *pip install -r requirements.txt* desde el directorio raíz del proyecto para instalar las dependencias necesarias.

3. Una vez tengamos configurado el entorno podremos hacer uso de la herramienta editando el fichero main.py añadiendo el repositorio del proyecto software que queremos y ejecutando el comando *python main.py*.

4. También podemos ejecutar los experimentos con el comando *python experimentation/run.py*, se recomienda modificar el archivo run.py para correr cada experimento individualmente, ya que son pesados. En la carpeta de *../experiments/results/* se encuentran los ficheros generados la última vez que se ejecutaron los experimentos.