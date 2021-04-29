from discord.ext import commands, tasks

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
        self.realNameIndex = 1
        self.emailAddrIndex = 3
        self.numResponses = len(self.formResponses())
        self.checkSignups.start()

    def formResponses(self):
        return self.gsheets.getValues(self.spreadsheetId, self.cellRange)

    # Sends an invite via email to the specified address.
    def sendEmail(self, emailAddr, invite):
        yag = yagmail.SMTP('stmattsyouth.bot@gmail.com', oauth2_file="credentials/yagmail_oauth2.json")
        contents = ["<b>**This is an automated email**</b>", '<hr>',
                    "<p>Hi!</p>", "Here is your single-use Discord invite link:",
                    f'<a href="{invite.url}">{invite.url}</a>',"<br>",
                    "<i>If you have any questions, reply to this email and a real person will get back to you!</i>",
                    "<br>", yagmail.inline("images/youth_logo.png")]
        yag.send(emailAddr, "St Matt's Youth Discord Sign-up Link", contents)

    # Checks to see if a new permission form has been filled out once every 5 seconds,
    # and sends an email invite to the new responses, if there are any.
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
                    invite = await channel.create_invite(max_uses=1, reason=f"Generating invite for {newResponse[self.realNameIndex]}")
                    self.sendEmail(newResponse[self.emailAddrIndex], invite)
                self.numResponses = currNumResponses

    # When the extension is unloaded, stop checking for signups
    def cog_unload(self):
        self.checkSignups.cancel()

def setup(bot):
    bot.add_cog(Signup(bot))