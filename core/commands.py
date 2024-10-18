from discord.ext import commands

from core.classes import ExtensionBase


class Commands(ExtensionBase):
    @commands.command(aliases=['Commands', 'cmd', 'cmds'])
    async def command(self, ctx, cmd):
        uptimelist = ['ut', 'Uptime', 'uptime']
        translist = ['translate', '翻譯', 'tr', '翻', '譯', 'Trans']
        talklist = ['Talk', 'talk']
        snipelist = ['Sinpe', 'snipe']
        pinglist = ['Ping', 'ping']
        invitelist = ['invite', '邀請', 'inv', 'Invite']
        chinalist = ['祖國', '黨', '毛澤東', '共產', '共產主義', '無產階級', '共產勢力', '五星紅旗', '中國', '中華人民共和國', 'China']
        avlist = ['av', 'Av']
        if str(cmd) in str(avlist):
            await ctx.send("`  Avatar 指令使用方法\n  Avatar's aliaes:[*av,*Av]\n  方法:[*av @member]or[*av]  `")

        if str(cmd) in str(chinalist):
            await ctx.send(
                "`  China 指令使用方法\n  China's aliaes:[*祖國,*黨,*毛澤東,*共產,*共產主義,*無產階級,*共產勢力,*五星紅旗,*中國,*中華人民共和國,*China]\n  方法:[*祖國]  `")

        if str(cmd) in str(invitelist):
            await ctx.send("`  Invite 指令使用方法\n  Invite's aliaes:[*invite,*邀請,'inv','Invite']\n  方法:[*邀請]  `")
        if str(cmd) in str(pinglist):
            await ctx.send("`  Ping 指令使用方法\n  Ping's aliaes:[*ping,*Ping]\n  方法:[*ping]  `")
        if str(cmd) in str(snipelist):
            await ctx.send("`  Snipe 指令使用方法\n  Snipe's aliaes:[*Snipe,*snipe]\n  方法:[*snipe]  `")
        if str(cmd) in str(talklist):
            await ctx.send("`  Talk 指令使用方法\n  Talk's aliaes:[*Snipe,*snipe]\n  方法:[*talk message]  `")
        if str(cmd) in str(translist):
            await ctx.send(
                "`  Translate 指令使用方法\n  Translate's aliaes:[*translate,*翻譯,*tr,*翻,*譯,*Trans]\n  方法:[*tr 要得到的語言 message]  `")
        if str(cmd) in str(uptimelist):
            await ctx.send("`  Uptime 指令使用方法\n  Uptime's aliaes:[*ping,*Ping]\n  方法:[*ut]  `")


async def setup(bot):
    await bot.add_cog(Commands(bot))
