from discord.ext import commands, tasks

import os
import yagmail
from .modules.gsheets import gsheets

# Must have followed steps 1 & 2 of the following link for this extension to work:
# https://developers.google.com/sheets/api/quickstart/python
class Signup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gsheets = gsheets()
        self.spreadsheetId = '1sLFGdC6ITTyBmqi7egNB62ztD5gUUMAXcihlEzFhCpw'
        self.cellRange = 'Form Responses 1!A2:D'
        self.emailAddrIndex = 3
        self.numResponses = len(self.formResponses())
        self.checkSignups.start()

    def formResponses(self):
        return self.gsheets.getValues(self.spreadsheetId, self.cellRange)

    def sendEmail(self, email, invite):
        yag = yagmail.SMTP('stmattsyouth.bot@gmail.com', os.getenv('EMAIL_PASSWORD'))
        contents = ["<b>**This is an automated email**</b>", '<hr>',
                    "<p>Hi!</p>", "Here is your single-use Discord invite link:",
                    f'<a href="{invite.url}">{invite.url}</a>',"<br>",
                    "<i>If you have any questions, reply to this email and a real person will get back to you!</i>",
                    "<br>", yagmail.inline("images/youth_logo.png")]
        yag.send(email, "St Matt's Youth Discord Sign-up Link", contents)

    @tasks.loop(seconds=5.0)
    async def checkSignups(self):
        responses = self.formResponses()
        if not responses:
            print('[ERROR]: Failed to retrieve data from Google Form responses!')
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
                    invite = await channel.create_invite(max_uses=1, reason=f"Generating invite for {newResponse[1]}")
                    self.sendEmail(newResponse[self.emailAddrIndex], invite)
                self.numResponses = currNumResponses

    # When the extension is unloaded, stop checking for signups
    def cog_unload(self):
        self.checkSignups.cancel()

def setup(bot):
    bot.add_cog(Signup(bot))