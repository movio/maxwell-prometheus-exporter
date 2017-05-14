FROM python:2-slim

MAINTAINER nicolas@movio.co

WORKDIR /usr/src/app

ARG config=/etc/maxwell-prometheus-exporter.cfg
ENV CONFIG=$config

COPY LICENSE /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY exporter/*.py /usr/src/app/exporter/
COPY setup.py /usr/src/app/
RUN pip install -e .

CMD python -u /usr/local/bin/maxwell-prometheus-exporter --config $CONFIG
