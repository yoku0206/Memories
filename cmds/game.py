import discord
from discord.ext import commands
from core.classes import Cog_Extension
from utils import default
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

    @commands.command(name='抽獎', description='就是Giveaway', aliases=['ga', 'gift'])
    @commands.check(default.check)
    async def giveaway(self, ctx):
        await ctx.message.delete()
        await ctx.send("**[抽獎小幫手]** 開始設定！\n請在15秒內在當前頻道完成回答！")
        questions = [
            "**[抽獎小幫手]** 你想要在哪個頻道舉辦？ __(15秒回答)__",
            "**[抽獎小幫手]** 這次的抽獎舉辦時間？ (s|h|m|d) __(15秒回答)__",
            "**[抽獎小幫手]** 這次抽獎的獎品是什麼呢？ __(15秒回答)__",
            "**[抽獎小幫手]** 總共要抽出幾份獎品呢？ __(15秒回答)__"
        ]
        ans = []

        def check(m):
            return m.channel == ctx.channel and m.author ==  ctx.author

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("**[抽獎小幫手]** 你沒有在時間內完成回答，下次請早點回答喔！")
                return
            else:
                ans.append(msg.content)

            try:
                c_id = int(ans[0][2:-1])
            except:
                await ctx.send(f"**[抽獎小幫手]** 請使用Mention的方式來指定頻道！\n像是這樣：{ctx.channel.mention}")
                return 

            channel = ctx.guild.get_channel(c_id)
            time = default.time_convert(ans[1])

            if time == -1:
                await ctx.send(f"**[抽獎小幫手]** 你不能使用 {ans[1][-1]} 這個單位！\n請使用： (s|m|h|d)")
                return
            elif time == -2:
                await ctx.send(f"**[抽獎小幫手]** 你輸入的時間必須為數字！ 而不是 {ans[1][:-1]}！")
                return
            prize= ans[2]

            await ctx.send(f"抽獎活動將在 {channel.mention} 舉辦 剩餘時間： {ans[1]}！")

            embed = discord.Embed(title="抽獎活動！", description= f"{prize}", color= ctx.author.color.random())
            embed.add_field(name= "舉辦人", value= ctx.author.mention, inline= False)
            embed.set_footer(text= f"結束時間剩餘： {ans[1]}", icon_url=f"{ctx.bot.user.avatar_url}")

            my_msg = await channel.send(embed=embed)

            await my_msg.add_reaction("🎉")

            await asyncio.sleep(time)

            new_msg = await channel.fetch_message(my_msg.id)

            users = await new_msg.reactions[0].user().flatten()
            users.pop(users.index(self.bot.user))

            # if len(users) <= 0:
            #     emptyEmbed = discord.Embed(title="Giveaway Time !!",
            #                        description=f"Win a {prize} today")
            #     emptyEmbed.add_field(name="Hosted By:", value=ctx.author.mention)
            #     emptyEmbed.set_footer(text="No one won the Giveaway")
            #     await myMsg.edit(embed=emptyEmbed)
            #     return
            # if len(users) > 0:
            #     winner = choice(users)
            #     winnerEmbed = Embed(title="Giveaway Time !!",
            #                         description=f"Win a {prize} today",
            #                         colour=0x00FFFF)
            #     winnerEmbed.add_field(name=f"Congratulations On Winning {prize}", value=winner.mention)
            #     winnerEmbed.set_image(url="https://firebasestorage.googleapis.com/v0/b/sociality-a732c.appspot.com/o/Loli.png?alt=media&token=ab5c8924-9a14-40a9-97b8-dba68b69195d")
            #     await myMsg.edit(embed=winnerEmbed)
            #     return

            winner = random.choice(users)

            winner_embed = discord.Embed(title= "**[抽獎小幫手]**", description= f"{prize}", color= winner.color.random())
            winner_embed.add_field(name= "贏家", value=winner.mention, inline=False)

            await channel.send(f"**[抽獎小幫手]** 恭喜！！ {winner.mention} 贏得了 {prize}！")
    

    @giveaway.error
    async def giveaway_command_error(self, ctx, exc):
        await ctx.message.delete()
        if isinstance(exc, commands.CheckFailure):
            await ctx.send("**[錯誤]** 你沒有權限這樣做！")
        else:
            await ctx.send("**[錯誤] 發生錯誤！")

        

def setup(bot):
    bot.add_cog(Game(bot))