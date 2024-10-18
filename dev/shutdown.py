from discord.ext import commands

from core.classes import ExtensionBase


class Shutdown(ExtensionBase):
    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author.id == 601720742949683201:
            await ctx.reply("機器人已關閉")
            await ctx.bot.close()
        else:
            await ctx.send("你長得不像偉大的梅川中央總書記")


async def setup(bot):
    await  bot.add_cog(Shutdown(bot))
