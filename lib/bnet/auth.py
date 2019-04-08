import aiohttp
from os import environ
from datetime import datetime, timedelta

class AccessToken:
    token = None
    expiration_date = None

    def __init__(self, json):
        self.token = json['access_token']
        expires_in_seconds = json['expires_in']
        self.expiration_date = datetime.now() + timedelta(seconds=expires_in_seconds)

    def is_expired(self):
        return self.expiration_date <= datetime.now()

async def fetch_fresh_token():
    client_id = environ['BNET_CLIENT_ID']
    client_secret = environ['BNET_CLIENT_SECRET']
    auth = aiohttp.BasicAuth(client_id, password=client_secret)
    async with aiohttp.ClientSession(auth=auth) as client:
        async with client.post('https://us.battle.net/oauth/token', data={ 'grant_type': 'client_credentials' }) as response:
            assert response.status == 200
            json = await response.json()
            return AccessToken(json)

async def get_access_token():
    return await fetch_fresh_token()

