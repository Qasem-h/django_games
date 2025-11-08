import re
import sys
from typing import TYPE_CHECKING, Any, Iterable, Optional, Tuple, Type, Union, cast
from urllib import parse as urlparse

if TYPE_CHECKING:
    from typing import overload

    from typing_extensions import Self

import django
from django import forms
from django.contrib.admin.filters import FieldListFilter
from django.core import checks, exceptions
from django.db.models import lookups
from django.db.models.fields import BLANK_CHOICE_DASH, CharField
from django.utils.encoding import force_str
from django.utils.functional import lazy
from django.utils.html import escape as escape_html

from django_games import Games, games, filters, ioc_data, widgets
from django_games.conf import settings

_entry_points: Iterable[Any]
try:
    import importlib.metadata

    if sys.version_info >= (3, 10):
        _entry_points = importlib.metadata.entry_points(
            group="django_games.Game"
        )
    else:
        _entry_points = importlib.metadata.entry_points().get(
            "django_games.Game", []
        )
except ImportError:  # Python <3.8  # pragma: no cover
    import pkg_resources  # type: ignore

    _entry_points = pkg_resources.iter_entry_points("django_games.Game")

EXTENSIONS = {ep.name: ep.load() for ep in _entry_points}  # type: ignore


class TemporaryEscape:
    __slots__ = ["game", "original_escape"]

    def __init__(self, game: "Game") -> None:
        self.game = game

    def __bool__(self) -> bool:
        return self.game._escape

    def __enter__(self) -> None:
        self.original_escape = self.game._escape
        self.game._escape = True

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        self.game._escape = self.original_escape


class Game:
    def __init__(
        self,
        code: str,
        icon_url: Optional[str] = None,
        str_attr: str = "code",
        custom_games: Optional[Games] = None,
    ):
        self.icon_url = icon_url
        self._escape = False
        self._str_attr = str_attr
        if custom_games is games:
            custom_games = None
        self.custom_games = custom_games
        # Attempt to convert the code to the alpha2 equivalent, but this
        # is not meant to be full validation so use the given code if no
        # match was found.
        self.code = self.games.alpha2(code) or code

    def __str__(self):
        return force_str(getattr(self, self._str_attr) or "")

    def __eq__(self, other):
        return force_str(self.code or "") == force_str(other or "")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(force_str(self))

    def __repr__(self):
        args = [f"code={self.code!r}"]
        if self.icon_url is not None:
            args.append(f"icon_url={self.icon_url!r}")
        if self._str_attr != "code":
            args.append(f"str_attr={self._str_attr!r}")
        return f"{self.__class__.__name__}({', '.join(args)})"

    def __bool__(self):
        return bool(self.code)

    def __len__(self):
        return len(force_str(self))

    @property
    def games(self):
        return self.custom_games or games

    @property
    def escape(self) -> TemporaryEscape:
        return TemporaryEscape(self)

    def maybe_escape(self, text) -> str:
        return escape_html(text) if self.escape else text

    @property
    def name(self) -> str:
        return self.maybe_escape(self.games.name(self.code))

    @property
    def alpha3(self) -> str:
        return self.games.alpha3(self.code)

    @property
    def numeric(self) -> Optional[int]:
        return self.games.numeric(self.code)

    @property
    def numeric_padded(self) -> Optional[str]:
        return self.games.numeric(self.code, padded=True)

    @property
    def icon(self) -> str:
        if not self.code:
            return ""
        icon_url = self.icon_url
        if icon_url is None:
            icon_url = settings.GAMES_ICON_URL
        url = icon_url.format(code_upper=self.code, code=self.code.lower())
        if not url:
            return ""
        url = urlparse.urljoin(settings.STATIC_URL, url)
        return self.maybe_escape(url)

    @property
    def icon_css(self) -> str:
        """
        Output the css classes needed to display an HTML element as a icon
        sprite.

        Requires the use of 'icons/sprite.css' or 'icons/sprite-hq.css'.
        Usage example::

            <i class="{{ ctry.icon_css }}" aria-label="{{ ctry.code }}></i>
        """
        if not self.code:
            return ""
        x, y = list(self.code.lower())
        return f"icon-sprite icon-{x} icon-_{y}"

    @property
    def unicode_icon(self):
        """
        Generate a unicode icon for the given game.

        The logic for how these are determined can be found at:

        https://en.wikipedia.org/wiki/Regional_Indicator_Symbol

        Currently, these glyphs appear to only be supported on OS X and iOS.
        """
        if not self.code:
            return ""

        # Don't really like magic numbers, but this is the code point for [A]
        # (Regional Indicator A), minus the code point for ASCII A. By adding
        # this to the uppercase characters making up the ISO 3166-1 alpha-2
        # codes we can get the icon.
        OFFSET = 127397
        points = [ord(x) + OFFSET for x in self.code.upper()]
        return chr(points[0]) + chr(points[1])

    @staticmethod
    def game_from_ioc(
        ioc_code: str, icon_url: Optional[str] = None
    ) -> Optional["Game"]:
        code = ioc_data.IOC_TO_ISO.get(ioc_code, "")
        if code == "":
            return None
        return Game(code, icon_url=icon_url)

    @property
    def ioc_code(self):
        return self.games.ioc_code(self.code)

    def __getattr__(self, attr):
        if attr in EXTENSIONS:
            return EXTENSIONS[attr](self)
        raise AttributeError


class MultipleGamesDescriptor:
    """
    A list-like wrapper that provides proper string representation for Django admin.

    This makes GameField(multiple=True) work correctly in admin list_display
    and readonly_fields by providing a comma-separated string of game names.

    Note: This does NOT inherit from list to avoid Django admin's special handling
    of list/tuple types in display_for_value, which would show codes instead of names.
    """

    def __init__(self, games_iter):
        self._games = list(games_iter)

    def __str__(self):
        """Return comma-separated game names for admin display."""
        if not self._games:
            return ""
        return ", ".join(str(game.name) for game in self._games)

    def __repr__(self):
        """Maintain list representation for debugging."""
        return f"[{', '.join(repr(game) for game in self._games)}]"

    def __iter__(self):
        """Allow iteration over games."""
        return iter(self._games)

    def __getitem__(self, index):
        """Allow indexing."""
        return self._games[index]

    def __len__(self):
        """Return number of games."""
        return len(self._games)

    def __bool__(self):
        """Return True if there are games."""
        return bool(self._games)

    def __eq__(self, other):
        """Check equality."""
        if isinstance(other, MultipleGamesDescriptor):
            return self._games == other._games
        return self._games == other


class GameDescriptor:
    """
    A descriptor for game fields on a model instance. Returns a Game when
    accessed so you can do things like::

        >>> from people import Person
        >>> person = Person.object.get(name='Chris')

        >>> person.game.name
        'New Zealand'

        >>> person.game.icon
        '/static/icons/nz.svg'
    """

    field: "GameField"

    def __init__(self, field: "GameField") -> None:
        self.field = field

    # Type-only overloads for descriptor protocol
    if TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> "Self": ...

        @overload
        def __get__(
            self, instance: Any, owner: Any
        ) -> Union[Game, MultipleGamesDescriptor]: ...

    def __get__(self, instance=None, owner=None):
        if instance is None:
            return self
        # Check in case this field was deferred.
        if self.field.name not in instance.__dict__:
            instance.refresh_from_db(fields=[self.field.name])
        value = instance.__dict__[self.field.name]
        if self.field.multiple:
            return MultipleGamesDescriptor(self.game(code) for code in value)
        return self.game(value)

    def game(self, code):
        return Game(
            code=code,
            icon_url=self.field.games_icon_url,
            str_attr=self.field.games_str_attr,
            custom_games=self.field.games,
        )

    def __set__(self, instance, value):
        value = self.field.get_clean_value(value)
        instance.__dict__[self.field.name] = value


class LazyChoicesMixin(widgets.LazyChoicesMixin):
    widget: Type[forms.widgets.ChoiceWidget]

    if django.VERSION < (5, 0):

        def _set_choices(self, value):
            """
            Also update the widget's choices.
            """
            super()._set_choices(value)
            self.widget.choices = value  # type: ignore


_Choice = Tuple[Any, str]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]


class LazyTypedChoiceField(LazyChoicesMixin, forms.TypedChoiceField):
    """
    A form TypedChoiceField that respects choices being a lazy object.
    """

    choices: Any
    widget = widgets.LazySelect


class LazyTypedMultipleChoiceField(LazyChoicesMixin, forms.TypedMultipleChoiceField):
    """
    A form TypedMultipleChoiceField that respects choices being a lazy object.
    """

    choices: Any
    widget = widgets.LazySelectMultiple


class GameField(CharField):
    """
    A game field for Django models that provides all ISO 3166-1 games as
    choices.
    """

    descriptor_class = GameDescriptor
    games: Games

    def __init__(self, *args: Any, **kwargs: Any):
        games_class: Type[Games] = kwargs.pop("games", None)
        self.games = games_class() if games_class else games
        self.games_icon_url = kwargs.pop("games_icon_url", None)
        self.games_str_attr = kwargs.pop("games_str_attr", "code")
        self.blank_label = kwargs.pop("blank_label", None)
        self.multiple = kwargs.pop("multiple", None)
        self.multiple_unique = kwargs.pop("multiple_unique", True)
        self.multiple_sort = kwargs.pop("multiple_sort", True)
        if django.VERSION >= (5, 0):
            # Use new lazy callable support
            kwargs["choices"] = lambda: self.games
        else:
            kwargs["choices"] = self.games
        if "max_length" not in kwargs:
            # Allow explicit max_length so migrations can correctly identify
            # changes in the multiple GameField fields when new games are
            # added to the available games dictionary.
            if self.multiple:
                kwargs["max_length"] = (
                    len(self.games.games)
                    - 1
                    + sum(len(code) for code in self.games.games)
                )
            else:
                kwargs["max_length"] = max(
                    len(code) for code in self.games.games
                )
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_multiple())
        return errors

    def _check_multiple(self):
        if not self.multiple or not self.null:
            return []

        hint = "Remove null=True argument on the field"
        if not self.blank:
            hint += " (just add blank=True if you want to allow no selection)"
        hint += "."

        return [
            checks.Error(
                "Field specifies multiple=True, so should not be null.",
                obj=self,
                id="django_games.E100",
                hint=hint,
            )
        ]

    def get_internal_type(self):
        return "CharField"

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def pre_save(self, *args, **kwargs):
        "Returns field's value just before saving."
        value = super(CharField, self).pre_save(*args, **kwargs)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        value = self.get_clean_value(value)
        if self.multiple:
            value = ",".join(value) if value else ""
        return super(CharField, self).get_prep_value(value)

    @property
    def flatchoices(self):
        """
        Override flatchoices to prevent admin choice lookups for multiple fields.

        For multiple=True fields, Django admin's display_for_field tries to
        look up the value in flatchoices. Since the value is a
        MultipleGamesDescriptor, we return None so Django skips the
        choice lookup and uses str() instead.
        """
        if self.multiple:
            return None
        return super().flatchoices

    def game_to_text(self, value):
        if hasattr(value, "code"):
            value = value.code
        if value is None:
            return None
        return force_str(value)

    def get_clean_value(self, value):
        if value is None:
            return None
        if not self.multiple:
            return self.game_to_text(value)
        if isinstance(value, (str, Game)):
            if isinstance(value, str) and "," in value:
                value = value.split(",")
            else:
                value = [value]
        else:
            try:
                iter(value)
            except TypeError:
                value = [value]
        cleaned_value = []
        seen = set()
        for c in value:
            c = self.game_to_text(c)
            if not c:
                continue
            if self.multiple_unique:
                if c in seen:
                    continue
                seen.add(c)
            cleaned_value.append(c)
        if self.multiple_sort:
            cleaned_value = sorted(cleaned_value)
        return cleaned_value

    def deconstruct(self):
        """
        Remove choices from deconstructed field, as this is the game list
        and not user editable.

        Not including the ``blank_label`` property, as this isn't database
        related.
        """
        name, path, args, kwargs = super(CharField, self).deconstruct()
        kwargs.pop("choices", None)
        if self.multiple:  # multiple determines the length of the field
            kwargs["multiple"] = self.multiple
        if not self.multiple_unique:
            kwargs["multiple_unique"] = False
        if not self.multiple_sort:
            kwargs["multiple_sort"] = False
        if self.games is not games:
            # Include the games class if it's not the default games
            # instance.
            kwargs["games"] = self.games.__class__
        return name, path, args, kwargs

    if django.VERSION >= (5, 0):

        def get_choices(
            self,
            include_blank=True,
            blank_choice=BLANK_CHOICE_DASH,
            limit_choices_to=None,
            ordering=(),
        ):
            if self.multiple:
                include_blank = False
            if self.blank_label is None:
                blank_choice = BLANK_CHOICE_DASH
            else:
                blank_choice = [("", self.blank_label)]
            return super().get_choices(
                include_blank=include_blank,
                blank_choice=blank_choice,
                limit_choices_to=limit_choices_to,
                ordering=ordering,
            )

    else:

        def _get_choices_legacy(
            self, include_blank=True, blank_choice=None, *args, **kwargs
        ):
            if blank_choice is None:
                if self.blank_label is None:
                    blank_choice = BLANK_CHOICE_DASH
                else:
                    blank_choice = [("", self.blank_label)]
            if self.multiple:
                include_blank = False
            return super().get_choices(
                *args, include_blank=include_blank, blank_choice=blank_choice, **kwargs
            )

        get_choices = lazy(_get_choices_legacy, list)

    def formfield(self, **kwargs):
        kwargs.setdefault(
            "choices_form_class",
            LazyTypedMultipleChoiceField if self.multiple else LazyTypedChoiceField,
        )
        if "coerce" not in kwargs:
            kwargs["coerce"] = super().to_python
        return super().formfield(**kwargs)

    def to_python(self, value):
        if not self.multiple:
            return super().to_python(value)
        if not value:
            return value
        if isinstance(value, str):
            value = value.split(",")
        # Store reference to parent's to_python for use in list comprehension
        # (super() doesn't work in comprehensions in Python 3.8)
        parent_to_python = super().to_python
        return [parent_to_python(v) for v in value if v]

    def validate(self, value, model_instance):
        """
        Use custom validation for when using a multiple games field.
        """
        if not self.multiple:
            return super().validate(value, model_instance)

        if not self.editable:
            # Skip validation for non-editable fields.
            return None

        if value and self.choices is not None:
            choices = [option_key for option_key, option_value in self.choices]
            for single_value in value:
                if single_value not in choices:
                    raise exceptions.ValidationError(
                        self.error_messages["invalid_choice"],
                        code="invalid_choice",
                        params={"value": single_value},
                    )

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages["blank"], code="blank")
        return None

    def value_to_string(self, obj):
        """
        Ensure data is serialized correctly.
        """
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def get_lookup(self, lookup_name):
        if not self.multiple and lookup_name in (
            "contains",
            "icontains",
            "startswith",
            "istartswith",
            "endswith",
            "iendswith",
            "regex",
            "iregex",
            "name",
            "iname",
        ):
            lookup_name = f"game_{lookup_name}"
        return super().get_lookup(lookup_name)


@GameField.register_lookup
class ExactNameLookup(lookups.Exact):
    lookup_name = "game_name"
    insensitive: bool = False

    def get_prep_lookup(self):
        return cast("GameField", self.lhs.output_field).games.by_name(
            force_str(self.rhs), insensitive=self.insensitive
        )

    def get_rhs_op(self, connection, rhs):
        return connection.operators["exact"] % rhs


@GameField.register_lookup
class IExactNameLookup(ExactNameLookup):
    lookup_name = "game_iname"
    insensitive: bool = True


class FullNameLookup(lookups.In):
    expr: str
    insensitive: bool = False
    escape_regex: bool = True

    def get_prep_lookup(self):
        if isinstance(self.rhs, str):
            value = self.expr.format(
                text=re.escape(self.rhs) if self.escape_regex else self.rhs
            )
            options = cast("GameField", self.lhs.output_field).games.by_name(
                value, regex=True, insensitive=self.insensitive
            )
            if len(self.rhs) == 2 and (
                self.rhs == self.rhs.upper() or self.insensitive
            ):
                options.add(self.rhs.upper())
            return options
        return super().get_prep_lookup()  # pragma: no cover


@GameField.register_lookup
class GameContains(FullNameLookup):
    lookup_name = "game_contains"
    expr = r"{text}"


@GameField.register_lookup
class GameIContains(GameContains):
    lookup_name = "game_icontains"
    insensitive = True


@GameField.register_lookup
class GameStartswith(FullNameLookup):
    lookup_name = "game_startswith"
    expr = r"^{text}"


@GameField.register_lookup
class GameIStartswith(GameStartswith):
    lookup_name = "game_istartswith"
    insensitive = True


@GameField.register_lookup
class GameEndswith(FullNameLookup):
    lookup_name = "game_endswith"
    expr = r"{text}$"


@GameField.register_lookup
class GameIEndswith(GameEndswith):
    lookup_name = "game_iendswith"
    insensitive = True


@GameField.register_lookup
class GameRegex(FullNameLookup):
    lookup_name = "game_regex"
    expr = r"{text}"
    escape_regex = False


@GameField.register_lookup
class GameIRegex(GameRegex):
    lookup_name = "game_iregex"
    insensitive = True


FieldListFilter.register(lambda f: isinstance(f, GameField), filters.GameFilter)
