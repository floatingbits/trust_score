# pull official base image
FROM python:3.12.11-slim
# set work directory
WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
# To be able to install mysqlclient via pip ?!?
RUN apt-get update
RUN apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .