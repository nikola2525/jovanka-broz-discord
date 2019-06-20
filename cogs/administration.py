from discord.ext import commands
from lib.database_manager import DBM
import asyncio


class Admin(commands.Cog):
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
                await member.add_roles(
                    role, reason='Default role koji daje Jovanka Broz')

    @commands.group(name='settings',
                    aliases=['s'],
                    invoke_without_command=True,
                    help='Command subgroup for WoW\'s guilds')
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Settings command passed...')

    @settings.command(name='joinmsg', aliases=['jm'])
    async def settings_on_join_message(self, ctx, *, msg):
        # Get settings
        settings = await DBM.guild_settings_get(ctx.guild.id)
        # Show current message if available
        try:
            await ctx.send("Trenutno ovo šaljem novim članovima:\n\n" +
                           settings['on_join']['msg'])
            # Prompt
            prompt = await ctx.send(
                "Da li želite da promenim tu poruku u ovo?\n\n" + msg)
            await prompt.add_reaction('👍')
            await prompt.add_reaction('👎')

            def check(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '👍'
                                               or str(reaction.emoji) == '👎')

            try:
                reaction, user = await self.bot.wait_for('reaction_add',
                                                         timeout=60.0,
                                                         check=check)
            except asyncio.TimeoutError:
                reaction = '👎'
                await ctx.send('Dosta sam čekala... Neću menjati poruku.')

            if reaction.emoji == '👎':
                print(reaction.emoji)
                await ctx.send('Poruka nije promenjena.')
                return
        except:
            pass
        # Set message
        await DBM.guild_settings_set(ctx.guild.id, "on_join.msg", msg)
        # ACK
        await ctx.send("Poruka je uspešno promenjena.")
        return

    @settings.command(name='joinrole', aliases=['jr'])
    async def settings_on_join_role(self, ctx, *, rolename):
        # Check if role exists on server
        if not [
                role for role in ctx.guild.roles
                if role.name.lower() == rolename.lower()
        ]:
            await ctx.send(f"Role {rolename} ne postoji na ovom serveru.")
            return
        # Get settings
        settings = await DBM.guild_settings_get(ctx.guild.id)
        # Show current message if available
        try:
            await ctx.send(
                f"Trenutni default role je {settings['on_join']['role']}")
            # Prompt
            prompt = await ctx.send(
                f"Da li želite da promenim default role u {rolename.title()}")
            await prompt.add_reaction('👍')
            await prompt.add_reaction('👎')

            def check(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '👍'
                                               or str(reaction.emoji) == '👎')

            try:
                reaction, user = await self.bot.wait_for('reaction_add',
                                                         timeout=60.0,
                                                         check=check)
            except asyncio.TimeoutError:
                reaction = '👎'
                await ctx.send('Dosta sam čekala... Neću menjati default role.'
                               )

            if reaction.emoji == '👎':
                print(reaction.emoji)
                await ctx.send('Default role nije promenjen.')
                return
        except:
            pass
        # Set message
        await DBM.guild_settings_set(ctx.guild.id, "on_join.role", rolename)
        # ACK
        await ctx.send("Default role je uspešno promenjen.")
        return


if __name__ == '__main__':
    print('Please run the bot.py file')
else:
    print(f'Cog loaded: {__name__}')
