import datetime

import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Clear(ExtensionBase):
    async def is_owner(ctx):
        return ctx.author.id == 601720742949683201

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.check(is_owner)
    async def clear(self, ctx, count="6", power=None):
        if count == "unlock" and str(power).isnumeric():
            second = int(power)
            second += 1
            await  ctx.channel.purge(limit=second)
        if count == "help":
            pingembed = discord.Embed(title='使用方式: *clear number/"unlock number" ', color=ctx.author.color)
            pingembed.set_author(name='中央總書記梅川',
                                 icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                          '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')
            pingembed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=pingembed)
        if count.isnumeric() != True and count != "unlock" and count != "help":
            await ctx.send("請輸入一個數字!!!不能是小數或負數")

        if count.isnumeric():
            fist = int(count)
            if fist > 15:
                await ctx.send("數值太大!")
                pass
            elif fist == 0:
                print("數值太小")
            else:
                fist += 1
                await ctx.channel.purge(limit=fist)
            pass


async def setup(bot):
    await bot.add_cog(Clear(bot))
