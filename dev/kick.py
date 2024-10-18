from datetime import datetime

import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Kick(ExtensionBase):
    @commands.command()
    async def kick(self, ctx, *, member: discord.Member = None, reason=None):

        if ctx.author.id == 601720742949683201:
            if member != None:
                await member.kick(reason=reason)
                embedVar = discord.Embed(
                    description="``` >>> 成功踢出 " + member + " ```",
                    color=ctx.author.color)
                embedVar.set_author(name='中央總書記梅川',
                                    icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                             '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')

                embedVar.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embedVar)
            else:
                await ctx.send("請輸入要踢出的對象名子")
        else:
            await ctx.send("你長得不像偉大的梅川中央總書記")


async def setup(bot):
    await  bot.add_cog(Kick(bot))
