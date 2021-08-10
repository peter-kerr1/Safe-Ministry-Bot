from discord import ChannelType
from discord.ext import commands
from discord.utils import get

import re
import aiohttp
from replit import db
from urllib.parse import urlparse
from .modules.wrappers import hasRole, isLeader
from .modules.constants import Roles

class LinkFilter(commands.Cog, name='Link Filter'):
    """
    Maintains a whitelist of websites that are allowed to be linked in messages.
    Automatically deletes non-image links that aren't in the whitelist.
    """
    def __init__(self, bot):
        self.bot = bot
        # This isn't necessarily the best regex; currently leaning on the cautious side
        self.urlRegex = 'https?://[^\s]*'
        self.imageFormats = ('image/png', 'image/jpeg', 'image/jpg', 'image/gif')
        # Allows us to assume that the whitelist key exists in the db in other functions
        if "whitelist" not in db.keys():
            db["whitelist"] = []

    @commands.group()
    async def whitelist(self, ctx):
        """Lists domains currently in the whitelist. See also ?help whitelist"""
        if ctx.invoked_subcommand is None:
            message = "```Allowed domains:\n"
            for domain in sorted(db["whitelist"]):
                message += f" • {domain}\n"
            message += "```"
            await ctx.send(message)

    @whitelist.command()
    @commands.check(isLeader)
    async def add(self, ctx, domain: str):
        """Adds a domain to the whitelist"""
        whitelist = db["whitelist"]
        if domain not in whitelist:
            whitelist.append(domain)
            db["whitelist"] = whitelist
            await ctx.send(f"**{domain}** added successfully.")
        else:
            await ctx.send(f"**{domain}** already in whitelist.")

    @whitelist.command()
    @commands.check(isLeader)
    async def remove(self, ctx, domain: str):
        """Removes a domain from the whitelist"""
        whitelist = db["whitelist"]
        if domain in whitelist:
            whitelist.remove(domain)
            db["whitelist"] = whitelist
            await ctx.send(f"**{domain}** removed successfully.")
        else:
            await ctx.send(f"**{domain}** not found in whitelist.")

    def inWhitelist(self, url):
        domain = urlparse(url).netloc
        domain = domain.replace('www.', '')
        return domain in db["whitelist"]

    async def isImageURL(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as r:
                if r.headers["content-type"] in self.imageFormats:
                    return True
                return False

    # Checks to see if the URLs in a user's message are allowed.
    # If any of them are not, a list of allowed domains is sent to the user
    # and the offending message is deleted.
    async def filterMessage(self, message):
        urls = re.findall(self.urlRegex, message.clean_content)
        for url in urls:
            if not await self.isImageURL(url) and not self.inWhitelist(url):
                msg = "Only image links and the following websites are currently allowed:\n```"
                for domain in sorted(db["whitelist"]):
                    msg += f" • {domain}\n"
                suggChannel = get(message.guild.channels, name="suggestions")
                msg += f"```If you think the link you just sent should be allowed, let us know in the {suggChannel.mention} channel!"
                await message.author.send(msg)
                await message.delete()
                return
                
    # Filters the messages of all members without the 'Youth Minister' or 'Leader' role
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore DMs with the bot
        if message.channel.type == ChannelType.private:
            return
        # Don't filter messages of youth minister or leaders
        if not hasRole(message.author, [Roles.YOUTH_MINISTER.value, Roles.LEADER.value]):
            await self.filterMessage(message)

    # Custom error message for when a non-leader tries to change the whitelist
    @add.error
    @remove.error
    async def permissionsError(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            command = ctx.invoked_subcommand
            await ctx.send(f"**[Error]** You must be a leader to use the **?{command}** command.")

def setup(bot):
    bot.add_cog(LinkFilter(bot))