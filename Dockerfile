FROM python:3.11-slim

WORKDIR /opt/chatapp

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip \
    &&pip3 install -r requirements.txt
