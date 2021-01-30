from discord.ext import commands
from discord.utils import find

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
        return find(lambda m: hasRole(m, ['Youth']), members) is not None

    # Returns True if there are 2 or more leaders in the voiceChannel, False otherwise.
    def validVoiceChannelState(self, voiceChannel):
        members = voiceChannel.members
        if self.youthPresent(members):
            leaders = [member for member in members if hasRole(member, ['Leader'])]
            if len(leaders) < 2:
                return False
        return True

    # Deafens or undeafens all members in a voice channel, based on whether 'deaf' is True or False.
    async def setChannelDeafness(self, voiceChannel, deaf):
        members = voiceChannel.members
        for member in members:
            await member.edit(deafen=deaf)
            if deaf is True and member.dm_channel is None:
                await member.send(f"**Voice channel currently disabled:** there are less than two leaders in the {voiceChannel.mention} voice channel.\n"
                                  "The channel will be enabled again when two or more leaders join.\n"
                                  "*This is the only time you will receive this message.*")

    # Checks whether a voice channel is following Safe Ministry guidelines,
    # and deafens/undeafens the channel accordingly.
    async def manageChannel(self, voiceChannel):
        if self.validVoiceChannelState(voiceChannel):
            await self.setChannelDeafness(voiceChannel, False)
        else:
            await self.setChannelDeafness(voiceChannel, True)

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