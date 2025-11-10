#!/usr/bin/env python

"""
Standalone diagnostic script for django_games.
Run with:
    poetry run python django_games/test.py
"""

import os
import django
from django.conf import settings

# ----------------------------------------------------------
# ✅ Step 1 — Minimal Django config (does NOT load Saleor)
# ----------------------------------------------------------
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=["django_games"],
        USE_I18N=False,
        GAMES_ONLY=None,
        GAMES_EXCLUDE=None,
        GAMES_INCLUDE=None,
    )
    django.setup()

print("\n===========================================")
print("✅ DJANGO_GAMES SELF-TEST")
print("===========================================\n")

# ----------------------------------------------------------
# ✅ Step 2 — Import django_games
# ----------------------------------------------------------
import django_games
from django_games import games

print(f"django_games module loaded from:")
print(f" → {django_games.__file__}\n")

# ----------------------------------------------------------
# ✅ Step 3 — Show which data file is providing GAMES
# ----------------------------------------------------------
try:
    # Try import from new file (if created)
    from django_games.games import GAMES, ALT_CODES
    source = "django_games/games.py"
except ImportError:
    # Fallback: old data.py version
    from django_games import data
    GAMES = data.GAMES
    ALT_CODES = data.ALT_CODES
    source = "django_games/data.py"

print(f"GAMES source file detected: {source}\n")

# ----------------------------------------------------------
# ✅ Step 4 — Display stats
# ----------------------------------------------------------
print(f"TOTAL GAMES FOUND: {len(GAMES)}")
print("\nFIRST 20 GAME CODES:")
print(list(GAMES.keys())[:20])

# ----------------------------------------------------------
# ✅ Step 5 — Validate ALT_CODES
# ----------------------------------------------------------
g = set(GAMES.keys())
a = set(ALT_CODES.keys())

print("\nVALIDATING ALT_CODES...")

missing_in_alt = g - a
missing_in_games = a - g

print(f"Missing in ALT_CODES: {missing_in_alt}")
print(f"Missing in GAMES: {missing_in_games}")

if missing_in_alt or missing_in_games:
    print("❌ ALT_CODES mismatch detected!")
else:
    print("✅ ALT_CODES perfectly match.")

# ----------------------------------------------------------
# ✅ Step 6 — Full list sorted
# ----------------------------------------------------------
print("\nFULL GAME CODE LIST (SORTED):")
for code in sorted(GAMES.keys()):
    print(" -", code)

print("\n===========================================")
print("✅ TEST COMPLETE")
print("===========================================\n")
