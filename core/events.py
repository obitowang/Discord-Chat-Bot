import json

from discord.ext import commands

from core.classes import ExtensionBase


class Events(ExtensionBase):

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     classid = '920185954487132210'
    #     if str(member.guild.id) in str(classid):
    #         role = get(member.guild.roles, name="客家人")
    #         await member.add_roles(role)



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        with open('trans.json') as f:
            transjson = json.load(f)
        msg = await self.bot.get_channel(data.channel_id).fetch_message(data.message_id)
        author = msg.author
        dmid = data.member
        if str(data.emoji) == "🧐" and author == self.bot.user:
            transjsonString = str(transjson).replace("{", "[")
            await dmid.send("```語言表: " + transjsonString.replace("}", "]") + "```")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        commandname = ctx.invoked_with.lower()
        passcommds = ['talk', 'china', 'about', '關於', 'info', '黨', '毛澤東', '共產', '共產主義', '無產階級', '共產勢力', '五星紅旗', '中國',
                      '中華人民共和國', '祖國', 'invite', '邀請', 'inv', "clear", "kick", 'GoogleMeet', 'gm', 'meet', 'p', 'skip','use']
        if isinstance(error, commands.CommandNotFound) and commandname not in passcommds:
            await ctx.send("中共國沒這項指令!")
        if isinstance(error, commands.MissingRequiredArgument) and commandname not in passcommds:
            await ctx.send("習皇帝找不到你的參數!")
        if isinstance(error, commands.CommandInvokeError) and commandname not in passcommds:
            await ctx.send("指令錯誤，Google吧!")


async def setup(bot):
    await bot.add_cog(Events(bot))
