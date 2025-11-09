#!/usr/bin/env python3
"""
Standalone tester for django_games:
- Game
- GameField
- Registry
- ALT_CODES
- value conversion
"""

import django
from django.conf import settings

# ✅ Minimal Django settings
settings.configure(
    INSTALLED_APPS=[
        "django_games",
        "django.contrib.contenttypes",
    ],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_I18N=False,
)

django.setup()

# ----------------------------------------------------
# Imports
# ----------------------------------------------------
from django.db import models, connection
from django_games.fields import GameField, Game
from django_games import games

LINE = "------------------------------------------------------------"


# ----------------------------------------------------
# Test Model for GameField
# ----------------------------------------------------
class TestModel(models.Model):
    name = models.CharField(max_length=64)
    game = GameField(blank=True)

    class Meta:
        app_label = "tests"


# ----------------------------------------------------
# ✅ CREATE TABLE (this fixes your error)
# ----------------------------------------------------
with connection.schema_editor() as editor:
    editor.create_model(TestModel)


# ----------------------------------------------------
# BEGIN TESTS
# ----------------------------------------------------
print("\n" + LINE)
print("✅ TEST 1 — Game class basic")
print(LINE)

g = Game("ROR")
print("Code:", g.code)
print("Name:", g.name)


# ----------------------------------------------------
print("\n" + LINE)
print("✅ TEST 2 — Registry (games.games)")
print(LINE)

all_codes = list(games.games.keys())
print("Total games loaded:", len(all_codes))
print("First 10 codes:", all_codes[:10])

print("WOWC →", games.name("WOWC"))
print("wowc →", games.name("wowc"))


# ----------------------------------------------------
print("\n" + LINE)
print("✅ TEST 3 — Game conversion (VALID USAGE)")
print(LINE)

raw = "EFT"

# ✅ Game class always returns object
g1 = Game(raw)
print("Game('EFT') →", g1.code, "→", g1.name)

# ✅ GameField.to_python returns raw string normally
gf = GameField()
py_val = gf.to_python(raw)
print("GameField.to_python('EFT') returned:", repr(py_val), "TYPE:", type(py_val).__name__)


# ----------------------------------------------------
print("\n" + LINE)
print("✅ TEST 4 — Model save/load")
print(LINE)

obj = TestModel.objects.create(
    name="Tester",
    game="POE2"
)

reload = TestModel.objects.get(pk=obj.pk)
print("Stored game raw:", reload.game)             # "POE2"
print("Code:", reload.game.code)                  # "POE2"
print("Name:", reload.game.name)                  # Full name


# ----------------------------------------------------
print("\n" + LINE)
print("✅ TEST 5 — ALT_CODES alias resolution")
print(LINE)

alias = "WOTLK"
canonical = games.alpha2(alias)
print("Alias:", alias)
print("Canonical:", canonical)
print("Name:", games.name(canonical))


# ----------------------------------------------------
print("\n" + LINE)
print("✅ TEST 6 — Lookup tests")
print(LINE)

print("games.name('WOW') =", games.name("WOW"))
print("games.name('invalid') =", games.name("invalid"))


# ----------------------------------------------------
print("\n" + LINE)
print("✅ TEST COMPLETE ✅")
print(LINE + "\n")
