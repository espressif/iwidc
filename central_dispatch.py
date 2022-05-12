import logging
from dispatch import DispatchHandler, Dispatch
from dispatches import flash_dispatch, monitor_dispatch


class UnhandledDispatch(DispatchHandler):
    def set_next(self, handler: Dispatch) -> Dispatch:
        # throw exception
        pass

    async def handle(self, ws, path: str, message: dict) -> bool:
        logging.error(
            "[Unhandled]: No dispatch handler could handle {}".format(path))

    async def handle_internal(self, ws, path: str, message: dict) -> bool:
        pass


class InitialDispatchHandler(DispatchHandler):
    async def handle(self, ws, path: str, message: dict) -> bool:
        result = await self.handle_internal(ws, path, message)
        if result == True:
            return await super().handle(ws, path, message)
        else:
            logging.error(
                "[Error]: Message protocol mismatch, canceling and exiting...")
            exit(1)

    async def handle_internal(self, ws, path, message: dict) -> bool:
        logging.info("[Internal]: Got Request to be parsed {}".format(path))
        return True
        # check the validity of message protocol and other protocol specification


def get_dispatch_handler() -> Dispatch:
    initial_handler = InitialDispatchHandler()
    flash = flash_dispatch.FlashDispatchHandler()
    monitor = monitor_dispatch.MonitorDispatchHandler()
    unhandled_handler = UnhandledDispatch()

    initial_handler.set_next(flash).set_next(
        monitor).set_next(unhandled_handler)

    return initial_handler
