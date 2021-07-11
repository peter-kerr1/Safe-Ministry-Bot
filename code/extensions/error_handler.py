from discord import DiscordException
from discord.ext import commands

import yagmail

class ErrorHandler(commands.Cog, name='Error Handler'):
    """
    
    """
    def __init__(self, bot):
        self.bot = bot
        self.devEmailAddress = "peter.kerr@outlook.com"

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, DiscordException):
            error = str(error).replace("Command raised an exception: ", '')
            await ctx.send("**[Error]** " + error)
        else:
            yag = yagmail.SMTP('stmattsyouth.bot@gmail.com', oauth2_file="credentials/yagmail_oauth2.json")
            currentTime = "time"
            contents = [f"An error occurred at {currentTime}. The error was:", "<br>",
                        f"{type(error)}: {error}"]
            yag.send(self.devEmailAddress, "Safe Ministry Bot Error", contents)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))