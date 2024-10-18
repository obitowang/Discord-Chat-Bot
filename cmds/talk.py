from discord.ext import commands

from core.classes import ExtensionBase


class Talk(ExtensionBase):

    @commands.command(pass_context=True)
    async def talk(self, ctx, *, message):
        await ctx.send(message)
        await ctx.message.delete()

    @talk.error
    async def talk_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            pass


async def setup(bot):
    await bot.add_cog(Talk(bot))
