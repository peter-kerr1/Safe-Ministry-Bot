from discord.ext import commands

from .modules.gsheets import gsheets

class NewMember(commands.Cog, name='New Member'):
    def __init__(self, bot):
        self.bot = bot
        self.gsheets = gsheets()
        self.spreadsheetId = '1sLFGdC6ITTyBmqi7egNB62ztD5gUUMAXcihlEzFhCpw'
        self.cellRange = 'Form Responses 1!A2:D'

    def formResponses(self):
        return self.gsheets.getValues(self.spreadsheetId, self.cellRange)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        print(member.name)
        print(f"{member.name}#{member.discriminator}")

        responses = self.formResponses()
        if not responses:
            print('[ERROR]: Failed to retrieve data from Google Form responses!')
        else:
            pass

def setup(bot):
    bot.add_cog(NewMember(bot))