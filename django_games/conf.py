from typing import Any, Dict, List

import django.conf


class AppSettings:

    def __getattribute__(self, attr: str):
        if attr == attr.upper():
            try:
                return getattr(django.conf.settings, attr)
            except AttributeError:
                pass
        return super().__getattribute__(attr)


class Settings(AppSettings):
    GAMES_ICON_URL = "icons/{code}.gif"
    GAMES_COMMON_NAMES = True
    GAMES_OVERRIDE: Dict[str, Any] = {}
    GAMES_ONLY: Dict[str, Any] = {}
    GAMES_FIRST: List[str] = []
    GAMES_FIRST_REPEAT = False
    GAMES_FIRST_BREAK = None
    GAMES_FIRST_SORT = False


settings = Settings()
