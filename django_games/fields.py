import re
import sys
from typing import Any, Iterable, Optional, Tuple, Type, Union, cast

import django
from django import forms
from django.contrib.admin.filters import FieldListFilter
from django.core import checks, exceptions
from django.db.models import lookups
from django.db.models.fields import BLANK_CHOICE_DASH, CharField
from django.utils.encoding import force_str
from django.utils.functional import lazy

from django_games import Games, games, filters, widgets
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
except ImportError:  # Python <3.8
    import pkg_resources

    _entry_points = pkg_resources.iter_entry_points("django_games.Game")

EXTENSIONS = {ep.name: ep.load() for ep in _entry_points}  # type: ignore


class TemporaryEscape:
    __slots__ = ["game", "original_escape"]

    def __init__(self, game):
        self.game = game

    def __bool__(self):
        return self.game._escape

    def __enter__(self):
        self.original_escape = self.game._escape
        self.game._escape = True

    def __exit__(self, type, value, traceback):
        self.game._escape = self.original_escape


class Game:
    """
    Represents a game entry (formerly had icon properties — removed).
    """

    def __init__(
        self,
        code: str,
        str_attr: str = "code",
        custom_games: Optional[Games] = None,
    ):
        self._escape = False
        self._str_attr = str_attr
        if custom_games is games:
            custom_games = None
        self.custom_games = custom_games
        # Convert to normalized code if exists in registry
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
    def escape(self):
        return TemporaryEscape(self)

    def maybe_escape(self, text) -> str:
        return text  # Escape removed (icons removed)

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

    # ------------------------------------------------------------
    # ✅ ICON PROPERTIES REMOVED CLEANLY (icon, icon_css, unicode_icon)
    # ------------------------------------------------------------

    # @property
    # def icon(self):  REMOVED
    # @property
    # def icon_css(self): REMOVED
    # @property
    # def unicode_icon(self): REMOVED

    # @staticmethod
    # def game_from_ioc(...): REMOVED (icon-specific)

    @property
    def ioc_code(self):
        return self.games.ioc_code(self.code)

    def __getattr__(self, attr):
        if attr in EXTENSIONS:
            return EXTENSIONS[attr](self)
        raise AttributeError()


class GameDescriptor:
    """
    Descriptor for GameField. (icon removed)
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            return self
        # Handle deferred fields
        if self.field.name not in instance.__dict__:
            instance.refresh_from_db(fields=[self.field.name])
        value = instance.__dict__[self.field.name]
        if self.field.multiple:
            return [self.game(code) for code in value]
        return self.game(value)

    def game(self, code):
        return Game(
            code=code,
            str_attr=self.field.games_str_attr,
            custom_games=self.field.games,
        )

    def __set__(self, instance, value):
        value = self.field.get_clean_value(value)
        instance.__dict__[self.field.name] = value


class LazyChoicesMixin(widgets.LazyChoicesMixin):
    if django.VERSION < (5, 0):

        def _set_choices(self, value):
            super()._set_choices(value)
            self.widget.choices = value


_Choice = Tuple[Any, str]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]


class LazyTypedChoiceField(LazyChoicesMixin, forms.TypedChoiceField):
    choices: Any
    widget = widgets.LazySelect


class LazyTypedMultipleChoiceField(
    LazyChoicesMixin, forms.TypedMultipleChoiceField
):
    choices: Any
    widget = widgets.LazySelectMultiple


class GameField(CharField):
    """
    Main model field for games.
    Icon-related arguments removed.
    """

    descriptor_class = GameDescriptor
    games: Games

    def __init__(self, *args: Any, **kwargs: Any):
        games_class: Type[Games] = kwargs.pop("games", None)
        self.games = games_class() if games_class else games
        self.games_str_attr = kwargs.pop("games_str_attr", "code")
        self.blank_label = kwargs.pop("blank_label", None)
        self.multiple = kwargs.pop("multiple", None)
        self.multiple_unique = kwargs.pop("multiple_unique", True)
        self.multiple_sort = kwargs.pop("multiple_sort", True)

        # dynamic choices
        if django.VERSION >= (5, 0):
            kwargs["choices"] = lambda: self.games
        else:
            kwargs["choices"] = self.games

        # Automatic max_length = longest game code
        if "max_length" not in kwargs:
            if self.multiple:
                kwargs["max_length"] = (
                    len(self.games)
                    - 1
                    + sum(len(code) for code in self.games.games)
                )
            else:
                kwargs["max_length"] = max(len(code) for code in self.games.games)

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
            hint += " (add blank=True if you want empty value allowed)"
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
        value = super(CharField, self).pre_save(*args, **kwargs)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        value = self.get_clean_value(value)
        if self.multiple:
            value = ",".join(value) if value else ""
        return super(CharField, self).get_prep_value(value)

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
            if self.multiple_unique and c in seen:
                continue
            seen.add(c)
            cleaned_value.append(c)

        if self.multiple_sort:
            cleaned_value = sorted(cleaned_value)
        return cleaned_value

    def deconstruct(self):
        name, path, args, kwargs = super(CharField, self).deconstruct()
        kwargs.pop("choices", None)
        if self.multiple:
            kwargs["multiple"] = self.multiple
        if not self.multiple_unique:
            kwargs["multiple_unique"] = False
        if not self.multiple_sort:
            kwargs["multiple_sort"] = False
        if self.games is not games:
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

        def get_choices(
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
                include_blank=include_blank, blank_choice=blank_choice, *args, **kwargs
            )

        get_choices = lazy(get_choices, list)

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
        output = []
        for item in value:
            output.append(super().to_python(item))
        return output

    def validate(self, value, model_instance):
        if not self.multiple:
            return super().validate(value, model_instance)

        if not self.editable:
            return

        if value:
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

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def get_lookup(self, lookup_name):
        if (
            not self.multiple
            and lookup_name
            in (
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
            )
        ):
            lookup_name = f"game_{lookup_name}"
        return super().get_lookup(lookup_name)


@GameField.register_lookup
class ExactNameLookup(lookups.Exact):
    lookup_name = "game_name"
    insensitive: bool = False

    def get_prep_lookup(self):
        return cast(GameField, self.lhs.output_field).games.by_name(
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
            options = cast(GameField, self.lhs.output_field).games.by_name(
                value, regex=True, insensitive=self.insensitive
            )
            if len(self.rhs) == 2 and (
                self.rhs == self.rhs.upper() or self.insensitive
            ):
                options.add(self.rhs.upper())
            return options
        return super().get_prep_lookup()


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
