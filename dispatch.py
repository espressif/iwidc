from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class Dispatch(ABC):
    @abstractmethod
    def set_next(self, handler: Dispatch) -> Dispatch:
        pass

    @abstractmethod
    async def handle(self, ws, path: str, message: dict) -> Optional[bool]:
        pass

    @abstractmethod
    async def handle_internal(self, ws, path: str, message: dict) -> Optional[bool]:
        pass


class DispatchHandler(Dispatch):
    _next_handler: Dispatch = None
    _path: str = None
    _websocket = None

    def set_next(self, handler: Dispatch) -> Dispatch:
        self._next_handler = handler
        return handler

    async def handle(self, ws, path: str, message: dict) -> bool:
        if self._path == path:
            return await self.handle_internal(ws, path, message)
        elif self._next_handler:
            return await self._next_handler.handle(ws, path, message)
        return None
