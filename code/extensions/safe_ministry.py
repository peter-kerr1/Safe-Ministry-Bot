from discord.ext import commands
from discord.utils import find

from .modules.wrappers import hasRole
from .modules.constants import Roles

import asyncio

class SafeMinistry(commands.Cog, name='Safe Ministry'):
    """
    Enforces safe ministry guidelines in line with those detailed in the Safe Ministry Blueprint for Youth Ministry Leaders,
    specifically the start of section 5 and section 5)g).
    """
    def __init__(self, bot):
        self.bot = bot
        self.tempChannel = None

    # Returns True if there is a Youth member present in the list of members, False otherwise
    def youthPresent(self, members):
        return find(lambda m: hasRole(m, [Roles.YOUTH.value]), members) is not None

    # Returns False if there are youth members in the voice channel and there are less than 2 leaders present.
    # True otherwise (including if there are no youth members.)
    def validVoiceChannelState(self, voiceChannel):
        members = voiceChannel.members
        if self.youthPresent(members):
            leaders = [member for member in members if hasRole(member, [Roles.LEADER.value, Roles.YOUTH_MINISTER.value])]
            if len(leaders) < 2:
                return False
        return True

    # Deafens or undeafens all members in a voice channel, based on whether 'deaf' is True or False.
    # Sharing camera/screen is included in this definition.
    async def setChannelDeafness(self, voiceChannel, deaf):
        # Find the category that contains the current voiceChannel
        category = voiceChannel.category or voiceChannel.guild
        
        # Enable/disable sharing camera & screen
        await voiceChannel.set_permissions(voiceChannel.guild.default_role, stream=(not deaf))

        # Manage deafness of members, shuffle if sharing camera/screen and deaf=True.
        # (Disabling sharing camera/screen doesn't stop them sharing if they were already doing so.)
        for member in voiceChannel.members:
            await member.edit(deafen=deaf)
            if deaf is True:
                if member.voice.self_stream or member.voice.self_video:
                    self.tempChannel = await category.create_voice_channel(f"{voiceChannel.name}-temp")
                    await member.move_to(self.tempChannel)
                    await asyncio.sleep(0.5)
                    await member.move_to(voiceChannel)
                    await self.tempChannel.delete()
                if member.dm_channel is None:
                    await member.send(f"**Voice channel currently disabled:** there are less than two leaders in the {voiceChannel.mention} voice channel.\n"
                                       "The channel will be enabled again when two or more leaders join.\n"
                                       "*This is the only time you will receive this message.*")

    # Checks whether a voice channel is following Safe Ministry guidelines,
    # and deafens/undeafens the channel accordingly.
    async def manageChannel(self, voiceChannel):
        # Don't process the temp channel used for moving members
        if voiceChannel is self.tempChannel:
            return
        
        if self.validVoiceChannelState(voiceChannel):
            await self.setChannelDeafness(voiceChannel, False)
        else:
            await self.setChannelDeafness(voiceChannel, True)

    # Ensure safe ministry guidelines are followed in voice channels
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Only trigger when someone joins, leaves or moves between voice channels,
        # and manage the appropriate channels.
        if before.channel is None and after.channel is not None:
            await self.manageChannel(after.channel)
        elif before.channel is not None and after.channel is None:
            await self.manageChannel(before.channel)
        elif before.channel is not after.channel:
            await self.manageChannel(before.channel)
            await self.manageChannel(after.channel)

def setup(bot):
    bot.add_cog(SafeMinistry(bot))