import datetime
from asyncio import sleep

import discord
from discord.ext import commands

from core.classes import ExtensionBase

snipe_message_author = {}
snipe_message_content = {}
snipe_message = {}
snipe_time = {}


class Snipe(ExtensionBase):

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global snipe_message_content
        global snipe_message_author
        global snipe_message
        global snipe_time
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        snipe_time = message.created_at
        snipe_message = message
        name = message.author
        icon = name.avatar_url
        channel = self.bot.get_channel(881848877102301254)
        if not isinstance(message.channel, discord.channel.DMChannel):

            SuperEmbed = discord.Embed(title="已刪除的訊息\n" + "> " + message.content, color=0xDAA520)
            SuperEmbed.set_footer(text="")
            SuperEmbed.set_author(name=name,
                                  icon_url=icon)
            SuperEmbed.add_field(name='群組名子', value=">  " + message.guild.name + " ", inline=False)
            SuperEmbed.add_field(name='頻道名子', value=">  " + "#" + message.channel.name + " ", inline=False)
            SuperEmbed.add_field(name='頻道類型', value=">  " + "一般頻道", inline=True)
            SuperEmbed.timestamp = message.created_at

            await channel.send(embed=SuperEmbed)
        else:
            SuperEmbed = discord.Embed(title="已刪除的訊息\n" + "> " + message.content, color=0xDAA520)
            SuperEmbed.add_field(name='頻道類型', value=">  " + "私人訊息頻道", inline=True)
            SuperEmbed.set_footer(text="")
            SuperEmbed.set_author(name=name,
                                  icon_url=icon)
            SuperEmbed.timestamp = message.created_at

            await channel.send(embed=SuperEmbed)
        await sleep(500)
        del snipe_time
        del snipe_message
        del snipe_message_author[message.channel.id]
        del snipe_message_content[message.channel.id]

    @commands.command()
    async def snipe(self, ctx):
        channel = ctx.channel
        try:

            name = snipe_message_author[channel.id]
            icon = name.avatar_url

            currenttime = datetime.datetime.utcnow()

            snipeEmbed = discord.Embed(title="> " + str(snipe_message_content[channel.id]), color=ctx.author.color)
            snipeEmbed.set_footer(text="")
            snipeEmbed.set_author(name=f"{snipe_message_author[channel.id]}",
                                  icon_url=icon)
            passtime = str(currenttime - snipe_time)[:-7]
            t = passtime
            h, m, s = t.split(':')
            snipeEmbed.add_field(name='** **', value="🗑 " + str(
                datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds()) + "s ago",
                                 inline=True)

            await ctx.send(embed=snipeEmbed)



        except:
            await ctx.send("這裡沒東西給你 Snipe 哈哈 下次加油吧")


async def setup(bot):
    await bot.add_cog(Snipe(bot))
