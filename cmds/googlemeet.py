import datetime

import discord
from discord.abc import PrivateChannel
from discord.ext import commands

from core.classes import ExtensionBase


class googlemeet(ExtensionBase):
    @commands.command(aliases=['GoogleMeet', 'gm'])
    async def meet(self, ctx, code):
        if '-' not in code:
            await ctx.reply("請輸入正確GoogleMeet代碼")
            await ctx.message.delete()

        elif isinstance(ctx.channel, PrivateChannel) == True:
            pingembed = discord.Embed(title='您的GoogleMeet網址: ' + 'https://meet.google.com/' + code,
                                      color=ctx.author.color)
            pingembed.set_author(name='中央總書記梅川',
                                 icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                          '/12f53eaa05b510b0pipee524904bd308f68.webp?size=1024')
            pingembed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=pingembed)
            await ctx.message.delete()
        elif isinstance(ctx.channel, PrivateChannel) != True:
            pingembed = discord.Embed(title='您的GoogleMeet網址: ' + 'https://meet.google.com/' + code,
                                      color=ctx.author.color)
            pingembed.set_author(name='中央總書記梅川',
                                 icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                          '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')
            pingembed.timestamp = datetime.datetime.utcnow()
            await ctx.author.send(embed=pingembed)
            await  ctx.reply("已成功私訊您GoogleMeet網址，認真上課吧!!")
            await ctx.message.delete()


async def setup(bot):
    await     bot.add_cog(googlemeet(bot))
