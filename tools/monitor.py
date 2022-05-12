import asyncio
import serial
import threading
import logging
from time import sleep
from singleton import Singleton


class Monitor(metaclass=Singleton):
    _port = None
    _serial = None
    _on_message_callback = None
    _thread = None

    def __init__(self, port: str, on_message_callback):
        self._port = port
        self._on_message_callback = on_message_callback

    def is_monitoring(self):
        if self._serial:
            return self._serial.is_open
        return False

    def stop(self):
        if self.is_monitoring:
            logging.debug("[{}]: Stoping the Serial Monitoring at port {}".format(
                __file__, self._port))
            pass

    async def start(self):
        if self.is_monitoring() is False:
            logging.debug("[{}]: Starting serial monitor".format(__file__))
            self._serial = serial.Serial()
            self._serial.port = self._port
            self._serial.timeout = 1
            self._serial.baudrate = 115200
            try:
                self._serial.open()
            except Exception:
                logging.error("[{}]: Failed to open the serial port {}".format(
                    __file__, self._port))
            else:
                logging.info(
                    "[{}]: Established connection with the Chip".format(__file__))
                self._thread = threading.Thread(
                    target=self.send_message_from_chip)
                self._thread.start()
                return self._thread

    def send_message_from_chip(self):
        while True:
            data = self._serial.readline()
            logging.debug("[{}]: From_Chip: {}".format(__file__, data))
            if callable(self._on_message_callback):
                asyncio.run(self._on_message_callback(data))

    def send_message_to_chip(self, message: str):
        if self.is_monitoring:
            logging.debug("[{}]: To_Chip: {}".format(__file__, message))
            self._serial.write(message.encode('utf8'))
            self._serial.flush()


def on_message(message: str):
    print(message)


if __name__ == "__main__":
    m = Monitor("/dev/cu.usbserial-00101414B", on_message)
    if m.is_monitoring() is False:
        m.start()
    sleep(20)
    m.stop()
