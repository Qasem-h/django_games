# django_games/graphql/types.py

import graphene  # type: ignore


class Game(graphene.ObjectType):
    """
    GraphQL type representing a game entry, similar to Country type in django-countries.
    """

    name = graphene.String(description="Full game name, e.g. 'World of Warcraft'.")
    code = graphene.String(description="Two-character game code, e.g. 'WC'.")
    alpha3 = graphene.String(
        description="Three-character game code, similar to ISO alpha-3 format."
    )
    numeric = graphene.Int(
        description="Numeric identifier for the game (if applicable)."
    )
    ioc_code = graphene.String(
        description="Optional IOC-style short game identifier."
    )

    @staticmethod
    def resolve_name(game, info):
        """Return the display name of the game."""
        return getattr(game, "name", None)

    @staticmethod
    def resolve_code(game, info):
        """Return the two-character code of the game."""
        return getattr(game, "code", None)

    @staticmethod
    def resolve_alpha3(game, info):
        """Return the three-character code of the game."""
        return getattr(game, "alpha3", None)

    @staticmethod
    def resolve_numeric(game, info):
        """Return the numeric identifier of the game."""
        return getattr(game, "numeric", None)

    @staticmethod
    def resolve_ioc_code(game, info):
        """Return the IOC code of the game."""
        return getattr(game, "ioc_code", None)
