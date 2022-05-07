# Advisory
Una herramienta para el análisis de vulnerabilidades en proyectos software **open-source**.

[![DOI](https://zenodo.org/badge/484736338.svg)](https://zenodo.org/badge/latestdoi/484736338)

## Trabajar con la herramienta

### Entorno de desarrollo

1. Debes tener [git](https://git-scm.com/) instalado localmente. 

2. Debes tener [docker](https://www.docker.com/) instalado localmente.

3. Adicionalmente sería recomendable utilizar un editor de código de su preferencia.

#### Obtención de la herramienta
1. Clonar el código de la rama **main** con el comando *git clone https://github.com/GermanMT/advisory.git*.

2. A continuación debemos modificicar el Dockerfile para añadir el propietario, repositorio y profundidad deseados para el grafo.

3. Para construir la imagen ejecutamos el comando *docker build -t advisory .* .

4. Para ver los resultados utilizamos el comando *docker run -e GIT_GRAPHQL_API_KEY=YOUR_GIT_API_KEY -e NVD_API_KEY=YOUR_NVD_API_KEY advisory*. Al cual deberemos añadir las dos API KEYS necesarias para la herramienta.

    1. Para conseguir una KEY de la API GraphQL de github debe estar registrado y entrar [aquí](https://github.com/settings/tokens). Debe darle todos los permisos.
    
    2. Para conseguir una KEY de la API de NVD debe entrar [aquí](https://nvd.nist.gov/developers/request-an-api-key) y seguir los pasos.