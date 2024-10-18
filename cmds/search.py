import random

import discord
from discord.ext import commands
from googleapiclient.discovery import build
from core.classes import ExtensionBase
api_key = 'AIzaSyCk7jMoYeMOPQCd5Ef6BOTLF8N4xqdui78'


class Search(ExtensionBase):

    @commands.command(aliases=["show"])
    async def search(self, ctx, *, search):
        blck = ['Porn', 'porn', 'sex', 'sexy', '做愛', '愛愛', 'xvideos', 'xvideo', '做愛', '內射', '性愛', '性交', '口交', '肛交',
                '奶頭', '老二', '陰莖', '鮑魚', '陰道', '性侵', 'pornhub', 'Pornhub', 'PornHub', 'Xvideos', 'xvideos', '色情']
        ran = random.randint(0, 9)
        try:




            resource = build("customsearch", "v1", developerKey=api_key).cse()
            result = resource.list(
                q=f"{search}", cx="35968fbed304a2d69", searchType="image"
            ).execute()
            url = result["items"][ran]["link"]
            embed1 = discord.Embed(title=f"成功搜尋 : ({search})", color=ctx.author.color)
            embed1.set_image(url=url)
            if search not in blck:
                await ctx.send(embed=embed1)
            if search in blck:
                if str(ctx.author.id) != str('601720742949683201'):
                    await ctx.reply(ctx.message.author.mention + " 你真他媽色情")
                else:
                    await ctx.send(embed=embed1)
        except Exception as e:
         print(e)


async def setup(bot):
    await  bot.add_cog(Search(bot))


# 用 serpapi api 的寫法
#
#     title = str(search)
#     block = ['Porn', 'porn', 'sex', 'sexy', '做愛', '愛愛', 'xvideos', 'xvideo', '做愛', '內射', '性愛', '性交', '口交', '肛交',
#              '奶頭', '老二', '陰莖', '鮑魚', '陰道', '性侵', 'pornhub', 'Pornhub', 'PornHub', 'Xvideos', 'xvideos', '色情', '打炮']
#     await ctx.channel.trigger_typing()
#     if not any(ext in search for ext in block):
#         params = {
#             "api_key": "b7841fe6fde0bc5297866d040d39a7ee269b259cbed18ff42e8cd64bf489476c",
#             "engine": "google",
#             "q": f"{search}",
#             "location": "Austin, Texas, United States",
#             "google_domain": "google.com",
#             "num": "8",
#             "tbm": "isch"
#
#         }
#
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         image_results = []
#         for image in results["images_results"]:
#             image_results.append(image["original"])
#         final_pic = random.choice(image_results)
#         embed1 = discord.Embed(title=f"成功搜尋 : ({title})", color=ctx.author.color)
#         embed1.set_image(url=final_pic)
#         await ctx.send(embed=embed1)
#     else:
#         embed1 = discord.Embed(title=f"你真色情啊 !! @{ctx.author.display_name}", color=ctx.author.color)
#         await ctx.reply(embed=embed1)
#
# except Exception as e:
# print(e)

