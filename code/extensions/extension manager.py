from discord.ext import commands

class ExtensionManager(commands.Cog, name='Extension Manager'):
    """Allows for the dynamic loading, unloading and reloading of extensions without taking the bot offline."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx, *, extension: str):
        """Loads an extension"""
        self.bot.load_extension(f"extensions.{extension}")

    @commands.command()
    async def unload(self, ctx, *, extension: str):
        # TODO: Prevent unloading the extension manager
        self.bot.unload_extension(f"extensions.{extension}")

    @commands.command()
    async def reload(self, ctx, *, extension: str):
        self.bot.reload_extension(f"extensions.{extension}")

    # TODO: Write an error handler to return an error message to ctx
    
def setup(bot):
    bot.add_cog(ExtensionManager(bot))