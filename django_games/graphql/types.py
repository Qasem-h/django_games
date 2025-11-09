import graphene  # type: ignore


class Game(graphene.ObjectType):
    name = graphene.String(description="Game name")
    code = graphene.String(description="Game code")


    @staticmethod
    def resolve_name(game, info):
        return game.name

    @staticmethod
    def resolve_code(game, info):
        return game.code
