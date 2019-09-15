# rpi_dht_modbus - Simple server to provide Modbus TCP access to DHT sensor series.

## Introduction

This is a combination of [Adafruit DHT library](https://github.com/adafruit/Adafruit_Python_DHT) and
[pymodbus](https://github.com/riptideio/pymodbus) Modbus stack.

The server runs as a Modbus TCP server and gives access to DHT sensors value via Modbus registers.

## Installation

You will need Python version 3 (tested on RPi model B with Python 3.5) with `virtualenv` module.
After repository cloning run:
```
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

After that you will have all needed libraries so the last step is to copy `config.json.sample`
into `config.json` and adjust it to your needs.

