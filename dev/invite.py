import asyncio
import datetime

import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Invite(ExtensionBase):
    global inv_msg_list
    inv_msg_list = []
    global inv_msg_channel_id
    inv_msg_channel_id = []

    async def is_owner(ctx):
        return ctx.author.id == 601720742949683201

    @commands.command(aliases=['邀請', 'inv'])
    @commands.check(is_owner)
    async def invite(self, ctx):
        global inv_msg_list
        global inv_msg_channel_id
        embedVar = discord.Embed(
            description='[:flag_cn:  邀請(Invite)  :flag_cn:]('
                        'https://discord.com/oauth2/authorize?client_id=880824023863418950&scope=bot "邀請習維尼去你的伺服器")',
            color=ctx.author.color)
        icon_url = self.bot.get_user(601720742949683201).avatar_url
        embedVar.set_author(name='中央總書記梅川',
                            icon_url=icon_url)
        embedVar.timestamp = datetime.datetime.utcnow()

        inv_msg = await ctx.send(embed=embedVar)
        inviteembed = discord.Embed(title=f"**五分鐘後將刪除 `機器人邀請訊息`\n 請盡快完成邀請 ! ! !**", color=ctx.author.color)
        inviteembed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/881848877102301254/978289338334986290/succes.png')
        inviteembed.timestamp = datetime.datetime.utcnow()
        await inv_msg.reply(embed=inviteembed)

        async def delete_msg():
            if inv_msg_list:
                await asyncio.sleep(360)
                channel = self.bot.get_channel(inv_msg_channel_id[0])
                msg = await channel.fetch_message(inv_msg_list[0])
                await msg.delete()
                inv_msg_list.pop(0)
                inv_msg_channel_id.pop(0)
                await delete_msg()

        inv_msg_channel_id.append(ctx.channel.id)
        inv_msg_list.append(inv_msg.id)
        await delete_msg()


async def setup(bot):
    await  bot.add_cog(Invite(bot))
