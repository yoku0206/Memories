import discord
from discord.ext import commands
from core.classes import Cog_Extension
from discord.ext.commands import VoiceChannelConverter
import random, asyncio, json


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

    @commands.command()
    async def mt(self, ctx):
        await ctx.message.delete()

        with open('guild.json', mode='r', encoding='utf8') as gfile:
            gdata = json.load(gfile)

        for i in gdata[str(ctx.guild.id)]['user']:
            try:
                member = await ctx.guild.fetch_member(int(i))
                print(f"名稱： {member.name}\nID: {member.id}\n")
            except:
                print(f"無法找到： {i}")
                pass
        await ctx.send("處理完成！")

def setup(bot):
    bot.add_cog(Game(bot))