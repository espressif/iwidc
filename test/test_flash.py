from dispatches import flash_dispatch
import unittest


class TestFlash(unittest.TestCase):
    def test_esptool_params(self):
        flash = flash_dispatch.FlashDispatchHandler()
        params = flash.get_esptool_args("test")
        expected = [
            "-p", "test",
            "-b", "115200",
            "--after", "hard_reset",
            "write_flash",
            "--flash_mode", "dio",
            "--flash_size", "detect",
            "--flash_freq", "40m"
        ]
        self.assertListEqual(params, expected)
