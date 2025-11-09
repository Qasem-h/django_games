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
    """

    # ======================================================================
    # ✅ CLEANED — CANONICAL → FRIENDLY NAMES (NO HUMAN STRINGS AS KEYS)
    # ======================================================================
    COMMON_NAMES = {

        # ============ WORLD OF WARCRAFT RETAIL ============
        "WOW": _("World of Warcraft"),
        "DFL": _("World of Warcraft: Dragonflight"),
        "TWW": _("World of Warcraft: The War Within"),
        "MDN": _("World of Warcraft: Midnight"),
        "TLT": _("World of Warcraft: The Last Titan"),

        # ============ WORLD OF WARCRAFT CLASSIC ============
        "WOWC": _("World of Warcraft Classic"),
        "ERA": _("World of Warcraft Classic Era"),
        "HC": _("World of Warcraft Classic Hardcore"),
        "SOD": _("World of Warcraft: Season of Discovery"),

        # ============ CLASSIC EXPANSIONS ============
        "TBCC": _("World of Warcraft: The Burning Crusade Classic"),
        "WOTLKC": _("World of Warcraft: Wrath of the Lich King Classic"),
        "CATAC": _("World of Warcraft: Cataclysm Classic"),
        "MOPC": _("World of Warcraft: Mists of Pandaria Classic"),
        "WODC": _("World of Warcraft: Warlords of Draenor Classic"),
        "LEGC": _("World of Warcraft: Legion Classic"),

        # ============ DIABLO SERIES ============
        "D1": _("Diablo"),
        "D2R": _("Diablo II: Resurrected"),
        "D3": _("Diablo III"),
        "D4": _("Diablo IV"),
        "D4VH": _("Diablo IV: Vessel of Hatred"),

        # ============ LOST ARK ============
        "LARK": _("Lost Ark"),

        # ============ AION SERIES ============
        "AION": _("Aion"),
        "AIC": _("Aion Classic"),

        # ============ ALBION ============
        "ALB": _("Albion Online"),

        # ============ NEW WORLD ============
        "NEW": _("New World"),
        "NWA": _("New World: Aeternum"),

        # ============ TARISLAND ============
        "TRS": _("Tarisland"),

        # ============ THRONE AND LIBERTY ============
        "TL": _("Throne and Liberty"),

        # ============ POE ============
        "POE": _("Path of Exile"),
        "POE2": _("Path of Exile 2"),

        # ============ POKEMMO ============
        "PKMMO": _("PokeMMO"),

        # ============ MORTAL ONLINE ============
        "MO2": _("Mortal Online 2"),

        # ============ MINECRAFT SKYBLOCK ============
        "SKY": _("Minecraft: Hypixel SkyBlock"),

        # ============ RUNESCAPE ============
        "RS3": _("RuneScape 3"),
        "OSRS": _("Old School RuneScape"),

        # ============ BLACK DESERT ============
        "BDO": _("Black Desert Online"),
        "BDM": _("Black Desert Mobile"),

        # ============ FFXIV ============
        "FFXIV": _("Final Fantasy XIV: A Realm Reborn"),

        # ============ ESO ============
        "ESO": _("The Elder Scrolls Online"),

        # ============ GW2 ============
        "GW2": _("Guild Wars 2"),

        # ============ TIBIA ============
        "TIB": _("Tibia"),

        # ============ SILKROAD ============
        "SRO": _("Silkroad Online"),

        # ============ TARKOV ============
        "EFT": _("Escape from Tarkov"),

        # ============ PROJECT ZOMBOID ============
        "PZ": _("Project Zomboid"),

        # ============ WARFRAME ============
        "WF": _("Warframe"),

        # ============ AQW ============
        "AQW": _("AdventureQuest Worlds"),

        # ============ ROR ============
        "ROR": _("Warhammer Online: Return of Reckoning"),
    }

    # ======================================================================
    # ✅ LEGACY NAMES (Keep as-is)
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
        "DI2": [
            _("Diablo II"),
            _("Diablo II: Lord of Destruction"),
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
    }

    def __getstate__(self):
        return None
