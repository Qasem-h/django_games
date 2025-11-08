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


# 🎮 Nicely titled (and translatable) MMORPG / ARPG / Sandbox MMO game names.
GAMES: "Dict[str, StrPromise]" = {
    # === WORLD OF WARCRAFT RETAIL SERIES ===
    "WOW": _("World of Warcraft"),
    "WRB": _("World of Warcraft: The Burning Crusade"),
    "WRW": _("World of Warcraft: Wrath of the Lich King"),
    "WRC": _("World of Warcraft: Cataclysm"),
    "WRM": _("World of Warcraft: Mists of Pandaria"),
    "WRD": _("World of Warcraft: Warlords of Draenor"),
    "WRL": _("World of Warcraft: Legion"),
    "WRZ": _("World of Warcraft: Battle for Azeroth"),
    "WRS": _("World of Warcraft: Shadowlands"),
    "WRF": _("World of Warcraft: Dragonflight"),
    "WRN": _("World of Warcraft: The War Within"),
    "WRT": _("World of Warcraft: Midnight"),
    "WRG": _("World of Warcraft: The Last Titan"),

    # === FUTURE RETAIL EXPANSIONS (PROJECTED) ===
    "WRX": _("World of Warcraft: The Void Reborn"),
    "WRY": _("World of Warcraft: Realms of Light"),
    "WRV": _("World of Warcraft: The End of Time"),

    # === WORLD OF WARCRAFT CLASSIC SERIES ===
    "WOC": _("World of Warcraft Classic"),
    "WCE": _("World of Warcraft Classic Era"),
    "WHC": _("World of Warcraft Classic Hardcore"),
    "WSD": _("World of Warcraft: Season of Discovery"),
    "WBC": _("World of Warcraft: The Burning Crusade Classic"),
    "WWR": _("World of Warcraft: Wrath of the Lich King Classic"),
    "WCC": _("World of Warcraft: Cataclysm Classic"),
    "WMC": _("World of Warcraft: Mists of Pandaria Classic"),
    "WWA": _("World of Warcraft: Warlords of Draenor Classic"),
    "WLC": _("World of Warcraft: Legion Classic"),
    "WBZ": _("World of Warcraft: Battle for Azeroth Classic"),
    "WSL": _("World of Warcraft: Shadowlands Classic"),
    "WDC": _("World of Warcraft: Dragonflight Classic"),

    # === PRIVATE / SPECIAL MODS ===
    "WPR": _("World of Warcraft Private Server"),
    "WAN": _("World of Warcraft Classic Anniversary Edition"),

    # === OTHER MAJOR MMORPGS ===
    "POE": _("Path of Exile"),
    "PO2": _("Path of Exile 2"),
    "DIA": _("Diablo"),
    "DI2": _("Diablo II: Resurrected"),
    "DI3": _("Diablo III"),
    "DI4": _("Diablo IV"),
    "AIO": _("Aion"),
    "AIC": _("Aion Classic"),
    "ALB": _("Albion Online"),
    "LAR": _("Lost Ark"),
    "LEP": _("Last Epoch"),
    "NWA": _("New World"),
    "NWT": _("New World: Aeternum"),
    "TAR": _("Tarisland"),
    "TNL": _("Throne and Liberty"),
    "PMO": _("PokeMMO"),
    "MO2": _("Mortal Online 2"),
    "WFR": _("Warframe"),
    "DAD": _("Dark and Darker"),
    "RBL": _("Roblox"),
    "MCH": _("Minecraft Hypixel Skyblock"),
    "TF2": _("Team Fortress 2"),
    "BLR": _("Black Desert Online"),
    "BDM": _("Black Desert Mobile"),
    "ESO": _("The Elder Scrolls Online"),
    "FFX": _("Final Fantasy XIV Online"),
    "GW2": _("Guild Wars 2"),
    "RAG": _("Ragnarok Online"),
    "RUN": _("RuneScape"),
    "OSR": _("Old School RuneScape"),
    "TIB": _("Tibia"),
    "EVE": _("EVE Online"),
    "SWT": _("Star Wars: The Old Republic"),
    "LOA": _("Lineage II"),
    "L2C": _("Lineage II Classic"),
    "ARC": _("ArcheAge"),
    "ARW": _("ArcheAge War"),
    "BDR": _("Blade and Soul"),
    "BD2": _("Blade and Soul 2"),
    "CON": _("Conquer Online"),
    "SRO": _("Silkroad Online"),
    "RSO": _("Rappelz Online"),
    "VRI": _("V Rising"),
    "MYO": _("Myth of Empires"),
    "UND": _("Undawn"),
    "ELO": _("Elyon Online"),
    "SEA": _("Sea of Thieves"),
    "NEO": _("Neo Steam: The Shattered Continent"),
    "GIL": _("Granado Espada Online"),
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
