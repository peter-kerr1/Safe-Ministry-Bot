from discord.ext import commands

class SafeMinistry(commands.Cog, name='Safe Ministry'):
    """
    Enforces safe ministry guidelines in line with those detailed in the Safe Ministry Blueprint for Youth Ministry Leaders,
    specifically the start of section 5 and section 5)g).
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def echo(ctx, *, message: str):
        await ctx.send(message)
    
def setup(bot):
    bot.add_cog(SafeMinistry(bot))