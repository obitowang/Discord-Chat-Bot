import datetime

import discord
from discord.ext import commands
from discord.utils import get

from core.classes import ExtensionBase


class China(ExtensionBase):
    @commands.command(aliases=['黨', '毛澤東', '共產', '共產主義', '無產階級', '共產勢力', '五星紅旗', '中國', '中華人民共和國', '祖國'])
    async def china(self, ctx):
        embedVar = discord.Embed(title='共产党万岁!!! 🇨🇳 🇨🇳 🇨🇳',
                                 description='[中共党史☭](https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9C%8B%E5%85%B1%E7%94'
                                             '%A2%E9%BB%A8%E6%AD%B7%E5%8F%B2 "浏览中国共产党伟大的历史")\n\n>>> '
                                             '没有共产党，就没有新中国。\n毛泽东一心为人民。\n全世界的无产阶级联合起了吧 !',
                                 color=ctx.author.color)
        embedVar.set_author(name='中央總書記梅川',
                            icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                     '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')
        embedVar.timestamp = datetime.datetime.utcnow()
        reactions = ["🇨🇳"]
        m = await ctx.send(embed=embedVar)
        for name in reactions:
            emoji = get(ctx.guild.emojis, name=name)
            await m.add_reaction(emoji or name)


async def setup(bot):
    await bot.add_cog(China(bot))
