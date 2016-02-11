# maxwell-prometheus-exporter
Feed [Maxwell](http://maxwells-daemon.io/) metrics into [Prometheus](http://prometheus.io/)

# Installation
[This blog post](https://www.digitalocean.com/community/tutorials/how-to-install-prometheus-using-docker-on-ubuntu-14-04)
from Ditial Ocean explains how to setup Prometheus, the node exporter and Grafana.

## Using docker

Build the docker image:

```
sudo docker build -t maxwell-prometheus-exporter:0.1.2 .
```

Then run it:

```
sudo docker run -d --name maxwell-prometheus-exporter -p 8081:8081 \
    -v /etc/maxwell-prometheus-exporter.cfg:/etc/maxwell-prometheus-exporter.cfg \
    maxwell-prometheus-exporter:0.1.2
```

## Using pip
```
sudo pip install .
```
And then run `maxwell-prometheus-exporter`

# Hacking
To install the package in editable development mode:
```
sudo pip install -e .
```

# Acknowledgements
This project is heavily based on [prometheus-es-exporter](https://github.com/Braedon/prometheus-es-exporter)
