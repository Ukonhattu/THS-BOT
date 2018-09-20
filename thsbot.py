import discord
from discord.ext import commands
import random
import os
import giphy_client
from giphy_client.rest import ApiException
import json
import wolframalpha
from googletrans import Translator

translator = Translator()



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
########Wolfram ALPHA
wa_client = wolframalpha.Client(os.environ['WOLFRAM_TOKEN'])
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

@bot.command()
async def komennot():
    commands = """Komennot:
?komennot: Kaikki komennot
?repla : Random repla THS elokuvista
?gif <tag>: Random gif, haettu tägin perusteella. Laita usean sanan tägit lainausmerkkeihin. Esim. ?gif \"Funny cat\"
?promt : Random kirjoitusprompti
?choose <asia> <toinen asia>: Valitsee yhden annetuista asioista. Asioita voi antaa mielivaltaisen määrän. Laita useamman sanan asiat lainausmerkkeihin.
?roll <noppien määrä>d<sivujen määrä>: antaa joukon random lukuja. Esim ?roll 4d20
?add <luku1> <luku2>: Laskee kaksi lukua yhteen. Vitun turha komento. Nauttikaa.
?wa <haku> : WolframAlpha. Laita usean sanan haut lainausmerkkeihin. Laskee mitä vain, vastaa mihin vain (ainakin melkein)"""
    await bot.say(commands)

@bot.command()
async def wa(params):
    res = wa_client.query(params)
    await bot.say(res.texts)

@bot.command()
async def translate(text, source='tunnista', target='fi'):
    if source == "tunnista":
        translation = translator.translate(text, dest=target)
    else:
        translation = translator.translate(text, dest=target, src=source)
    await bot.say(translation.text)




bot.run(token)