import bson
import uuid

class MessageProtocol:
    _message = None
    def __init__(self, messageType: str):
        self._message = {
            "messageType": messageType,
            "version": "0.0.1",
            "uuid": str(uuid.uuid4())
        }
    def add(self, key: str, val):
        self._message[key] = val
    def encode(self):
        return bson.BSON.encode(self._message)
