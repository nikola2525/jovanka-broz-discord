import aiohttp
import asyncio
import redis
import pickle
from os import environ
from datetime import datetime, timedelta

r = redis.from_url(environ['REDIS_URL'])


class AccessToken:
    token = None
    expiration_date = datetime.now()

    def __init__(self, json):
        self.token = json['access_token']
        expires_in_seconds = json['expires_in']
        self.expiration_date = datetime.now() + timedelta(
            seconds=expires_in_seconds)

    def is_expired(self):
        return self.expiration_date <= datetime.now()


async def fetch_fresh_token(region):
    client_id = environ['BNET_CLIENT_ID']
    r.set('bnet_client_id', client_id)
    client_secret = environ['BNET_CLIENT_SECRET']
    auth = aiohttp.BasicAuth(client_id, password=client_secret)
    async with aiohttp.ClientSession(auth=auth) as client:
        async with client.post('https://' + region + '.battle.net/oauth/token',
                               data={'grant_type':
                                     'client_credentials'}) as response:
            assert response.status == 200
            json = await response.json()
            return AccessToken(json)


async def get_access_token(region):
    raw_token = r.get(get_token_key(region))

    if raw_token is None:
        token = await fetch_fresh_token(region)
        r.set(get_token_key(region), pickle.dumps(token))
        return token
    else:
        token = pickle.loads(raw_token)
        if token.is_expired():
            invalidate_current_token()
            get_access_token(region)
        else:
            return token


def invalidate_current_token():
    r.delete(get_token_key())


def get_token_key(region):
    client_id = r.get('bnet_client_id') or 'unknown'
    return region + 'bnet_access_token_%s' % client_id


async def main():
    token = await get_access_token()
    print(token.token)
    print(token.expiration_date)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
