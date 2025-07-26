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
from discord.ext import tasks
from typeids import lookup_type_id

from secret import discordToken


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0
        self.message = None

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def get_message(self, message):
        if message == None:
            pass
        else:
            self.message = message

    @tasks.loop(seconds=30)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(1398417004611899442)  # channel ID goes here
        self.counter += 1
        await channel.send(lookup_type_id(self.counter))

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

def bot_init():
    intents = discord.Intents.default()
    client = MyClient(intents=intents)
    client.run(discordToken)
