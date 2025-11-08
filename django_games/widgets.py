import copy
from typing import Any, Dict, List, Union
from urllib import parse as urlparse

import django
from django.forms import widgets
from django.utils.functional import Promise
from django.utils.html import escape
from django.utils.safestring import mark_safe

from django_games.conf import settings

# JavaScript handler that updates the displayed icon when a game is selected.
GAME_CHANGE_HANDLER = (
    "var e=document.getElementById('icon_' + this.id);"
    "if (e) e.src = '%s'"
    ".replace('{code}', this.value.toLowerCase() || '__')"
    ".replace('{code_upper}', this.value.toUpperCase() || '__');"
)

ChoiceList = List[List[Union[int, str]]]


# === Lazy Choices Support (for compatibility with Django < 5.0) ===
class LazyChoicesMixin:
    if django.VERSION < (5, 0):

        def get_choices(self) -> ChoiceList:
            """Resolve lazy choices only when accessed."""
            if isinstance(self._choices, Promise):
                self._choices = list(self._choices)
            return self._choices

        def set_choices(self, value: ChoiceList) -> None:
            self._choices = value

        choices = property(get_choices, set_choices)


class LazySelectMixin(LazyChoicesMixin):
    attrs: Dict[str, str]

    if django.VERSION < (5, 0):
        def __deepcopy__(self, memo: Dict[int, Any]):
            obj = copy.copy(self)
            obj.attrs = self.attrs.copy()
            obj.choices = copy.copy(self._choices)
            memo[id(self)] = obj
            return obj

    def use_required_attribute(self, initial: Any) -> bool:
        """
        Override Django’s default logic to allow for blank separators in game lists.
        Prevents incorrect omission of `required` when a blank option isn’t first.
        """
        if self.is_hidden:
            return False
        if self.allow_multiple_selected:
            return True
        return any(
            self._choice_has_empty_value(choice)
            for choice in self.choices
        )


class LazySelect(LazySelectMixin, widgets.Select):
    """Single-select widget that supports lazy translated choices."""


class LazySelectMultiple(LazySelectMixin, widgets.SelectMultiple):
    """Multi-select widget that supports lazy translated choices."""


# === Game Selection Widget with Icon Preview ===
class GameSelectWidget(LazySelect):
    """
    A form Select widget that displays the game’s icon next to the dropdown
    and updates dynamically when the user selects a different game.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.layout = kwargs.pop("layout", None) or (
            '{widget}<img class="game-select-icon" id="{icon_id}" '
            'style="margin: 6px 4px 0" src="{game.icon}">'
        )
        super().__init__(*args, **kwargs)

    def render(self, name: str, value: Any, attrs: Dict[str, Any] | None = None, renderer=None) -> str:
        from django_games.fields import Game

        attrs = attrs or {}
        widget_id = attrs.get("id", "")
        if widget_id:
            icon_id = f"icon_{widget_id}"
            attrs["onchange"] = GAME_CHANGE_HANDLER % urlparse.urljoin(
                settings.STATIC_URL, settings.GAMES_ICON_URL
            )
        else:
            icon_id = ""

        widget_render = super().render(name, value, attrs, renderer=renderer)
        game = value if isinstance(value, Game) else Game(value or "__")

        with game.escape:
            return mark_safe(
                self.layout.format(
                    widget=widget_render,
                    game=game,
                    icon_id=escape(icon_id),
                )
            )
