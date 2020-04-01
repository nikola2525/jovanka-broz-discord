import aiohttp

from .auth import get_access_token


class InvalidResponse(Exception):
    def __init__(self, message, code, url, params):
        super().__init__(message)
        self.code = code
        self.url = url
        self.params = params

    def __str__(self):
        return 'Status: {0} ({1}): {2} {3}'.format(
            self.code,
            self.message,
            self.url,
            self.params
        )


async def fetch_guild_profile(realm, name, fields, region='eu',
                              locale='eu_GB'):
    return await fetch_wow_resource('guild', realm, name, fields, region,
                                    locale)


async def fetch_character_profile(realm,
                                  name,
                                  fields,
                                  region='eu',
                                  locale='eu_GB'):
    return await fetch_wow_resource('character', realm, name, fields, region,
                                    locale)


async def fetch_wow_resource(resource,
                             realm,
                             name,
                             fields,
                             region='eu',
                             locale='en_GB'):
    async with aiohttp.ClientSession() as client:
        token = await get_access_token(region)
        params = {
            'locale': locale,
            'fields': fields,
            'access_token': token.token,
            'namespace': 'profile-' + region
        }
        url = 'https://' + region + '.api.blizzard.com/data/wow/' + resource + '/' + realm + '/' + name
        async with client.get(url, params=params) as response:
            if 200 <= response.status <= 299:
                json = await response.json()
                return json
            else:
                raise InvalidResponse(response.reason, response.status, url, params)
