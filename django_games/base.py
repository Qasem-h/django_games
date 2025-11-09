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

    # ======================================================================
    # ✅ COMMUNITY-FRIENDLY NAMES → CANONICAL CODE MAP (WOWC + LARK UPDATED)
    # ======================================================================
    COMMON_NAMES = {

        # ======================
        # ✅ WORLD OF WARCRAFT
        # ======================
        "WOW": _("World of Warcraft"),
        "WOW RETAIL": _("World of Warcraft"),
        "WORLD OF WARCRAFT": _("World of Warcraft"),

        # --- Classic (renamed to WOWC) ---
        "WOW CLASSIC": _("World of Warcraft Classic"),
        "WOW VANILLA": _("World of Warcraft Classic"),
        "WOWC": _("World of Warcraft Classic"),
        "CLASSIC": _("World of Warcraft Classic"),

        "WOW ERA": _("World of Warcraft Classic Era"),
        "WOW HARDCORE": _("World of Warcraft Classic Hardcore"),
        "WOW HC": _("World of Warcraft Classic Hardcore"),
        "WOW SOD": _("World of Warcraft: Season of Discovery"),
        "WOW PRIVATE": _("World of Warcraft Private Server"),

        # --- Retail Expansions ---
        "WOW TBC": _("World of Warcraft: The Burning Crusade"),
        "WOW WOTLK": _("World of Warcraft: Wrath of the Lich King"),
        "WOW CATA": _("World of Warcraft: Cataclysm"),
        "WOW MOP": _("World of Warcraft: Mists of Pandaria"),
        "WOW WOD": _("World of Warcraft: Warlords of Draenor"),
        "WOW LEGION": _("World of Warcraft: Legion"),
        "WOW BFA": _("World of Warcraft: Battle for Azeroth"),
        "WOW SHADOWLANDS": _("World of Warcraft: Shadowlands"),

        "WOW DF": _("World of Warcraft: Dragonflight"),
        "DRAGONFLIGHT": _("World of Warcraft: Dragonflight"),

        "WOW WW": _("World of Warcraft: The War Within"),
        "WOW WAR WITHIN": _("World of Warcraft: The War Within"),

        "WOW MIDNIGHT": _("World of Warcraft: Midnight"),
        "WOW TITAN": _("World of Warcraft: The Last Titan"),

        # ======================
        # ✅ PATH OF EXILE
        # ======================
        "POE": _("Path of Exile"),
        "PATH OF EXILE": _("Path of Exile"),
        "POE 2": _("Path of Exile 2"),
        "POE2": _("Path of Exile 2"),

        # ======================
        # ✅ DIABLO SERIES
        # ======================
        "D1": _("Diablo"),
        "DIABLO": _("Diablo"),
        "DIABLO 1": _("Diablo"),

        "D2": _("Diablo II: Resurrected"),
        "DIABLO 2": _("Diablo II: Resurrected"),
        "DIABLO II": _("Diablo II: Resurrected"),

        "D3": _("Diablo III"),
        "DIABLO 3": _("Diablo III"),

        "D4": _("Diablo IV"),
        "DIABLO 4": _("Diablo IV"),

        "D4X": _("Diablo IV: Vessel of Hatred"),
        "D4 EXPANSION": _("Diablo IV: Vessel of Hatred"),

        # ======================
        # ✅ LOST ARK (RENAMED → LARK)
        # ======================
        "LOST ARK": _("Lost Ark"),
        "LARK": _("Lost Ark"),
        "LA": _("Lost Ark"),
        "LAK": _("Lost Ark"),

        # ======================
        # ✅ ALBION ONLINE
        # ======================
        "ALB": _("Albion Online"),
        "ALBION": _("Albion Online"),
        "ALBION ONLINE": _("Albion Online"),

        # ======================
        # ✅ AION SERIES
        # ======================
        "AION": _("Aion"),
        "AION CLASSIC": _("Aion Classic"),

        # ======================
        # ✅ NEW WORLD
        # ======================
        "NEW WORLD": _("New World"),
        "NEW WORLD AETERNUM": _("New World: Aeternum"),
        "AETERNUM": _("New World: Aeternum"),

        # ======================
        # ✅ TARISLAND
        # ======================
        "TARISLAND": _("Tarisland"),

        # ======================
        # ✅ THRONE AND LIBERTY
        # ======================
        "THRONE AND LIBERTY": _("Throne and Liberty"),
        "TNL": _("Throne and Liberty"),

        # ======================
        # ✅ POKEMMO
        # ======================
        "POKEMMO": _("PokeMMO"),

        # ======================
        # ✅ MORTAL ONLINE 2
        # ======================
        "MORTAL ONLINE 2": _("Mortal Online 2"),
        "MO2": _("Mortal Online 2"),

        # ======================
        # ✅ WARFRAME
        # ======================
        "WARFRAME": _("Warframe"),
        "WF": _("Warframe"),

        # ======================
        # ✅ MINECRAFT / HYPIXEL
        # ======================
        "MINECRAFT": _("Minecraft"),
        "HYPIXEL": _("Minecraft: Hypixel SkyBlock"),
        "HYPIXEL SKYBLOCK": _("Minecraft: Hypixel SkyBlock"),
        "SKYBLOCK": _("Minecraft: Hypixel SkyBlock"),

        # ======================
        # ✅ RUNESCAPE SERIES
        # ======================
        "RUNESCAPE": _("RuneScape 3"),
        "RUNESCAPE 3": _("RuneScape 3"),
        "RS3": _("RuneScape 3"),
        "RS": _("RuneScape 3"),

        "OSRS": _("Old School RuneScape"),
        "OLD SCHOOL RUNESCAPE": _("Old School RuneScape"),

        # ======================
        # ✅ BLACK DESERT SERIES
        # ======================
        "BLACK DESERT": _("Black Desert Online"),
        "BDO": _("Black Desert Online"),

        "BLACK DESERT MOBILE": _("Black Desert Mobile"),
        "BDM": _("Black Desert Mobile"),

        # ======================
        # ✅ FFXIV
        # ======================
        "FFXIV": _("Final Fantasy XIV Online"),
        "FF14": _("Final Fantasy XIV Online"),
        "FINAL FANTASY XIV": _("Final Fantasy XIV Online"),

        # ======================
        # ✅ ESO
        # ======================
        "ESO": _("The Elder Scrolls Online"),
        "TESO": _("The Elder Scrolls Online"),

        # ======================
        # ✅ GUILD WARS 2
        # ======================
        "GW2": _("Guild Wars 2"),
        "GW": _("Guild Wars 2"),

        # ======================
        # ✅ TIBIA
        # ======================
        "TIBIA": _("Tibia"),

        # ======================
        # ✅ CONQUER ONLINE
        # ======================
        "CONQUER ONLINE": _("Conquer Online"),

        # ======================
        # ✅ SILKROAD
        # ======================
        "SILKROAD": _("Silkroad Online"),
        "SILKROAD ONLINE": _("Silkroad Online"),

        # ======================
        # ✅ TARKOV
        # ======================
        "TARKOV": _("Escape from Tarkov"),
        "EFT": _("Escape from Tarkov"),

        # ======================
        # ✅ PROJECT ZOMBOID
        # ======================
        "PZ": _("Project Zomboid"),

        # ======================
        # ✅ AQW
        # ======================
        "AQW": _("AdventureQuest Worlds"),

        # ======================
        # ✅ WARHAMMER ONLINE / ROR
        # ======================
        "WARHAMMER ONLINE": _("Warhammer Online: Return of Reckoning"),
        "RETURN OF RECKONING": _("Warhammer Online: Return of Reckoning"),
        "ROR": _("Warhammer Online: Return of Reckoning"),
    }

    # ======================================================================
    # ✅ LEGACY TITLES (Historical, Beta, Old Versions)
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
