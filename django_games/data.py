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


ALT_CODES = {
    # === WORLD OF WARCRAFT RETAIL (100s) ===
    "WOW": ("WOW", 100),
    "DFL": ("DFL", 101),
    "TWW": ("TWW", 102),
    "MDN": ("MDN", 103),
    "TLT": ("TLT", 104),

    # === WORLD OF WARCRAFT CLASSIC (200s) ===
    "WOWC": ("WOWC", 200),
    "ERA": ("ERA", 201),
    "HC": ("HC", 202),
    "SOD": ("SOD", 203),

    # === CLASSIC EXPANSIONS (210–230) ===
    "TBCC": ("TBCC", 210),
    "WOTLKC": ("WOTLKC", 211),
    "CATAC": ("CATAC", 212),
    "MOPC": ("MOPC", 213),
    "WODC": ("WODC", 214),
    "LEGC": ("LEGC", 215),

    # === PRIVATE / SPECIAL (240s) ===
    "PRS": ("PRS", 240),
    "ANV": ("ANV", 241),

    # === DIABLO SERIES (300s) ===
    "D1": ("D1", 300),
    "D2R": ("D2R", 301),
    "D3": ("D3", 302),
    "D4": ("D4", 303),
    "D4VH": ("D4VH", 304),

    # === MAJOR MMORPGS (400–499) ===
    "AION": ("AION", 400),
    "AIC": ("AIC", 401),
    "ALB": ("ALB", 402),
    "AA": ("AA", 403),
    "AAW": ("AAW", 404),
    "BNS": ("BNS", 405),
    "BNS2": ("BNS2", 406),
    "BDO": ("BDO", 407),
    "BDM": ("BDM", 408),
    "CO": ("CO", 409),
    "CORE": ("CORE", 410),
    "DAD": ("DAD", 411),
    "EVE": ("EVE", 412),
    "ESO": ("ESO", 413),
    "FFXIV": ("FFXIV", 414),
    "GE": ("GE", 415),
    "GW2": ("GW2", 416),
    "LARK": ("LARK", 417),
    "LEP": ("LEP", 418),
    "L2": ("L2", 419),
    "L2C": ("L2C", 420),
    "SKY": ("SKY", 421),
    "MHW": ("MHW", 422),
    "MO2": ("MO2", 423),
    "MOE": ("MOE", 424),
    "NST": ("NST", 425),
    "NEW": ("NEW", 426),
    "NWA": ("NWA", 427),
    "PKMMO": ("PKMMO", 428),
    "POE": ("POE", 429),
    "POE2": ("POE2", 430),
    "RO": ("RO", 431),
    "RVD": ("RVD", 432),
    "RS3": ("RS3", 433),
    "OSRS": ("OSRS", 434),
    "RPL": ("RPL", 435),
    "SRO": ("SRO", 436),
    "SWTOR": ("SWTOR", 437),
    "TRS": ("TRS", 438),
    "TIB": ("TIB", 439),
    "TL": ("TL", 440),
    "VR": ("VR", 441),

    # === FPS / SURVIVAL / ACTION (500–599) ===
    "ABI": ("ABI", 500),
    "APEX": ("APEX", 501),
    "BS": ("BS", 502),
    "COC": ("COC", 503),
    "CR": ("CR", 504),
    "CS2": ("CS2", 505),
    "DBD": ("DBD", 506),
    "D2": ("D2", 507),
    "DT": ("DT", 508),
    "EFT": ("EFT", 509),
    "FIN": ("FIN", 510),
    "F76": ("F76", 511),
    "FH5": ("FH5", 512),
    "GEN": ("GEN", 513),
    "HSR": ("HSR", 514),
    "HD": ("HD", 515),
    "LOL": ("LOL", 516),
    "MS": ("MS", 517),
    "NBA2K": ("NBA2K", 518),
    "OH": ("OH", 519),
    "OW2": ("OW2", 520),
    "PAL": ("PAL", 521),
    "PZ": ("PZ", 522),
    "QF": ("QF", 523),
    "REM2": ("REM2", 524),
    "RUST": ("RUST", 525),
    "SOT": ("SOT", 526),
    "TF2": ("TF2", 527),
    "TFD": ("TFD", 528),
    "VAL": ("VAL", 529),
    "WF": ("WF", 530),
    "WW": ("WW", 531),
    "ZZZ": ("ZZZ", 532),

    # === SPECIAL MMORPGs (600s) ===
    "AQW": ("AQW", 600),
    "ROR": ("ROR", 601),
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
    check_common_names()
