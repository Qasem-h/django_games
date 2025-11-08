from typing import Any, Dict, List

import django.conf


class AppSettings:
    """
    A holder for app-specific default settings that allows overriding via
    the project's settings.
    """

    def __getattribute__(self, attr: str):
        if attr == attr.upper():
            try:
                return getattr(django.conf.settings, attr)
            except AttributeError:
                pass
        return super().__getattribute__(attr)


class Settings(AppSettings):
    GAMES_ICON_URL = "icons/{code}.svg"
    """
    The URL for a icon.

    It can either be relative to the static url, or an absolute url.

    The location is parsed using Python's string formatting and is passed the
    following arguments:

        * code
        * code_upper

    For example: ``GAMES_ICON_URL = 'icons/16x10/{code_upper}.png'``
    """

    GAMES_COMMON_NAMES = True
    """
    Whether to use the common names for some games, as opposed to the
    official ISO name.

    Some examples:
        "Bolivia" instead of "Bolivia, Plurinational State of"
        "South Korea" instead of "Korea (the Republic of)"
        "Taiwan" instead of "Taiwan (Province of China)"
    """

    GAMES_OVERRIDE: Dict[str, Any] = {}
    """
    A dictionary of names to override the defaults.

    Note that you will need to handle translation of customised game names.

    Setting a game's name to ``None`` will exclude it from the game list.
    For example::

        GAMES_OVERRIDE = {
            'NZ': _('Middle Earth'),
            'AU': None
        }
    """

    GAMES_ONLY: Dict[str, Any] = {}
    """
    Similar to GAMES_OVERRIDE
    A dictionary of names to include in selection.

    Note that you will need to handle translation of customised game names.

    For example::

        GAMES_ONLY = {
            'NZ': _('Middle Earth'),
            'AU': _('Desert'),
        }
    """

    GAMES_FIRST: List[str] = []
    """
    Games matching the game codes provided in this list will be shown
    first in the games list (in the order specified) before all the
    alphanumerically sorted games.
    """

    GAMES_FIRST_REPEAT = False
    """
    Games listed in :attr:`GAMES_FIRST` will be repeated again in the
    alphanumerically sorted list if set to ``True``.
    """

    GAMES_FIRST_BREAK = None
    """
    Games listed in :attr:`GAMES_FIRST` will be followed by a null
    choice with this title (if set) before all the alphanumerically sorted
    games.
    """

    GAMES_FIRST_SORT = False
    """
    Games listed in :attr:`GAMES_FIRST` will be alphanumerically
    sorted based on their translated name instead of relying on their
    order in :attr:`GAMES_FIRST`.
    """


settings = Settings()
