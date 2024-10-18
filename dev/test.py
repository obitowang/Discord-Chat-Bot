import asyncio
import os
import re
import urllib
import urllib.request
from random import random
import aiohttp
import discord
import youtube_dl
from discord.ext import commands
from youtube_dl import YoutubeDL

from core.classes import ExtensionBase

'''
用在測試一些 指令 不是一個 實質機器人的功能

'''

class Test(ExtensionBase):

    async def is_owner(ctx):
        return ctx.author.id == 601720742949683201


    @commands.command(pass_context=True)
    async def test(self, ctx, *, query):
        color = 0x0da2ff



async def setup(bot):
    await  bot.add_cog(Test(bot))
