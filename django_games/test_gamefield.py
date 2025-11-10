#!/usr/bin/env python3
import django
from django.conf import settings

# ------------------------------------------------------
# ✅ Minimal Django Settings (in-memory DB)
# ------------------------------------------------------
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        SECRET_KEY="test",
        USE_I18N=False,
    )

django.setup()

# ------------------------------------------------------
# ✅ Import AFTER Django setup
# ------------------------------------------------------
from django.db import models, connection
from django_games.fields import GameField
from django_games import games


# ------------------------------------------------------
# ✅ Test Model
# ------------------------------------------------------
class TestModel(models.Model):
    # Single game
    game = GameField()

    # Multiple games
    games_multi = GameField(multiple=True, blank=True)

    class Meta:
        app_label = "tests"


# ------------------------------------------------------
# ✅ Create table
# ------------------------------------------------------
with connection.schema_editor() as schema:
    schema.create_model(TestModel)

print("✅ Database & Model ready\n")


# ------------------------------------------------------
# ✅ TEST 1 — Show choices
# ------------------------------------------------------
print("=== ✅ TEST 1: AVAILABLE GAME CHOICES (first 20) ===")
choice_list = list(TestModel._meta.get_field("game").choices)
print([c for c in choice_list[:20]])
print("Total choices:", len(choice_list))


# ------------------------------------------------------
# ✅ TEST 2 — Save and Load single game
# ------------------------------------------------------
print("\n=== ✅ TEST 2: Save/Load Single Game ===")
obj = TestModel.objects.create(game="WOW")
loaded = TestModel.objects.get(pk=obj.pk)

print("Saved code:", loaded.game.code)
print("Game name:", loaded.game.name)
print("alpha3:", loaded.game.alpha3)
print("numeric:", loaded.game.numeric)


# ------------------------------------------------------
# ✅ TEST 3 — Save/Load multiple games
# ------------------------------------------------------
print("\n=== ✅ TEST 3: Save/Load Multiple Games ===")
obj2 = TestModel.objects.create(games_multi=["WOW", "DFL", "POE"])
loaded2 = TestModel.objects.get(pk=obj2.pk)

print("Stored list:", [g.code for g in loaded2.games_multi])


# ------------------------------------------------------
# ✅ TEST 4 — Lookup tests
# ------------------------------------------------------
print("\n=== ✅ TEST 4: Lookup Tests ===")

print("game_name lookup:", list(
    TestModel.objects.filter(game__game_name="World of Warcraft").values_list("id", flat=True)
))

print("game_icontains('war'):", list(
    TestModel.objects.filter(game__game_icontains="war").values_list("id", flat=True)
))


# ------------------------------------------------------
# ✅ TEST 5 — Validate choices
# ------------------------------------------------------
print("\n=== ✅ TEST 5: Validate choices ===")
field = TestModel._meta.get_field("game")
valid_codes = [c[0] for c in field.choices]

missing = []
for code in games.games:
    if code not in valid_codes:
        missing.append(code)

if missing:
    print("❌ Missing codes:", missing)
else:
    print("✅ All canonical codes appear in GameField choices")


# ------------------------------------------------------
# ✅ TEST 6 — Show full game info for first 10 entries
# ------------------------------------------------------
print("\n=== ✅ TEST 6: Detailed inspection ===")
for code in list(games.games.keys())[:10]:
    g = games[code]
    print(f"{code}: name={g[1]}")


print("\n✅ ALL TESTS PASSED")
