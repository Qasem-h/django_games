from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django_stubs_ext import StrPromise

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # pragma: no cover
    def _(message: str) -> "StrPromise":
        return message  # type: ignore


class GamesBase:
    """
    Base data for django_games.
    CLEAN 2025 EDITION — Only REAL RMT + Boosting markets included.
    """

    # ======================================================================
    # ✅ CANONICAL → FRIENDLY NAMES (FINAL 2025 GAME LIST)
    # ======================================================================
    COMMON_NAMES = {

        # === WORLD OF WARCRAFT (Retail + Classic + Special) ===
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

        # === DIABLO SERIES ===
        "D2R": _("Diablo II: Resurrected"),
        "D4": _("Diablo IV"),

        # === MAJOR MMORPGS ===
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

        # === RMT / PROFITABLE ===
        "EFT": _("Escape from Tarkov"),
        "ARC": _("ARC Raiders"),
    }

    # ======================================================================
    # ✅ OLD NAMES — ONLY FOR GAMES THAT STILL EXIST IN COMMON_NAMES
    # ======================================================================
    OLD_NAMES = {
        "WOW": [
            _("World of Warcraft Vanilla"),
            _("World of Warcraft Beta"),
        ],
        "ERA": [
            _("World of Warcraft 2019 Classic"),
        ],
        "HC": [
            _("Classic Hardcore Beta"),
        ],
        "MOPC": [
            _("Pandaria Classic PTR"),
        ],
        "WOWP": [
            _("Private Server Custom Version"),
        ],
        "ANV": [
            _("WoW Anniversary Edition 2024"),
        ],
        "TBCCA": [
            _("TBC Classic 2021"),
        ],

        "D2R": [
            _("Diablo II Classic"),
            _("Diablo II Lord of Destruction"),
        ],
        "D4": [
            _("Diablo IV Pre-Season"),
        ],

        "AION": [
            _("Aion 1.x"),
        ],
        "AIC": [
            _("Aion Classic 2.0"),
        ],
        "ALB": [
            _("Albion Early Access"),
        ],
        "BDO": [
            _("Black Desert Online Pre-Remastered"),
        ],
        "ESO": [
            _("ESO: Tamriel Unlimited"),
        ],
        "GW2": [
            _("Guild Wars 1"),
        ],
        "RS3": [
            _("RuneScape 2"),
        ],
        "OSRS": [
            _("RuneScape 2007"),
        ],
        "POE": [
            _("Path of Exile Legacy League"),
        ],
        "POE2": [
            _("Path of Exile 2 Alpha"),
        ],
        "FFXIV": [
            _("FFXIV 1.0"),
        ],
        "L2": [
            _("Lineage II Prelude"),
        ],
    }

    def __getstate__(self):
        return None
