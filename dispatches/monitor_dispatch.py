import os
import logging
from dispatch import DispatchHandler
from message.message_protocol import MessageProtocol
from tools.monitor import Monitor


class MonitorDispatchHandler(DispatchHandler):
    m: Monitor = None

    def __init__(self):
        self._path = "/monitor"

    async def sendMessage(self, ws, msg: MessageProtocol):
        await ws.send(msg.encode())

    async def handle_internal(self, ws, path: str, message: dict) -> bool:
        async def on_message_callback(msg):
            m = MessageProtocol("monitor")
            m.add("monitor-type", "message-from-chip")
            m.add("message", msg)

            await self.sendMessage(ws, m)

        if message["messageType"] == "monitor":
            logging.info("[Monitor 👀]: New request received")
            if message["monitor-type"] == "start":
                if not self.m:
                    self.m = Monitor(
                        message["serial_port"], on_message_callback)
                    await self.m.start()
                else:
                    await self.m.start()
            elif message["monitor-type"] == "stop":
                if self.m and self.m.is_monitoring() == True:
                    self.m.stop()
                    self.m = None
            elif message["monitor-type"] == "message-to-chip":
                if self.m and self.m.is_monitoring() == True:
                    self.m.send_message_to_chip(message["message"])
                else:
                    self.m = Monitor(
                        message["serial_port"], on_message_callback)
                    self.m.send_message_to_chip(message["message"])
            else:
                logging.info(
                    "[Monitor 👀]: Error, unrecognized message type, skipping!")
                logging.debug(message)
        else:
            logging.warning(
                "[Monitor ⚠️]: Can't be processed by the Monitor Dispatch")
            errMsg = MessageProtocol("monitor")
            errMsg.add("message", "messageType is not supported")
            await self.sendMessage(ws, errMsg)
