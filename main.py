import os

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix=">")


@bot.event
async def on_ready():
    print('Wattbot esta ready <3')

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')

bot.run(os.getenv("TOKEN"))
