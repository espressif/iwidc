import unittest
import asyncio
from message.message_protocol import MessageProtocol
from dispatches import monitor_dispatch
from unittest.mock import patch


class MockMonitor:
    is_monitor_started = False

    def __init__(self, port: str, on_message_callback):
        self._port = port
        self._on_message_callback = on_message_callback

    async def start(self):
        self.is_monitor_started = True
        if callable(self._on_message_callback):
            await self._on_message_callback("monitor has started")
        return True

    def is_monitoring(self):
        return self.is_monitor_started

    def send_message_to_chip(self, msg: str):
        return msg


class TestMonitorDispatch(unittest.TestCase):
    msg = None

    async def sendMessage(self, msg: MessageProtocol):
        self.msg = msg

    def test_monitor_dispatch(self):
        async def async_test():
            with patch.object(monitor_dispatch, "Monitor") as mock_monitor:
                mock_monitor.return_value = MockMonitor(
                    "test", self.sendMessage)
                msg = MessageProtocol("monitor")
                msg.add("monitor-type", "start")
                msg.add("serial_port", "test")
                dispatcher = monitor_dispatch.MonitorDispatchHandler()
                await dispatcher.handle_internal(None, "/monitor", msg._message)
                self.assertEqual(self.msg, "monitor has started")
        return asyncio.get_event_loop().run_until_complete(async_test())
