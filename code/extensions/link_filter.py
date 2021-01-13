from discord.ext import commands

import re
import requests
from urllib.parse import urlparse

class LinkFilter(commands.Cog, name='Link Filter'):
    def __init__(self, bot):
        self.bot = bot
        # This isn't necessarily the best regex, but it doesn't need to be perfect
        self.regex = "https?://[^\s/$.?#].[^\s]*$"
        self.imageFormats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
        self.whitelist = ["youtube.com", "youtu.be"]

    def inWhitelist(url):
        domain = urlparse(url).netloc
        domain = domain.replace("www.", '')
        return domain in self.whitelist

    def isImageURL(self, url):
        r = requests.head(url)
        if r.headers["content-type"] in self.imageFormats:
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        urls = re.findall(self.regex, message.clean_content)
        for url in urls:
            if not self.isImageURL(url) or not self.inWhitelist(url):
                await message.author.send("Only image URLs and the following websites are allowed:")
                await message.delete()

def setup(bot):
    bot.add_cog(LinkFilter(bot))