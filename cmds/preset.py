import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension, Gloable_Func, Logger
from core import check
import json, datetime, asyncio, os

with open('settings.json', mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Setting():
    def __init__(self, bot):
        self.bot = bot

    def Guild_Json_Load(self):
        with open('guild.json', mode='r', encoding=' utf8') as gfile:
            gdata = json.load(gfile)
        return gdata

    def Guild_Json_Write(self, gdata):
        with open('guild.json', mode= 'w', encoding=' utf8') as gfile:
            json.dump(gdata, gfile, indent=4, ensure_ascii=False)


class Preset(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # async def time_task():
        #     await self.bot.wait_until_ready()
        #     while not self.bot.is_closed():
        #         gdata = Setting.Guild_Json_Load(self)
        #         now_time = datetime.datetime.now() #.strftime('%H%M%S')
        #         time_delta = datetime.timedelta(hours=8)
        #         new_dt = now_time + time_delta
        #         datetime_format = new_dt.strftime("%H%M")
        #         for guilds in gdata:
        #             if gdata[guilds]['settings']['stop'] == 0 and datetime_format == gdata[guilds]['settings']['ann_time']:
        #                 gdata[guilds]['settings']['stop'] = 1
        #                 guild = self.bot.get_guild(int(guilds))
        #                 try:
        #                     channel = guild.get_chaennl(int(gdata[guilds]['settings']['channel']))
        #                     await channel.send("**各位早安！又是美好的一天呢XD**")
        #                 except:
        #                     pass
                        
        #                 for user in gdata[guilds]['user']:
        #                     gdata[guilds]['user'][user]['today'] = "False"

        #             elif gdata[guilds]['settings']['stop'] == 0 and datetime_format == "0800":
        #                 gdata[guilds]['settings']['stop'] = 1
        #                 guild = self.bot.get_guild(int(guilds))
        #                 try:
        #                     channel = guild.get_chaennl(int(gdata[guilds]['settings']['channel']))
        #                     await channel.send("**各位早安！又是美好的一天呢XD**")
        #                 except:
        #                     pass
                        
        #                 for user in gdata[guilds]['user']:
        #                     gdata[guilds]['user'][user]['today'] = "False"
                    
        #             elif gdata[guilds]['settings']['stop'] == 1 and datetime_format == "1200":
        #                 gdata[guilds]['settings']['stop'] = 0
        #                 await asyncio.sleep(1)
        #                 pass

        #             Setting.Guild_Json_Write(self, gdata)
        #             gdata = Setting.Guild_Json_Load(self)

        #             await asyncio.sleep(1)
        
        # self.bg_task = self.bot.loop.create_task(time_task())



def setup(bot):
    bot.add_cog(Preset(bot))