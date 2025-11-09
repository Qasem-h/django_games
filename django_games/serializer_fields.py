from typing import Any

from django.utils.encoding import force_str
from rest_framework import serializers

from django_games import games


class GameField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.game_dict = kwargs.pop("game_dict", None)
        self.name_only = kwargs.pop("name_only", None)
        field_games = kwargs.pop("games", None)
        self.games = field_games or games
        super().__init__(
            self.games,  # type: ignore
            *args,
            **kwargs,
        )

    def to_representation(self, obj):
        code = self.games.alpha2(obj)
        if not code:
            return ""
        if self.name_only:
            return force_str(self.games.name(obj))
        if not self.game_dict:
            return code
        return {"code": code, "name": force_str(self.games.name(obj))}

    def to_internal_value(self, data: Any):
        if not self.allow_blank and data == "":
            self.fail("invalid_choice", input=data)

        if isinstance(data, dict):
            data = data.get("code")
        game = self.games.alpha2(data)
        if data and not game:
            game = self.games.by_name(force_str(data))
            if not game:
                self.fail("invalid_choice", input=data)
        return game
