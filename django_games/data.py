#!/usr/bin/env python
"""
This is a self-contained data file that contains all major MMORPG, ARPG,
and Sandbox MMO game codes, modeled after ISO 3166-1 format.

To regenerate automatically, prepare a CSV file containing updated titles
and codes and run this file directly.
"""

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

GAMES: "Dict[str, StrPromise]" = {
    # === WORLD OF WARCRAFT (RETAIL) ===
    "WOW": _("World of Warcraft"),
    "WTB": _("World of Warcraft: The Burning Crusade"),
    "WOT": _("World of Warcraft: Wrath of the Lich King"),
    "CAT": _("World of Warcraft: Cataclysm"),
    "MOP": _("World of Warcraft: Mists of Pandaria"),
    "WOD": _("World of Warcraft: Warlords of Draenor"),
    "LEG": _("World of Warcraft: Legion"),
    "BFA": _("World of Warcraft: Battle for Azeroth"),
    "SDL": _("World of Warcraft: Shadowlands"),
    "DFL": _("World of Warcraft: Dragonflight"),
    "TWW": _("World of Warcraft: The War Within"),
    "MDN": _("World of Warcraft: Midnight"),
    "TLT": _("World of Warcraft: The Last Titan"),

    # === WORLD OF WARCRAFT (CLASSIC) ===
    "CLA": _("World of Warcraft Classic"),
    "ERA": _("World of Warcraft Classic Era"),
    "HDC": _("World of Warcraft Classic Hardcore"),
    "SOD": _("World of Warcraft: Season of Discovery"),
    "TBC": _("World of Warcraft: The Burning Crusade Classic"),
    "WTC": _("World of Warcraft: Wrath of the Lich King Classic"),
    "CTC": _("World of Warcraft: Cataclysm Classic"),
    "MPC": _("World of Warcraft: Mists of Pandaria Classic"),
    "WDC": _("World of Warcraft: Warlords of Draenor Classic"),
    "LGC": _("World of Warcraft: Legion Classic"),
    "BFC": _("World of Warcraft: Battle for Azeroth Classic"),
    "SLC": _("World of Warcraft: Shadowlands Classic"),
    "DFC": _("World of Warcraft: Dragonflight Classic"),

    # === PRIVATE / SPECIAL ===
    "PRS": _("World of Warcraft Private Server"),
    "ANV": _("World of Warcraft Classic Anniversary Edition"),

    # === DIABLO SERIES ===
    "DIA": _("Diablo"),
    "DIR": _("Diablo II: Resurrected"),
    "DIT": _("Diablo III"),
    "DIV": _("Diablo IV"),
    "VOH": _("Diablo IV: Vessel of Hatred"),

    # === MAJOR MMORPGS ===
    "AIO": _("Aion"),
    "AIC": _("Aion Classic"),
    "AON": _("Albion Online"),
    "ARC": _("ArcheAge"),
    "ARW": _("ArcheAge War"),
    "BLS": _("Blade & Soul"),
    "BLS": _("Blade & Soul"),
    "BDO": _("Black Desert Online"),
    "BDM": _("Black Desert Mobile"),
    "CON": _("Conquer Online"),
    "CPK": _("Corepunk"),
    "DAD": _("Dark and Darker"),
    "EVE": _("EVE Online"),
    "ESO": _("The Elder Scrolls Online"),
    "FFX": _("Final Fantasy XIV: A Realm Reborn"),
    "GRA": _("Granado Espada"),
    "GLD": _("Guild Wars 2"),
    "LAR": _("Lost Ark"),
    "LEP": _("Last Epoch"),
    "LIN": _("Lineage II"),
    "LNC": _("Lineage II Classic"),
    "HYP": _("Minecraft: Hypixel Skyblock"),
    "MHW": _("Monster Hunter Wilds"),
    "MOT": _("Mortal Online 2"),
    "MOE": _("Myth of Empires"),
    "NST": _("Neo Steam: The Shattered Continent"),
    "NEW": _("New World"),
    "NWA": _("New World: Aeternum"),
    "PKM": _("PokeMMO"),
    "POE": _("Path of Exile"),
    "POT": _("Path of Exile 2"),
    "RAG": _("Ragnarok Online"),
    "RVD": _("Ravendawn"),
    "RSC": _("RuneScape 3"),
    "OSR": _("Old School RuneScape"),
    "RPL": _("Rappelz Online"),
    "SLK": _("Silkroad Online"),
    "SWT": _("Star Wars: The Old Republic"),
    "TRS": _("Tarisland"),
    "TIB": _("Tibia"),
    "TNL": _("Throne and Liberty"),
    "VRS": _("V Rising"),

    # === FPS / SURVIVAL / ACTION ===
    "ABI": _("Arena Breakout: Infinite"),
    "APX": _("Apex Legends"),
    "BRS": _("Brawl Stars"),
    "COC": _("Clash of Clans"),
    "CRL": _("Clash Royale"),
    "CSR": _("Counter-Strike 2"),
    "DBD": _("Dead by Daylight"),
    "DSN": _("Destiny 2"),
    "DTI": _("Warhammer 40,000: Darktide"),
    "EFT": _("Escape from Tarkov"),
    "FIN": _("The Finals"),
    "FLT": _("Fallout 76"),
    "FHZ": _("Forza Horizon 5"),
    "GEN": _("Genshin Impact"),
    "HSR": _("Honkai: Star Rail"),
    "HYD": _("Hay Day"),
    "LOL": _("League of Legends"),
    "MPS": _("MapleStory"),
    "NBA": _("NBA 2K"),
    "OHM": _("Once Human"),
    "OVW": _("Overwatch"),
    "PLW": _("Palworld"),
    "PZB": _("Project Zomboid"),
    "QNF": _("The Quinfall"),
    "REM": _("Remnant II"),
    "RST": _("Rust"),
    "SOT": _("Sea of Thieves"),
    "TFT": _("Team Fortress 2"),
    "TFD": _("The First Descendant"),
    "VAL": _("Valorant"),
    "WFM": _("Warframe"),
    "WUW": _("Wuthering Waves"),
    "ZZZ": _("Zenless Zone Zero"),

    # === SPECIAL MMORPGS ===
    "AQW": _("AdventureQuest Worlds"),
    "WOR": _("Warhammer Online: Return of Reckoning"),
}



# --- ALT_CODES left unchanged ---
ALT_CODES = {}
# (You can safely keep ALT_CODES empty or reuse ISO mappings if needed.)


def self_generate(output_filename: str, filename: str = "games.csv"):  # pragma: no cover
    """Generate this file automatically from a CSV list."""
    import csv
    import re
    import unicodedata

    games = []
    with open(filename, encoding="utf-8") as csv_file:
        for row in csv.reader(csv_file):
            if not row or not row[0].strip():
                continue
            name = re.sub(r"\s+", " ", row[0].strip())
            code = row[1].strip().upper()
            games.append((name, code))
    games.sort(key=lambda g: unicodedata.normalize("NFKD", g[0]).encode("ascii", "ignore"))

    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("#!/usr/bin/env python\n# Auto-generated file\nGAMES = {\n")
        for name, code in games:
            output_file.write(f'    "{code}": _("{name}"),\n')
        output_file.write("}\n")


def check_icons(verbosity: int = 1):
    """Check that all defined games have matching icons."""
    this_dir = os.path.dirname(__file__)
    icon_dir = os.path.join(this_dir, "static", "icons")
    files = {os.path.splitext(f)[0].upper() for f in os.listdir(icon_dir) if f.endswith(".svg")}
    missing = set(GAMES) - files
    if missing:
        print("Missing icons for:")
        for code in sorted(missing):
            print(f"  {code} ({GAMES[code]})")
    elif verbosity:
        print("All games have icons. ✓")


def check_common_names() -> None:
    """Check for any unmapped common game names."""
    missing = set(GamesBase.COMMON_NAMES) - set(GAMES)
    if missing:
        print("The following common names do not match an official game code:")
        for code in sorted(missing):
            print(f"  {code}")


if __name__ == "__main__":  # pragma: no cover
    print(f"{len(GAMES)} games registered.")
    check_icons()
    check_common_names()
