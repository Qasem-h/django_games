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

    # Common shorthand, acronyms, and alternative spellings
    COMMON_NAMES = {
        # --- World of Warcraft ---
        "WOW": _("World of Warcraft"),
        "WOW RETAIL": _("World of Warcraft"),
        "WOW CLASSIC": _("World of Warcraft Classic"),
        "WOW ERA": _("World of Warcraft Classic Era"),
        "WOW HARDCORE": _("World of Warcraft Classic Hardcore"),
        "WOW SOD": _("World of Warcraft: Season of Discovery"),
        "WOW PRIVATE": _("World of Warcraft Private Server"),
        "WOW VANILLA": _("World of Warcraft Classic"),
        "WOW DF": _("World of Warcraft: Dragonflight"),
        "WOW WW": _("World of Warcraft: The War Within"),
        "WOW MIDNIGHT": _("World of Warcraft: Midnight"),
        "WOW TITAN": _("World of Warcraft: The Last Titan"),

        # --- Path of Exile ---
        "POE": _("Path of Exile"),
        "POE 2": _("Path of Exile 2"),
        "PATH OF EXILE": _("Path of Exile"),
        "PATH OF EXILE 2": _("Path of Exile 2"),

        # --- Diablo ---
        "D1": _("Diablo"),
        "D2": _("Diablo II: Resurrected"),
        "D3": _("Diablo III"),
        "D4": _("Diablo IV"),

        # --- Albion Online ---
        "ALB": _("Albion Online"),
        "ALBION": _("Albion Online"),

        # --- Lost Ark ---
        "LOST ARK": _("Lost Ark"),
        "LA": _("Lost Ark"),

        # --- Aion ---
        "AION": _("Aion"),
        "AION CLASSIC": _("Aion Classic"),

        # --- New World ---
        "NEW WORLD": _("New World"),
        "NEW WORLD AETERNUM": _("New World: Aeternum"),

        # --- Tarisland ---
        "TARISLAND": _("Tarisland"),

        # --- Throne and Liberty ---
        "THRONE AND LIBERTY": _("Throne and Liberty"),
        "TNL": _("Throne and Liberty"),

        # --- PokeMMO ---
        "POKEMMO": _("PokeMMO"),

        # --- Mortal Online 2 ---
        "MORTAL ONLINE 2": _("Mortal Online 2"),

        # --- Warframe ---
        "WARFRAME": _("Warframe"),

        # --- Minecraft Hypixel ---
        "MINECRAFT": _("Minecraft Hypixel Skyblock"),
        "HYPIXEL": _("Minecraft Hypixel Skyblock"),

        # --- Roblox ---
        "ROBLOX": _("Roblox"),

        # --- Dark and Darker ---
        "DARK AND DARKER": _("Dark and Darker"),

        # --- Team Fortress 2 ---
        "TEAM FORTRESS 2": _("Team Fortress 2"),
        "TF2": _("Team Fortress 2"),

        # --- RuneScape ---
        "RUNESCAPE": _("RuneScape"),
        "OSRS": _("Old School RuneScape"),

        # --- Black Desert ---
        "BLACK DESERT": _("Black Desert Online"),
        "BDO": _("Black Desert Online"),
        "BLACK DESERT MOBILE": _("Black Desert Mobile"),

        # --- Final Fantasy XIV ---
        "FFXIV": _("Final Fantasy XIV Online"),
        "FINAL FANTASY XIV": _("Final Fantasy XIV Online"),

        # --- Elder Scrolls Online ---
        "ESO": _("The Elder Scrolls Online"),
        "ELDER SCROLLS ONLINE": _("The Elder Scrolls Online"),

        # --- Guild Wars ---
        "GW2": _("Guild Wars 2"),
        "GUILD WARS 2": _("Guild Wars 2"),

        # --- Tibia / Conquer / Silkroad ---
        "TIBIA": _("Tibia"),
        "CONQUER ONLINE": _("Conquer Online"),
        "SILKROAD": _("Silkroad Online"),
        "SILKROAD ONLINE": _("Silkroad Online"),
    }

    # Legacy titles or outdated references
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
    }

    def __getstate__(self):
        # Prevent pickling errors (matches Django’s standard for static registries)
        return None
