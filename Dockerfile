FROM python:3.8.10-alpine
  
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONBUFFERED 1

RUN apk update
RUN apk add --update postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev libffi-dev   

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip -vvv install --upgrade --force-reinstall cffi

RUN pip install -r requirements.txt
