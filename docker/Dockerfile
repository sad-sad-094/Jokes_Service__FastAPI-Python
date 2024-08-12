FROM python:3.11.9-slim-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc cron \
  && apt-get clean

RUN pip install --upgrade pip
# RUN pip install pipenv
COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . .
EXPOSE 80