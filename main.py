#!/usr/bin/env python
import asyncio
import sys
import os
import bson
import websockets
import argparse
import logging
import serial.tools.list_ports
from central_dispatch import get_dispatch_handler


config = {}


async def central_dispatch(websocket, path):
    while True:
        data = await websocket.recv()
        logging.info("[Message 📦]: Received of length: {} and type: {}".format(
            len(data), type(data)))
        try:
            data = bson.BSON.decode(data)
        except:
            logging.error(
                "[Error]: Error while parsing bson to dict, only bson encoded")
        else:
            logging.info(
                "Finally received the message from the websocket client")
            data["serial_port"] = config["serial_port"]
            dispatch_handler = get_dispatch_handler()
            await dispatch_handler.handle(websocket, path, data)


def main(host: str, port: int, serial_port: str):
    config["serial_port"] = serial_port
    if sys.platform == "win32" and sys.version_info >= (3, 8, 0):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    event_loop = asyncio.get_event_loop()

    start_server = websockets.serve(
        central_dispatch, host=host, port=port, max_size=2**32)

    logging.info('[Start]: Connection started!')

    event_loop.run_until_complete(start_server)
    event_loop.run_forever()


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s : %(process)d : %(thread)d : %(message)s",
        handlers=[logging.FileHandler("iwidc.log"), logging.StreamHandler()]
    )

    comports = [comport.device for comport in serial.tools.list_ports.comports()]
    comports.append('test')
    # ask user to enter the serial port
    parser = argparse.ArgumentParser(
        description='Desktop bridge for idf-web to flash and monitor esp-32 chip')
    parser.add_argument("--port",
                        choices=comports,
                        required=True, type=str, help="Comport where you want to flash or monitor")

    args = parser.parse_args()
    try:
        main("127.0.0.1", 3362, args.port)
    except websockets.exceptions.WebSocketException:
        logging.warning("[idf-web-ide]: Connection Closed OK 🖐🏼")
    except KeyboardInterrupt:
        logging.info('[Exit]: Bye!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except OSError as err:
        logging.error("OS error: {0}".format(err))
    except Exception as err:
        logging.error("Unhandled Exception: {0}".format(err))

