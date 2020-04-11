import discord
import re
import datetime
import json
from event import Events
import configparser
client = discord.Client()


# Discord bot things
@client.event
async def on_ready():
    print("The bot is ready!")
    #await client.change_presence(game=discord.Game(name="Making a bot"))


@client.event
async def on_message(message):
    # if message.author == client.user or not (message.channel.name == "schedule" or message.channel.name == "bot"):
    #     return
    if message.content.startswith('.add ') and message.channel.name == "orar_manager":
        await message.channel.send(events.add(message.content))
    if message.content.startswith('.addR ') and message.channel.name == "orar_manager":
        await message.channel.send(events.addR(message.content))
    if message.content.startswith('.orar'):
        if message.channel.name == "311" or message.channel.name == "312" or message.channel.name == "313" or message.channel.name == "314" or message.channel.name == "315":
            await message.channel.send(events.show(message.content, message.channel.name))
        else:
            await message.channel.send(events.show(message.content, "all"))


# Inits and config read
config = configparser.ConfigParser()
config.read("./config.ini")
TOKEN = str(config.get("bot", "token"))

events = Events('events.json')

# Bot run
client.run(TOKEN)
