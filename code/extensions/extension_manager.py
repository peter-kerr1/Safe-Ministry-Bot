import os
from discord.ext import commands

# This variable is local to this file
name='Extension Manager'

class ExtensionManager(commands.Cog, name=name):
    """
    Allows for the dynamic loading, unloading and reloading of extensions, given the filename containing the extension.
    Use '!curr_extensions' to see the currently loaded extensions.
    Use '!list_extensions' to see all extensions available.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx, *, extension: str):
        """Loads an extension, given the extension filename"""
        self.bot.load_extension(f"extensions.{extension}")

    @commands.command()
    async def unload(self, ctx, *, extension: str):
        """Unloads an extension, given the extension filename"""
        if extension == 'extension_manager':
            await ctx.send(f"Unloading of {name} prevented.")
        else:
            self.bot.unload_extension(f"extensions.{extension}")

    @commands.command()
    async def reload(self, ctx, *, extension: str):
        """Reloads an extension, given the extension filename"""
        self.bot.reload_extension(f"extensions.{extension}")

    @commands.command()
    async def curr_extensions(self, ctx):
        """Lists the currently loaded extensions"""
        extList = "```Currently loaded extensions:\n"
        for extName in self.bot.extensions:
            extList += f" • {extName.split('.')[1]}\n"
        extList += "```"
        await ctx.send(extList)

    @commands.command()
    async def list_extensions(self, ctx):
        """Lists all extensions available"""
        extList = "```Available extensions:\n"
        for filename in os.listdir('./extensions'):
            if filename.endswith('.py'):
                extList += f" • {filename[:-3]}\n"
        extList += "```"
        await ctx.send(extList)

    # Ensures that only members with the Administrator permission can run the above commands
    async def cog_check(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(['administrator'])
        return True

    async def cog_command_error(self, ctx, error):
        await ctx.send("**Error:** " + str(error))
    
def setup(bot):
    bot.add_cog(ExtensionManager(bot))