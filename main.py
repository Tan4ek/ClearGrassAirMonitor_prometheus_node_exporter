#!/usr/bin/python3

import configparser
import logging
from time import sleep, time

import miio
from prometheus_client import start_http_server, Gauge

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=config.get('logging', 'level', fallback='INFO'),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    MONITOR_IP = config['air-monitor']['Host']
    MONITOR_TOKEN = config['air-monitor']['Token']

    battery = Gauge('home_battery', 'Battery', ['device'])
    temperature = Gauge('home_temperature', 'temperature', ['device'])
    humidity = Gauge('home_humidity', 'humidity', ['device'])
    co2 = Gauge('home_co2', 'co2', ['device'])
    pm25 = Gauge('home_pm25', 'pm25', ['device'])
    tvoc = Gauge('home_tvoc', 'tvoc', ['device'])
    update_ts = Gauge('home_update_ts', 'update_ts', ['device'])

    start_http_server(config['prometheus-client'].getint('Port'))

    monitor_conn = None
    while True:
        sleep_time = config['prometheus-client'].getint('RefreshPeriodSeconds')
        try:
            if monitor_conn is None:
                logging.info("try conn monitor...")
                monitor_conn = miio.airqualitymonitor.AirQualityMonitor(ip=MONITOR_IP, token=MONITOR_TOKEN,
                                                                        model='cgllc.airmonitor.s1')
            st = monitor_conn.status()
            logging.info(st)
            battery.labels('monitor').set(st.battery)
            temperature.labels('monitor').set(st.temperature)
            humidity.labels('monitor').set(st.humidity)
            co2.labels('monitor').set(st.co2)
            pm25.labels('monitor').set(st.pm25)
            tvoc.labels('monitor').set(st.tvoc)
            update_ts.labels('monitor').set(int(time()))
        except Exception as ex:
            logging.error(ex)
            sleep_time = 1

        sleep(sleep_time)
