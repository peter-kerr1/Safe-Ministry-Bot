from discord.ext import commands
from discord.utils import find

from .modules.gsheets import gsheets
from .modules.wrappers import addRole

class NewMember(commands.Cog, name='New Member'):
    def __init__(self, bot):
        self.bot = bot
        self.gsheets = gsheets()
        self.spreadsheetId = '1sLFGdC6ITTyBmqi7egNB62ztD5gUUMAXcihlEzFhCpw'
        self.cellRange = 'Form Responses 1!A2:D'
        self.realNameIndex = 1
        self.accNameIndex = 2

    def formResponses(self):
        return self.gsheets.getValues(self.spreadsheetId, self.cellRange)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        responses = self.formResponses()
        if not responses:
            print("[ERROR]: Failed to retrieve data from Google Form responses!")
        else:
            accountName = f"{member.name}#{member.discriminator}"
            reponse = find(lambda r: r[self.accNameIndex] == accountName, responses[::-1])
            if reponse is not None:
                nickname = reponse[self.realNameIndex]
                await member.edit(nick=nickname)
            else:
                if await addRole(member, "Muted", f"{member.name}'s permission form could not be found; muting."):
                    await member.send("You have been muted because I can't find your permission form.\n"
                                      "This is probably because your Discord username was mispelt in the form - try filling it out again and rejoining.\n"
                                      "Otherwise, you can message a member with the Admin role and they should be able to help you.")

def setup(bot):
    bot.add_cog(NewMember(bot))