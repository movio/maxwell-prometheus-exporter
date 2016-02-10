FROM python:2-slim

MAINTAINER nicolas@movio.co

WORKDIR /usr/src/app

COPY exporter/*.py /usr/src/app/exporter/
COPY setup.py /usr/src/app/
COPY LICENSE /usr/src/app/

RUN pip install -e .

RUN apt-get update && apt-get install -y git && apt-get clean

RUN git clone https://github.com/mysql/mysql-connector-python.git && \
    cd mysql-connector-python && python ./setup.py build && python ./setup.py install

ENV CONFIG=/etc/maxwell-prometheus-exporter.cfg

CMD python -u /usr/local/bin/maxwell-prometheus-exporter --config $CONFIG
