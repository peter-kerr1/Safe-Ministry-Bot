from discord.utils import get
from .constants import Roles

# Adds a role to a member, if it exists.
# Returns True on success, False on failure.
async def addRole(member, role, reason=None):
    role = get(member.guild.roles, name=role)
    if role is not None:
        await member.add_roles(role, reason=reason)
        return True
    return False

# Returns True if the member has any of the specified roles, False otherwise
def hasRole(member, roles):
    for role in roles:
        if get(member.roles, name=role) is not None:
            return True
    return False

# Returns true if the message author is a Youth Minister or Leader.
# Designed to be used as a check for a command, eg: @commands.check(isLeader) above a command definition.
async def isLeader(ctx):
    return hasRole(ctx.author, [Roles.YOUTH_MINISTER.value, Roles.LEADER.value])

# Returns the channel in the guild that has a name matching channelName
def getChannel(guild, channelName):
    return get(guild.channels, name=channelName)