from typing import Any


class MethodBaseClass:
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {}

    def find_source(self, mic_data):
        pass

    def get_settings(self):
        pass

    def set_setting(self, setting, value):
        pass
