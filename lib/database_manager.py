from os import environ

import motor.motor_asyncio
from uritools import urisplit


class DBM:
    connection_uri = environ['MONGODB_URI']
    db_name = urisplit(connection_uri).path[1:]
    client = motor.motor_asyncio.AsyncIOMotorClient(connection_uri, retry_writes=False)

    db = client[db_name]

    coll_new_apps = db['atb_applications']
    coll_old_apps = db['atb_processed']

    @staticmethod
    async def guild_sub(ctx, realm_slug, guild_name):
        sub = {
            "sub_name": ctx.author.name,
            "sub_dif": ctx.author.discriminator,
            "sub_id": ctx.author.id,
            "guild_name": guild_name,
            "realm_slug": realm_slug
        }
        sub_in_db = await DBM.db['guild_roster_subs'].find_one(sub)
        # Add if not found
        if not sub_in_db:
            await DBM.db['guild_roster_subs'].insert_one(sub)
            print(
                f'User {sub["sub_name"]+sub["sub_dif"]} added to the database')
            return True
        else:
            return False

    @staticmethod
    async def guild_unsub(ctx, realm_slug, guild_name):
        sub = {
            "sub_name": ctx.author.name,
            "sub_dif": ctx.author.discriminator,
            "sub_id": ctx.author.id,
            "guild_name": guild_name,
            "realm_slug": realm_slug
        }
        sub_in_db = await DBM.db['guild_roster_subs'].find_one(sub)
        if not sub_in_db:
            return False
        else:
            await DBM.db['guild_roster_subs'].delete_one(sub)
            return True

    @staticmethod
    async def guild_update(guild_info):
        search_filter = {
            "guild_name": guild_info['guild_name'],
            "realm_slug": guild_info['realm_slug']
        }
        # Check if roster is in DB
        db_guild_info = await DBM.db['guild_roster_current'].find_one(
            search_filter)
        # Update if it is
        if db_guild_info:
            await DBM.db['guild_roster_current'].find_one_and_update(
                search_filter,
                {'$set': {
                    'guild_roster': guild_info['guild_roster']
                }})
        # Insert if not
        else:
            await DBM.db['guild_roster_current'].insert_one(guild_info)

    @staticmethod
    async def guild_settings_init(guild_id, guild_name):
        guild_settings = {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "on_join": {
                "msg": None,
                "role": None
            }
        }
        await DBM.db['discord_server_settings'].insert_one(guild_settings)

    @staticmethod
    async def guild_settings_get(guild_id):
        settings = await DBM.db['discord_server_settings'].find_one(
            {"guild_id": guild_id})
        return settings

    @staticmethod
    async def get_on_join_message(guild_id):
        settings = await DBM.db['discord_server_settings'].find_one(
            {"guild_id": guild_id})
        return settings['on_join']['msg']

    @staticmethod
    async def get_on_join_role(guild_id):
        settings = await DBM.db['discord_server_settings'].find_one(
            {"guild_id": guild_id})
        return settings['on_join']['role']


    @staticmethod
    async def guild_settings_set(guild_id, key, value):
        search_filter = {"guild_id": guild_id}
        await DBM.db['discord_server_settings'].find_one_and_update(
            search_filter, {'$set': {
                key: value
            }})
