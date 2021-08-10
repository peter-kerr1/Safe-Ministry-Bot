from discord import DiscordException
from discord.ext import commands

import yagmail
from datetime import datetime
import pytz

class ErrorHandler(commands.Cog, name='Error Handler'):
    """
    Handles error messages, and where they are sent.
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
        # If nothing is found, we keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # If the error is contained inside the Discord.py library, output the error message to the context where is was caused.
        # If the error is from something else, it is probably a breaking bug. Email the error message to the dev.
        if isinstance(error, DiscordException):
            error = str(error).replace("Command raised an exception: ", '')
            await ctx.send("**[Error]** " + error)
        else:
            currentTime = datetime.now(pytz.timezone('Australia/Sydney')).strftime("%H:%M")
            yag = yagmail.SMTP('stmattsyouth.bot@gmail.com', oauth2_file="credentials/yagmail_oauth2.json")
            contents = [f"An error occurred at {currentTime}. The error was:", "<br>"
                        f"{str(type(error))[1:-1]}: {error}"]
            yag.send(self.devEmailAddress, "Safe Ministry Bot Error", contents)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))