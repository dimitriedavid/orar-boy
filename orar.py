import discord
from discord.ext import tasks
import re
import datetime
import json
import asyncio
from event import Events
import configparser
client = discord.Client()


# Discord bot things
@client.event
async def on_ready():
    print("The bot is ready!")
    client.loop.create_task(updateEvent())

@client.event
async def on_message(message):
    try:
        if message.content.startswith('.add ') and message.channel.name == "orar_manager":
            await message.channel.send(events.add(message.content))
        if message.content.startswith('.addR ') and message.channel.name == "orar_manager":
            await message.channel.send(events.addR(message.content))
        if message.content.startswith('.orar'):
            if message.channel.name == "311" or message.channel.name == "312" or message.channel.name == "313" or message.channel.name == "314" or message.channel.name == "315":
                await message.channel.send(events.show(message.content, message.channel.name))
            else:
                await message.channel.send(events.show(message.content, "all"))
        if message.content.startswith('.del') and message.channel.name == "orar_manager":
            await message.channel.send(events.delete(message.content))
    except:
        print("We caught an error")

# Move events that passed into the old_events file
async def updateEvent():
    while True:
        channel = client.get_channel(698667176596471858);
        res = events.updateOldEvents()
        if res != 0:
            await channel.send(res)
        await asyncio.sleep(300)

# Inits and config read
config = configparser.ConfigParser()
config.read("./config.ini")
TOKEN = str(config.get("bot", "token"))

events = Events('events.json', 'old_events.json')

# Bot run
client.run(TOKEN)
