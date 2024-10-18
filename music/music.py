import asyncio
import datetime
import json
import os
import time

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from core.classes import ExtensionBase

'''
版本 = Beta 0.8

2022/5/19

Imporve:
1. 引進 search song 功能
2. 機器人 閒置超過五分鐘自動離開
3. 所有回應 加上通知Icon

Issues :
 1. loop 指令 功能正常 只是 運行時 後台 會爆錯


'''


class music(ExtensionBase):

    # async def guild_check(ctx):
    #     return ctx.author.guild.id == 615388023353507863

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_guilds_data()

    def __init__(self, bot):
        # 新版
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jsonfile/music', 'music.json')

        self.clear_all_data_init()
        # 舊版
        self.bot = bot

        # 通用 無須加到 josn
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}



    async def play_next(self, ctx):
        if not ctx.voice_client is None:
            if ctx.voice_client.is_playing():
                self.change_data_boolean_value(ctx.guild.id, "is_bot_playing", True)
            else:
                self.change_data_boolean_value(ctx.guild.id, "is_bot_playing", False)
            if self.get_data_boolean_value(ctx.guild.id, "has_been_stopLoop"):
                self.change_data_boolean_value(ctx.guild.id, "loop", False)
            if len(self.get_data_String_value(ctx.guild.id, "queue")) >= 1:

                with YoutubeDL(self.YDL_OPTIONS) as ydl:

                        info = ydl.extract_info(self.get_data_String_value(ctx.guild.id, "queue")[0], download=False)
                        url2 = info['formats'][0]['url']
                        vidtitle = info.get("title", None)
                        vidurl = self.get_data_String_value(ctx.guild.id, "queue")[0]
                        video_thumbnail = info.get("thumbnail")
                        self.change_data_String_value(ctx.guild.id, "now_playing_thumbnail", video_thumbnail)
                        self.change_data_String_value(ctx.guild.id, "now_playing_url", vidurl)

                        self.change_data_String_value(ctx.guild.id, "now_playing_uploader", info.get("uploader", None))
                        self.change_data_String_value(ctx.guild.id, "now_playing_duration", (info.get("duration", None)))
                        self.change_data_String_value(ctx.guild.id, "now_playing_reacter_id", ctx.author.id)
                        self.change_data_String_value(ctx.guild.id, "now_playing", vidtitle)

                    if not self.get_data_boolean_value(ctx.guild.id, "is_skip") and not self.get_data_boolean_value(
                            ctx.guild.id, "loop") and not self.get_data_boolean_value(ctx.guild.id,
                                                                                      "is_loop_disable") and not self.get_data_boolean_value(
                        ctx.guild.id, "is_skip_succes"):
                        await ctx.channel.trigger_typing()
                        playembed = discord.Embed(title="成功播放 !!!", color=ctx.author.color)
                        playembed.add_field(name=vidtitle, value=f'[影片連結]({vidurl})', inline=True)
                        playembed.set_image(url=video_thumbnail)
                        playembed.set_thumbnail(
                            url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                        playembed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed=playembed)
                    elif self.get_data_boolean_value(ctx.guild.id, "first_loop") and not self.get_data_boolean_value(
                            ctx.guild.id, "is_loop_enable") and not self.get_data_boolean_value(ctx.guild.id,
                                                                                                "is_skip") and not self.get_data_boolean_value(
                        ctx.guild.id, "is_skip_succes"):
                        await ctx.channel.trigger_typing()
                        self.change_data_boolean_value(ctx.guild.id, "first_loop", False)
                        playembed = discord.Embed(title="成功播放 !!!", color=ctx.author.color)
                        playembed.add_field(name=vidtitle, value=f'[影片連結]({vidurl})', inline=True)
                        playembed.set_image(url=video_thumbnail)
                        playembed.set_thumbnail(
                            url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                        playembed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed=playembed)
                    elif self.get_data_boolean_value(ctx.guild.id, "is_skip"):
                        pass



                    loop = asyncio.get_event_loop()
                    try:


                        ctx.voice_client.play(discord.FFmpegPCMAudio(url2, **self.FFMPEG_OPTIONS),
                                          after=lambda ex: loop.create_task(self.play_next(ctx)))

                    except Exception as e :
                     print(e)

                    self.change_data_boolean_value(ctx.guild.id, "is_playing", True)
                    self.change_data_boolean_value(ctx.guild.id, "is_skip", False)

                    if ctx.voice_client.is_playing():
                        self.change_data_boolean_value(ctx.guild.id, "is_bot_playing", True)

                    else:
                        self.change_data_boolean_value(ctx.guild.id, "is_bot_playing", False)

                    if not self.get_data_boolean_value(ctx.guild.id, "loop") and not self.get_data_boolean_value(
                            ctx.guild.id, "is_loop_disable"):
                        self.del_queue_url(ctx.guild.id, 0)



                    elif (not self.get_data_boolean_value(ctx.guild.id, "loop") and self.get_data_boolean_value(
                            ctx.guild.id, "is_loop_disable")) and len(
                        self.get_data_String_value(ctx.guild.id, "queue")) >= 1:
                        ctx.voice_client.stop()
                        self.del_queue_url(ctx.guild.id, 0)

                        self.change_data_boolean_value(ctx.guild.id, "is_loop_disable", False)

                    else:
                        try:

                            await self.play_next(ctx)
                        except:

                            pass

            elif not self.get_data_boolean_value(ctx.guild.id, "is_bot_playing"):
                await ctx.channel.trigger_typing()
                self.change_data_boolean_value(ctx.guild.id, "is_playing", False)
                self.save_last_channel(ctx.guild, ctx.channel)

                stopembed = discord.Embed(title="**音樂通知 !**", color=ctx.author.color)
                stopembed.add_field(name="**音樂清單已經全數播放完畢 ! **", value='\uFEFF', inline=False)
                stopembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                stopembed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=stopembed)
            else:
               pass

    # 偵測網址 是否可用
    def is_supported(self, url):
        extractors = youtube_dl.extractor.gen_extractors()
        for e in extractors:
            if e.suitable(url) and e.IE_NAME != 'generic':
                return True
        return False

    # 加載 music 指令時 會 先刪除 所有檔案
    def clear_all_data_init(self):
        try:
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
                music_file = {}
            with open(self.json_path, 'w') as f:
                json.dump(music_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("刪除全部檔案有錯誤", e)

    # 加載 每個群組資料
    def check_guilds_data(self):
        server_list = []
        for guild in self.bot.guilds:
            server_list.append(guild.id)
        with open(self.json_path, 'r') as f:
            music_file = json.load(f)
        for i in range(len(server_list)):
            if not str(server_list[i]) in music_file:
                music_file[server_list[i]] = {}
                music_file[server_list[i]]['queue'] = []
                music_file[server_list[i]]['loop'] = False
                music_file[server_list[i]]['bot'] = None
                music_file[server_list[i]]['start_count'] = False
                music_file[server_list[i]]['first_loop'] = False
                music_file[server_list[i]]['is_loop_disable'] = False
                music_file[server_list[i]]['is_resume'] = False
                music_file[server_list[i]]['is_pause'] = False
                music_file[server_list[i]]['skip_loopSong'] = False
                music_file[server_list[i]]['has_been_stopLoop'] = False
                music_file[server_list[i]]['is_skip'] = False
                music_file[server_list[i]]['is_skip_succes'] = False
                music_file[server_list[i]]['skip_name'] = ""
                music_file[server_list[i]]['skip_url'] = ""
                music_file[server_list[i]]['is_playing'] = False
                music_file[server_list[i]]['is_bot_playing'] = False
                music_file[server_list[i]]['is_loop_enable'] = False
                music_file[server_list[i]]['now_playing'] = ""
                music_file[server_list[i]]['wrong_url'] = False
                music_file[server_list[i]]['now_playing_reacter_id'] = None
                music_file[server_list[i]]['now_playing_thumbnail'] = ""
                music_file[server_list[i]]['now_playing_url'] = ""
                music_file[server_list[i]]['now_playing_uploader'] = ""
                music_file[server_list[i]]['now_playing_duration'] = None

        with open(self.json_path, 'w') as f:
            json.dump(music_file, f, indent=4)

    def change_data_boolean_value(self, guild_id, value_name, boolean):
        # 專用於 設定 False 或者 True 的 布林直
        try:
            guild_id = str(guild_id)
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
                music_file[guild_id][value_name] = [boolean]
            with open(self.json_path, 'w', encoding="utf-8") as f:
                json.dump(music_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("設定布林值有錯誤", f"name={value_name}", f"錯誤 = {e}")

    def change_data_String_value(self, guild_id, value_name, string):
        # 專用於 設定 False 或者 True 的 String 值
        try:
            value_name = str(value_name)
            guild_id = str(guild_id)
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
                music_file[guild_id][value_name] = [string]
            with open(self.json_path, 'w', encoding="utf-8") as f:
                json.dump(music_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("設定String值有錯誤", f"name={value_name}", f"錯誤 = {e}")

    def get_data_String_value(self, guild_id, value_name):
        try:
            # 專用於 設定 False 或者 True 的 String 值
            guild_id = str(guild_id)
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)

            return music_file[guild_id][value_name]
        except Exception as e:
            print("抓取String值有錯誤", f"name={value_name}", f"錯誤= {e}")

    def catch_String_valueable(self, guild_id, value_name):
        try:
            # 專用於 設定 False 或者 True 的 String 值
            guild_id = str(guild_id)
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)

            return music_file[guild_id][value_name][0]
        except Exception as e:
            print("catch_String 有錯誤", f"name={value_name}", f"錯誤= {e}")

    def get_data_boolean_value(self, guild_id, value_name):
        try:
            # 專用於 設定 False 或者 True 的 String 值
            guild_id = str(guild_id)
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
                final_value = music_file[guild_id][value_name]
            if final_value == False:
                return False
            else:
                final_value = music_file[guild_id][value_name][0]
                if final_value == True:
                    return True
                else:
                    return False
        except Exception as e:
            print("抓取boolean 有錯", f"name=f{value_name}", f"錯誤 = {e}")

    # 添加網址到 音樂列表
    def added_queue_url(self, guild_id, url):
        try:
            guild_id = str(guild_id)
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
            music_file[guild_id]['queue'].append(url)
            with open(self.json_path, 'w', encoding="utf-8") as f:
                json.dump(music_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("新增音樂清單出錯", f"錯誤 = {e}")

    # 刪除音樂網址
    def del_queue_url(self, guild_id, delete_type):
        try:
            guild_id = str(guild_id)
            # 回傳值 delete_type : 0 = 刪一個 , 1 = 全刪
            if delete_type == 0:
                with open(self.json_path, 'r', encoding="UTF-8") as f:
                    music_file = json.load(f)
                if music_file[guild_id]['queue']:
                    music_file[guild_id]['queue'].pop(0)

                with open(self.json_path, 'w', encoding="UTF-8") as f:
                    json.dump(music_file, f, indent=4, ensure_ascii=False)
            elif delete_type == 1:
                with open(self.json_path, 'r', encoding="UTF-8") as f:
                    music_file = json.load(f)
                music_file[guild_id]['queue'].clear()
                with open(self.json_path, 'w', encoding="UTF-8") as f:
                    json.dump(music_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("刪除網址有錯誤", f"錯誤 = {e}")

    @commands.command()
    async def p(self, ctx, url, *keyword):
        botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)

        async def play_music(self, final_url):
            url = final_url
            if botvoice is None and not ctx.author.voice is None:
                await ctx.channel.trigger_typing()
                joinembed = discord.Embed(title=f"**成功加入到 : `#{ctx.author.voice.channel}` **",
                                          color=ctx.author.color)
                joinembed.timestamp = datetime.datetime.utcnow()
                joinembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                self.save_last_channel(ctx.guild, ctx.channel)

                await ctx.send(embed=joinembed)

            if ctx.author.voice != None:
                await ctx.channel.trigger_typing()
                self.added_queue_url(ctx.guild.id, url)
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    added_name = info.get("title", None)
                    added_url = info.get("url", None)
                    added_thumbnail = info.get("thumbnail", None)

                addded_queue_embed = discord.Embed(title="成功加入播放清單 !!", color=ctx.author.color)
                addded_queue_embed.add_field(name=added_name, value=f'[影片連結]({self.get_data_String_value(ctx.guild.id, "queue")[0]})', inline=True)
                addded_queue_embed.set_thumbnail(url=added_thumbnail)
                addded_queue_embed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)

                await ctx.send(embed=addded_queue_embed)
            elif botvoice != None and ctx.author.id == 601720742949683201:
                await ctx.channel.trigger_typing()
                self.added_queue_url(ctx.guild.id, url)
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    added_name = info.get("title", None)
                    added_url = info.get("url", None)
                    added_thumbnail = info.get("thumbnail", None)
                addded_queue_embed = discord.Embed(title="成功加入播放清單 !!", color=ctx.author.color)

                addded_queue_embed.add_field(name=added_name, value=f'[影片連結]({added_url})', inline=True)
                addded_queue_embed.set_thumbnail(url=added_thumbnail)
                addded_queue_embed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=addded_queue_embed)
            else:
                await ctx.channel.trigger_typing()
                playingmbed = discord.Embed(title="**你不在語音頻道 !!! **", color=ctx.author.color)
                playingmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                playingmbed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=playingmbed)
            if ctx.author.voice is not None and botvoice is None:
                await ctx.author.voice.channel.connect()
                self.save_last_channel(ctx.guild, ctx.channel)
                await self.play_next(ctx)
            else:
                if not self.get_data_boolean_value(ctx.guild.id, "is_playing"):
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await self.play_next(ctx)

        if self.is_supported(url) and not url == "search":

            if not "playlist?" in str(url):
                try:
                    with YoutubeDL(self.YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(url, download=False)
                except Exception as ele:
                    find = "Unable to recognize tab page"
                    if find in str(ele):
                        self.change_data_boolean_value(ctx.guild.id, "wrong_url", True)
                if not self.get_data_boolean_value(ctx.guild.id, "wrong_url"):
                    await play_music(self, url)
                else:
                    await ctx.channel.trigger_typing()
                    self.change_data_boolean_value(ctx.guild.id, "wrong_url", False)
                    playingmbed = discord.Embed(title="請勿貼搜尋結果 ! ! ", color=ctx.author.color)
                    playingmbed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                    playingmbed.add_field(name="**正確用法 : 請貼單一的YouTube 音樂/影片 連結 ! ! !**", value='\uFEFF',
                                          inline=False)
                    playingmbed.timestamp = datetime.datetime.utcnow()
                    await ctx.reply(embed=playingmbed)
            else:
                await ctx.channel.trigger_typing()
                playingmbed = discord.Embed(title="請勿貼 影片/音樂 清單  ! ! ", color=ctx.author.color)
                playingmbed.add_field(name="**機器人尚未支持 播放 影片/音樂 的清單連結**", value='\uFEFF',
                                      inline=False)
                playingmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                playingmbed.add_field(name="**正確用法 : 請貼單一的YouTube 音樂/影片 連結 ! ! !**", value='\uFEFF',
                                      inline=False)

                playingmbed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=playingmbed)
        elif url == "search":

            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                video = ydl.extract_info(f"ytsearch:{keyword}", download=False)['entries'][0]['webpage_url']

            await play_music(self, video)

        else:
            await ctx.channel.trigger_typing()
            playingmbed = discord.Embed(title=f"`{url}` 不是一個有效的Youtube 音樂/影片 網址 ! ! !", color=ctx.author.color)
            playingmbed.add_field(name="請重新添加 你喜歡的 `音樂/影片` 的網址 !!!", value='\uFEFF', inline=False)
            playingmbed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            playingmbed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=playingmbed)

    @commands.command(aliases=['np', 'now'])
    async def nowplaying(self, ctx):

            if self.get_data_boolean_value(ctx.guild.id, "is_bot_playing"):
                guild_member = self.bot.get_guild(ctx.guild.id)
                reacter_np = guild_member.get_member(
                    self.catch_String_valueable(ctx.guild.id, "now_playing_reacter_id"))
                if int(self.catch_String_valueable(ctx.guild.id, "now_playing_duration")) < 3600:

                    min_time = time.strftime("%M:%S", time.gmtime(
                        int(self.catch_String_valueable(ctx.guild.id, "now_playing_duration"))))
                else:
                    min_time = time.strftime("%H:%M:%S", time.gmtime(
                        int(self.catch_String_valueable(ctx.guild.id, "now_playing_duration"))))
                nowplayingmbed = discord.Embed(title="**現在播放的是 !!!**", color=ctx.author.color)
                nowplayingmbed.add_field(name=self.catch_String_valueable(ctx.guild.id, "now_playing"),
                                         value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "now_playing_url")})',
                                         inline=False)
                nowplayingmbed.add_field(name="上傳者",
                                         value=self.catch_String_valueable(ctx.guild.id, "now_playing_uploader"),
                                         inline=True)
                nowplayingmbed.add_field(name="點歌者", value=reacter_np.mention, inline=True)
                nowplayingmbed.add_field(name="影片時長", value=min_time, inline=True)
                nowplayingmbed.set_thumbnail(url=self.catch_String_valueable(ctx.guild.id, "now_playing_thumbnail"))
                await ctx.channel.trigger_typing()
                nowplayingmbed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=nowplayingmbed)
            else:
                await ctx.channel.trigger_typing()

                nowplayingmbed = discord.Embed(title="**無音樂播放中 ! ! **", color=ctx.author.color)
                nowplayingmbed.timestamp = datetime.datetime.utcnow()
                nowplayingmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=nowplayingmbed)


    @commands.command(aliases=['l'])
    async def loop(self, ctx):

        if ctx.author.voice != None or ctx.author.id == 601720742949683201:
            if self.get_data_boolean_value(ctx.guild.id, "loop"):

                self.change_data_boolean_value(ctx.guild.id, "loop", False)
                loopembed = discord.Embed(title="`LOOP(循環播放) 功能關閉!`", color=ctx.author.color)
                self.change_data_boolean_value(ctx.guild.id, "is_loop_disable", True)
                loopembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)

                loopembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                await ctx.channel.trigger_typing()
                await ctx.send(embed=loopembed)
            else:
                loopembed = discord.Embed(title="`LOOP(循環播放) 功能開啟!`", color=ctx.author.color)
                self.change_data_boolean_value(ctx.guild.id, "loop", True)
                if self.get_data_boolean_value(ctx.guild.id, "is_bot_playing"):
                    self.change_data_boolean_value(ctx.guild.id, "is_loop_enable", True)
                    addurl = self.catch_String_valueable(ctx.guild.id, "now_playing_url")
                    self.added_queue_url(str(ctx.guild.id), addurl)
                self.change_data_boolean_value(ctx.guild.id, "first_loop", True)
                loopembed.timestamp = datetime.datetime.utcnow()
                loopembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.channel.trigger_typing()
                await ctx.send(embed=loopembed)
        else:
            waringmbed = discord.Embed(title="**你不在語音頻道 !!! **", color=ctx.author.color)
            waringmbed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            waringmbed.timestamp = datetime.datetime.utcnow()
            self.save_last_channel(ctx.guild, ctx.channel)
            await ctx.send(embed=waringmbed)

    @commands.command(aliases=['queue'])
    async def q(self, ctx, *, value=""):
        async with ctx.typing():
            if self.get_data_boolean_value(ctx.guild.id, "loop"):
                mode = "開啟"
            else:
                mode = "關閉"
            if value == "" and len(self.get_data_String_value(ctx.guild.id, "queue")) >= 1:
                queue_embed = discord.Embed(title="**音樂清單**", color=ctx.author.color)
                queue_embed.add_field(name="**現在播放中 : **", value='\uFEFF', inline=False)
                queue_embed.add_field(name=self.catch_String_valueable(ctx.guild.id, "now_playing"),
                                      value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "now_playing_url")})',
                                      inline=False)
                queue_embed.add_field(name=f"LOOP(循環)模式 : {mode}", value='\uFEFF', inline=False)
                queue_embed.add_field(name="**下表為即將播放 : **", value="----------------------------", inline=False)
                queue_embed.set_thumbnail(url=self.catch_String_valueable(ctx.guild.id, "now_playing_thumbnail"))
                for i in range(len(self.get_data_String_value(ctx.guild.id, "queue"))):
                    try:
                        with YoutubeDL(self.YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(self.get_data_String_value(ctx.guild.id, "queue")[i],
                                                    download=False)
                            name = info.get("title", None)
                        final = str(i + 1) + ". " + str(name)
                        queue_embed.add_field(

                            name=final, value=f"[影片連結]({self.get_data_String_value(ctx.guild.id, 'queue')[i]})",
                            inline=False
                        )
                    except:
                        pass
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=queue_embed)
            elif value == "clear":
                if len(self.get_data_String_value(ctx.guild.id, "queue")) >= 1:
                    self.del_queue_url(str(ctx.guild.id), 1)
                    queue_clear_embed = discord.Embed(title="**已清除 音樂清單 **", color=ctx.author.color)
                    queue_clear_embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/978289315450867742/waring.png')
                    queue_clear_embed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=queue_clear_embed)
                else:
                    queue_clear_embed = discord.Embed(title="**音樂清單是空的 ! **", color=ctx.author.color)
                    queue_clear_embed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/978289315450867742/waring.png')
                    queue_clear_embed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=queue_clear_embed)

            elif not len(self.get_data_String_value(ctx.guild.id, "queue")) >= 1 and not self.get_data_boolean_value(
                    ctx.guild.id, "is_playing"):

                loopembed = discord.Embed(title="**音樂清單是空的**", color=ctx.author.color)
                loopembed.add_field(name=f"LOOP(循環)模式 : {mode}", value='\uFEFF', inline=False)
                loopembed.add_field(name="**透過 -play / -p 可以新增/播放 音樂到音樂清單喔 !  ! **", value='\uFEFF', inline=False)
                loopembed.timestamp = datetime.datetime.utcnow()
                loopembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=loopembed)
            elif not len(self.get_data_String_value(ctx.guild.id, "queue")) >= 1 and self.get_data_boolean_value(
                    ctx.guild.id, "is_playing"):
                queue_embed = discord.Embed(title="**音樂清單**", color=ctx.author.color)
                queue_embed.add_field(name="**現在播放中 : **", value='\uFEFF', inline=False)
                queue_embed.add_field(name=self.catch_String_valueable(ctx.guild.id, "now_playing"),
                                      value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "now_playing_url")})',
                                      inline=False)
                queue_embed.add_field(name="----------------------------", value='\uFEFF', inline=False)
                queue_embed.add_field(name="**音樂清單是空的**", value='\uFEFF', inline=False)
                queue_embed.add_field(name=f"LOOP(循環)模式 : {mode}", value='\uFEFF', inline=False)
                queue_embed.add_field(name="**透過 -play / -p 可以新增/播放 音樂到音樂清單喔 !  ! **", value='\uFEFF', inline=False)
                queue_embed.set_thumbnail(url=self.catch_String_valueable(ctx.guild.id, "now_playing_thumbnail"))
                queue_embed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=queue_embed)
        pass

    @commands.command()
    async def pause(self, ctx):
        async with ctx.typing():
            botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)
            if ctx.author.voice != None or (botvoice != None and ctx.author.id == 601720742949683201):
                if self.get_data_boolean_value(ctx.guild.id, "is_playing") and not self.get_data_boolean_value(
                        ctx.guild.id,
                        "is_pause"):
                    ctx.voice_client.pause()
                    self.change_data_boolean_value(ctx.guild.id, "is_pause", True)
                    pauseembed = discord.Embed(title="**歌曲已經暫停播放!**", color=ctx.author.color)
                    pauseembed.add_field(name="**Tips : 可以使用resume指令 或 再使用一次pause指令 可以繼續播放音樂**", value='\uFEFF',
                                         inline=False)
                    pauseembed.timestamp = datetime.datetime.utcnow()
                    pauseembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=pauseembed)
                elif self.get_data_boolean_value(ctx.guild.id, "is_pause"):
                    self.change_data_boolean_value(ctx.guild.id, "is_pause", False)
                    ctx.voice_client.resume()
                    pauseembed = discord.Embed(title="**歌曲已經繼續播放! (可以使用pause指令暫停播放)**", color=ctx.author.color)
                    pauseembed.add_field(name="**Tips : -可以使用pause指令 或 再使用一次pause指令 可以暫停播放音樂**", value='\uFEFF',
                                         inline=False)
                    pauseembed.timestamp = datetime.datetime.utcnow()
                    pauseembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=pauseembed)
                else:
                    pauseembed = discord.Embed(title="**沒有歌 在播放中!!**", color=ctx.author.color)
                    pauseembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                    pauseembed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=pauseembed)
            elif botvoice == None and ctx.author.id == 601720742949683201:
                waringmbed = discord.Embed(title="**機器人不在語音頻道 !!! **", color=ctx.author.color)
                waringmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                waringmbed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=waringmbed)
            else:
                waringmbed = discord.Embed(title="**你不在語音頻道 !!! **", color=ctx.author.color)
                waringmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                waringmbed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=waringmbed)
        pass

    @commands.command()
    async def resume(self, ctx):
        async with ctx.typing():
            botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)
            if ctx.author.voice != None or (botvoice != None and ctx.author.id == 601720742949683201):
                if self.get_data_boolean_value(ctx.guild.id, "is_playing") and not self.get_data_boolean_value(
                        ctx.guild.id,
                        "is_resume"):
                    self.change_data_boolean_value(ctx.guild.id, "is_resume", True)
                    ctx.voice_client.resume()
                    pauseembed = discord.Embed(title="**歌曲已經繼續播放!**", color=ctx.author.color)
                    pauseembed.add_field(name="**Tips : -可以使用pause指令 或 再使用一次resume指令 可以暫停播放音樂**", value='\uFEFF',
                                         inline=False)
                    pauseembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                    pauseembed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=pauseembed)
                elif self.get_data_boolean_value(ctx.guild.id, "is_resume"):
                    self.change_data_boolean_value(ctx.guild.id, "is_resume", False)
                    ctx.voice_client.pause()
                    pauseembed = discord.Embed(title="**歌曲已經暫停播放!**", color=ctx.author.color)
                    pauseembed.add_field(name="**Tips : -可以使用pause指令 或 再使用一次resume指令 可以繼續播放音樂**", value='\uFEFF',
                                         inline=False)
                    pauseembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                    pauseembed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=pauseembed)
                else:
                    pauseembed = discord.Embed(title="**沒有歌 在播放中!!**", color=ctx.author.color)
                    pauseembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                    pauseembed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=pauseembed)
            elif botvoice == None and ctx.author.id == 601720742949683201:
                waringmbed = discord.Embed(title="**機器人不在語音頻道 !!! **", color=ctx.author.color)
                waringmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                waringmbed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=waringmbed)
            else:
                waringmbed = discord.Embed(title="**你不在語音頻道 !!! **", color=ctx.author.color)
                waringmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                waringmbed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=waringmbed)
        pass

    @commands.command()
    async def stop(self, ctx):

        botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if ctx.author.voice != None or (botvoice != None and ctx.author.id == 601720742949683201):
            await ctx.channel.trigger_typing()
            if not self.get_data_boolean_value(ctx.guild.id, "is_playing"):
                stopembed = discord.Embed(title="**無音樂播放中 ! ! **", color=ctx.author.color)
                stopembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                stopembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=stopembed)

            else:
                await ctx.channel.trigger_typing()
                stopembed = discord.Embed(title="**音樂已全部暫停了**", color=ctx.author.color)
                stopembed.add_field(name="**音樂清單已全部清空**", value='\uFEFF', inline=False)
                stopembed.timestamp = datetime.datetime.utcnow()
                stopembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=stopembed)
                self.change_data_boolean_value(ctx.guild.id, "loop", False)
                ctx.voice_client.stop()
                self.del_queue_url(ctx.guild.id, 1)
        elif botvoice == None and ctx.author.id == 601720742949683201:
            await ctx.channel.trigger_typing()
            waringmbed = discord.Embed(title="**機器人不在語音頻道 !!! **", color=ctx.author.color)
            waringmbed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            waringmbed.timestamp = datetime.datetime.utcnow()
            self.save_last_channel(ctx.guild, ctx.channel)
            await ctx.send(embed=waringmbed)
        else:
            await ctx.channel.trigger_typing()
            waringmbed = discord.Embed(title="**你不在語音頻道 !!! **", color=ctx.author.color)
            waringmbed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            waringmbed.timestamp = datetime.datetime.utcnow()
            self.save_last_channel(ctx.guild, ctx.channel)
            await ctx.send(embed=waringmbed)

    @commands.command(aliases=['fs'])
    async def forceskip(self, ctx):
        async with ctx.typing():
            botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)
            if ctx.author.voice != None or (botvoice != None and ctx.author.id == 601720742949683201):
                if ctx.author.id == 601720742949683201 and self.get_data_boolean_value(ctx.guild.id, "is_playing"):
                    self.change_data_boolean_value(ctx.guild.id, "loop", False)
                    ctx.voice_client.stop()
                    forceskipembed = discord.Embed(title="強制停止放音樂! ", color=ctx.author.color)
                    forceskipembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                    forceskipembed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=forceskipembed)
                elif ctx.author.id != 601720742949683201:
                    self.save_last_channel(ctx.guild, ctx.channel)
                    devembed = discord.Embed(title="**運行結果 ! **", color=ctx.author.color)
                    devembed.add_field(name="**你不是管理人員 無法使用此指令 !!!**", value='\uFEFF', inline=False)
                    devembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                    devembed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=devembed)
                else:
                    forceskipembed = discord.Embed(title="沒有音樂播放中! ", color=ctx.author.color)
                    forceskipembed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                    forceskipembed.timestamp = datetime.datetime.utcnow()
                    self.save_last_channel(ctx.guild, ctx.channel)
                    await ctx.send(embed=forceskipembed)
            elif botvoice == None and ctx.author.id == 601720742949683201:
                waringmbed = discord.Embed(title="**機器人不在語音頻道 !!! **", color=ctx.author.color)
                waringmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                waringmbed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=waringmbed)
            else:
                waringmbed = discord.Embed(title="**你不在語音頻道 !!! **", color=ctx.author.color)
                waringmbed.timestamp = datetime.datetime.utcnow()
                waringmbed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=waringmbed)
        pass

    @commands.command()
    async def skip(self, ctx):
        botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if ctx.author.voice != None or (botvoice != None and ctx.author.id == 601720742949683201):
            if self.get_data_boolean_value(ctx.guild.id, "is_playing") and len(
                    self.get_data_String_value(ctx.guild.id, "queue")) >= 1 and not self.get_data_boolean_value(
                ctx.guild.id, "loop"):
                await ctx.channel.trigger_typing()
                self.change_data_String_value(ctx.guild.id, "skip_name",
                                              (self.get_data_String_value(ctx.guild.id, "now_playing")))

                self.change_data_String_value(ctx.guild.id, "skip_url",
                                              (self.get_data_String_value(ctx.guild.id, "now_playing_url")))
                self.change_data_boolean_value(ctx.guild.id, "is_skip", True)
                self.change_data_boolean_value(ctx.guild.id, "loop", False)
                self.change_data_boolean_value(ctx.guild.id, "has_been_stopLoop", True)
                ctx.voice_client.stop()
                self.change_data_boolean_value(ctx.guild.id, "is_skip_succes", True)
                await self.play_next(ctx)
                playembed = discord.Embed(title="SKIP(跳過)提醒 !", color=ctx.author.color)
                playembed.add_field(name=f"已跳過了! [{self.catch_String_valueable(ctx.guild.id, 'skip_name')}]",
                                    value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "skip_url")})',
                                    inline=False)
                playembed.add_field(name=f"接著將播放! [{self.catch_String_valueable(ctx.guild.id, 'now_playing')}]",
                                    value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "now_playing_url")})',
                                    inline=True)
                playembed.set_image(url=self.catch_String_valueable(ctx.guild.id, "now_playing_thumbnail"))
                playembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                playembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=playembed)
                self.change_data_boolean_value(ctx.guild.id, "is_skip_succes", False)
            elif self.get_data_boolean_value(ctx.guild.id, "loop") and self.get_data_boolean_value(ctx.guild.id,
                                                                                                   "is_bot_playing"):
                await ctx.channel.trigger_typing()
                self.change_data_boolean_value(ctx.guild.id, "skip_loopSong", True)
                self.change_data_boolean_value(ctx.guild.id, "loop", False)

                self.change_data_String_value(ctx.guild.id, "skip_name",
                                              (self.get_data_String_value(ctx.guild.id, "now_playing")))

                self.change_data_String_value(ctx.guild.id, "skip_url",
                                              (self.get_data_String_value(ctx.guild.id, "now_playing_url")))
                self.change_data_boolean_value(ctx.guild.id, "is_skip", True)
                self.del_queue_url(ctx.guild.id, 0)
                ctx.voice_client.stop()
                playembed = discord.Embed(title="SKIP(跳過)提醒 !abc", color=ctx.author.color)
                playembed.add_field(name=f"已跳過了! [{self.catch_String_valueable(ctx.guild.id, 'skip_name')}]",
                                    value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "skip_url")})',
                                    inline=False)

                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    find = ydl.extract_info(self.get_data_String_value(ctx.guild.id, "queue")[0], download=False)
                    self.change_data_String_value(ctx.guild.id, "now_playing", find.get("title", None))

                    self.change_data_String_value(ctx.guild.id, "now_playing_url",
                                                  self.get_data_String_value(ctx.guild.id, "queue")[0])

                    self.change_data_String_value(ctx.guild.id, "now_playing_thumbnail", find.get("thumbnail"))

                playembed.add_field(name=f"接著將播放! [{self.catch_String_valueable(ctx.guild.id, 'now_playing')}]",
                                    value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "now_playing_url")})',
                                    inline=True)
                playembed.set_image(url=self.catch_String_valueable(ctx.guild.id, "now_playing_thumbnail"))
                playembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                playembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=playembed)
            elif self.get_data_boolean_value(ctx.guild.id, "is_playing"):
                await ctx.channel.trigger_typing()
                ctx.voice_client.stop()
                self.del_queue_url(ctx.guild.id, 0)
                skipembed = discord.Embed(title="Skip(跳過)提醒 ! ", color=ctx.author.color)
                skipembed.add_field(name=f"已跳過{self.catch_String_valueable(ctx.guild.id, 'now_playing')}",
                                    value=f'[影片連結]({self.catch_String_valueable(ctx.guild.id, "now_playing_url")})',
                                    inline=False)
                skipembed.add_field(name="**音樂清單是空的喔 !**", value='\uFEFF', inline=True)
                skipembed.set_thumbnail(url=self.catch_String_valueable(ctx.guild.id, "now_playing_thumbnail"))
                skipembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=skipembed)
            else:
                await ctx.channel.trigger_typing()
                skipembed = discord.Embed(title="**無音樂播放中 ! ! **", color=ctx.author.color)
                skipembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                skipembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=skipembed)
        elif botvoice == None and ctx.author.id == 601720742949683201:
            await ctx.channel.trigger_typing()
            waringmbed = discord.Embed(title="**機器人不在語音頻道 !!! **", color=ctx.author.color)
            waringmbed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            waringmbed.timestamp = datetime.datetime.utcnow()
            self.save_last_channel(ctx.guild, ctx.channel)
            await ctx.send(embed=waringmbed)
        else:
            await ctx.channel.trigger_typing()
            waringmbed = discord.Embed(title="**你不在語音頻道 !!! **", color=ctx.author.color)
            waringmbed.timestamp = datetime.datetime.utcnow()
            waringmbed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            self.save_last_channel(ctx.guild, ctx.channel)
            await ctx.send(embed=waringmbed)

    @commands.command()
    async def join(self, ctx):
        botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if ctx.author.voice is None:
            async with ctx.typing():
                joinembed = discord.Embed(title=f"**你不在語音頻道**", color=ctx.author.color)
                joinembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                joinembed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=joinembed)
            pass
        elif ctx.author.voice is not None and botvoice is None:
            async with ctx.typing():
                await ctx.author.voice.channel.connect()

                joinembed = discord.Embed(title=f"**成功加入到 : `#{ctx.author.voice.channel}` **", color=ctx.author.color)
                joinembed.timestamp = datetime.datetime.utcnow()
                joinembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=joinembed)
            pass
        else:
            async with ctx.typing():
                await ctx.guild.voice_client.move_to(ctx.author.voice.channel)
                joinembed = discord.Embed(title=f"**成功移動到 : `#{ctx.author.voice.channel}` **", color=ctx.author.color)
                joinembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                joinembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                await ctx.send(embed=joinembed)
            pass

    @commands.command()
    async def leave(self, ctx):
        botvoice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if botvoice is None:

            leaveembed = discord.Embed(title="**我不在語音頻道**", color=ctx.author.color)
            leaveembed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            self.save_last_channel(ctx.guild, ctx.channel)

            leaveembed.timestamp = datetime.datetime.utcnow()
            await ctx.channel.trigger_typing()
            await ctx.reply(embed=leaveembed)
        elif ctx.author.voice is None and ctx.author.id != 601720742949683201:
            leaveembed = discord.Embed(title="**你不在語音頻道**", color=ctx.author.color)
            leaveembed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
            leaveembed.timestamp = datetime.datetime.utcnow()
            self.save_last_channel(ctx.guild, ctx.channel)
            await ctx.reply(embed=leaveembed)
        else:
            connect_channel = ctx.guild.voice_client.channel
            await ctx.guild.voice_client.disconnect()
            leaveembed = discord.Embed(title=f"**成功離開 : `#{connect_channel}`**", color=ctx.author.color)
            self.change_data_boolean_value(ctx.guild.id, "start_count", False)
            leaveembed.timestamp = datetime.datetime.utcnow()
            leaveembed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
            self.save_last_channel(ctx.guild, ctx.channel)
            await ctx.channel.trigger_typing()
            await ctx.reply(embed=leaveembed)

    @commands.command(aliases=['ms'])
    async def music_reset(self, ctx):

            if ctx.author.id == 601720742949683201:
                music_resetmbed = discord.Embed(title="**運行結果 ! **", color=ctx.author.color)
                await ctx.channel.trigger_typing()
                try:
                    ctx.voice_client.stop()
                    self.bot.unload_extension("music.music")
                    self.bot.load_extension("music.music")
                    self.check_guilds_data()
                    music_resetmbed.add_field(name="**成功重啟 音樂指令 !**", value='\uFEFF', inline=False)
                    music_resetmbed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977447912734851082/images_preview_rev_1.png')
                except:
                    music_resetmbed.add_field(name="**重啟失敗 出問題了 !!!**", value='\uFEFF', inline=False)
                    music_resetmbed.set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/881848877102301254/977448394702323712/FetchedFromUrl_1653112242368_preview_rev_1.png')
                music_resetmbed.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=music_resetmbed)
            else:
                await ctx.channel.trigger_typing()
                devembed = discord.Embed(title="**運行結果 ! **", color=ctx.author.color)
                devembed.add_field(name="**你不是管理人員 無法使用此指令 !!!**", value='\uFEFF', inline=False)
                devembed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
                devembed.timestamp = datetime.datetime.utcnow()
                self.save_last_channel(ctx.guild, ctx.channel)
                await ctx.send(embed=devembed)


    @commands.command()
    async def music(self, ctx):
        async with ctx.typing():
            musicembedVar = discord.Embed(title='**音樂指令幫助 !💖 **',
                                          description='**可以嵾考以下的指令操作教學**' + "\n\u200b",
                                          color=ctx.author.color)
            musicembedVar.set_author(name='中央總書記梅川',
                                     icon_url='https://cdn.discordapp.com/avatars/601720742949683201'
                                              '/12f53eaa05b510b0ee524904bd308f68.webp?size=1024')
            musicembedVar.add_field(name='開發者⭐', value="!!!!!梅川 ♡ (((*°▽° *）九（* °▽°*)))♪#7051" + "\n\u200b",
                                    inline=False)
            musicembedVar.add_field(name='**以下為指令操作教學**', value="**--------------------------**", inline=False)
            musicembedVar.add_field(name='**1.播放音樂指令🎷 \n使用方式-p 或 -play 後面接Youtube網址**',
                                    value="\n**說明 : 可以透過-p 或者 -play的指令 將你要的歌 加入播放清單**", inline=False)
            musicembedVar.add_field(name='**2.循環音樂指令🎸 \n使用方式 : -loop 或 -l**',
                                    value="**說明:輸入-l 或 -loop 可以開啟/關閉 循環播放功能 讓你一直聽你愛的音樂**", inline=False)
            musicembedVar.add_field(name='**3.暫停播放音樂指令🥁 \n使用方式 : -pause**', value="**說明:輸入-pause 可以暫停目前正在播放的音樂**",
                                    inline=False)
            musicembedVar.add_field(name='**4.繼續播放音樂指令🎤 \n使用方式 : -resume**', value="**說明:輸入-resume 可以繼續播放 已經暫停的音樂**",
                                    inline=False)
            musicembedVar.add_field(name='**5.跳過音樂指令📯 \n使用方式 : -skip**', value="**說明:輸入-skip 可以跳過當前正在播放的音樂 並自動播放下一首**",
                                    inline=False)
            musicembedVar.add_field(name='**6.結束播放音樂指令🎵 \n使用方式 : -stop**',
                                    value="**說明:輸入-stop 可以結束目前播放的音樂 並且自動清除音樂清單**",
                                    inline=False)
            musicembedVar.add_field(name='**7.查詢音樂清單指令📻 \n使用方式 : -q 或者 -queue**',
                                    value="**說明:輸入 -q 或者 -queue 可以查詢目前的音樂清單**", inline=False)
            musicembedVar.add_field(name='8.查詢目前播放的音樂指令⭐ \n使用方式 : -np 或者 -nowplaying',
                                    value="**說明:輸入 -np 或者 -nowplaying 可以查詢目前正在播放的音樂詳情**", inline=False)
            musicembedVar.add_field(name='9.強制結束音樂指令🔥 \n使用方式 : -fs 或者 -forceskip',
                                    value="**說明:輸入 -fs 或者 -forceskip 強制結束音樂 (僅限開發者使用)**", inline=False)
            musicembedVar.add_field(name='10.機器人加入指令🚀 \n使用方式 : -join ', value="**說明:輸入 -join 將機器人邀到你所在的語音頻道上**",
                                    inline=False)
            musicembedVar.add_field(name='11.機器人離開指令⚽ \n使用方式 : -leave ', value="**說明:輸入 -leave 將機器人踢出你所在的頻道上**",
                                    inline=False)
            musicembedVar.add_field(name='--------------------------', value="音樂指令幫助 說明完畢", inline=False)
            musicembedVar.timestamp = datetime.datetime.utcnow()
            musicembedVar.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/977238033097195520/picwish.png')
            reactions = ['🇹🇼']
            m = await ctx.send(embed=musicembedVar)
            self.save_last_channel(ctx.guild, ctx.channel)
            for name in reactions:
                emoji = get(ctx.guild.emojis, name=name)
                await m.add_reaction(emoji or name)
        pass

    def get_last_voice_channel_data(self, guild, channel, last_author):
        try:
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
                music_file[str(guild.id)]["last_voice_channel"] = str(channel)
                music_file[str(guild.id)]["last_voice_channel_id"] = channel.id
                music_file[str(guild.id)]["last_send_author_id"] = (last_author)
            with open(self.json_path, 'w', encoding="utf-8") as f:
                json.dump(music_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("儲存 ctx 錯誤", e)

    def save_last_channel(self, guild, channel):
        try:

            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
                music_file[str(guild.id)]["last_text_channel"] = str(channel)
                music_file[str(guild.id)]["last_text_channel_id"] = channel.id
            with open(self.json_path, 'w', encoding="utf-8") as f:
                json.dump(music_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("儲存 save_last_channel 錯誤", e)

    def get_last_data(self, guild_id, value_name):
        try:
            with open(self.json_path, 'r', encoding="utf-8") as f:
                music_file = json.load(f)
                value = music_file[str(guild_id)][str(value_name)]
            return value

        except Exception as e:
            print("抓取 get_last_data 錯誤", e)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global someone_joined
        someone_joined = False
        global final_member

        if (before.channel is None or after.channel is not None) and self.get_data_boolean_value(member.guild.id,
                                                                                                 "start_count"):
            current_channel_plus = discord.utils.get(member.guild.channels, id=after.channel.id)
            member_guild_plus = member.guild
            if self.bot.user in current_channel_plus.members:
                someone_joined = True

        async def startcount():

            await asyncio.sleep(10)
            final_time = int(round(time.time() - now_time))
            botvoice = get(self.bot.voice_clients, guild=before.channel.guild.id)

            if (final_time >= 300 and not someone_joined) and not botvoice is None:
                await do_this()

            if someone_joined:
                self.change_data_boolean_value(member.guild.id, "start_count", False)
                pass
            elif final_time >= 310:

                await do_this()

            else:
                await startcount()

        async def do_this():
            connect_channel = self.get_last_data(before.channel.guild.id, "last_voice_channel")
            guild_member = self.bot.get_guild(before.channel.guild.id)
            author_last = guild_member.get_member(self.get_last_data(before.channel.guild.id, "last_send_author_id"))
            text_channel = self.bot.get_channel(
                (self.get_last_data(before.channel.guild.id, "last_text_channel_id")))
            self.change_data_boolean_value(before.channel.guild.id, "loop", False)
            self.del_queue_url(str(before.channel.guild.id), 1)
            self.change_data_boolean_value(before.channel.guild.id, "is_bot_playing", False)
            self.change_data_boolean_value(before.channel.guild.id, "is_playing", False)
            leaveembed = discord.Embed(title=f"**機器人已自動離開 : `#{connect_channel}`**",
                                       color=author_last.color)
            leaveembed.add_field(name='**原因 : 機器人閒置超過五分鐘**', value='\uFEFF', inline=False)
            leaveembed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/881848877102301254/978256099125915708/1_-removebg-preview.png')
            if self.get_data_boolean_value(before.channel.guild.id, "is_playing"):
                leaveembed.add_field(name='**已暫停音樂播放 和 清除音樂清單了**', value='\uFEFF', inline=False)
            leaveembed.timestamp = datetime.datetime.utcnow()
            await member_guild_plus.voice_client.disconnect()
            await text_channel.trigger_typing()
            await text_channel.send(embed=leaveembed)

        botvoice = get(self.bot.voice_clients, guild=member.guild)

        if not before.channel is None or after.channel is None:  # 有成員離開語音頻道 包含 移動到其他頻道也算 (or 改成 and 可以去掉 成員移動)
            if botvoice is not None and not (member == self.bot.user):  # 如果 機器人在語音頻道 和 退出的人不是機器人
                if member.guild.voice_client.is_connected():  # 偵測機器人 是否連接到 (退出成員) 的群組語音中
                    current_channel = discord.utils.get(member.guild.channels, id=before.channel.id)
                    if (len(current_channel.members) == 1 and current_channel.members[
                        0] == self.bot.user):  # 偵測 語音頻道人數 只剩一個 和 語音頻道中只剩下機器人
                        self.get_last_voice_channel_data(before.channel.guild, before.channel, member.id)
                        now_time = time.time()
                        member_guild_plus = member.guild
                        self.change_data_boolean_value(member.guild.id, "start_count", True)
                        await startcount()


async def setup(bot):
    await bot.add_cog(music(bot))
