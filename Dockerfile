FROM python:3.9

WORKDIR /usr/advisory

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY / .

ARG CACHE_DATE=1

# Comando para ejecutar el fichero main con el análisis
# Modifique estos parametros para analizar el repositorio que desea
# o: Propietario del repositorio
# r: Nombre del repositorio
# d: Profundidad del grafo
RUN [ "python", "main.py", "-o", "GermanMT", "-r", "urllib3", "-d", "1"]

# Comando para correr los experimentos
# RUN [ "python", "experimentation/run.py" ]