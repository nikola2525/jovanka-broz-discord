import os
import asyncio

import discord
from discord.ext import commands

from lib.database_manager import DBM
from lib import background_tasks
from cogs.administration import Admin
from cogs.guild_roster_updates import GRU
from cogs.music import Music

#import sys
#sys.path.insert(1, 'lib')
#from database_manager import DBM
#import background_tasks

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix = '#',intents=intents)

@client.event
async def on_ready():
    print("Jovanka je tu.")
    

async def load_client_extensions():
    #for filename in os.listdir('./GreenBot/cogs'):
    client.remove_command('help')
    cogsPth = os.path.join(".", "cogs")
    for filename in os.listdir(cogsPth):
        if filename.endswith('.py'):
            await client.load_extension("cogs." + filename[:-3])
    

async def main():
    async with client:
        client.loop.create_task(load_client_extensions())
        await client.start(os.environ['JB_DISC_TOKEN'])
        #await client.start(os.environ['5ded5436ba52cdf5e698948b7e9978b312688553fc527526bc5a9e1a7517d24b'])

asyncio.run(main())
