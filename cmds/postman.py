import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension, Gloable_Func, Logger
from core import check
from cmds.main import Setting
import datetime, asyncio, json, requests
from discord.ext.commands import MemberConverter


with open('settings.json', mode= 'r', encoding= 'utf8') as jfile:
    jdata = json.load(jfile)

class PostMan(Cog_Extension):
    
    @commands.command(aliases=["post"])
    async def webjson_postman(self, ctx):
        response = requests.get('https://jsonstorage.net/api/items/', {
            "id": "3202bdcb-5212-4789-822a-5864caa6e62e"
        })

        data = response.json()

        with open('guild.json', mode='r', encoding='utf8') as gfile:
            gdata = json.load(gfile)

        data = gdata

        update = requests.put('https://jsonstorage.net/api/items/', 
            params = {"id": "3202bdcb-5212-4789-822a-5864caa6e62e"},
            json = data
        )

        message = await ctx.send("資料處理完成...")
        await asyncio.sleep(5)
        await message.delete()

def setup(bot):
    bot.add_cog(PostMan(bot))