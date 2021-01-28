from discord import ChannelType
from discord.ext import commands

import re
import aiohttp
from replit import db
from urllib.parse import urlparse
from .modules.wrappers import hasRole, isLeader, getChannel

class LinkFilter(commands.Cog, name='Link Filter'):
    def __init__(self, bot):
        self.bot = bot
        # This isn't necessarily the best regex, but it doesn't need to be perfect
        self.urlRegex = 'https?://[^\s/$.?#].[^\s]*$'
        self.imageFormats = ('image/png', 'image/jpeg', 'image/jpg', 'image/gif')
        # Allows us to assume that the whitelist key exists in the db in other functions
        if "whitelist" not in db.keys():
            db["whitelist"] = []

    @commands.group()
    async def whitelist(self, ctx):
        if ctx.invoked_subcommand is None:
            message = "```Allowed websites:\n"
            for domain in sorted(db["whitelist"]):
                message += f" • {domain}\n"
            message += "```"
            await ctx.send(message)

    @whitelist.command()
    @commands.check(isLeader)
    async def add(self, ctx, domain: str):
        if domain not in db["whitelist"]:
            whitelist = db["whitelist"]
            whitelist.append(domain)
            db["whitelist"] = whitelist
            await ctx.send(f"**{domain}** added successfully.")
        else:
            await ctx.send(f"**{domain}** already in whitelist.")

    @whitelist.command()
    @commands.check(isLeader)
    async def remove(self, ctx, domain: str):
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

    async def filterMessage(self, message):
        urls = re.findall(self.urlRegex, message.clean_content)
        for url in urls:
            if not await self.isImageURL(url) and not self.inWhitelist(url):
                msg = "Only image links and the following websites are currently allowed:\n```"
                for domain in sorted(db["whitelist"]):
                    msg += f" • {domain}\n"
                suggChannel = getChannel(message.guild, "suggestions")
                msg += f"```If you think the link you just sent should be allowed, let us know in the {suggChannel.mention} channel!"
                await message.author.send(msg)
                await message.delete()
                return

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore DMs with the bot
        if message.channel.type == ChannelType.private:
            return
        # Don't filter messages of youth minister or leaders
        author = message.author
        if not hasRole(author, ['Youth Minister', 'Leader']):
            await self.filterMessage(message)

    @add.error
    @remove.error
    async def permissionsError(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            command = ctx.invoked_subcommand
            await ctx.send(f"**[Error]** You must be a leader to use the **!{command}** command.")

    # Print out error messages to the channel where they were invoked
    async def cog_command_error(self, ctx, error):
        if not isinstance(error, commands.CheckFailure):
            error = str(error).replace("Command raised an exception: ", '')
            await ctx.send("**[Error]** " + error)

def setup(bot):
    bot.add_cog(LinkFilter(bot))