import datetime

import discord
from discord.ext import commands
from discord.utils import get

from core.classes import ExtensionBase


class About(ExtensionBase):
    @commands.command(aliases=['關於', 'info'])
    async def about(self, ctx):
        embedVar = discord.Embed(title='習皇帝👑',
                                 description='一個互動式的高級Discord機器人🦾' + "\n\u200b",
                                 color=ctx.author.color)
        embedVar.set_author(name='中央總書記梅川',
                            icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                     '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')
        embedVar.add_field(name='擁有者⭐', value="!!!!!梅川 ♡ (((*°▽° *）九（* °▽°*)))♪#7051" + "\n\u200b", inline=False)
        embedVar.add_field(name='開發時間🕐', value="2021-12-14", inline=True)

        embedVar.add_field(name='操作說明📖', value="在輸入欄打*help or *command" + "\n\u200b", inline=True)
        embedVar.add_field(name='政治偏好☭', value="永遠效忠共產黨   🇨🇳  🇨🇳  🇨🇳", inline=False)
        embedVar.timestamp = datetime.datetime.utcnow()
        embedVar.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/690932480005505024/975229097766707231/hi.png')
        reactions = ['🇨🇳']
        m = await ctx.send(embed=embedVar)
        for name in reactions:
            emoji = get(ctx.guild.emojis, name=name)
            await m.add_reaction(emoji or name)


async def setup(bot):
    await bot.add_cog(About(bot))
