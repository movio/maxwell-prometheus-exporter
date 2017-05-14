# -*- coding: utf-8 -*-

import sys
import time
import os
import argparse
from mysql import connector
import configparser
from prometheus_client import start_http_server, Gauge

BINLOG_FILE_SIZE_BYTES = 512 * 1024 * 1024
GAUGES = {}

def metric_name_escape(name):
    return name.replace(".", "_").replace("-", "_").replace(" ", "_")

def setGaugeValue(name, labels, labelValues, value, description = ""):
    name = metric_name_escape(name)
    if name not in GAUGES:
        GAUGES[name] = Gauge(name, description, labels)
    if labels:
        GAUGES[name].labels(*labelValues).set(value)
    else:
        GAUGES[name].set(value)

def usage(message):
    print "ERROR:", message
    sys.exit(-1)

def validate_config(config):
    if "exporter" not in config.sections():
        usage("could not find section [exporter]")
    if not config.has_option('exporter', 'port'):
        usage("could not find port option in section [exporter]")
    if not config.has_option('exporter', 'refresh_interval_ms'):
        usage("could not find refresh_interval_ms option in section [exporter]")
    if not config.has_option('exporter', 'die_on_connection_failure'):
        usage("could not find die_on_connection_failure option in section [exporter]")
    if config.sections() == ["exporter"]:
        usage("you must specify at least one host section")

    for section in config.sections():
        if section == "exporter": continue
        if not config.has_option(section, 'username'):
            usage("[%s] section is missing a username option" % section)
        if not config.has_option(section, 'password'):
            usage("[%s] section is missing a password option" % section)
        if not config.has_option(section, 'port'):
            usage("[%s] section is missing a port option" % section)
        if not config.has_option(section, 'hostname'):
            usage("[%s] section is missing a hostname option" % section)


def calculateBacklog(binlog_name, binlog_position, maxwell_binlog_name, maxwell_binlog_position):
    if (binlog_name == maxwell_binlog_name):
        return binlog_position - maxwell_binlog_position
    ordinal = int(binlog_name.split('.')[1])
    maxwell_ordinal = int(maxwell_binlog_name.split('.')[1])
    return (binlog_position - maxwell_binlog_position) + (BINLOG_FILE_SIZE_BYTES) * (ordinal - maxwell_ordinal)


def main():
    parser = argparse.ArgumentParser(description='Feed Maxwell metrics into Prometheus.')
    parser.add_argument('--config', metavar='CONFIG', type=str, required=True,
                        help='path to config file')
    args = parser.parse_args()
    config = configparser.ConfigParser()

    if not os.path.exists(args.config):
        usage('Cannot find config: %s' % args.config)

    config.read(args.config)

    validate_config(config)

    start_http_server(config.getint('exporter', 'port'))

    print "Starting loop"
    while True:
        for section in config.sections():
            if section == 'exporter': continue
            host_config = {
                'user': config.get(section, 'username'),
                'password': config.get(section, 'password'),
                'host': config.get(section, 'hostname'),
                'port': config.getint(section, 'port'),
                'database': 'maxwell',
                'raise_on_warnings': True,
            }
            try:
                connection = connector.connect(**host_config)
            except Exception as e:
                if config.getboolean('exporter', 'die_on_connection_failure'):
                    raise
                print 'Failed to connect to MySQL:', e
                continue
            cursor = connection.cursor()
            cursor.execute("SHOW MASTER STATUS")
            row = cursor.fetchall()[0]
            binlog_name = row[0]
            binlog_position = row[1]

            cursor.execute("SELECT * from maxwell.positions")
            row = cursor.fetchall()[0]
            maxwell_binlog_name = row[1]
            maxwell_binlog_position = row[2]

            cursor.close()
            connection.close()

            backlog = calculateBacklog(binlog_name, binlog_position, maxwell_binlog_name, maxwell_binlog_position)
            setGaugeValue('maxwell:master_binlog_position_bytes', ['host'], [section], binlog_position)
            setGaugeValue('maxwell:maxwell_binlog_position_bytes', ['host'], [section], maxwell_binlog_position)
            setGaugeValue('maxwell:backlog_bytes', ['host'], [section], backlog)

        time.sleep(config.getint('exporter', 'refresh_interval_ms') / 1000.0)
