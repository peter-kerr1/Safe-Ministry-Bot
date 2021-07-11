from discord.ext import commands

import os

class ExtensionManager(commands.Cog, name='Extension Manager'):
    """
    Allows for the dynamic loading, unloading and reloading of extensions, given the filename containing the extension.
    Use '?ext' to see the currently loaded extensions.
    Use '?ext all' to see all extensions available.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ext(self, ctx):
        """Lists the currently loaded extensions. See also ?help ext"""
        if ctx.invoked_subcommand is None:
            extList = "```Currently loaded extensions:\n"
            for extName in sorted(self.bot.extensions):
                extList += f" • {extName.split('.')[1]}\n"
            extList += "```"
            await ctx.send(extList)

    @ext.command()
    async def load(self, ctx, *, extension: str):
        """Loads an extension, given the extension filename"""
        self.bot.load_extension(f"extensions.{extension}")
        await ctx.send(f"**{extension}** loaded successfully.")

    @ext.command()
    async def unload(self, ctx, *, extension: str):
        """Unloads an extension, given the extension filename"""
        extManagerFilename = os.path.basename(__file__)[:-3]
        if extension == extManagerFilename:
            await ctx.send(f"Unloading of **{extManagerFilename}** prevented.")
        else:
            self.bot.unload_extension(f"extensions.{extension}")
            await ctx.send(f"**{extension}** unloaded successfully.")

    @ext.command()
    async def reload(self, ctx, *, extension: str):
        """Reloads an extension, given the extension filename"""
        self.bot.reload_extension(f"extensions.{extension}")
        await ctx.send(f"**{extension}** reloaded successfully.")

    @ext.command()
    async def all(self, ctx):
        """Lists the filenames of all extensions available"""
        extList = "```Available extensions:\n"
        for filename in sorted(os.listdir('./extensions')):
            if filename.endswith('.py'):
                extList += f" • {filename[:-3]}\n"
        extList += "```"
        await ctx.send(extList)

    # Ensures that only members with the Administrator permission can run the above commands
    async def cog_check(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(['administrator'])
        return True

def setup(bot):
    bot.add_cog(ExtensionManager(bot))