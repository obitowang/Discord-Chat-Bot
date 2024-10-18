import datetime
import time

import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Uptime(ExtensionBase):
    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @commands.command(aliases=['ut'])
    async def uptime(self, ctx, ):
        alltime = 0

        with open('jsonfile/runtime/runtime.txt') as infile:

            for line in infile:
                try:
                    num = int(line)
                    alltime += num
                except ValueError:
                    pass

        seconds = alltime + int(round(time.time() - startTime))
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60

        dayss = seconds // seconds_in_day
        hourss = (seconds - (dayss * seconds_in_day)) // seconds_in_hour
        minutess = (seconds - (dayss * seconds_in_day) - (hourss * seconds_in_hour)) // seconds_in_minute
        final_time = f"{dayss} 天, {hourss} 小時, {minutess} 分鐘"
        uptimee = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))

        uptimeembed = discord.Embed(title="現階段運行時間", description="> ** " + uptimee + " **", color=ctx.author.color)

        uptimeembed.add_field(name="累積運行時間", value="> ** " + str(final_time) + " **", inline=False)
        uptimeembed.set_author(name='中央總書記梅川',
                               icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                        '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')

        await ctx.send(embed=uptimeembed)


async def setup(bot):
    await bot.add_cog(Uptime(bot))


