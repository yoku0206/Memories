import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Converter, MemberConverter
from core.classes import Cog_Extension
from utils import default
import json, asyncio, os, datetime
import psutil


jdata = default.Settings_Load()


class Infomation(Cog_Extension, name='資訊', description='有關資訊的內容都在這！'):

    @commands.command(aliases=['tg'])
    async def time_get(self, ctx):
        await ctx.message.delete()
        time = default.time_get()
        await ctx.send(time)

    @commands.command(name="關於", aliases=['about', 'stats', 'status'])
    async def about(self, ctx):
        """ 關於機器人 """
        ram_usage = psutil.Process(os.getpid()).memory_full_info().rss / 1024 ** 2
        avg_members = round(len(self.bot.users) / len(self.bot.guilds))

        embed_colour = discord.Embed.Empty
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            embed_colour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embed_colour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        # embed.add_field(name="Last boot", value=timesince.format(Setting.time_get(self) - self.bot.uptime), inline=True)
        embed.add_field(
            name=f"Developer",
            value=str(self.bot.get_user(jdata['Owner_id'])), inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avg_members} users/server )", inline=True)
        embed.add_field(name="Commands loaded", value=str(len([x.name for x in self.bot.commands])), inline=True)
        embed.add_field(name="RAM", value=f"{ram_usage:.2f} MB", inline=True)
        embed.set_footer(text="簽到機器人 By 天夜Yoku#6529", icon_url=f"{ctx.bot.user.avatar_url}")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **beta**", embed=embed)

    @commands.command(name='使用者資訊', description='使用者資訊', aliases=['user'])
    async def user_info(self, ctx, *, target = None):
        await ctx.message.delete()

        if target == None:
            user = ctx.author
        else:
            try:
                user = await MemberConverter().convert(ctx, target)
            except:
                message = await ctx.send("**[錯誤]** 請輸入正確的使用者！")
                await asyncio.sleep(60)
                await message.delete()
                return
        
        status_dict = {
            "online": "線上",
            "offline": "離線",
            "dnd": "請勿打擾",
            "idle": "閒置"
        }
        activity_dict = {
            "Custom": "自訂",
            "Playing": "正在玩",
            "Listening": "正在聽",
            "Watching": "正在看",
            "Streaming": "直播中"
        }
        
        activity_type = str(user.activity.type).split('.')[-1].title()

        if str(user.status) in status_dict:
            status = status_dict[str(user.status)]
        else:
            status = str(user.status)
        if user.activity:
            if activity_type in activity_dict:
                activity = activity_dict[activity_type]
            else:
                activity = activity_type
            activety_name = f"\n```{user.activity.name}```"
        else:
            activity = "N/A"
            activety_name = ""

        embed_fields = {
            "名稱": user.name,
            "ID": user.id,
            "機器人？": user.bot,
            "狀態": status,
            "活動": f"{activity} {activety_name}",
            "身分組": user.top_role.name,
            "建立日期": user.created_at.strftime('%Y/%m/%d %H:%M:%S'),
            "加入日期": user.joined_at.strftime('%Y/%m/%d %H:%M:%S'),
            "加成": bool(user.premium_since)
        }

        embed = discord.Embed(title = "使用者資訊",
            color = user.color, 
            timestamp = datetime.datetime.today())
        embed.set_thumbnail(url=f"{user.avatar_url}")
        for name in embed_fields:
            embed.add_field(name= name, value= embed_fields[name], inline= True)
        embed.set_footer(text="簽到機器人 By 天夜Yoku#6529", icon_url=f"{ctx.bot.user.avatar_url}")
        em = await ctx.send(embed= embed)
        await asyncio.sleep(60)
        await em.delete()
        




def setup(bot):
    bot.add_cog(Infomation(bot))

