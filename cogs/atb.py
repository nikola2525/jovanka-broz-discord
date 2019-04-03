from discord.ext import commands
from lib.database_manager import DBM
import discord


class ATB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server_message = await DBM.get_on_join_message(member.guild)
        await member.send(server_message)

        member_role = await DBM.get_on_join_role(member.guild)
        for role in member.guild.roles:
            if member_role.lower() == role.name.lower():
                await member.add_roles(role, reason='Default role koji daje Jovanka Broz')

    @commands.group(name='settings', aliases=['s'], invoke_without_command=True, help='Command subgroup for WoW\'s guilds')
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Settings command passed...')

    @settings.command(name='joinmsg', aliases=['jm'])
    async def settings_on_join_message(self, ctx, *msg):
        return

    @settings.command(name='joinrole', aliases=['jr'])
    async def settings_on_join_role(self, ctx, *rolename):
        return


if __name__ == '__main__':
    print('Please run the bot.py file')
else:
    print(f'Cog loaded: {__name__}')
