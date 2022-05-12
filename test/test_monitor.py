
import asyncio
import unittest
import tools.monitor
from unittest.mock import patch


class MockSerial:
    port = "init_port"
    timeout = 1
    baudrate = 9600
    is_open = False
    curr_line = ""

    def open(self):
        self.is_open = True
        return True

    def close():
        return True

    def readline():
        return "message from mock serial"

    def write(self, msg: str):
        self.curr_line = msg
        return "written message: {}".format(msg)

    def flush(self):
        return None


class TestMonitor(unittest.TestCase):
    msg = None

    async def sendMessage(self, msg: str):
        print(msg)
        self.msg = msg

    def test_monitor_send_message(self):
        async def async_test():
            with patch("tools.monitor.serial.Serial") as mock_serial:
                mock_serial.return_value = MockSerial
                mon = tools.monitor.Monitor("test", self.sendMessage)
                mon._serial = MockSerial()
                mon._serial.port = "test"
                mon._serial.timeout = 1
                mon._serial.baudrate = 115200
                mon._serial.open()
                mon.send_message_to_chip("test-message")
                self.assertEqual(mon._serial.curr_line, "test-message".encode("utf8"))
        return asyncio.get_event_loop().run_until_complete(async_test())
