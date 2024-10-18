import datetime

import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Ping(ExtensionBase):
    @commands.command()
    async def ping(self, ctx):
        pingg = f'{round(self.bot.latency * 1000)}'' ms'
        pingembed = discord.Embed(title=pingg, color=ctx.author.color)
        pingembed.set_author(name='中央總書記梅川',
                             icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                      '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')
        pingembed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=pingembed)


async def setup(bot):
    await bot.add_cog(Ping(bot))
