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
        await ctx.send(f"'{extension}' loaded successfully.")

    @commands.command()
    async def unload(self, ctx, *, extension: str):
        """Unloads an extension, given the extension filename"""
        if extension == 'extension_manager':
            await ctx.send(f"Unloading of '{os.path.basename(__file__)[:-3]}' prevented.")
        else:
            self.bot.unload_extension(f"extensions.{extension}")
            await ctx.send(f"'{extension}' unloaded successfully.")

    @commands.command()
    async def reload(self, ctx, *, extension: str):
        """Reloads an extension, given the extension filename"""
        self.bot.reload_extension(f"extensions.{extension}")
        await ctx.send(f"'{extension}' reloaded successfully.")

    @commands.command()
    async def curr_ext(self, ctx):
        """Lists the currently loaded extensions"""
        extList = "```Currently loaded extensions:\n"
        for extName in sorted(self.bot.extensions):
            extList += f" • {extName.split('.')[1]}\n"
        extList += "```"
        await ctx.send(extList)

    @commands.command()
    async def list_ext(self, ctx):
        """Lists the filenames of all extensions available"""
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

    # Print out error messages to the channel where they were invoked
    async def cog_command_error(self, ctx, error):
        error = str(error).replace("Command raised an exception: ", '')
        await ctx.send("**[Error]** " + error)
    
def setup(bot):
    bot.add_cog(ExtensionManager(bot))