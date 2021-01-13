from discord.utils import get

# Adds a role to a member, if it exists.
# Returns True on success, False on failure.
async def addRole(member, role, reason=None):
    role = get(member.guild.roles, name=role)
    if role is not None:
        await member.add_roles(role, reason=reason)
        return True
    return False