import asyncio
import datetime
import os
import time
from itertools import cycle
import discord
from discord.ext import commands, tasks

intents = discord.Intents().all()
intents.members = True
prefix = '*'
token = 'OTIwMzE5NTI3MTk4Mjg5OTcw.G1yrPA.vAEHoXGh9L6Q58JN9wro9qt4sZ155YTVo9ZdOA'
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jsonfile/runtime', 'runtime.json')
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
bot.remove_command('help')
status = cycle(['考取哈佛大學中', '考取清華大學中', '考取台大電機中', 'Apex Legends'])
moive = cycle(['Pornhub', 'Xvideos', 'AvPorn'])



@bot.event
async def on_ready():
    print('機器人上線了 ! !')
    change_status.start()





@bot.event
async def close():
    print("機器人斷線了 ! !")





@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(moive)))

async def load_extensions():
    for coree in os.listdir('./core'):
        if coree.endswith(".py") and "classes" not in coree:
            await bot.load_extension(f'core.{coree[:-3]}')

    for music in os.listdir('./music'):
        if music.endswith(".py"):
            await bot.load_extension(f'music.{music[:-3]}')

    for filename in os.listdir('./cmds'):
        if filename.endswith(".py"):
            await  bot.load_extension(f'cmds.{filename[:-3]}')
    for filename in os.listdir('./dev'):
        if filename.endswith(".py"):
            await bot.load_extension(f'dev.{filename[:-3]}')
async def main():
    async with bot:
        await load_extensions()
        await bot.start('0000')

asyncio.run(main())
