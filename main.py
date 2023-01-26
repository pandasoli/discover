import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from cmds.create import create
from cmds.ask import ask
from cmds.clear import clear
from valid import valid_stuff


intents = discord.Intents.default()
intents.message_content = True
load_dotenv()

bot = commands.Bot(command_prefix = 'd!', intents = intents)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')

bot.add_command(create)
bot.add_listener(ask, 'on_message')
bot.add_command(clear)

bot.run(os.getenv('BOT_TOKEN'))
