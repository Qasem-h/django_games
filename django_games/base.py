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
    # ✅ CANONICAL → FRIENDLY NAMES (HIGH + MEDIUM RMT MARKETS ONLY)
    # ======================================================================
    COMMON_NAMES = {

        # === WORLD OF WARCRAFT RETAIL ===
        "WOW": _("World of Warcraft"),
        "DFL": _("World of Warcraft: Dragonflight"),
        "TWW": _("World of Warcraft: The War Within"),
        "MDN": _("World of Warcraft: Midnight"),
        "TLT": _("World of Warcraft: The Last Titan"),

        # === WOW CLASSIC ===
        "WOWC": _("World of Warcraft Classic"),
        "ERA": _("World of Warcraft Classic Era"),
        "HC": _("World of Warcraft Classic Hardcore"),
        "SOD": _("World of Warcraft: Season of Discovery"),

        # === CLASSIC EXPANSIONS ===
        "TBCC": _("World of Warcraft: The Burning Crusade Classic"),
        "WOTLKC": _("World of Warcraft: Wrath of the Lich King Classic"),
        "CATAC": _("World of Warcraft: Cataclysm Classic"),
        "MOPC": _("World of Warcraft: Mists of Pandaria Classic"),
        "TBCCA": _("World of Warcraft: The Burning Crusade Classic Anniversary"),

        # === PRIVATE / SPECIAL ===
        "WOWP": _("World of Warcraft Private Server"),
        "ANV": _("World of Warcraft Classic Anniversary Edition"),

        # === DIABLO SERIES ===
        "D2R": _("Diablo II: Resurrected"),  # MUST HAVE — RUNES RMT
        "D4": _("Diablo IV"),
        "D4VH": _("Diablo IV: Vessel of Hatred"),

        # === TOP MMORPG RMT GAMES ===
        "AION": _("Aion"),
        "AIC": _("Aion Classic"),
        "ALB": _("Albion Online"),
        "BDO": _("Black Desert Online"),    # ADDED — huge RMT
        "EVE": _("EVE Online"),
        "ESO": _("The Elder Scrolls Online"),
        "FFXIV": _("Final Fantasy XIV"),
        "GW2": _("Guild Wars 2"),
        "LARK": _("Lost Ark"),
        "LEP": _("Last Epoch"),
        "L2": _("Lineage II"),
        "MO2": _("Mortal Online 2"),
        "NEW": _("New World"),
        "NWA": _("New World: Aeternum"),
        "POE": _("Path of Exile"),
        "POE2": _("Path of Exile 2"),
        "RO": _("Ragnarok Online"),
        "RS3": _("RuneScape 3"),
        "OSRS": _("Old School RuneScape"),
        "TRS": _("Tarisland"),
        "TNL": _("Throne and Liberty"),

        # === OPTIONAL BUT PROFITABLE ===
        "EFT": _("Escape from Tarkov"),  # Roubles
        "RUST": _("Rust"),
        "TIB": _("Tibia"),               # very strong in SA / EU
    }

    # ======================================================================
    # ✅ OLD NAMES — Only for games that still exist in COMMON_NAMES
    # ======================================================================
    OLD_NAMES = {
        "WOW": [
            _("World of Warcraft Vanilla"),
            _("World of Warcraft Beta"),
        ],
        "POE": [
            _("Path of Exile Closed Beta"),
            _("Path of Exile Legacy League"),
        ],
        "ESO": [
            _("The Elder Scrolls Online: Tamriel Unlimited"),
        ],
        "GW2": [
            _("Guild Wars 1"),
            _("Guild Wars Factions"),
        ],
        "RS3": [
            _("RuneScape 2"),
            _("RuneScape HD"),
        ],
        "OSRS": [
            _("RuneScape 2007"),
        ],
        "AION": [
            _("Aion 1.x"),
            _("Aion 2.x"),
        ],
        "POE2": [
            _("Path of Exile 2 Alpha"),
        ],
        "L2": [
            _("Lineage II Prelude"),
        ],
        "FFXIV": [
            _("FFXIV 1.0"),
        ],
        "D2R": [
            _("Diablo II Classic"),
            _("Diablo II Lord of Destruction"),
        ],
        "BDO": [
            _("Black Desert Online Pre-Remastered"),
        ],
        "TIB": [
            _("Tibia 7.x Era"),
        ],
    }

    def __getstate__(self):
        return None
