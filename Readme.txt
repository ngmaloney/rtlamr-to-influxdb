# rtlamr-to-influxdb

This script uses `rtl_tcp` and `rtlamr` to read electricity meter data via an RTL-SDR device and sends the readings to an InfluxDB database.

## Requirements

- Python 3.x
- RTL-SDR device
- `rtl_tcp`
- `rtlamr`
- `pandas`
- `influxdb`

## Installation

1. Install the required software:
  ```sh
  sudo apt-get install rtl-sdr
  go get github.com/bemasher/rtlamr
  pip install -r requirments.txt
  ```

2. Clone this repository:
  ```sh
  git clone https://github.com/ngmaloney/rtlamr-to-influxdb.git
  cd rtlamr-to-influxdb
  ```

## Usage

1. Start `rtl_tcp`:
  ```sh
  rtl_tcp &
  ```

2. Run `rtlamr` to read meter data:
  ```sh
  rtlamr | python rtlamr_to_influxdb.py
  ```

## Configuration

Edit the `.env` file to set your InfluxDB connection details and other parameters.

INFLUXDB_URL = "http://influxdb.local:8086"
INFLUXDB_TOKEN = "YOUR_TOKEN_HERE"
INFLUXDB_ORG = "YOUR_ORG_HERE"
INFLUXDB_BUCKET = "YOUR_BUCKET_HERE"

## License

This project is licensed under the MIT License.