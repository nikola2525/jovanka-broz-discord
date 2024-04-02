import discord

from datetime import datetime

from lib import utilities as u
from lib.database_manager import DBM
from lib import bnet

#import sys
#sys.path.insert(1, 'lib')
#import utilities as u
#from database_manager import DBM
#import bnet


def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]


async def new_atb_apps(bot):
    test_channel = bot.get_channel(509555856816340993)
    # trial_channel = bot.get_channel(421561007522185236)
    apps = DBM.coll_new_apps.find()
    apps.sort([('_id', -1)])  # Reverse Sort
    apps = await apps.to_list(100)
    if apps:
        for app in apps:
            embed = discord.Embed(title=' ',
                                  description=' ',
                                  color=u.color_pick(2000))
            # Set requested run as author so we can put a pretty little icon
            embed.set_author(
                name='Nova prijava: {} ({})'.format(app['personal_name'],
                                                    app['yob']),
                icon_url='https://cdn0.iconfinder.com/data/icons/large-weather-icons/256/Heat.png'
            )

            embed.add_field(
                name='Reci nam nesto o sebi',
                value='```{}```'.format(
                    app['personal_other'][:1018]
                    if app['personal_other'] else '<Nista nije uneto>'),
                inline=False)

            embed.add_field(name='Ime maina i spec',
                            value='{} ({})'.format(
                                app['main_name']
                                if app['main_name'] else '<Nista nije uneto>',
                                app['class_and_spec'] if app['class_and_spec']
                                else '<Nista nije uneto>'),
                            inline=True)

            embed.add_field(name='Armory Link',
                            value=app['armory_url']
                            if app['armory_url'] else '<Nista nije uneto>',
                            inline=False)

            embed.add_field(name='UI Link',
                            value=app['ui_screenshot_url'] if
                            app['ui_screenshot_url'] else '<Nista nije uneto>',
                            inline=False)

            embed.add_field(name='Konfiguracija kompa',
                            value='```{}```'.format(
                                app['pc_config'][:1018]
                                if app['pc_config'] else '<Nista nije uneto>'),
                            inline=True)

            embed.add_field(
                name='Mikrofon',
                value='Da' if app['microphone'] == 'true' else 'Ne',
                inline=False)

            embed.add_field(name='Raid iskustvo',
                            value='```{}```'.format(
                                app['game_other'][:1018] if app['game_other']
                                else '<Nista nije uneto>'),
                            inline=False)

            embed.add_field(
                name='Dodatne Informacije',
                value='```{}```'.format(
                    app['game_additional'][:1018]
                    if app['game_additional'] else '<Nista nije uneto>'),
                inline=False)

            embed.add_field(name='Kontakt',
                            value=app['contact_info']
                            if app['contact_info'] else '<Nista nije uneto>',
                            inline=False)

            embed.set_footer(text='Aplikacija popunjena {}'.format(
                datetime.utcfromtimestamp(
                    app['created_at']).strftime('%Y-%m-%d %H:%M:%S')), )

            await test_channel.send("@everyone", embed=embed)
            app.pop('_id', None)
            print(app)

        print('processing')
        await DBM.coll_old_apps.insert_many(apps)
        await DBM.coll_new_apps.delete_many({})


async def guild_roster_check(bot):
    """Requests guild roster from BNet API every minute
    and compares it with a previously saved roster
    then works out if any changes happened"""
    # Retrieve all guilds that need checking
    guilds_to_check = list(
        set([
            doc["guild_name"] + '-' + doc["realm_slug"]
            async for doc in DBM.db['guild_roster_subs'].find({})
        ]))
    for guild in guilds_to_check:
        # Vars for easier typing
        guild_name, realm_slug = guild.split('-', 1)
        # Retrieve current members of a specified guild from Blizzard API
        guild = await bnet.fetch_guild_profile(realm_slug, guild_name,
                                               'roster')
        bnet_guild_roster = guild['members']
        # Get the roster from the database
        db_guild_roster = DBM.db['guild_roster_current'].find({
            "guild_name":
            guild_name,
            "realm_slug":
            realm_slug
        })
        # Only filter out the member names
        bnet_guild_roster_short = [
            member['character']['name'] for member in bnet_guild_roster
        ]
        guild_info = {
            "guild_name": guild_name,
            "realm_slug": realm_slug,
            "guild_roster": bnet_guild_roster_short
        }
        try:
            db_guild_roster = [doc async for doc in db_guild_roster][0]
        except:
            print(
                f'Guild {guild_name.title()} on {realm_slug.title()} has not been found in internal DB, updating. . .'
            )
            await DBM.guild_update(guild_info)
            continue
        # Check if any differences are present
        members_left = [
            member for member in db_guild_roster['guild_roster']
            if member not in bnet_guild_roster_short
        ]
        members_joined = [
            member for member in bnet_guild_roster_short
            if member not in db_guild_roster['guild_roster']
        ]

        if members_left or members_joined:
            # Update the database
            print('Updating')
            await DBM.guild_update(guild_info)
            # Inform subscribed users
            await guild_sub_announcer(bot, guild_info, members_joined,
                                      members_left)
        else:
            print(
                f'No roster changes detected in {guild_name.title()} on {realm_slug.title()}.'
            )


async def guild_sub_announcer(bot, guild_info, joined, left):
    print(f'Announcing roster changes for {guild_info["guild_name"].title()}')
    # Get members that are subscribed
    subbed_users = DBM.db['guild_roster_subs'].find({
        "guild_name":
        guild_info['guild_name'],
        "realm_slug":
        guild_info['realm_slug']
    })
    print()
    announce_users = [user async for user in subbed_users]
    print(announce_users)
    # Print them fellas that left/got kicked
    embed = discord.Embed(
        title=' ', description=' ', color=u.color_pick(3300)
    ).set_author(
        name=f'{guild_info["guild_name"].title()} on {guild_info["realm_slug"].title()}',
        url='',
    )
    if joined:
        joined = ", ".join(joined)
        for chunk in chunks(joined, 1000):
            embed.add_field(
                name='New members:',
                value=f'```{chunk}```',
                inline=False,
            )
    if left:
        left = ", ".join(left)
        for chunk in chunks(left, 1000):
            embed.add_field(
                name='Members that left the guild:',
                value=f'```{chunk}```',
                inline=False,
            )

    for sub in announce_users:
        print("announcing to user", sub)
        user = bot.get_user(sub['sub_id'])
        await user.send(embed=embed)
