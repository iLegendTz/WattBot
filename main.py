import os

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

client = commands.Bot(command_prefix=">")


@client.event
async def on_ready():
    print('Wattbot esta ready <3')

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

client.run(os.getenv("TOKEN"))
