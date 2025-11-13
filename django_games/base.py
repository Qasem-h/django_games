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
    Canonical-friendly names must use ONLY canonical codes.
    CLEANED for real RMT + boosting markets (2025 edition)
    """

    # ======================================================================
    # ✅ CLEANED — CANONICAL → FRIENDLY NAMES (ACTIVE RMT + BOOSTING GAMES)
    # ======================================================================
    COMMON_NAMES = {

        # === WORLD OF WARCRAFT RETAIL ===
        "WOW": _("World of Warcraft"),
        "DFL": _("World of Warcraft: Dragonflight"),
        "TWW": _("World of Warcraft: The War Within"),
        "MDN": _("World of Warcraft: Midnight"),
        "TLT": _("World of Warcraft: The Last Titan"),

        # === WORLD OF WARCRAFT CLASSIC ===
        "WOWC": _("World of Warcraft Classic"),
        "ERA": _("World of Warcraft Classic Era"),
        "HC": _("World of Warcraft Classic Hardcore"),
        "SOD": _("World of Warcraft: Season of Discovery"),

        # === CLASSIC EXPANSIONS ===
        "TBCC": _("World of Warcraft: The Burning Crusade Classic"),
        "WOTLKC": _("World of Warcraft: Wrath of the Lich King Classic"),
        "CATAC": _("World of Warcraft: Cataclysm Classic"),
        "MOPC": _("World of Warcraft: Mists of Pandaria Classic"),
        "WODC": _("World of Warcraft: Warlords of Draenor Classic"),
        "LEGC": _("World of Warcraft: Legion Classic"),

        # === PRIVATE / SPECIAL ===
        "WOWP": _("World of Warcraft Private Server"),
        "ANV": _("World of Warcraft Classic Anniversary Edition"),
        "TBCCA": _("World of Warcraft: The Burning Crusade Classic Anniversary"),


        # === DIABLO SERIES ===
        "D2R": _("Diablo II: Resurrected"),
        "D3": _("Diablo III"),
        "D4": _("Diablo IV"),
        "D4VH": _("Diablo IV: Vessel of Hatred"),

        # === TOP MMORPG RMT GAMES ===
        "AION": _("Aion"),
        "AIC": _("Aion Classic"),
        "ALB": _("Albion Online"),
        "BNS": _("Blade & Soul"),
        "BDO": _("Black Desert Online"),
        "EVE": _("EVE Online"),
        "ESO": _("The Elder Scrolls Online"),
        "FFXIV": _("Final Fantasy XIV: A Realm Reborn"),
        "GW2": _("Guild Wars 2"),
        "LARK": _("Lost Ark"),

        "LEP": _("Last Epoch"),
        "L2": _("Lineage II"),
        "L2C": _("Lineage II Classic"),
        "SKY": _("Minecraft: Hypixel SkyBlock"),
        "MO2": _("Mortal Online 2"),
        "MOE": _("Myth of Empires"),
        "NEW": _("New World"),
        "NWA": _("New World: Aeternum"),
        "POE": _("Path of Exile"),
        "POE2": _("Path of Exile 2"),
        "RO": _("Ragnarok Online"),
        "RVD": _("Ravendawn"),
        "RS3": _("RuneScape 3"),
        "OSRS": _("Old School RuneScape"),
        "SWTOR": _("Star Wars: The Old Republic"),
        "TRS": _("Tarisland"),
        "TIB": _("Tibia"),
        "TL": _("Throne and Liberty"),
        "VR": _("V Rising"),

        # === SURVIVAL / EXTRACTION (REAL MONEY FARMING) ===
        "D2": _("Destiny 2"),
        "EFT": _("Escape from Tarkov"),
        "RUST": _("Rust"),
        "TFD": _("The First Descendant"),
        "WF": _("Warframe"),
    }

    # ======================================================================
    # ✅ CLEANED OLD NAMES — ONLY KEEP GAMES THAT STILL EXIST IN COMMON_NAMES
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
            _("Guild Wars"),
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
        "D2": [
            _("Destiny 2 — Old Seasons"),
        ],
        "BDO": [
            _("Black Desert Online — Pre-Remaster"),
        ],
    }

    def __getstate__(self):
        return None
