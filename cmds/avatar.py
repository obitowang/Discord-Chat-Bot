import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Avatar(ExtensionBase):
    @commands.command()
    async def av(self, ctx, *, avamember: discord.Member = None):

        if avamember is None:
            selfname = ctx.message.author.display_name
            selfurl = ctx.message.author.avatar_url

            embedVar = discord.Embed(title="\u2605 " + selfname + " 's avatar" + " \u2605", color=ctx.author.color)
            embedVar.set_image(url=selfurl)
            embedVar.set_author(name=ctx.message.author.name,
                                icon_url=selfurl)

            await ctx.send(embed=embedVar)

        else:
            displayname = avamember.display_name
            embedVar = discord.Embed(title="\u2605 " + displayname + " 's avatar" + " \u2605", color=avamember.color)

            userAvatarUrl = avamember.avatar_url
            embedVar.set_image(url=userAvatarUrl)
            embedVar.set_author(name=avamember,
                                icon_url=userAvatarUrl)

            await ctx.send(embed=embedVar)


async def setup(bot):
    await bot.add_cog(Avatar(bot))
