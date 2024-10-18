import os

import discord
from discord.ext import commands

from core.classes import ExtensionBase


class Config(ExtensionBase):

    @commands.command()
    async def unload(self, ctx, cog=None):
        error_thumbnail = False
        if str(ctx.author.id) != "601720742949683201":
            await ctx.send("你長得不像偉大的梅川中央總書記")
        if str(ctx.author.id) == "601720742949683201":
            if not cog:
                # No cog, means we reload all cogs

                embed = discord.Embed(
                    title="移除指令通知",
                    color=0xDAA520,
                    timestamp=ctx.message.created_at
                )

                for ext in os.listdir("./cmds/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:

                            self.bot.unload_extension(f"cmds.{ext[:-3]}")
                            embed.add_field(
                                name=f"成功移除指令: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except:
                            error_thumbnail = True
                            e = f'原因 : 指令`{ext}` 尚未加載'
                            embed.add_field(
                                name=f"無法移除指令: `{ext}`",
                                value=e,
                                inline=False
                            )
                for extt in os.listdir("./dev/"):
                    if extt.endswith(".py") and not extt.startswith("_"):
                        try:

                            self.bot.unload_extension(f"dev.{extt[:-3]}")
                            embed.add_field(
                                name=f"成功移除指令: `{extt}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except:
                            error_thumbnail = True
                            e = f'原因 : 指令`{extt}` 尚未加載'
                            embed.add_field(
                                name=f"無法移除指令: `{extt}`",
                                value=e,
                                inline=False
                            )
                if error_thumbnail:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                    error_thumbnail = False
                else:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=embed)
            else:
                # unload the specific cog

                embed = discord.Embed(
                    title="移除中所有指令通知",
                    color=0xDAA520,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cmds/{ext}") and not os.path.exists(f"./dev/{ext}"):

                    # if the file does not exist
                    embed.add_field(
                        name=f"移除指令失敗: `{ext}`",
                        value="沒有找到這個指令",
                        inline=False
                    )
                    error_thumbnail = True

                elif ext.endswith(".py") and not ext.startswith("_"):
                    if os.path.exists(f"./cmds/{ext}"):
                        try:

                            self.bot.unload_extension(f"cmds.{ext[:-3]}")
                            embed.add_field(
                                name=f"成功移除指令: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:

                            error_thumbnail = True
                            e = f'原因 : 指令`{ext}` 尚未加載'
                            embed.add_field(
                                name=f"無法移除指令: `{ext}`",
                                value=e,
                                inline=False
                            )

                    elif os.path.exists(f"./dev/{ext}"):
                        try:

                            self.bot.unload_extension(f"dev.{ext[:-3]}")
                            embed.add_field(
                                name=f"成功移除指令: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:

                            error_thumbnail = True
                            e = f'原因 : 指令`{ext}` 尚未加載'
                            embed.add_field(
                                name=f"無法移除指令: `{ext}`",
                                value=e,
                                inline=False
                            )
                if error_thumbnail:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                    error_thumbnail = False
                else:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=embed)

    @commands.command()
    async def load(self, ctx, cog=None):
        error_thumbnail_load = False
        if str(ctx.author.id) != "601720742949683201":
            await ctx.send("你長得不像偉大的梅川中央總書記")
        if str(ctx.author.id) == "601720742949683201":
            if not cog:
                # No cog, means we load all cogs

                embed = discord.Embed(
                    title="運行結果",
                    color=0xDAA520,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cmds/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:

                            self.bot.load_extension(f"cmds.{ext[:-3]}")

                            embed.add_field(
                                name=f"成功加載指令 : `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except:
                            error_thumbnail_load = True
                            e = f'原因 : 指令`{ext}` 已經加載完成'
                            embed.add_field(
                                name=f"加載指令失敗 : `{ext}`",
                                value=e,
                                inline=False
                            )
                for extt in os.listdir("./dev/"):
                    if extt.endswith(".py") and not extt.startswith("_"):
                        try:

                            self.bot.load_extension(f"dev.{extt[:-3]}")

                            embed.add_field(
                                name=f"成功加載指令 : `{extt}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except:
                            error_thumbnail_load = True
                            e = f'原因 : 指令`{extt}` 已經加載完成'
                            embed.add_field(
                                name=f"加載指令失敗 : `{extt}`",
                                value=e,
                                inline=False
                            )
                if error_thumbnail_load:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                    error_thumbnail_load = False
                else:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=embed)
            else:
                # reload the specific cog

                embed = discord.Embed(
                    title="運行結果",
                    color=0xDAA520,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cmds/{ext}") and not os.path.exists(f"./dev/{ext}"):
                    # if the file does not exist

                    embed.add_field(
                        name=f"加載指令失敗 : `{ext}`",
                        value="找不到這個指令",
                        inline=False
                    )
                    error_thumbnail_load = True

                elif ext.endswith(".py") and not ext.startswith("_"):
                    if os.path.exists(f"./cmds/{ext}"):
                        try:
                            self.bot.load_extension(f"cmds.{ext[:-3]}")

                            embed.add_field(
                                name=f"成功加載指令 : `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:
                            error_thumbnail_load = True
                            e = f'原因 : 指令`{ext}` 已經加載完成'
                            embed.add_field(
                                name=f"加載指令失敗 : `{ext}`",
                                value=e,
                                inline=False
                            )
                    elif os.path.exists(f"./dev/{ext}"):
                        try:

                            self.bot.load_extension(f"dev.{ext[:-3]}")
                            embed.add_field(
                                name=f"成功加載指令 : `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:
                            error_thumbnail_load = True
                            e = f'原因 : 指令`{ext}` 已經加載完成'
                            embed.add_field(
                                name=f"加載指令失敗 : `{ext}`",
                                value=e,
                                inline=False
                            )
                if error_thumbnail_load:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                    error_thumbnail_load = False
                else:

                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=embed)

    @commands.command()
    async def reload(self, ctx, cog=None):
        error_thumb_reload = False
        if str(ctx.author.id) != "601720742949683201":
            await ctx.send("你長得不像偉大的梅川中央總書記")
        if str(ctx.author.id) == "601720742949683201":
            if not cog:
                # No cog, means we reload all cogs

                embed = discord.Embed(
                    title="運行結果",
                    color=0xDAA520,
                    timestamp=ctx.message.created_at
                )
                for ext in (os.listdir("./cmds/")):
                    if ext.endswith(".py") and not ext.startswith("_"):

                        try:

                            self.bot.unload_extension(f"cmds.{ext[:-3]}")
                            self.bot.load_extension(f"cmds.{ext[:-3]}")
                            embed.add_field(
                                name=f"成功重載指令 : `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )

                        except:
                            error_thumb_reload = True
                            e = f'原因 : 指令`{ext}` 尚未加載'
                            embed.add_field(
                                name=f"指令失敗 : `{ext}`",
                                value=e,
                                inline=False
                            )
                for extt in (os.listdir("./dev/")):
                    if extt.endswith(".py") and not extt.startswith("_"):

                        try:

                            self.bot.unload_extension(f"dev.{extt[:-3]}")
                            self.bot.load_extension(f"dev.{extt[:-3]}")
                            embed.add_field(
                                name=f"成功重載指令 : `{extt}`",
                                value='\uFEFF',
                                inline=False
                            )

                        except:
                            error_thumb_reload = True
                            e = f'原因 : 指令`{extt}` 尚未加載'
                            embed.add_field(
                                name=f"指令失敗 : `{extt}`",
                                value=e,
                                inline=False
                            )
                if error_thumb_reload:
                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                    error_thumb_reload = False
                else:
                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=embed)
            else:
                # reload the specific cog

                embed = discord.Embed(
                    title="運行結果",
                    color=0xDAA520,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cmds/{ext}") and not os.path.exists(f"./dev/{ext}"):
                    # if the file does not exist

                    embed.add_field(
                        name=f"指令失敗 : `{ext}`",
                        value="找不到這個指令",
                        inline=False
                    )
                    error_thumb_reload = True

                elif ext.endswith(".py") and not ext.startswith("_"):
                    if os.path.exists(f"./cmds/{ext}"):
                        try:
                            self.bot.unload_extension(f"cmds.{ext[:-3]}")
                            self.bot.load_extension(f"cmds.{ext[:-3]}")

                            embed.add_field(
                                name=f"成功重載指令: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:
                            error_thumb_reload = True
                            e = f'原因 : 指令`{ext}` 尚未加載'
                            embed.add_field(
                                name=f"指令失敗 : `{ext}`",
                                value=e,
                                inline=False
                            )
                    elif os.path.exists(f"./dev/{ext}"):
                        try:

                            self.bot.unload_extension(f"dev.{ext[:-3]}")
                            self.bot.load_extension(f"dev.{ext[:-3]}")
                            embed.add_field(
                                name=f"成功重載指令: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:
                            error_thumb_reload = True
                            e = f'原因 : 指令`{ext}` 尚未加載'
                            embed.add_field(
                                name=f"指令失敗 : `{ext}`",
                                value=e,
                                inline=False
                            )
                if error_thumb_reload:
                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                    error_thumb_reload = False
                else:
                    embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Config(bot))
