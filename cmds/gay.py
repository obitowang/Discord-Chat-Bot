import random

import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Gay(ExtensionBase):
    @commands.command()
    async def gay(self, ctx, *, gaymember: discord.Member = None):
        point = random.randint(0, 100)
        if gaymember is None:
            selfname = ctx.message.author.display_name
            selfurl = ctx.message.author.avatar_url

            embedVar = discord.Embed(title=str(point) + '% Gay 指數', color=ctx.author.color)
            embedVar.set_author(name=ctx.message.author.name,
                                icon_url=selfurl)
            await ctx.send(embed=embedVar)
        else:
            displayname = gaymember.display_name
            embedVar = discord.Embed(title=str(point) + '% Gay 指數', color=gaymember.color)

            userAvatarUrl = gaymember.avatar_url
            embedVar.set_author(name=gaymember,
                                icon_url=userAvatarUrl)

            await ctx.send(embed=embedVar)


async def setup(bot):
    await bot.add_cog(Gay(bot))
