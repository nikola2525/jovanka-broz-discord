import discord
from discord.ext import commands

from lib import bnet
from lib.database_manager import DBM


class GRU(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def guild_exists(self, realm_slug, guild_name):
        try:
            await bnet.fetch_guild_profile(realm_slug, guild_name, 'members')
            return True
        except bnet.InvalidResponse as error:
            if error.code == 404:
                return False
            else:
                raise

    @commands.command(
        name='gsub',
        description='Subscribe to receive roster updates for specified guild')
    async def gsub(self, ctx, realm_slug, *guild_name_parts):
        guild_name = ' '.join(guild_name_parts).lower()

        if await self.guild_exists(realm_slug, guild_name):
            if await DBM.guild_sub(ctx, realm_slug, guild_name):
                await ctx.send(
                    f'Subscribed to recieve roster changes in {guild_name.title()} on {realm_slug.title()}'
                )
            else:
                await ctx.send('Already subscribed to that guild')
        else:
            await ctx.send(
                f'Server ({realm_slug.title()}) or Guild ({guild_name.title()}) not found'
            )

    @commands.command(
        name='gunsub',
        description=
        'Unsubscribe from receiving roster updates for specified guild')
    async def gunsub(self, ctx, realm_slug, *guild_name_parts):
        guild_name = ' '.join(guild_name_parts).lower()

        if await self.guild_exists(realm_slug, guild_name):
            if await DBM.guild_unsub(ctx, realm_slug, guild_name):
                await ctx.send('Unsubscribed from {} on {}'.format(
                    guild_name.title(), realm_slug.title()))
            else:
                await ctx.send('You are not subbed to that guild')
        else:
            await ctx.send(
                f'Server ({realm_slug.title()}) or Guild ({guild_name.title()}) not found'
            )


if __name__ == '__main__':
    print('Please run the bot.py file')
else:
    print(f'Cog loaded: {__name__}')
