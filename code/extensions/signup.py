from discord.ext import commands, tasks

import yagmail
from .modules.gsheets import gsheets
from .modules.constants import Roles

# Must have followed steps 1 & 2 of the following link for this extension to work:
# https://developers.google.com/sheets/api/quickstart/python
class Signup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gsheets = gsheets()
        self.spreadsheetId = '10q9-Hd-_9NMbCPils45QTnojtE6UHd2zavbZDs-y0ec'
        self.cellRange = 'Form Responses 1!A2:D'
        self.realNameIndex = 1
        self.emailAddrIndex = 3
        self.numResponses = len(self.formResponses())
        self.checkSignups.start()

    def formResponses(self):
        return self.gsheets.getValues(self.spreadsheetId, self.cellRange)

    # Sends an invite via email to the specified address
    def sendEmail(self, emailAddr, invite):
        yag = yagmail.SMTP('stmattsyouth.bot@gmail.com', oauth2_file="credentials/yagmail_oauth2.json")
        contents = ["<b>**This is an automated email**</b>", '<hr>',
                    "<p>Hi!</p>", "Here is your single-use Discord invite link, which expires after 7 days:",
                    f'<a href="{invite.url}">{invite.url}</a>',"<br>",
                    "<i>If you have any questions, reply to this email and a real person will get back to you!</i>",
                    "<br>", yagmail.inline("images/youth_logo.png")]
        yag.send(emailAddr, "St Matt's Youth Discord Sign-up Link", contents)

    # Manually send an invite link to a specified address.
    # Can be used to confirm that emails are working.
    @commands.command(name='sendinv')
    @commands.has_role(Roles.ADMIN.value)
    async def sendInv(self, ctx, *, email: str):
        welcomeChannelId = 793985785412976640
        channel = self.bot.get_channel(welcomeChannelId)
        weekInSeconds = 60*60*24*7
        invite = await channel.create_invite(max_uses=1, max_age=weekInSeconds, reason=f"Sending manual invite to {email}")
        try:
            self.sendEmail(email, invite)
        except:
            # Now that the refresh tokens have been fixed, this shouldn't happen.
            # Hence I'm not going to try to constrain the scope of the except :P
            await ctx.send(f"Email failed!")
        else:
            await ctx.send(f"Email sent!")

    # Checks to see if a new permission form has been filled out once every 5 seconds,
    # and sends an email invite to the new responses, if there are any.
    # This code is intentionally messy to remind me of certain things when this bot gets launched to run on multiple servers
    @tasks.loop(seconds=5.0)
    async def checkSignups(self):
        responses = self.formResponses()
        if not responses:
            raise UnboundLocalError("Google form responses could not be loaded")
        else:
            currNumResponses = len(responses)
            if currNumResponses > self.numResponses:

                # guild = get(self.bot.guilds, name="St Matts Youth")
                # if guild is not None:
                #     print(guild.channels)
                welcomeChannelId = 793985785412976640
                channel = self.bot.get_channel(welcomeChannelId)

                numNewResponses = currNumResponses - self.numResponses
                for newResponse in responses[-numNewResponses:]:
                    weekInSeconds = 60*60*24*7
                    invite = await channel.create_invite(max_uses=1, max_age=weekInSeconds, reason=f"Generating invite for {newResponse[self.realNameIndex]}")
                    self.sendEmail(newResponse[self.emailAddrIndex], invite)
                self.numResponses = currNumResponses

    # When the extension is unloaded, stop checking for signups
    def cog_unload(self):
        self.checkSignups.cancel()

def setup(bot):
    bot.add_cog(Signup(bot))