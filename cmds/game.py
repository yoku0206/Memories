import discord
from discord.ext import commands
from core.classes import Cog_Extension
from discord.ext.commands import VoiceChannelConverter
import random, asyncio, json, requests

class Setting():
    def __init__(self, bot):
        self.bot = bot

    def Guild_Json_Load(self):
        response = requests.get('https://jsonstorage.net/api/items/', {
            "id": "3202bdcb-5212-4789-822a-5864caa6e62e"
        })
        data = response.json()
        return data

    def Guild_Json_Write(self, data):
        update = requests.put('https://jsonstorage.net/api/items/', 
            params = {"id": "3202bdcb-5212-4789-822a-5864caa6e62e"},
            json = data
        )

class Game(Cog_Extension):
    
    @commands.command()
    async def random(self, ctx, ch = None):
        await ctx.message.delete()
        if ch == None:
            if ctx.author.voice.channel == None:
                await ctx.send("請輸入一個語音頻道或在一個語音頻道內！")
            else:
                try:
                    channel = ctx.author.voice.channel
                except:
                    await ctx.send("請輸入一個語音頻道或在一個語音頻道內！")
        else:
            try:
                channel = await VoiceChannelConverter().convert(ctx, int(ch))
            except:
                channel = await VoiceChannelConverter().convert(ctx, ch)
        
        if channel == None:
            pass
        else:
            await ctx.send(f"抽獎範圍：1 <= X <= {len(channel.voice_states)}\n將在10秒後公告中獎數字！")
            await asyncio.sleep(5)
            await ctx.send("剩餘 **5** 秒！")
            await asyncio.sleep(5)
            await ctx.send(f"恭喜抽中： **{random.randint(1, len(channel.voice_states))}**")

    @commands.command(aliases=["tf"])
    async def twenty_five(self, ctx, mode=None):
        await ctx.message.delete()

        gdata = Setting.Guild_Json_Load(self)

        if "game" not in gdata[str(ctx.guild.id)]:
            gdata[str(ctx.guild.id)]['game'] = {
                "lottery": []
            }
        else:
            pass

        Setting.Guild_Json_Write(self, gdata)

        gdata = Setting.Guild_Json_Load(self)

        lottery = gdata[str(ctx.guild.id)]['game']['lottery']

        if len(lottery) == 25:
                lottery.clear()

        async def number_gen(self):
            i =  random.randint(1, 25)
            if i in lottery:
                await number_gen(self)
            else:
                lottery.append(i)
                await ctx.send(f"**`恭喜！抽到的數字為 {i}`**")

        if mode == None:
            await number_gen(self)
        elif mode == "test":
            while len(lottery) != 25:
                await number_gen(self)
        Setting.Guild_Json_Write(self, gdata)

        

def setup(bot):
    bot.add_cog(Game(bot))