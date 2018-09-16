import discord
from discord.ext import commands
import random
import os
import giphy_client
from giphy_client.rest import ApiException
import json

description = '''The Hopeless Situation - Discord bot for everything'''
bot = commands.Bot(command_prefix='?', description=description)
replat_f = open("randot/replat.txt", "r")
replat = replat_f.readlines()
wrprompit_f = open("randot/wrpromt.txt", "r")
wrprompit = list(filter(None, wrprompit_f.readlines()))
token = os.environ['BOT_TOKEN']
####################
##Giphy config######
####################
api_instance = giphy_client.DefaultApi()
api_key = os.environ['GIPHY_TOKEN']
#######################################


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    
    for server in bot.servers:
        for channel in server.channels:
            if str(channel) == "general":
                await bot.send_message(channel, "Olen palannut entistä parempana! (Minut on päivitetty)")
                break

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))



@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

#############THS OMAT KOMENNOT ALKAA TÄSTÄ###############

@bot.command()
async def repla():
    await bot.say(replat[random.randint(0,len(replat)-1)])

@bot.command()
async def prompt():
    a = wrprompit[random.randint(0, len(wrprompit)-1)]

    await bot.say(a)


@bot.command()
async def gif(rtag):
    try:
        api_response = api_instance.gifs_random_get(api_key, tag=rtag)
        gif = api_response.data.image_url
        if not gif:
            await bot.say("haulla %s ei löyty gifiä" % rtag)
            return
        embed = discord.Embed()
        embed.set_image(url=gif)
        content = "Random gif tägillä: " + rtag  
        await bot.say(content=content,embed=embed)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)


bot.run(token)