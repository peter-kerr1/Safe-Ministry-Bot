import discord
from discord.ext import commands

import asyncio
import random

@commands.command()
async def ping(ctx):
    """Returns the latency (ping) of the bot"""
    await ctx.send(f"My ping is `{round(ctx.bot.latency * 1000)}ms`")

@commands.command()
async def coinflip(ctx):
    """Flips a coin"""
    coinEmoji = "<a:spinningCoin:804150050779037746>"
    message = await ctx.send(f"{coinEmoji} **Flipping...** {coinEmoji}")
    await asyncio.sleep(1.5)
    await message.edit(content=random.choice(["**Heads!**", "**Tails!**"]))

@commands.command()
async def botmsg(ctx, *, message: str):
    """Updates the bot's current activity"""
    # emoji = discord.PartialEmoji(name='spinningCoin', animated=True, id=804150050779037746)
    # activity = discord.Activity(type=discord.ActivityType.listening,
    #                             name="God | type ?help to see what I can do!",
    #                             details="this is another test")
    await ctx.bot.change_presence(activity=discord.Game(message))

def setup(bot):
    bot.add_command(ping)
    bot.add_command(coinflip)
    bot.add_command(botmsg)