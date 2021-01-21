from discord.ext import commands
from discord.utils import find, get

from .modules.wrappers import hasRole

class SafeMinistry(commands.Cog, name='Safe Ministry'):
    """
    Enforces safe ministry guidelines in line with those detailed in the Safe Ministry Blueprint for Youth Ministry Leaders,
    specifically the start of section 5 and section 5)g).
    """
    def __init__(self, bot):
        self.bot = bot
        
    # Returns True if there is a Youth member present in the list of members, False otherwise
    def youthPresent(self, members):
        return find(lambda m: hasRole(m, 'Youth'), members) is not None

    def validVoiceChannelState(self, voiceChannel):
        members = voiceChannel.members
        if self.youthPresent(members):
            leaders = [member for member in members if hasRole(member, 'Leader')]
            if len(leaders) < 2:
                return False
        return True

    async def setChannelDeafness(self, channel, deaf):
        members = channel.members
        for member in members:
            await member.edit(deafen=deaf)
            if deaf is True:# and member.dm_channel is None:
                await member.send("You have been automatically deafened in line with rule x.x:\n\
                    *2 leaders pls*")

    async def manageChannel(self, channel):
        if self.validVoiceChannelState(channel):
            await self.setChannelDeafness(channel, False)
        else:
            await self.setChannelDeafness(channel, True)

    # Ensure safe ministry guidelines are followed in voice channels
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Only trigger when someone joins or leaves a voice channel
        if before.channel is None and after.channel is not None:
            await self.manageChannel(after.channel)
        elif before.channel is not None and after.channel is None:
            await self.manageChannel(before.channel)

def setup(bot):
    bot.add_cog(SafeMinistry(bot))