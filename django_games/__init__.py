#!/usr/bin/env python
import itertools
import re
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Union,
    overload,
)

from django.utils.encoding import force_str
from django.utils.translation import get_language, override
from typing_extensions import Literal

from django_games.conf import settings

from .base import GamesBase

try:
    import pyuca  # type: ignore

    collator = pyuca.Collator()

    # Use UCA sorting if it's available.
    def sort_key(item):
        return collator.sort_key(item[1])

except ImportError:
    # Fallback if the UCA sorting is not available.
    import unicodedata

    # Cheap and dirty method to sort against ASCII characters only.
    def sort_key(item):
        return (
            unicodedata.normalize("NFKD", item[1])
            .encode("ascii", "ignore")
            .decode("ascii")
        )


GameCode = Union[str, int, None]


class GameTuple(NamedTuple):
    code: str
    name: str

    def __repr__(self):
        return f"({self.code!r}, {self.name!r})"


class Games(GamesBase):


    _games: Dict[str, Union[str, Dict]]

    def get_option(self, option: str):
        value = getattr(self, option, None)
        if value is not None:
            return value
        return getattr(settings, f"GAMES_{option.upper()}")

    @property
    def games(self) -> Dict[str, Union[str, dict]]:

        if not hasattr(self, "_games"):
            only: Iterable[Union[str, Tuple[str, str]]] = self.get_option("only")
            only_choices = True
            if only:
                if not isinstance(only, dict):
                    for item in only:
                        if isinstance(item, str):
                            only_choices = False
                            break
            self._shadowed_names: Dict[str, List[str]] = {}
            if only and only_choices:
                self._games = dict(only)  # type: ignore
            else:

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
                override: Dict[str, Union[str, dict]] = self.get_option("override")
                if override:
                    self._games.update(override)
                    self._games = dict(
                        (code, name)
                        for code, name in self._games.items()
                        if name is not None
                    )

            self.games_first = []
            first: List[str] = self.get_option("first") or []
            for code in first:
                code = self.alpha2(code)
                if code in self._games:
                    self.games_first.append(code)
        return self._games

    @games.deleter
    def games(self):
  
        if hasattr(self, "_games"):
            del self._games
        if hasattr(self, "_shadowed_names"):
            del self._shadowed_names

    @property
    def shadowed_names(self):
        if not getattr(self, "_shadowed_names", False):
            # Getting games populates shadowed names.
            self.games
        return self._shadowed_names

    def translate_code(self, code: str, ignore_first: List[str] = None):
        """
        Return translated games for a game code.
        """
        game = self.games[code]
        if isinstance(game, dict):
            if "names" in game:
                names = game["names"]
            else:
                names = [game["name"]]
        else:
            names = [game]
        if ignore_first and code in ignore_first:
            names = names[1:]
        for name in names:
            yield self.translate_pair(code, name)

    def translate_pair(self, code: str, name: Union[str, Dict] = None):
   
        if name is None:
            name = self.games[code]
        if isinstance(name, dict):
            if "names" in name:
                game_name: str = name["names"][0]
                fallback_names: List[str] = name["names"][1:]
            else:
                game_name = name["name"]
                fallback_names = []
        else:
            game_name = name
            fallback_names = self.shadowed_names.get(code, [])
        language = get_language()
        if language and language.split("-")[0] != "en" and fallback_names:

            with override("en"):
                source_name = force_str(game_name)
            game_name = force_str(game_name)
            if game_name == source_name:
                for fallback_name in fallback_names:
                    with override("en"):
                        source_fallback_name = force_str(fallback_name)
                    fallback_name = force_str(fallback_name)
                    if fallback_name != source_fallback_name:
                        game_name = fallback_name
                        break
        else:
            game_name = force_str(game_name)
        return GameTuple(code, game_name)

    def __iter__(self):

        games = self.games

        games_first = (self.translate_pair(code) for code in self.games_first)

        if self.get_option("first_sort"):
            games_first = sorted(games_first, key=sort_key)

        for item in games_first:
            yield item

        if self.games_first:
            first_break = self.get_option("first_break")
            if first_break:
                yield GameTuple("", force_str(first_break))
        ignore_first = None if self.get_option("first_repeat") else self.games_first
        games = tuple(
            itertools.chain.from_iterable(
                self.translate_code(code, ignore_first) for code in games
            )
        )

        # Return sorted game list.
        for item in sorted(games, key=sort_key):
            yield item

    def alpha2(self, code: GameCode) -> str:
        code_str = force_str(code).upper()
  
        if code_str in self.games:
            return code_str
        return ""

    def name(self, code: GameCode) -> str:

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
    ) -> str:
        ...

    @overload
    def by_name(
        self,
        game: str,
        *,
        regex: Literal[True],
        language: str = "en",
        insensitive: bool = True,
    ) -> Set[str]:
        ...

    def by_name(
        self,
        game: str,
        *,
        regex: bool = False,
        language: str = "en",
        insensitive: bool = True,
    ) -> Union[str, Set[str]]:

        code_list = set()
        if regex:
            re_match = re.compile(game, insensitive and re.IGNORECASE)
        elif insensitive:
            game = game.lower()
        with override(language):
            for code, check_game in self.games.items():
                if isinstance(check_game, dict):
                    if "names" in check_game:
                        check_names: List[str] = check_game["names"]
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
                            name = name.lower()
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

    def __len__(self):
  
        count = len(self.games)
        count += len(self.games_first)
        if self.games_first and self.get_option("first_break"):
            count += 1
        return count

    def __bool__(self):
        return bool(self.games)

    def __contains__(self, code):
  
        return code in self.games

    def __getitem__(self, index):

        try:
            return next(itertools.islice(self.__iter__(), index, index + 1))
        except TypeError:
            return list(
                itertools.islice(self.__iter__(), index.start, index.stop, index.step)
            )


games = Games()
