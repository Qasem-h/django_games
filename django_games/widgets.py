import copy
from typing import List, Union
from urllib import parse as urlparse

from django.forms import widgets
from django.utils.html import escape
from django.utils.functional import Promise
from django.utils.safestring import mark_safe

from django_games.conf import settings



ChoiceList = List[List[Union[int, str]]]


class LazyChoicesMixin:
    
    def get_choices(self) -> ChoiceList:
        if isinstance(self._choices, Promise):
            self._choices: ChoiceList = list(self._choices)
        return self._choices

    def set_choices(self, value: ChoiceList):
        self._set_choices(value)

    choices = property(get_choices, set_choices)

    def _set_choices(self, value: ChoiceList):
        self._choices = value


class LazySelectMixin(LazyChoicesMixin):
    
    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.attrs = self.attrs.copy()
        obj.choices = copy.copy(self._choices)
        memo[id(self)] = obj
        return obj


class LazySelect(LazySelectMixin, widgets.Select):  # type: ignore
    """
    A form Select widget that respects choices being a lazy object.
    """


class LazySelectMultiple(LazySelectMixin, widgets.SelectMultiple):  # type: ignore
    """
    A form SelectMultiple widget that respects choices being a lazy object.
    """