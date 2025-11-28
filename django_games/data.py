#!/usr/bin/env python
from typing import TYPE_CHECKING, Dict

from django_games.base import GamesBase

if TYPE_CHECKING:
    from django_stubs_ext import StrPromise

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    def _(message: str) -> "StrPromise":
        return message  # type: ignore


# =======================================================
# CANONICAL GAME CODES — COMMUNITY STANDARD (NOV 2025)
# CLEANED FOR REAL RMT MARKET
# =======================================================
GAMES = {

    "WOW": _("World of Warcraft"),
    "TWW": _("World of Warcraft: The War Within"),
    "MDN": _("World of Warcraft: Midnight"),
    "ERA": _("World of Warcraft Classic Era"),
    "HC": _("World of Warcraft Classic Hardcore"),
    "SOD": _("World of Warcraft: Season of Discovery"),
    "MOPC": _("World of Warcraft: Mists of Pandaria Classic"),
    "WOWP": _("World of Warcraft Private Server"),
    "ANV": _("World of Warcraft Classic Anniversary Edition"),
    "TBCCA": _("World of Warcraft: The Burning Crusade Classic Anniversary"),

    "D2R": _("Diablo II: Resurrected"),
    "D4": _("Diablo IV"),

    "AION": _("Aion"),
    "AIC": _("Aion Classic"),
    "ALB": _("Albion Online"),
    "BDO": _("Black Desert Online"),
    "ESO": _("The Elder Scrolls Online"),
    "EVE": _("EVE Online"),
    "FFXIV": _("Final Fantasy XIV"),
    "GW2": _("Guild Wars 2"),
    "LARK": _("Lost Ark"),

    "LEP": _("Last Epoch"),
    "L2": _("Lineage II"),
    "MO2": _("Mortal Online 2"),
    "NWA": _("New World: Aeternum"),
    "POE": _("Path of Exile"),
    "POE2": _("Path of Exile 2"),
    "RS3": _("RuneScape 3"),
    "OSRS": _("Old School RuneScape"),
    "TRS": _("Tarisland"),
    "TNL": _("Throne and Liberty"),

    "EFT": _("Escape from Tarkov"),
    "ARC": _("ARC Raiders"),
}



# =======================================================
# ALT CODES — CLEANED & ALIGNED
# =======================================================
ALT_CODES = {

    "WOW": ("WOW", 100),
    "TWW": ("TWW", 102),
    "MDN": ("MDN", 103),

    "ERA": ("ERA", 201),
    "HC": ("HC", 202),
    "SOD": ("SOD", 203),
    "MOPC": ("MOPC", 213),

    "WOWP": ("WOWP", 240),
    "ANV": ("ANV", 241),
    "TBCCA": ("TBCCA", 215),

    "D2R": ("D2R", 300),
    "D4": ("D4", 303),

    "AION": ("AION", 400),
    "AIC": ("AIC", 401),
    "ALB": ("ALB", 402),
    "BDO": ("BDO", 403),
    "ESO": ("ESO", 413),
    "EVE": ("EVE", 414),
    "FFXIV": ("FFXIV", 415),
    "GW2": ("GW2", 416),
    "LARK": ("LARK", 417),

    "LEP": ("LEP", 418),
    "L2": ("L2", 419),
    "MO2": ("MO2", 423),
    "NWA": ("NWA", 427),
    "POE": ("POE", 429),
    "POE2": ("POE2", 430),
    "RS3": ("RS3", 433),
    "OSRS": ("OSRS", 434),
    "TRS": ("TRS", 438),
    "TNL": ("TNL", 440),

    "EFT": ("EFT", 509),
    "ARC": ("ARC", 525),
}


# =======================================================
# FILE GEN / DEBUG (unchanged)
# =======================================================
def self_generate(
    output_filename: str, filename: str = "iso3166-1.csv"
):  # pragma: no cover
    import csv
    import re
    import unicodedata

    games = []
    with open(filename) as csv_file:
        for row in csv.reader(csv_file):
            name = row[0].rstrip("*")
            name = re.sub(r"\(the\)", "", name)
            name = re.sub(r" +\[(.+)\]", r" (\1)", name)
            if name:
                games.append((name, row[1], row[2], int(row[3])))
    with open(__file__) as source_file:
        contents = source_file.read()

    def sort_key(row):
        return (
            unicodedata.normalize("NFKD", row[0])
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    games = sorted(games, key=sort_key)

    match = re.match(
        r"(.*\nGAMES(?:: [^\n]+)? = \{\n)(.*?)(\n\}.*)", contents, re.DOTALL
    )
    if not match:
        raise ValueError('Expected a "GAMES =" section in the source file!')
    bits = match.groups()
    game_list = []
    for game_row in games:
        name = game_row[0].replace('"', r"\"").strip()
        game_list.append(f'    "{game_row[1]}": _("{name}"),')
    content = bits[0]
    content += "\n".join(game_list)

    alt_match = re.match(
        r"(.*\nALT_CODES(?:: [^\n]+)? = \{\n)(.*)(\n\}.*)", bits[2], re.DOTALL
    )
    if not alt_match:
        raise ValueError('Expected an "ALT_CODES =" section in the source file!')
    alt_bits = alt_match.groups()
    alt_list = [
        f'    "{game_row[1]}": ("{game_row[2]}", {game_row[3]}),'
        for game_row in games
    ]
    content += alt_bits[0]
    content += "\n".join(alt_list)
    content += alt_bits[2]

    with open(output_filename, "w") as output_file:
        output_file.write(content)
    return games


def check_common_names() -> None:
    common_names_missing = set(GamesBase.COMMON_NAMES) - set(GAMES)
    if common_names_missing:
        print("")
        print("The following common names do not match an official game code:")
        for code in sorted(common_names_missing):
            print(f"  {code}")


if __name__ == "__main__":
    games = self_generate(__file__)
    print(f"Wrote {len(games)} games.\n")
    check_common_names()
