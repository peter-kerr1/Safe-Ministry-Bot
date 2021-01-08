from discord.ext import commands, tasks
from discord.utils import get

import os
import pickle
import yagmail
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Must have followed steps 1 & 2 of the following link for this extension to work:
# https://developers.google.com/sheets/api/quickstart/python
class Signup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.credentials = self.getCredentials()
        self.sheets = build('sheets', 'v4', credentials=self.credentials).spreadsheets()
        self.spreadsheetId = '1sLFGdC6ITTyBmqi7egNB62ztD5gUUMAXcihlEzFhCpw'
        self.cellRange = 'Form Responses 1!A2:D'
        self.numResponses = len(self.getResponses())
        self.checkSignups.start()

    # Get permission to access the stored Google Form responses
    def getCredentials(self):
        creds = None
        if os.path.exists('sheetsToken.pickle'):
            with open('sheetsToken.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', ['https://www.googleapis.com/auth/spreadsheets.readonly'])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('sheetsToken.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def getResponses(self):
        result = self.sheets.values().get(spreadsheetId=self.spreadsheetId,
                                          range=self.cellRange).execute()
        return result.get('values', [])

    @tasks.loop(seconds=5.0)
    async def checkSignups(self):
        values = self.getResponses()
        if not values:
            print('[ERROR]: Failed to retrieve data from Form responses!')
        else:
            currNumResponses = len(values)
            if currNumResponses > self.numResponses:

                # guild = get(self.bot.guilds, name="St Matts Youth")
                # if guild is not None:
                #     print(guild.channels)
                welcomeChannelId = 793985785412976640
                channel = self.bot.get_channel(welcomeChannelId)

                numNewResponses = currNumResponses - self.numResponses
                for newResponse in values[-numNewResponses:]:
                    invite = await channel.create_invite(max_uses=1, reason=f"Generating invite for {newResponse[1]}")
                    yag = yagmail.SMTP('stmattsyouth.bot@gmail.com', os.getenv('EMAIL_PASSWORD'))
                    contents = ["<b>**This is an automated email**</b>", '<hr>',
                                "<p>Hi!</p>", "Here is your single-use Discord invite link:",
                                f'<a href="{invite.url}">{invite.url}</a>',"<br>",
                                "<i>If you have any questions, reply to this email and a real person will get back to you!</i>",
                                "<br>", yagmail.inline("images/st_matts_youth_logo.png")]
                    yag.send(newResponse[3], "St Matt's Youth Discord Sign-up Link", contents)
                self.numResponses = currNumResponses

    # When the extension is unloaded, stop checking for signups
    def cog_unload(self):
        self.checkSignups.cancel()

def setup(bot):
    bot.add_cog(Signup(bot))