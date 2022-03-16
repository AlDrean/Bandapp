FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install virtualenv

RUN virtualenv env

RUN env/bin/pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./api/* /app/api/

WORKDIR /app/api

ENTRYPOINT /app/env/bin/uvicorn main:app --reload

