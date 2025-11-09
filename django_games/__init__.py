#!/usr/bin/env python
import itertools
import re
from collections.abc import Iterable
from contextlib import contextmanager
from gettext import NullTranslations
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    TypedDict,
    Union,
    cast,
    overload,
)

from asgiref.local import Local
from django.utils.encoding import force_str
from django.utils.translation import override, trans_real

from django_games.conf import settings

from .base import GamesBase

if TYPE_CHECKING:
    from django_stubs_ext import StrPromise

    class ComplexGameName(TypedDict):
        name: "StrPromise"
        names: "List[StrPromise]"
        alpha3: str
        numeric: int
        ioc_code: str

    GameName = Union[
        StrPromise,  # type: ignore
        ComplexGameName,
    ]
    GameCode = Union[str, int, None]


try:
    import pyuca  # type: ignore

    collator = pyuca.Collator()

    # Use UCA sorting if it's available.
    def sort_key(item: Tuple[str, str]) -> Any:
        return collator.sort_key(item[1])

except ImportError:
    # Fallback if the UCA sorting is not available.
    import unicodedata

    # Cheap and dirty method to sort against ASCII characters only.
    def sort_key(item: Tuple[str, str]) -> Any:
        return (
            unicodedata.normalize("NFKD", item[1])
            .encode("ascii", "ignore")
            .decode("ascii")
        )


_translation_state = Local()


class EmptyFallbackTranslator(NullTranslations):
    def gettext(self, message: str) -> str:
        if not getattr(_translation_state, "fallback", True):
            # Interrupt the fallback chain.
            return ""
        return super().gettext(message)


@contextmanager
def no_translation_fallback():
    if not settings.USE_I18N:
        yield
        return
    # Ensure the empty fallback translator has been installed.
    catalog = trans_real.catalog()
    original_fallback = catalog._fallback  # type: ignore
    if not isinstance(original_fallback, EmptyFallbackTranslator):
        empty_fallback_translator = EmptyFallbackTranslator()
        empty_fallback_translator._fallback = original_fallback  # type: ignore
        catalog._fallback = empty_fallback_translator  # type: ignore
    # Set the translation state to not use a fallback while inside this context.
    _translation_state.fallback = False
    try:
        yield
    finally:
        _translation_state.fallback = True


class AltCodes(NamedTuple):
    alpha3: str
    numeric: Optional[int]


class GameTuple(NamedTuple):
    code: str
    name: str

    def __repr__(self) -> str:
        """
        Display the repr as a standard tuple for better backwards
        compatibility with outputting this in a template.
        """
        return f"({self.code!r}, {self.name!r})"


class Games(GamesBase):
    """
    An object containing a list of ISO3166-1 games.

    Iterating this object will return the games as namedtuples (of
    the game ``code`` and ``name``), sorted by name.
    """

    _games: Dict[str, "GameName"]
    _alt_codes: Dict[str, AltCodes]

    def get_option(self, option: str):
        """
        Get a configuration option, trying the options attribute first and
        falling back to a Django project setting.
        """
        value = getattr(self, option, None)
        if value is not None:
            return value
        return getattr(settings, f"GAMES_{option.upper()}")

    @property
    def games(self) -> Dict[str, "GameName"]:
        """
        Return the a dictionary of games, modified by any overriding
        options.

        The result is cached so future lookups are less work intensive.
        """
        if not hasattr(self, "_games"):
            only: Iterable[Union[str, Tuple[str, StrPromise]]] = self.get_option("only")
            only_choices = True
            # Originally used ``only`` as a dict, still supported.
            if only and not isinstance(only, dict):
                for item in only:
                    if isinstance(item, str):
                        only_choices = False
                        break
            self._shadowed_names: Dict[str, List[StrPromise]] = {}
            if only and only_choices:
                self._games = dict(only)  # type: ignore
            else:
                # Local import so that games aren't loaded into memory
                # until first used.
                from django_games.data import GAMES

                games_dict = dict(GAMES)
                if only:
                    self._games = {}
                    for item in only:
                        if isinstance(item, str):
                            self._games[item] = games_dict[item]
                        else:
                            key, value = item
                            self._games[key] = value
                else:
                    self._games = games_dict.copy()  # type: ignore
                if self.get_option("common_names"):
                    for code, name in self.COMMON_NAMES.items():
                        if code in self._games:
                            self._games[code] = name
                override: Dict[str, Union[GameName, None]] = self.get_option(
                    "override"
                )
                if override:
                    _games = cast(
                        "Dict[str, Union[GameName, None]]", self._games.copy()
                    )
                    _games.update(override)
                    self._games = {
                        code: name
                        for code, name in _games.items()
                        if name is not None
                    }

                if self.get_option("common_names"):
                    for code in self.COMMON_NAMES:
                        if code in self._games and code not in override:
                            self._shadowed_names[code] = [games_dict[code]]
                for code, names in self.OLD_NAMES.items():
                    if code in self._games and code not in override:
                        game_shadowed = self._shadowed_names.setdefault(code, [])
                        game_shadowed.extend(names)

            self.games_first = []
            first: List[str] = self.get_option("first") or []
            for code in first:
                code = self.alpha2(code)
                if code in self._games:
                    self.games_first.append(code)
        return self._games

    @games.deleter
    def games(self):
        """
        Reset the games cache in case for some crazy reason the settings or
        internal options change. But surely no one is crazy enough to do that,
        right?
        """
        if hasattr(self, "_games"):
            del self._games
        if hasattr(self, "_alt_codes"):
            del self._alt_codes
        if hasattr(self, "_ioc_codes"):
            del self._ioc_codes
        if hasattr(self, "_shadowed_names"):
            del self._shadowed_names

    @property
    def alt_codes(self) -> Dict[str, AltCodes]:
        if not hasattr(self, "_alt_codes"):
            # Again, local import so data is not loaded unless it's needed.
            from django_games.data import ALT_CODES

            self._alt_codes = ALT_CODES  # type: ignore
            altered = False
            for code, game in self.games.items():
                if isinstance(game, dict) and (
                    "alpha3" in game or "numeric" in game
                ):
                    if not altered:
                        self._alt_codes = self._alt_codes.copy()
                        altered = True
                    alpha3, numeric = self._alt_codes.get(code, ("", None))
                    if "alpha3" in game:
                        alpha3 = game["alpha3"]
                    if "numeric" in game:
                        numeric = game["numeric"]
                    self._alt_codes[code] = AltCodes(alpha3, numeric)
        return self._alt_codes

    @property
    def ioc_codes(self) -> Dict[str, str]:
        if not hasattr(self, "_ioc_codes"):
            from django_games.ioc_data import ISO_TO_IOC

            self._ioc_codes = ISO_TO_IOC
            altered = False
            for code, game in self.games.items():
                if isinstance(game, dict) and "ioc_code" in game:
                    if not altered:
                        self._ioc_codes = self._ioc_codes.copy()
                        altered = True
                    self._ioc_codes[code] = game["ioc_code"]
        return self._ioc_codes

    @property
    def shadowed_names(self):
        if not getattr(self, "_shadowed_names", False):
            # Getting games populates shadowed names.
            self.games  # noqa: B018
        return self._shadowed_names

    def translate_code(self, code: str, ignore_first: Optional[List[str]] = None):
        """
        Return translated games for a game code.
        """
        game = self.games[code]
        if isinstance(game, dict):
            names = game["names"] if "names" in game else [game["name"]]
        else:
            names = [game]
        if ignore_first and code in ignore_first:
            names = names[1:]
        for name in names:
            yield self.translate_pair(code, name)

    def translate_pair(self, code: str, name: Optional["GameName"] = None):
        """
        Force a game to the current activated translation.

        :returns: ``GameTuple(code, translated_game_name)`` namedtuple
        """
        if name is None:
            name = self.games[code]
        if isinstance(name, dict):
            if "names" in name:
                fallback_names: List[StrPromise] = name["names"][1:]
                name = name["names"][0]
            else:
                fallback_names = []
                name = name["name"]
        else:
            fallback_names = self.shadowed_names.get(code, [])
        if fallback_names:
            with no_translation_fallback():
                game_name = force_str(name)
                # Check if there's an older translation available if there's no
                # translation for the newest name.
                if not game_name:
                    for fallback_name in fallback_names:
                        fallback_name_str = force_str(fallback_name)
                        if fallback_name_str:
                            game_name = fallback_name_str
                            break
            if not game_name:
                # Use the translation's fallback game name.
                game_name = force_str(name)
        else:
            game_name = force_str(name)
        return GameTuple(code, game_name)

    def __iter__(self):
        """
        Iterate through games, sorted by name.

        Each game record consists of a namedtuple of the two letter
        ISO3166-1 game ``code`` and short ``name``.

        The sorting happens based on the thread's current translation.

        Games that are in ``settings.GAMES_FIRST`` will be
        displayed before any sorted games (in the order provided),
        and are only repeated in the sorted list if
        ``settings.GAMES_FIRST_REPEAT`` is ``True``.

        The first games can be separated from the sorted list by the
        value provided in ``settings.GAMES_FIRST_BREAK``.
        """
        # Initializes games_first, so needs to happen first.
        games = self.games

        # Yield games that should be displayed first.
        games_first = (self.translate_pair(code) for code in self.games_first)

        if self.get_option("first_sort"):
            games_first = sorted(games_first, key=sort_key)

        yield from games_first

        if self.games_first:
            first_break = self.get_option("first_break")
            if first_break:
                yield GameTuple("", force_str(first_break))

        # Force translation before sorting.
        ignore_first = None if self.get_option("first_repeat") else self.games_first
        games = tuple(
            itertools.chain.from_iterable(
                self.translate_code(code, ignore_first) for code in games
            )
        )

        # Return sorted game list.
        yield from sorted(games, key=sort_key)

    def alpha2(self, code: "GameCode") -> str:
        """
        Return the normalized game code when passed any type of ISO 3166-1
        game code.

        Overridden games objects may actually have game codes that are
        not two characters (for example, "GB-WLS"), so the returned length of
        the code is not guaranteed.

        If no match is found, returns an empty string.
        """
        code_str = force_str(code).upper()
        # Check if the code exists directly in games first, before trying
        # to resolve it as an alternative code (alpha3/numeric). This allows
        # custom game codes in GAMES_OVERRIDE to work correctly, even
        # if they match the format of alternative codes (issue #474).
        if code_str in self.games:
            return code_str

        find_index: Optional[int]
        find_value: Union[str, int, None]

        if code_str.isdigit():
            find_index = 1
            find_value = int(code_str)
        elif len(code_str) == 3:
            find_index = 0
            find_value = code_str
        else:
            find_index = None
            find_value = None
        if find_index is not None:
            code_str = ""
            for alpha2, alt_codes in self.alt_codes.items():
                if alt_codes[find_index] == find_value:
                    code_str = alpha2
                    break
        if code_str in self.games:
            return code_str
        return ""

    def name(self, code: "GameCode") -> str:
        """
        Return the name of a game, based on the code.

        If no match is found, returns an empty string.
        """
        alpha2 = self.alpha2(code)
        if alpha2 not in self.games:
            return ""
        return self.translate_pair(alpha2)[1]

    @overload
    def by_name(
        self,
        game: str,
        *,
        regex: Literal[False] = False,
        language: str = "en",
        insensitive: bool = True,
    ) -> str: ...

    @overload
    def by_name(
        self,
        game: str,
        *,
        regex: Literal[True],
        language: str = "en",
        insensitive: bool = True,
    ) -> Set[str]: ...

    def by_name(
        self,
        game: str,
        *,
        regex: bool = False,
        language: str = "en",
        insensitive: bool = True,
    ) -> Union[str, Set[str]]:
        """
        Fetch a game's ISO3166-1 two letter game code from its name.

        An optional language parameter is also available. Warning: This depends
        on the quality of the available translations.

        If no match is found, returns an empty string.

        If ``regex`` is set to True, then rather than returning a string
        containing the matching game code or an empty string, a set of
        matching game codes is returned.

        If ``insensitive`` is set to False (True by default), then the search
        will be case sensitive.

        ..warning:: Be cautious about relying on this returning a game code
            (especially with any hard-coded string) since the ISO names of
            games may change over time.
        """
        code_list = set()
        if regex:
            re_match = re.compile(game, insensitive and re.IGNORECASE)
        elif insensitive:
            game = game.lower()
        with override(language):
            for code, check_game in self.games.items():
                if isinstance(check_game, dict):
                    if "names" in check_game:
                        check_names: List[StrPromise] = check_game["names"]
                    else:
                        check_names = [check_game["name"]]
                else:
                    check_names = [check_game]
                for name in check_names:
                    if regex:
                        if re_match.search(str(name)):
                            code_list.add(code)
                    else:
                        if insensitive:
                            if game == name.lower():
                                return code
                        else:
                            if game == name:
                                return code
                if code in self.shadowed_names:
                    for shadowed_name in self.shadowed_names[code]:
                        if regex:
                            if re_match.search(str(shadowed_name)):
                                code_list.add(code)
                        else:
                            if insensitive:
                                shadowed_name = shadowed_name.lower()
                            if game == shadowed_name:
                                return code
        if regex:
            return code_list
        return ""

    def alpha3(self, code: "GameCode") -> str:
        """
        Return the ISO 3166-1 three letter game code matching the provided
        game code.

        If no match is found, returns an empty string.
        """
        alpha2 = self.alpha2(code)
        try:
            alpha3 = self.alt_codes[alpha2][0]
        except KeyError:
            alpha3 = ""
        return alpha3 or ""

    @overload
    def numeric(self, code: Union[str, int, None]) -> Optional[int]: ...

    @overload
    def numeric(self, code: Union[str, int, None], padded=True) -> Optional[str]: ...

    def numeric(self, code: Union[str, int, None], padded: bool = False):
        """
        Return the ISO 3166-1 numeric game code matching the provided
        game code.

        If no match is found, returns ``None``.

        :param padded: Pass ``True`` to return a 0-padded three character
            string, otherwise an integer will be returned.
        """
        alpha2 = self.alpha2(code)
        try:
            num = self.alt_codes[alpha2][1]
        except KeyError:
            num = None
        if num is None:
            return None
        if padded:
            return f"{num:03d}"
        return num

    def ioc_code(self, code: "GameCode") -> str:
        """
        Return the International Olympic Committee three letter code matching
        the provided ISO 3166-1 game code.

        If no match is found, returns an empty string.
        """
        alpha2 = self.alpha2(code)
        return self.ioc_codes.get(alpha2, "")

    def __len__(self):
        """
        len() used by several third party applications to calculate the length
        of choices. This will solve a bug related to generating fixtures.
        """
        count = len(self.games)
        # Add first games, and the break if necessary.
        count += len(self.games_first)
        if self.games_first and self.get_option("first_break"):
            count += 1
        return count

    def __bool__(self):
        return bool(self.games)

    def __contains__(self, code):
        """
        Check to see if the games contains the given code.
        """
        return code in self.games

    def __getitem__(self, index):
        """
        Some applications expect to be able to access members of the field
        choices by index.
        """
        try:
            return next(itertools.islice(self.__iter__(), index, index + 1))
        except TypeError:
            return list(
                itertools.islice(self.__iter__(), index.start, index.stop, index.step)
            )


games = Games()
