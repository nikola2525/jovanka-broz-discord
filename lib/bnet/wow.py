import aiohttp
import lib.bnet.auth as auth

async def fetch_guild_profile(realm, name, fields, region='eu', locale='eu_GB'):
    return await fetch_wow_resource('guild', realm, name, fields, region, locale)

async def fetch_character_profile(realm, name, fields, region='eu', locale='eu_GB'):
    return await fetch_wow_resource('character', realm, name, fields, region, locale)

async def fetch_wow_resource(resource, realm, name, fields, region='eu', locale='en_GB'):
    async with aiohttp.ClientSession() as client:
        token = await auth.get_access_token()
        params = { 'locale': locale, 'fields': fields, 'access_token': token.token }
        url = 'https://' + region + '.api.blizzard.com/wow/' + resource + '/'+ realm + '/' + name
        async with client.get(url, params=params) as response:
            json = await response.json()
            return json

