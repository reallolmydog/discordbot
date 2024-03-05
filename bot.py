#basic discord bot that some parts have been removed from due to them being for specific use or potentially giving private information

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

description="basic bot testing"
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
f=open("swears.txt", "r")
stringbadwords=f.read()
badwords=stringbadwords.split(" ")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.listen('on_message') #automod
async def automod(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    if any(word in user_message for word in badwords) and username !="CobbleBot - DEV":
        await message.delete()
        await message.channel.send(f'{username}: {user_message} ({channel})')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command() # sets staff online
async def update(ctx):
    count = 0
    for member in ctx.guild.members:
        role=member.get_role(int("1126594054960988161"))
        if member.status != discord.Status.offline:
            if role in member.roles:
                count =count+ 1
    channel=bot.get_channel(int("1164587938668105868"))
    newname="number of staff online: " + str(count)
    await channel.edit(name = newname)

@bot.command() # commands relating to removing and muting users
@commands.has_role("Devs")
async def purge (ctx, limit: int):
    await ctx.channel.purge(limit=limit)

@bot.command()
@commands.has_role("Devs")
async def mute(ctx, member: discord.Member=None, time=None, *, reason=None):
    if not member:
        await ctx.send("You must mention a member to mute!")
        return
    elif not time:
        await ctx.send("You must mention a time!")
        return
    else:
        if not reason:
            reason="No reason given"
        #Now timed mute manipulation
    try:
        time_interval = time[:-1] #Gets the numbers from the time argument, start to -1
        duration = time[-1] #Gets the timed manipulation, s, m, h, d
        if duration == "s":
            time_interval = time_interval * 1
        elif duration == "m":
            time_interval = time_interval * 60
        elif duration == "h":
            time_interval = time_interval * 60 * 60
        elif duration == "d":
            time_interval = time_interval * 86400
        else:
            await ctx.send("Invalid duration input")
            return
    except Exception as e:
        print(e)
        await ctx.send("Invalid time input")
        return
    guild = ctx.guild
    Muted = discord.utils.get(guild.roles, name="Muted")
    if not Muted:
        Muted = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    else:
        await member.add_roles(Muted, reason=reason)
        muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted by {ctx.author.mention} for {reason} to {time}")
        await ctx.send(embed=muted_embed)
        await asyncio.sleep(int(time_interval))
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title='Mute over!', description=f'{ctx.author.mention} muted to {member.mention} for {reason} is over after {time}')
        await ctx.send(embed=unmute_embed)

@bot.command() #command relating to manipulation of auto mod
async def addword(ctx, word: str):
    if (word not in badwords):
        badwords.insert(0,word)
    else:
        await ctx.send("Word already exists in list")
    setofwords=""
    for i in range (0,len(badwords)):
        setofwords=setofwords+badwords[i]+" "
    setofwords=setofwords.strip()
    f=open("swears.txt", "w")
    f.write(setofwords)
    f.close()
    await ctx.send(f'words updated')

@bot.command()
async def checkwords(ctx):
    await ctx.send(badwords)

@bot.command()
async def deleteword(ctx, word: str):
    try:
        badwords.remove(word)
    except:
        await ctx.send("word does not exist in list")
    setofwords=""
    for i in range (0,len(badwords)):
        setofwords=setofwords+badwords[i]+" "
    setofwords=setofwords.strip()
    f=open("swears.txt", "w")
    f.write(setofwords)
    f.close()
    await ctx.send(f'words updated')

@bot.command() # commands relating to removing users
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked')

@bot.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} has banned')

bot.run(TOKEN)
