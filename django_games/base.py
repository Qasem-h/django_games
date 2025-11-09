try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    def _(x):
        return x


class GamesBase:
    COMMON_NAMES = {
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


    def __getstate__(self):
        return None
