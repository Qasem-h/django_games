# Django Games

A Django application that provides **Game**, **Region**, **Server**, and **Faction** fields — similar to `django-countries`, but designed for **MMORPGs**, **boosting services**, and **virtual marketplaces**.

---

## ⚙️ Quick Start

### 1. Install

```bash
pip install django-games

```



### 2. Add to INSTALLED_APPS

```bash
INSTALLED_APPS = [
    # ...
    "django_games",
]
```


### 3. Use in your models

```bash

from django_games.fields import GameField

class PlayerProfile(models.Model):
    game = GameField()
```