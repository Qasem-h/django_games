# test_gamefield.py

import django
from django.conf import settings

# ============================================
# ✅ STEP 1 — Configure Django BEFORE imports
# ============================================
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django_games",
            "__main__",  # ✅ our test module is an app
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        GAMES_ONLY=None,     # ✅ important default
        SECRET_KEY="test",
    )

django.setup()


# ============================================
# ✅ STEP 2 — Import AFTER setup
# ============================================
from django.db import models
from django_games.fields import GameField
from django_games import games


# ============================================
# ✅ STEP 3 — Dummy model with app_label
# ============================================
class Dummy(models.Model):
    game = GameField()
    game_multi = GameField(multiple=True)

    class Meta:
        app_label = "__main__"   # ✅ required


# ============================================
# ✅ STEP 4 — Create table
# ============================================
with django.db.connection.schema_editor() as schema:
    schema.create_model(Dummy)

print("\n✅ Database & Model ready\n")


# ============================================
# ✅ TEST 1: Choices
# ============================================
field = Dummy._meta.get_field("game")
choices = list(field.choices)

print("=== ✅ TEST 1: AVAILABLE GAME CHOICES (first 20) ===")
print(choices[:20])
print("Total choices:", len(choices), "\n")


# ============================================
# ✅ TEST 2: Save & load
# ============================================
obj = Dummy.objects.create(game="WOW")
loaded = Dummy.objects.get(pk=obj.pk)

print("=== ✅ TEST 2: Save/Load Single Game ===")
print("Saved code:", loaded.game.code)
print("Game name:", loaded.game.name)
print("alpha3:", loaded.game.alpha3)
print("numeric:", loaded.game.numeric, "\n")


# ============================================
# ✅ TEST 3: Multiple games
# ============================================
obj2 = Dummy.objects.create(game_multi=["WOW", "POE", "DFL"])
loaded2 = Dummy.objects.get(pk=obj2.pk)

print("=== ✅ TEST 3: Save/Load Multiple Games ===")
print("Stored list:", loaded2.game_multi, "\n")


# ============================================
# ✅ TEST 4: Lookups
# ============================================
print("=== ✅ TEST 4: Lookup Tests ===")
print("game_name:", list(Dummy.objects.filter(game__game_name="World of Warcraft").values_list("id", flat=True)))
print("game_icontains('war'):", list(Dummy.objects.filter(game__game_icontains="war").values_list("id", flat=True)), "\n")


# ============================================
# ✅ TEST 5: Validate all canonical codes appear
# ============================================
canonical = set(games.games.keys())
field_codes = {c[0] for c in choices}

print("=== ✅ TEST 5: Validate choices ===")
missing = canonical - field_codes
if missing:
    print("❌ Missing:", missing)
else:
    print("✅ All canonical codes appear in choices\n")


# ============================================
# ✅ TEST 6: Detailed inspection
# ============================================
for code in list(canonical)[:10]:
    g = games[code]             # ✅ correct!
    print(f"{code}: name={g.name}")