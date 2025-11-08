from django import template

from django_games.fields import Game, games

register = template.Library()


@register.simple_tag
def get_game(code):
    return Game(code=code)


@register.simple_tag
def get_games():
    return list(games)
