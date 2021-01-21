from discord.ext import commands

import re
import requests
from urllib.parse import urlparse
from .modules.wrappers import hasRole

class LinkFilter(commands.Cog, name='Link Filter'):
    def __init__(self, bot):
        self.bot = bot
        # This isn't necessarily the best regex, but it doesn't need to be perfect
        self.regex = 'https?://[^\s/$.?#].[^\s]*$'
        self.imageFormats = ('image/png', 'image/jpeg', 'image/jpg', 'image/gif')
        self.whitelist = ['youtube.com', 'youtu.be']

    def inWhitelist(self, url):
        domain = urlparse(url).netloc
        domain = domain.replace('www.', '')
        return domain in self.whitelist

    def isImageURL(self, url):
        r = requests.head(url)
        if r.headers['content-type'] in self.imageFormats:
            return True
        return False

    async def filterMessage(self, message):
        urls = re.findall(self.regex, message.clean_content)
        for url in urls:
            if not self.isImageURL(url) and not self.inWhitelist(url):
                await message.author.send("Only image URLs and the following websites are allowed:")
                await message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if not hasRole(author, ['Youth Minister', 'Leader']):
            await self.filterMessage(message)

def setup(bot):
    bot.add_cog(LinkFilter(bot))