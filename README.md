# br_game
poetry install
poetry run daphne BattleRoyale.asgi:application
poetry run daphne -p 8787 BattleRoyale.asgi:application