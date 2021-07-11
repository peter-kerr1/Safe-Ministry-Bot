import os
import logging
import discord
from dotenv import load_dotenv

from discord.ext import commands

from keep_awake import keep_awake

# For logging events/errors
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # Options in decending order: CRITICAL, ERROR, WARNING, INFO, DEBUG; default WARNING
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Initialize the bot
bot = commands.Bot(command_prefix='?',
                   help_command=commands.DefaultHelpCommand(no_category='Misc', dm_help=True),
                   intents=discord.Intents.all())

# Load all extensions to start
for filename in os.listdir('./extensions'):
    if filename.endswith('.py'):
        bot.load_extension(f"extensions.{filename[:-3]}")

# Load the bot password (TOKEN) as an environment variable from a '.env' file in the same directory
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Keep the program running even when repl.it is closed
keep_awake()

# Start the bot
bot.run(TOKEN)