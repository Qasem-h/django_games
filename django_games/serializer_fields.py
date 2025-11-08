from typing import Any, Optional

from django.utils.encoding import force_str
from rest_framework import serializers

from django_games import games


class GameField(serializers.ChoiceField):
    """
    Custom DRF field for serializing/deserializing MMORPG game codes.

    Examples:
        - Input: "WOW" → Output: "World of Warcraft"
        - Input: "World of Warcraft" → Output: "WOW"
        - Input: {"code": "WOW", "name": "World of Warcraft"} → same mapping
    """

    def __init__(
        self,
        *args,
        game_dict: bool = False,
        name_only: bool = False,
        field_games: Optional[Any] = None,
        **kwargs,
    ):
        self.game_dict = game_dict
        self.name_only = name_only
        self.games = field_games or games
        super().__init__(choices=self.games, *args, **kwargs)

    def to_representation(self, value: Any) -> Any:
        code = self.games.alpha2(value)
        if not code:
            return ""
        name = force_str(self.games.name(value))
        if self.name_only:
            return name
        if self.game_dict:
            return {"code": code, "name": name}
        return code

    def to_internal_value(self, data: Any) -> str:
        if not self.allow_blank and data == "":
            self.fail("invalid_choice", input=data)

        # Handle dict input { "code": "WOW" }
        if isinstance(data, dict):
            data = data.get("code")

        if not data:
            self.fail("invalid_choice", input=data)

        # Try resolving by code first
        game_code = self.games.alpha2(data)
        if game_code:
            return game_code

        # Try resolving by name next
        game_code = self.games.by_name(force_str(data))
        if not game_code:
            self.fail("invalid_choice", input=data)

        return game_code
