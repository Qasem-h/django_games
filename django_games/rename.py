#!/usr/bin/env python3
import os
import re
import shutil
from datetime import datetime

# === CONFIG ===
SOURCE_DIR = "/Users/qasemhajizadeh/Dev/TryMMO/django_games/django_games/icon"
TARGET_DIR = "/Users/qasemhajizadeh/Dev/TryMMO/django_games/django_games/static/icons"

# === GAME DEFINITIONS ===
def _(x):
    return x

GAMES = {
    # === WORLD OF WARCRAFT RETAIL SERIES ===
    "WOW": _("World of Warcraft"),
    "WRB": _("World of Warcraft: The Burning Crusade"),
    "WRW": _("World of Warcraft: Wrath of the Lich King"),
    "WRC": _("World of Warcraft: Cataclysm"),
    "WRM": _("World of Warcraft: Mists of Pandaria"),
    "WRD": _("World of Warcraft: Warlords of Draenor"),
    "WRL": _("World of Warcraft: Legion"),
    "WRZ": _("World of Warcraft: Battle for Azeroth"),
    "WRS": _("World of Warcraft: Shadowlands"),
    "WRF": _("World of Warcraft: Dragonflight"),
    "WRN": _("World of Warcraft: The War Within"),
    "WRT": _("World of Warcraft: Midnight"),
    "WRG": _("World of Warcraft: The Last Titan"),
    "WRX": _("World of Warcraft: The Void Reborn"),
    "WRY": _("World of Warcraft: Realms of Light"),
    "WRV": _("World of Warcraft: The End of Time"),

    # === WORLD OF WARCRAFT CLASSIC SERIES ===
    "WOC": _("World of Warcraft Classic"),
    "WCE": _("World of Warcraft Classic Era"),
    "WHC": _("World of Warcraft Classic Hardcore"),
    "WSD": _("World of Warcraft: Season of Discovery"),
    "WBC": _("World of Warcraft: The Burning Crusade Classic"),
    "WWR": _("World of Warcraft: Wrath of the Lich King Classic"),
    "WCC": _("World of Warcraft: Cataclysm Classic"),
    "WMC": _("World of Warcraft: Mists of Pandaria Classic"),
    "WWA": _("World of Warcraft: Warlords of Draenor Classic"),
    "WLC": _("World of Warcraft: Legion Classic"),
    "WBZ": _("World of Warcraft: Battle for Azeroth Classic"),
    "WSL": _("World of Warcraft: Shadowlands Classic"),
    "WDC": _("World of Warcraft: Dragonflight Classic"),

    # === PRIVATE / SPECIAL ===
    "WPR": _("World of Warcraft Private Server"),
    "WAN": _("World of Warcraft Classic Anniversary Edition"),

    # === OTHER MMORPGs ===
    "POE": _("Path of Exile"),
    "PO2": _("Path of Exile 2"),
    "DIA": _("Diablo"),
    "DI2": _("Diablo II: Resurrected"),
    "DI3": _("Diablo III"),
    "DI4": _("Diablo IV"),
    "AIO": _("Aion"),
    "AIC": _("Aion Classic"),
    "ALB": _("Albion Online"),
    "LAR": _("Lost Ark"),
    "LEP": _("Last Epoch"),
    "NWA": _("New World"),
    "NWT": _("New World: Aeternum"),
    "TAR": _("Tarisland"),
    "TNL": _("Throne and Liberty"),
    "PMO": _("PokeMMO"),
    "MO2": _("Mortal Online 2"),
    "WFR": _("Warframe"),
    "DAD": _("Dark and Darker"),
    "RBL": _("Roblox"),
    "MCH": _("Minecraft Hypixel Skyblock"),
    "TF2": _("Team Fortress 2"),
    "BLR": _("Black Desert Online"),
    "BDM": _("Black Desert Mobile"),
    "ESO": _("The Elder Scrolls Online"),
    "FFX": _("Final Fantasy XIV Online"),
    "GW2": _("Guild Wars 2"),
    "RAG": _("Ragnarok Online"),
    "RUN": _("RuneScape"),
    "OSR": _("Old School RuneScape"),
    "TIB": _("Tibia"),
    "EVE": _("EVE Online"),
    "SWT": _("Star Wars: The Old Republic"),
    "LOA": _("Lineage II"),
    "L2C": _("Lineage II Classic"),
    "ARC": _("ArcheAge"),
    "ARW": _("ArcheAge War"),
    "BDR": _("Blade and Soul"),
    "BD2": _("Blade and Soul 2"),
    "CON": _("Conquer Online"),
    "SRO": _("Silkroad Online"),
    "RSO": _("Rappelz Online"),
    "VRI": _("V Rising"),
    "MYO": _("Myth of Empires"),
    "UND": _("Undawn"),
    "ELO": _("Elyon Online"),
    "SEA": _("Sea of Thieves"),
    "NEO": _("Neo Steam: The Shattered Continent"),
    "GIL": _("Granado Espada Online"),
}

# === HELPERS ===
def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()

def tokenize(text: str):
    return set(normalize(text).split())

def match_filename_to_game(filename: str):
    """Deep fuzzy match: checks word overlap between filename and game title."""
    base = os.path.splitext(filename)[0]
    base_tokens = tokenize(base)
    best_code, best_score = None, 0

    for code, title in GAMES.items():
        title_tokens = tokenize(title)
        overlap = len(base_tokens & title_tokens)
        if not overlap:
            continue
        score = overlap / max(len(title_tokens), 1)
        if score > best_score:
            best_code, best_score = code, score

    return best_code, best_score

# === MAIN ===
def main():
    print("🎮 Scanning all icons deeply...\n")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Source directory not found: {SOURCE_DIR}")
        return
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    icons = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(".svg")]
    if not icons:
        print("⚠️ No .svg files found in source folder.")
        return

    matched, unmatched = [], []

    for icon in icons:
        code, score = match_filename_to_game(icon)
        src = os.path.join(SOURCE_DIR, icon)

        if code and score >= 0.25:  # tolerate slightly imperfect names
            dest = os.path.join(TARGET_DIR, f"{code}.svg")
            if os.path.exists(dest):
                os.remove(dest)
            shutil.copy2(src, dest)
            matched.append((icon, code, round(score, 2)))
        else:
            unmatched.append(icon)

    # === Summary ===
    print("\n✅ Matched Icons:")
    for orig, code, score in sorted(matched, key=lambda x: x[1]):
        print(f"  {orig:<45} →  {code}.svg   ({score*100:.0f}% match)")

    if unmatched:
        print("\n⚠️ Unmatched Icons:")
        for icon in unmatched:
            print(f"  {icon}")

    print(f"\n📦 Done! {len(matched)} icons copied to {TARGET_DIR}")
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
