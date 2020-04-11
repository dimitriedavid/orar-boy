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
    if message.author == client.user or not (message.channel.name == "schedule" or message.channel.name == "bot"):
        return
    if message.content.startswith('.add ') and message.channel.name == "bot":
        await message.channel.send(add(message.content))
    if message.content.startswith('.orar'):
        await message.channel.send(orar(message.content))


# Inits and file reads
events = []
with open('events.json', 'r') as i:
    try:
        test = json.load(i)
        for ob in test:
            events.append(event(ob["name"], ob["date"], ob["time_specified"]))
    except json.decoder.JSONDecodeError:
        print("Events.json empty.")

config = configparser.ConfigParser()
config.read("./config.ini")
TOKEN = str(config.get("bot", "token"))

# Bot run
client.run("TOKEN")
