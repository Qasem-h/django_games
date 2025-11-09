import copy
from typing import Dict, List, Union

import django
from django.forms import widgets
from django.utils.functional import Promise
from django.utils.html import escape
from django.utils.safestring import mark_safe


ChoiceList = List[List[Union[int, str]]]


# ------------------------------------------------------------
# Lazy Choice Mixins (unchanged, required by Django 5.x logic)
# ------------------------------------------------------------

class LazyChoicesMixin:
    if django.VERSION < (5, 0):

        def get_choices(self) -> ChoiceList:
            """
            Resolve lazy choices at render time.
            """
            if isinstance(self._choices, Promise):
                self._choices = list(self._choices)
            return self._choices

        def set_choices(self, value: ChoiceList):
            self._set_choices(value)

        choices = property(get_choices, set_choices)

        def _set_choices(self, value: ChoiceList):
            self._choices = value


class LazySelectMixin(LazyChoicesMixin):
    attrs: Dict[str, str]

    if django.VERSION < (5, 0):
        def __deepcopy__(self, memo):
            """
            Ensure select widgets copy cleanly with lazy choices.
            """
            obj = copy.copy(self)
            obj.attrs = self.attrs.copy()
            obj.choices = copy.copy(self._choices)
            memo[id(self)] = obj
            return obj

    def use_required_attribute(self, initial):
        """
        Check if ANY choice is blank — not just the first.
        Required for correctness with custom game lists.
        """

        # No required attribute for hidden widgets.
        if self.is_hidden:
            return False

        # Multiple select: required always ok.
        if self.allow_multiple_selected:
            return True

        # Check any choice has an empty value.
        return any(
            self._choice_has_empty_value(choice)
            for choice in self.choices
        )


# ------------------------------------------------------------
# Lazy <select> widgets
# ------------------------------------------------------------

class LazySelect(LazySelectMixin, widgets.Select):
    """
    Standard <select> widget with lazy choice support.
    """


class LazySelectMultiple(LazySelectMixin, widgets.SelectMultiple):
    """
    Standard <select multiple> widget with lazy choice support.
    """


# ------------------------------------------------------------
# GAME SELECT WIDGET (CLEAN — 100% NO ICONS)
# ------------------------------------------------------------

class GameSelectWidget(LazySelect):
    """
    Clean version of Game select widget.
    Icons removed: NO <img>, NO JS handler, NO URL building.
    """

    def __init__(self, *args, **kwargs):
        # Original layout included: {widget}<img src="{game.icon}">
        # Clean version includes only the dropdown widget.
        self.layout = "{widget}"
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        from django_games.fields import Game

        attrs = attrs or {}

        # Render base <select>
        widget_render = super().render(name, value, attrs, renderer=renderer)

        # Convert raw string into Game object (keeps name logic working)
        game = value if isinstance(value, Game) else Game(value or "")

        # Escape context active while rendering
        with game.escape:
            return mark_safe(self.layout.format(widget=widget_render))
