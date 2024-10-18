import discord
from discord.ext import commands

from core.classes import ExtensionBase


class vote(ExtensionBase):
    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):

        if len(options) > 2:
            await ctx.send('```太多選項了 ```')
            return

        if len(options) == 2 and options[0] == "yes" and options[1] == "no":
            reactions = ['👍', '👎']
        else:
            reactions = ['👍', '👎']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)

        poll_embed = discord.Embed(title=question, color=0x31FF00, description=''.join(description))

        react_message = await ctx.send(embed=poll_embed)

        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)


async def setup(bot):
    await bot.add_cog(vote(bot))
