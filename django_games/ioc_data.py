#!/usr/bin/env python3
"""
django_games/ioc_data.py
========================
IOC-style franchise codes → ISO-style canonical game codes.

IOC = broad franchise / shorthand grouping (WOW, POE, DIABLO, etc.)
ISO = exact canonical game code used in django_games.data.GAMES.

This version is fully synchronized with the updated GAMES dataset:
- WOWC (Classic)
- LARK (Lost Ark)
- AIC (Aion Classic)
- DFL / TWW / MDN / TLT (Retail expansions)
- All classic expansions unchanged (TBCC, WOTLKC, etc.)
"""

# =====================================================================
# ✅ IOC (Franchise / Shorthand) → ISO (Canonical Game Code)
# =====================================================================
IOC_TO_ISO = {

    # ==============================
    # ✅ WORLD OF WARCRAFT (Retail)
    # ==============================
    "WOW": "WOW",
    "WOW RETAIL": "WOW",

    # --- Retail expansions (canonical in GAMES) ---
    "DFL": "DFL",
    "DRAGONFLIGHT": "DFL",
    "TWW": "TWW",
    "WARWITHIN": "TWW",
    "MDN": "MDN",
    "MIDNIGHT": "MDN",
    "TLT": "TLT",
    "TITAN": "TLT",

    # ==============================
    # ✅ WORLD OF WARCRAFT CLASSIC
    # ==============================
    "WOWC": "WOWC",
    "CLASSIC": "WOWC",
    "ERA": "ERA",
    "HC": "HC",
    "HARDCORE": "HC",
    "SOD": "SOD",

    # --- Classic expansions ---
    "TBCC": "TBCC",
    "TBC": "TBCC",
    "WOTLKC": "WOTLKC",
    "CATAC": "CATAC",
    "MOPC": "MOPC",
    "WODC": "WODC",
    "LEGC": "LEGC",

    # Private / Anniversary
    "PRS": "PRS",
    "ANV": "ANV",

    # ==============================
    # ✅ DIABLO SERIES
    # ==============================
    "DIABLO": "D1",
    "D1": "D1",
    "D2R": "D2R",
    "D3": "D3",
    "D4": "D4",
    "D4VH": "D4VH",

    # ==============================
    # ✅ PATH OF EXILE
    # ==============================
    "POE": "POE",
    "POE2": "POE2",
    "PO2": "POE2",

    # ==============================
    # ✅ LOST ARK (Renamed -> LARK)
    # ==============================
    "LARK": "LARK",
    "LOSTARK": "LARK",
    "LAK": "LARK",
    "LA": "LARK",

    # ==============================
    # ✅ MAJOR MMORPG
    # ==============================
    "AION": "AION",
    "AIONC": "AIC",
    "AIC": "AIC",

    "ALB": "ALB",
    "AA": "AA",
    "AAW": "AAW",
    "BNS": "BNS",
    "BNS2": "BNS2",
    "BDO": "BDO",
    "BDM": "BDM",
    "CO": "CO",
    "CORE": "CORE",
    "DAD": "DAD",
    "EVE": "EVE",
    "ESO": "ESO",
    "FFXIV": "FFXIV",
    "GW2": "GW2",
    "RO": "RO",
    "RVD": "RVD",
    "RS3": "RS3",
    "OSRS": "OSRS",
    "RPL": "RPL",
    "SRO": "SRO",
    "SWTOR": "SWTOR",
    "TRS": "TRS",
    "TIB": "TIB",
    "TL": "TL",
    "VR": "VR",

    # ==============================
    # ✅ FPS / SURVIVAL / ACTION
    # ==============================
    "ABI": "ABI",
    "APEX": "APEX",
    "BS": "BS",
    "COC": "COC",
    "CR": "CR",
    "CS2": "CS2",
    "DBD": "DBD",
    "DESTINY": "D2",
    "D2": "D2",
    "DT": "DT",
    "EFT": "EFT",
    "FIN": "FIN",
    "F76": "F76",
    "FH5": "FH5",
    "GEN": "GEN",
    "HSR": "HSR",
    "HD": "HD",
    "LOL": "LOL",
    "MS": "MS",
    "NBA2K": "NBA2K",
    "OH": "OH",
    "OW2": "OW2",
    "PAL": "PAL",
    "PZ": "PZ",
    "QF": "QF",
    "REM2": "REM2",
    "RUST": "RUST",
    "SOT": "SOT",
    "TF2": "TF2",
    "TFD": "TFD",
    "VAL": "VAL",
    "WF": "WF",
    "WW": "WW",
    "ZZZ": "ZZZ",

    # ==============================
    # ✅ SPECIAL / LEGACY MMORPG
    # ==============================
    "AQW": "AQW",
    "ROR": "ROR",
}


# =====================================================================
# ✅ Reverse Mapping: ISO → IOC (one direction guaranteed)
# =====================================================================
ISO_TO_IOC = {iso: ioc for ioc, iso in IOC_TO_ISO.items()}


# =====================================================================
# ✅ Historical Aliases (for old crawlers / legacy imports)
# =====================================================================
IOC_HISTORICAL_TO_ISO = {
    "WOWR": "DFL",        # old Dragonflight ref
    "WOWCL": "WOWC",      # classic shorthand
    "WOWHC": "HC",
    "WOWSD": "SOD",
    "POEX": "POE",
    "DIAB": "D1",
    "DIIV": "D4",
    "AIONC": "AIC",
    "FF14": "FFXIV",
    "RS3": "RS3",
    "OSRS": "OSRS",
    "GWII": "GW2",
}


# =====================================================================
# ✅ Validation: ensures IOC_TO_ISO only uses real GAMES[] codes
# =====================================================================
def check_ioc_games(verbosity: int = 1):
    """
    Verify that all IOC codes correctly map to GAMES in django_games.data.GAMES
    """
    from django_games.data import GAMES

    if verbosity:
        print("Checking IOC <-> Game mappings…")

    missing = []
    for iso in ISO_TO_IOC:
        if iso not in GAMES:
            missing.append(iso)

    if missing:
        print("⚠️ Missing canonical codes in GAMES:")
        for m in missing:
            print(f"  - {m}")
    else:
        print("✅ All IOC mappings match canonical GAMES!")

    return missing


if __name__ == "__main__":
    check_ioc_games()
