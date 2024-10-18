from io import BytesIO

import discord
from PIL import Image
from discord.ext import commands

from core.classes import ExtensionBase


class marry(ExtensionBase):
    @commands.command()
    async def marry(self, ctx, user: discord.Member = None):

        if user is None:
            married = Image.open("pictures/married.png")
            asset = ctx.author.avatar_url_as(size=128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)
            pfp = pfp.resize((35, 42))
            married.paste(pfp, (135, 45))
            pfp = Image.open(data)
            pfp = pfp.resize((35, 44))
            married.paste(pfp, (70, 25))
            married.save("pictures/head.png")

            await ctx.send(file=discord.File("pictures/head.png"))

        elif user is not None:

            married = Image.open("pictures/married.png")
            asset = user.avatar_url_as(size=128)
            data = BytesIO(await asset.read())
            assett = ctx.author.avatar_url_as(size=128)
            dataa = BytesIO(await assett.read())
            pfp = Image.open(dataa)
            pfp = pfp.resize((35, 44))
            married.paste(pfp, (70, 25))
            pfp = Image.open(data)
            pfp = pfp.resize((35, 42))
            married.paste(pfp, (135, 45))

            married.save("pictures/head.png")
            await ctx.send(file=discord.File("pictures/head.png"))


async def setup(bot):
    await  bot.add_cog(marry(bot))
