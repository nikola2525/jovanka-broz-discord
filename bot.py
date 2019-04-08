import os
import discord
import asyncio
from discord.ext import commands
from cogs.administration import Admin
from cogs.guild_roster_updates import GRU
from lib.database_manager import DBM
from cogs.music import Music
from lib import background_tasks


class JovankaBroz(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = "v0.1"
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.atb_apps())
        self.bg_task = self.loop.create_task(self.roster_changes())

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='Zivela Jugoslavija!'))

        print('---------------------')
        print(f'Ulogovala sam se kao {self.user.name} ({self.user.id})')
        print(f'Verzija: {self.version}')
        print(f'Trenutno sam na tacno {len(self.guilds)} servera...!')
        print('---------------------')

        # for guild in self.guilds:
        #     await DBM.guild_settings_init(guild.id, guild.name)
    
    async def on_message(self, message):
        await self.process_commands(message)

    async def on_guild_join(self, guild):
        await DBM.guild_settings_init(guild.id, guild.name)

    async def on_member_join(self, member):
        return

    async def atb_apps(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await background_tasks.new_atb_apps(bot)
            print('ATB applications have been processed')
            print('---------------------')
            await asyncio.sleep(60)  # task runs every 60 seconds

    async def roster_changes(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await background_tasks.guild_roster_check(bot)
            print('Guild rosters have been checked.')
            print('---------------------')
            await asyncio.sleep(60)  # task runs every 60 seconds


def get_prefix(bot, message):
    prefixes = ['!']
    if not message.guild:
        return '!'
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = JovankaBroz(command_prefix=get_prefix, description='Jovanka Broz')
bot.add_cog(Admin(bot))
bot.add_cog(GRU(bot))
bot.add_cog(Music(bot))

bot.run(os.environ['JB_DISC_TOKEN'], bot=True, reconnect=True)

