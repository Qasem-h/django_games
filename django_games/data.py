#!/usr/bin/env python
import glob
import os
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
# =======================================================
GAMES: "Dict[str, StrPromise]" = {
    # === WORLD OF WARCRAFT RETAIL ===
    "WOW": _("World of Warcraft"),
    "DFL": _("World of Warcraft: Dragonflight"),
    "TWW": _("World of Warcraft: The War Within"),
    "MDN": _("World of Warcraft: Midnight"),
    "TLT": _("World of Warcraft: The Last Titan"),

    # === WORLD OF WARCRAFT CLASSIC (RENAMED) ===
    "WOWC": _("World of Warcraft Classic"),
    "ERA": _("World of Warcraft Classic Era"),
    "HC": _("World of Warcraft Classic Hardcore"),
    "SOD": _("World of Warcraft: Season of Discovery"),

    # === CLASSIC EXPANSIONS (UNCHANGED) ===
    "TBCC": _("World of Warcraft: The Burning Crusade Classic"),
    "WOTLKC": _("World of Warcraft: Wrath of the Lich King Classic"),
    "CATAC": _("World of Warcraft: Cataclysm Classic"),
    "MOPC": _("World of Warcraft: Mists of Pandaria Classic"),
    "WODC": _("World of Warcraft: Warlords of Draenor Classic"),
    "LEGC": _("World of Warcraft: Legion Classic"),

    # === PRIVATE / SPECIAL ===
    "PRS": _("World of Warcraft Private Server"),
    "ANV": _("World of Warcraft Classic Anniversary Edition"),

    # === DIABLO SERIES ===
    "D1": _("Diablo"),
    "D2R": _("Diablo II: Resurrected"),
    "D3": _("Diablo III"),
    "D4": _("Diablo IV"),
    "D4VH": _("Diablo IV: Vessel of Hatred"),

    # === MAJOR MMORPGs ===
    "AION": _("Aion"),
    "AIC": _("Aion Classic"),
    "ALB": _("Albion Online"),
    "AA": _("ArcheAge"),
    "AAW": _("ArcheAge War"),
    "BNS": _("Blade & Soul"),
    "BNS2": _("Blade & Soul 2"),
    "BDO": _("Black Desert Online"),
    "BDM": _("Black Desert Mobile"),
    "CO": _("Conquer Online"),
    "CORE": _("Corepunk"),
    "DAD": _("Dark and Darker"),
    "EVE": _("EVE Online"),
    "ESO": _("The Elder Scrolls Online"),
    "FFXIV": _("Final Fantasy XIV: A Realm Reborn"),
    "GE": _("Granado Espada"),
    "GW2": _("Guild Wars 2"),

    # === LOST ARK RENAMED ===
    "LARK": _("Lost Ark"),

    "LEP": _("Last Epoch"),
    "L2": _("Lineage II"),
    "L2C": _("Lineage II Classic"),
    "SKY": _("Minecraft: Hypixel SkyBlock"),
    "MHW": _("Monster Hunter Wilds"),
    "MO2": _("Mortal Online 2"),
    "MOE": _("Myth of Empires"),
    "NST": _("Neo Steam: The Shattered Continent"),
    "NEW": _("New World"),
    "NWA": _("New World: Aeternum"),
    "PKMMO": _("PokeMMO"),
    "POE": _("Path of Exile"),
    "POE2": _("Path of Exile 2"),
    "RO": _("Ragnarok Online"),
    "RVD": _("Ravendawn"),
    "RS3": _("RuneScape 3"),
    "OSRS": _("Old School RuneScape"),
    "RPL": _("Rappelz Online"),
    "SRO": _("Silkroad Online"),
    "SWTOR": _("Star Wars: The Old Republic"),
    "TRS": _("Tarisland"),
    "TIB": _("Tibia"),
    "TL": _("Throne and Liberty"),
    "VR": _("V Rising"),

    # === FPS / SURVIVAL / ACTION ===
    "ABI": _("Arena Breakout: Infinite"),
    "APEX": _("Apex Legends"),
    "BS": _("Brawl Stars"),
    "COC": _("Clash of Clans"),
    "CR": _("Clash Royale"),
    "CS2": _("Counter-Strike 2"),
    "DBD": _("Dead by Daylight"),
    "D2": _("Destiny 2"),
    "DT": _("Warhammer 40,000: Darktide"),
    "EFT": _("Escape from Tarkov"),
    "FIN": _("THE FINALS"),
    "F76": _("Fallout 76"),
    "FH5": _("Forza Horizon 5"),
    "GEN": _("Genshin Impact"),
    "HSR": _("Honkai: Star Rail"),
    "HD": _("Hay Day"),
    "LOL": _("League of Legends"),
    "MS": _("MapleStory"),
    "NBA2K": _("NBA 2K"),
    "OH": _("Once Human"),
    "OW2": _("Overwatch 2"),
    "PAL": _("Palworld"),
    "PZ": _("Project Zomboid"),
    "QF": _("The Quinfall"),
    "REM2": _("Remnant II"),
    "RUST": _("Rust"),
    "SOT": _("Sea of Thieves"),
    "TF2": _("Team Fortress 2"),
    "TFD": _("The First Descendant"),
    "VAL": _("VALORANT"),
    "WF": _("Warframe"),
    "WW": _("Wuthering Waves"),
    "ZZZ": _("Zenless Zone Zero"),

    # === SPECIAL MMORPGs ===
    "AQW": _("AdventureQuest Worlds"),
    "ROR": _("Warhammer Online: Return of Reckoning"),
}


# =======================================================
# ALT_CODES — FULL BACKWARD + COMMON ALIASES (ZERO 404s)
# =======================================================
ALT_CODES: Dict[str, str] = {
    # Retail legacy expansions → retail bucket
    "WTB": "WOW", "WOT": "WOW", "CAT": "WOW", "MOP": "WOW",
    "WOD": "WOW", "LEG": "WOW", "BFA": "WOW", "SDL": "WOW",

    # Dragonflight alias
    "DFL": "DFL",

    # Classic aliases → NEW canonical code
    "CLASSIC": "WOWC",
    "WOWC": "WOWC",
    "CLA": "WOWC",

    # Hardcore aliases
    "HDC": "HC",
    "WHC": "HC",

    # Classic expansions
    "TBC": "TBCC", "WOTLK": "WOTLKC", "CATA": "CATAC",

    # Private servers
    "WOWP": "PRS",

    # Diablo
    "DIA": "D1", "DIR": "D2R", "DIT": "D3", "DIV": "D4", "VOH": "D4VH",

    # Final Fantasy XIV aliases
    "FF14": "FFXIV", "FFX": "FFXIV", "FF": "FFXIV",

    # Shooter/MOBA aliases
    "VALO": "VAL", "APX": "APEX", "OVW": "OW2", "OW": "OW2", "CSR": "CS2",

    # LOST ARK RENAMED (new canonical LARK)
    "LOSTARK": "LARK",
    "LA": "LARK",
    "LAR": "LARK",
    "LAK": "LARK",

    # Community shortcuts
    "PKM": "PKMMO",
    "POT": "POE2",
    "OSR": "OSRS",
    "RSC": "RS3",
    "TARI": "TRS",
    "LE": "LEP",
    "WOR": "ROR",

    # Mortal Online shortcuts
    "MO": "MO2",

    # Conquer Online variants
    "CO1": "CO",
    "CO2": "CO",

    # Palworld
    "PLW": "PAL",

    # The First Descendant
    "T1D": "TFD",

    # NBA 2K aliases
    "NBA": "NBA2K",
    "2K": "NBA2K",

    # Safety maps
    "MDN": "MDN",
    "TLT": "TLT",
    "D4VH": "D4VH",
}


def self_generate(
    output_filename: str, filename: str = "iso3166-1.csv"
):  # pragma: no cover
    """
    The following code can be used for self-generation of this file.

    It requires a UTF-8 CSV file containing the short ISO name and two letter
    game code as the first two columns.
    """
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

    # Sort games.
    def sort_key(row):
        return (
            unicodedata.normalize("NFKD", row[0])
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    games = sorted(games, key=sort_key)

    # Write games.
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
    # Write alt codes.
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
    # Generate file.
    with open(output_filename, "w") as output_file:
        output_file.write(content)
    return games


def check_icons(verbosity: int = 1):
    files = {}
    this_dir = os.path.dirname(__file__)
    for path in glob.glob(os.path.join(this_dir, "static", "icons", "*.gif")):
        files[os.path.basename(os.path.splitext(path)[0]).upper()] = path

    icons_missing = set(GAMES) - set(files)
    if icons_missing:  # pragma: no cover
        print("The following game codes are missing a icon:")
        for code in sorted(icons_missing):
            print(f"  {code} ({GAMES[code]})")
    elif verbosity:  # pragma: no cover
        print("All game codes have icons. :)")

    code_missing = set(files) - set(GAMES)
    # Special-case EU and __
    for special_code in ("EU", "__"):
        code_missing.discard(special_code)
    if code_missing:  # pragma: no cover
        print("")
        print("The following icons don't have a matching game code:")
        for path in sorted(code_missing):
            print(f"  {path}")


def check_common_names() -> None:
    common_names_missing = set(GamesBase.COMMON_NAMES) - set(GAMES)
    if common_names_missing:  # pragma: no cover
        print("")
        print("The following common names do not match an official game code:")
        for code in sorted(common_names_missing):
            print(f"  {code}")


if __name__ == "__main__":  # pragma: no cover
    games = self_generate(__file__)
    print(f"Wrote {len(games)} games.")

    print("")
    check_icons()
    check_common_names()
