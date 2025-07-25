#!/usr/bin/env python3

# This module instantiates and provides the api for the discord bot to run
# The discord bot will take results in the shape of
'''
{"RESPONSE": {
"BUY": [Item1, Item2..]
}
{
"SELL": [Item3], [Item4]..
}}
'''

import discord
from discord.ext import commands
from secret import discordToken

def bot_init():
    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # don't respond to ourselves
            if message.author == self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

        async def send_message(self, message_content):
            await general.send(message_content)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(discordToken)
