from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django_stubs_ext import StrPromise

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    def _(message: str) -> "StrPromise":
        return message  # type: ignore


class GamesBase:
    """
    Base data for django_games.

    Provides alternative spellings, abbreviations, and legacy names for
    lookups across Saleor, dashboards, and game metadata integrations.
    """

class GamesBase:

    COMMON_NAMES = {
        # ✅ wow series…  
        # (unchanged — uses full names, not codes)
        # ✅ This section stays exactly as provided.
        # ✅ No need to modify because these are *lookup strings*, not codes.

        "WOW": _("World of Warcraft"),
        "WOW RETAIL": _("World of Warcraft"),
        "WOW CLASSIC": _("World of Warcraft Classic"),
        "WOW VANILLA": _("World of Warcraft Classic"),
        "WOW ERA": _("World of Warcraft Classic Era"),
        "WOW HARDCORE": _("World of Warcraft Classic Hardcore"),
        "WOW HC": _("World of Warcraft Classic Hardcore"),
        "WOW SOD": _("World of Warcraft: Season of Discovery"),
        "WOW PRIVATE": _("World of Warcraft Private Server"),

        # Retail expansions
        "WOW TBC": _("World of Warcraft: The Burning Crusade"),
        "WOW WOTLK": _("World of Warcraft: Wrath of the Lich King"),
        "WOW CATA": _("World of Warcraft: Cataclysm"),
        "WOW MOP": _("World of Warcraft: Mists of Pandaria"),
        "WOW WOD": _("World of Warcraft: Warlords of Draenor"),
        "WOW LEGION": _("World of Warcraft: Legion"),
        "WOW BFA": _("World of Warcraft: Battle for Azeroth"),
        "WOW SHADOWLANDS": _("World of Warcraft: Shadowlands"),
        "WOW DF": _("World of Warcraft: Dragonflight"),
        "WOW WW": _("World of Warcraft: The War Within"),
        "WOW MIDNIGHT": _("World of Warcraft: Midnight"),
        "WOW TITAN": _("World of Warcraft: The Last Titan"),

        # ✅ Path of Exile
        "POE": _("Path of Exile"),
        "POE 2": _("Path of Exile 2"),

        # ✅ Diablo
        "D1": _("Diablo"),
        "DIABLO": _("Diablo"),
        "D2": _("Diablo II: Resurrected"),
        "D3": _("Diablo III"),
        "D4": _("Diablo IV"),
        "D4X": _("Diablo IV: Vessel of Hatred"),

        # ✅ Albion Online
        "ALB": _("Albion Online"),
        "ALBION": _("Albion Online"),

        # ✅ Lost Ark
        "LOST ARK": _("Lost Ark"),
        "LA": _("Lost Ark"),

        # ✅ AION
        "AION": _("Aion"),
        "AION CLASSIC": _("Aion Classic"),

        # ✅ New World
        "NEW WORLD": _("New World"),
        "NEW WORLD AETERNUM": _("New World: Aeternum"),

        # ✅ Others (exactly as you provided)
        "TARISLAND": _("Tarisland"),
        "THRONE AND LIBERTY": _("Throne and Liberty"),
        "TNL": _("Throne and Liberty"),
        "POKEMMO": _("PokeMMO"),
        "MORTAL ONLINE 2": _("Mortal Online 2"),
        "WARFRAME": _("Warframe"),
        "MINECRAFT": _("Minecraft"),
        "HYPIXEL": _("Minecraft: Hypixel Skyblock"),
        "HYPIXEL SKYBLOCK": _("Minecraft: Hypixel Skyblock"),

        "ROBLOX": _("Roblox"),
        "DARK AND DARKER": _("Dark and Darker"),

        "TF2": _("Team Fortress 2"),
        "TEAM FORTRESS 2": _("Team Fortress 2"),

        "RUNESCAPE": _("RuneScape 3"),
        "RS3": _("RuneScape 3"),
        "RS": _("RuneScape 3"),
        "OSRS": _("Old School RuneScape"),

        "BLACK DESERT": _("Black Desert Online"),
        "BDO": _("Black Desert Online"),
        "BLACK DESERT MOBILE": _("Black Desert Mobile"),
        "BDM": _("Black Desert Mobile"),

        "FFXIV": _("Final Fantasy XIV Online"),

        "ESO": _("The Elder Scrolls Online"),
        "TESO": _("The Elder Scrolls Online"),

        "GW2": _("Guild Wars 2"),
        "GW": _("Guild Wars 2"),

        "TIBIA": _("Tibia"),
        "CONQUER ONLINE": _("Conquer Online"),
        "SILKROAD": _("Silkroad Online"),
        "SILKROAD ONLINE": _("Silkroad Online"),

        "TARKOV": _("Escape from Tarkov"),
        "EFT": _("Escape from Tarkov"),

        "PZ": _("Project Zomboid"),

        "AQW": _("AdventureQuest Worlds"),

        "WARHAMMER ONLINE": _("Warhammer Online: Return of Reckoning"),
        "RETURN OF RECKONING": _("Warhammer Online: Return of Reckoning"),
    }

    # Legacy titles
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
            _("Diablo II Lord of Destruction"),
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
