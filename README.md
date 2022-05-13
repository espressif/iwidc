[![GitHub release](https://img.shields.io/github/release/espressif/iwidc.svg?style=flat-square&label=Latest%20release)](https://github.com/espressif/iwidc/releases/latest)
[![Release workflow](https://img.shields.io/github/workflow/status/espressif/iwidc/Release?label=Release%20Status)](https://github.com/espressif/iwidc/actions?workflow=Release)

# ESP IDF Web IDE Desktop Companion (ESP-IWIDC)

ESP IWI-DC is a remote flasher, monitor and band of tools for the client side application for bridging the web-ide based flash and monitor.

For the best results use IWIDC with Chrome Web Browser.

## Getting started

- `git clone --recursive https://github.com/espressif/iwidc.git`
- `cd esp-iwidc`
- Use python 3.x or create a new virtual environment.
- `pip3 install -r requirements.txt`
- Run `python3 main.py` to see available serial ports.
- Run `python3 main.py --port [SERIAL_PORT_OF_ESP_32]`

Use python 3.x:
- `pip3 install -r requirements.txt`

Run:
- `python3 main.py --port [SERIAL_PORT_OF_ESP_32]`


### With Pipenv (to isolate environment of the package / easy install)

Clone repo:
- `git clone --recursive https://github.com/espressif/iwidc.git`
- `cd esp-iwidc`

Use python 3.x:
- `python3 -m pip install pipenv`
- `python3 -m pipenv lock`
- `python3 -m pipenv install --ignore-pipfile`
- `python3 -m pipenv shell`

Run:
- `python3 main.py` to see available serial ports.
- `python3 main.py --port [SERIAL_PORT_OF_ESP_32]` to start desktop companion.


## Windows users - How to find your port number
- connect device
- open command line and type `mode`

Other option: Open Device manager and expand Ports (COM & LPT). 
 
If device is not visible, check Espressif docs article [Establish Serial Connection with ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/establish-serial-connection.html)

### Testing

In a terminal run `python3 -m unittest discover -v test "*test*.py"` or from Visual Studio Code with `ms-python.python` Python extension, you can run test and see the output in the `Python Test Log` output.

## Build executable with PyInstaller

Run (either using system python or the virtual environment from before):

- `pip install pyinstaller`
- `pyinstaller --onefile main.py`

and find the executable in `dist/main.exe`.


### Windows driver installation

- download and unzip [IDF-ENV](https://github.com/espressif/idf-env)
- open a PowerShell under Administrator
- run `idf-env driver install --espressif --ftdi --silabs`

- unplug & plug device to let the system apply the driver
