import discord
from discord.ext import commands
from lib import utilities as u
from lib.database_manager import DBM


class GRU(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gsub', description='Subscribe to receive roster updates for specified guild')
    async def gsub(self, ctx, realm_slug, *guild_name):
        guild_name = ' '.join(guild_name).lower()
        print(f'{ctx.message.author} subbed to {guild_name} on realm({realm_slug})')
        # Get members of a guild from WoW API
        bnet_groster = await u.get_guild_roster(realm_slug, guild_name)  # WoW API Roster Count
        # get_guild_roster() returns 404 if guild or realm are not found
        if bnet_groster[0] == 404:
            await ctx.send('Server or Guild not found')
            return
        # Check if the user that invoked the command already exists in DB for specified guild on specified realm
        sub = {
            "sub_name"  : ctx.author.name,
            "sub_dif"   : ctx.author.discriminator,
            "sub_id"    : ctx.author.id,
            "guild_name": guild_name,
            "realm_slug": realm_slug
        }
        added = await DBM.guild_sub(sub)
        if added:
            await ctx.send(
                f'Subscribed to recieve roster changes in {guild_name.title()} on {realm_slug.title()}'
            )
        else:
            await ctx.send('Already subscribed to that guild')

    @commands.command(name='gunsub', description='Unsubscribe from receiving roster updates for specified guild')
    async def gunsub(self, ctx, realm_slug, *guild_name):
        guild_name = ' '.join(guild_name).lower()
        print(f'{ctx.message.author} unsubbed from {guild_name} on realm({realm_slug})')
        # Get members of a guild from WoW API
        bnet_groster = await u.get_guild_roster(realm_slug, guild_name)  # WoW API Roster Count
        # get_guild_roster() returns 404 if guild or realm are not found
        if bnet_groster[0] == 404:
            await ctx.send('Server or Guild not found')
            return

        sub = {
            "sub_name": ctx.author.name,
            "sub_dif": ctx.author.discriminator,
            "sub_id": ctx.author.id,
            "guild_name": guild_name,
            "realm_slug": realm_slug
        }
        # Check if the user that invoked the command already exists in DB for specified guild on specified realm
        removed = await DBM.guild_unsub(sub)
        if removed:
            await ctx.send('Unsubscribed from {} on {}'.format(guild_name.title(), realm_slug.title()))
        else:
            await ctx.send('You are not subbed to that guild')


if __name__ == '__main__':
    print('Please run the bot.py file')
else:
    print(f'Cog loaded: {__name__}')
