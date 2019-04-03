import motor.motor_asyncio
import os


class DBM:
    db_main_client = motor.motor_asyncio.AsyncIOMotorClient(
            'mongodb://trishma:josipbroz369@ds036178.mlab.com:36178/jovanka-broz'
        )
    db_apps_client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://trishma:baza123@ds157528.mlab.com:57528/patrisha"
        )

    db_main = db_main_client['jovanka-broz']
    db_apps = db_apps_client['patrisha']

    coll_new_apps = db_apps['atb_applications']
    coll_old_apps = db_apps['atb_processed']

    @staticmethod
    async def guild_sub(sub):
        sub_in_db = await DBM.db_main['guild_roster_subs'].find_one(sub)
        # Add if not found
        if not sub_in_db:
            await DBM.db_main['guild_roster_subs'].insert_one(sub)
            print(f'User {sub["sub_name"]+sub["sub_dif"]} added to the database')
            return True
        else:
            return False

    @staticmethod
    async def guild_unsub(sub):
        sub_in_db = await DBM.db_main['guild_roster_subs'].find_one(sub)
        if not sub_in_db:
            return False
        else:
            await DBM.db_main['guild_roster_subs'].delete_one(sub)
            return True

    @staticmethod
    async def guild_update(guild_info):
        search_filter = {
            "guild_name": guild_info['guild_name'],
            "realm_slug": guild_info['realm_slug']
        }
        # Check if roster is in DB
        db_guild_info = await DBM.db_main['guild_roster_current'].find_one(search_filter)
        # Update if it is
        if db_guild_info:
            await DBM.db_main['guild_roster_current'].find_one_and_update(
                search_filter, {
                    '$set': {'guild_roster': guild_info['guild_roster']}
                }
            )
        # Insert if not
        else:
            await DBM.db_main['guild_roster_current'].insert_one(guild_info)

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
        await DBM.db_main['discord_server_settings'].insert_one(guild_settings)

    @staticmethod
    async def guild_settings_get(guild_id):
        settings = await DBM.db_main['discord_server_settings'].find_one({"guild_id": guild_id})
        return settings

    @staticmethod
    async def guild_settings_set(guild_id, key, value):
        search_filter = {
            "guild_id": guild_id
        }
        await DBM.db_main['discord_server_settings'].find_one_and_update(
            search_filter, {
                '$set': {key: value}
            }
        )
