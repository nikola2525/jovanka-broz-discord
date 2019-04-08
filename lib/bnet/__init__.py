__version__ = "0.0.1"

from os import environ

from .wow import (
    fetch_guild_profile,
    fetch_character_profile,
)

__all__ = (
    'fetch_guild_profile',
    'fetch_character_profile',
)

try:
    environ['BNET_CLIENT_ID']
    environ['BNET_CLIENT_SECRET']
except KeyError as e:
    print("Missing Battle.net credentials. Make sure %s is set as environment variable and try again." % e)
    print("You can find your credentials at https://develop.battle.net/access/")

