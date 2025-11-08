#!/usr/bin/env python3
"""
django_games/ioc_data.py
========================
This module provides mappings similar to IOC <-> ISO codes,
adapted for MMORPG / ARPG / Sandbox MMO registry usage.

Each key represents a "franchise" or "series code" (IOC style),
and maps to a 3-letter game code (ISO style) as defined in django_games.data.GAMES.
"""

# === IOC-Style (Franchise) to ISO-Style (Game Code) ===
IOC_TO_ISO = {
    # === WORLD OF WARCRAFT SERIES ===
    "WOW": "WOW",
    "WRC": "WRC",
    "WRM": "WRM",
    "WRD": "WRD",
    "WRL": "WRL",
    "WRZ": "WRZ",
    "WRS": "WRS",
    "WRF": "WRF",
    "WRN": "WRN",
    "WRT": "WRT",
    "WRG": "WRG",
    "WOC": "WOC",
    "WCE": "WCE",
    "WHC": "WHC",
    "WSD": "WSD",
    "WBC": "WBC",
    "WWR": "WWR",
    "WCC": "WCC",
    "WMC": "WMC",
    "WWA": "WWA",
    "WLC": "WLC",
    "WBZ": "WBZ",
    "WSL": "WSL",
    "WDC": "WDC",

    # === PRIVATE / SPECIAL ===
    "WPR": "WPR",
    "WAN": "WAN",

    # === MAJOR MMORPG TITLES ===
    "POE": "POE",
    "PO2": "PO2",
    "DIA": "DIA",
    "DI2": "DI2",
    "DI3": "DI3",
    "DI4": "DI4",
    "AIO": "AIO",
    "AIC": "AIC",
    "ALB": "ALB",
    "LAR": "LAR",
    "LEP": "LEP",
    "NWA": "NWA",
    "NWT": "NWT",
    "TAR": "TAR",
    "TNL": "TNL",
    "PMO": "PMO",
    "MO2": "MO2",
    "WFR": "WFR",
    "DAD": "DAD",
    "RBL": "RBL",
    "MCH": "MCH",
    "TF2": "TF2",
    "BLR": "BLR",
    "BDM": "BDM",
    "ESO": "ESO",
    "FFX": "FFX",
    "GW2": "GW2",
    "RAG": "RAG",
    "RUN": "RUN",
    "OSR": "OSR",
    "TIB": "TIB",
    "EVE": "EVE",
    "SWT": "SWT",
    "LOA": "LOA",
    "L2C": "L2C",
    "ARC": "ARC",
    "ARW": "ARW",
    "BDR": "BDR",
    "BD2": "BD2",
    "CON": "CON",
    "SRO": "SRO",
    "RSO": "RSO",
    "VRI": "VRI",
    "MYO": "MYO",
    "UND": "UND",
    "ELO": "ELO",
    "SEA": "SEA",
    "NEO": "NEO",
    "GIL": "GIL",
}

# === Reverse Mapping: ISO → IOC ===
ISO_TO_IOC = {iso: ioc for ioc, iso in IOC_TO_ISO.items()}

# === Historical / Legacy Aliases (Optional) ===
IOC_HISTORICAL_TO_ISO = {
    "WOWR": "WRF",  # Dragonflight under older code
    "WOWC": "WRC",  # Cataclysm-era reference
    "WOWM": "WRM",  # Mists of Pandaria alias
    "WOWCL": "WOC",  # WoW Classic shorthand
    "WOWHC": "WHC",  # Hardcore alias
    "WOWSD": "WSD",  # Season of Discovery alias
    "POEX": "POE",   # Path of Exile legacy
    "POE2": "PO2",   # Path of Exile 2 beta
    "DIAB": "DIA",   # Diablo alias
    "DIIV": "DI4",   # Diablo IV alias
    "AIONC": "AIC",  # Aion Classic alias
    "NWAL": "NWA",   # New World alias
    "BDON": "BLR",   # Black Desert alias
    "FF14": "FFX",   # FFXIV common tag
    "RS3": "RUN",    # RuneScape 3
    "OSRS": "OSR",   # Old School RuneScape
    "GWII": "GW2",   # Guild Wars 2 alias
}

def check_ioc_games(verbosity: int = 1):
    """
    Verify that all IOC codes correctly map to GAMES in data.py
    """
    from django_games.data import GAMES

    if verbosity:
        print("Checking IOC <-> Game mappings…")

    missing = []
    for key in ISO_TO_IOC:
        if key not in GAMES:
            missing.append(key)

    if missing:
        print("⚠️ Missing entries in GAMES for:")
        for m in missing:
            print(f"  - {m}")
    else:
        print("✅ All IOC codes map correctly!")

    return missing


if __name__ == "__main__":
    # Run validation manually
    check_ioc_games()
