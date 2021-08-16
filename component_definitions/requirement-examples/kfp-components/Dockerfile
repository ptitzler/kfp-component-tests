FROM python:3.7-alpine

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./0-n/src /pipelines/component/src
COPY ./1-n/src /pipelines/component/src
