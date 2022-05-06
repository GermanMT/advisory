FROM python:3.9

WORKDIR /usr/advisory

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY / .

ARG CACHE_DATE=1

RUN [ "python", "main.py" ]
# RUN [ "python", "experimentation/run.py" ]