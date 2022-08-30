import glob
import os

from django_games.base import GamesBase

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    def _(x):
        return x


GAMES = {
    "NW":  _("New World"),
    "LA":  _("Lost Ark"),
    "D2":  _("Destiny 2"),
    "WWR": _("World of Warcraft"),
    "WWC": _("World of Warcraft Classic"),
    "POE": _("Path of Exile"),
    "F14": _("FINAL FANTASY XIV: A Realm Reborn"),
    "ESO": _("The Elder Scroll Online"),
    "OSR": _("Old School RuneScape"),
    "RS3": _("RuneScape 3"),
    "GW2": _("Guild Wars 2"),
    		
}


def self_generate(
    output_filename: str, filename: str = "iso3166-1.csv"
):  # pragma: no cover

    import csv
    import re
    import unicodedata
    
    games = []
    with open(filename, "r") as csv_file:
        for row in csv.reader(csv_file):
            name = row[0].rstrip("*")
            name = re.sub(r"\(the\)", "", name)
            name = re.sub(r" +\[(.+)\]", r" (\1)", name)
            if name:
                games.append((name, row[1], row[2], int(row[3])))
    with open(__file__, "r") as source_file:
        contents = source_file.read()
    # Sort games.
    def sort_key(row):

        return (
            unicodedata.normalize("NFKD", row[0])
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    games = sorted(games, key=sort_key)

    # Write games.
    match = re.match(r"(.*\nGAMES = \{\n)(.*?)(\n\}.*)", contents, re.DOTALL)
    if not match:
        raise ValueError('Expected a "GAMES =" section in the source file!')
    bits = match.groups()
    game_list = []
    for game_row in games:
        name = game_row[0].replace('"', r"\"").strip()
        game_list.append(f'    "{game_row[1]}": _("{name}"),')
    content = bits[0]
    content += "\n".join(game_list)

    # Generate file.
    with open(output_filename, "w") as output_file:
        output_file.write(content)
    return games



if __name__ == "__main__":  # pragma: no cover
    games = self_generate(__file__)
    print(f"Wrote {len(games)} games.")

    print("")
