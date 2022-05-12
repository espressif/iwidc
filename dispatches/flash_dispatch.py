import os
import logging
import esptool
from dispatch import DispatchHandler
from message.message_protocol import MessageProtocol


class FlashDispatchHandler(DispatchHandler):
    _TMP_DIR_NAME = "bins"

    def __init__(self):
        self._path = "/flash"

    def get_esptool_args(self, serial_port: str):
        esptool_params = [
                "-p", serial_port,
                "-b", "115200",
                "--after", "hard_reset",
                "write_flash",
                "--flash_mode", "dio",
                "--flash_size", "detect",
                "--flash_freq", "40m"
            ]
        return esptool_params

    async def handle_internal(self, ws, path: str, message: dict) -> bool:
        if message["messageType"] == "flash":
            self.create_temp_dir(self._TMP_DIR_NAME)

            logging.info("[Flash ⚡️]: New request received")

            esptool_params = self.get_esptool_args(message["serial_port"])
            sections = message["sections"]

            for section in sections:
                bin_path = os.path.join(self._TMP_DIR_NAME, section["name"])
                with open(bin_path, 'wb') as fp:
                    fp.write(bytes(section["bin"]["data"]))
                esptool_params.append(section["offset"])
                esptool_params.append(bin_path)

            msg = None

            try:
                esptool.main(esptool_params)
            except Exception as e:
                msg = MessageProtocol("flash_error")
                msg.add("error", str(e))
                logging.error("❌ [Flash ⚡️]: Failed!")
            else:
                msg = MessageProtocol("flash_done")
                logging.info("[Flash ⚡️]: Done!")
            finally:
                encoded_msg = msg.encode()
                await ws.send(encoded_msg)
        else:
            logging.info(
                "[Flash ⚠️]: Can't be processed by the Flash Dispatch")

    def create_temp_dir(self, folder_name: str) -> bool:
        try:
            os.mkdir(folder_name)
            return True
        except:
            return False
