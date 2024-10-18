from discord.ext import commands

from core.classes import ExtensionBase


class Speak(ExtensionBase):
    async def is_owner(ctx):
        return ctx.author.id == 601720742949683201

    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def speak(self, ctx, id, *, message):
        channel = self.bot.get_channel(int(id))
        await channel.send(message)

    @speak.error
    async def speak_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            pass


async def setup(bot):
    await    bot.add_cog(Speak(bot))
