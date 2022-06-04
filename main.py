from discord import Intents
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='env.env', verbose=True)

bot = commands.Bot(
    command_prefix='^^^',
    help_command=None,
    intents=Intents.all()
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot}')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
