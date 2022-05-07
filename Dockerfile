FROM python:3.9

WORKDIR /usr/advisory

COPY / .

RUN pip install -r requirements.txt

# Comando para ejecutar el fichero main con el análisis
# Modifique estos parametros para analizar el repositorio que desea
# o: Propietario del repositorio
# r: Nombre del repositorio
# d: Profundidad del grafo
CMD [ "python", "main.py", "-o", "GermanMT", "-r", "cpython", "-d", "1"]

# Comando para correr los experimentos
# CMD [ "python", "experimentation/run.py" ]