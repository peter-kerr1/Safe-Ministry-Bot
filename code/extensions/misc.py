from discord.ext import commands

@commands.command()
async def ping(ctx):
    """Returns the latency (ping) of the bot"""
    await ctx.send(f"My ping is `{round(ctx.bot.latency * 1000)}ms`")

def setup(bot):
    bot.add_command(ping)