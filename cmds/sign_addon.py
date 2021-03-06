import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension, Gloable_Func, Logger
from core import check
from cmds.main import Setting
import datetime, asyncio, json
from discord.ext.commands import MemberConverter


with open('settings.json', mode= 'r', encoding= 'utf8') as jfile:
    jdata = json.load(jfile)

class Sign_Addon(Cog_Extension):
    
    @commands.command(aliases=["ranks"])
    async def sign_scoreboard(self, ctx, page: int = 1):
        await ctx.message.delete()

        await Setting.Guild_Info(self, ctx)
        gdata = Setting.Guild_Json_Load(self)

        temp = {}

        for i in gdata[str(ctx.guild.id)]['user']:
            temp[i] = gdata[str(ctx.guild.id)]['user'][i]['total']

        data = sorted(temp.items(), key=lambda x:x[1], reverse=True)

        data_page = len(data) // 10
        data_count = len(data) % 10

        if page > data_page:
            if data_count > 0:
                j = 1
            else:
                j = 0
            page = len(data) // 10 + j
        else:
            pass
        num = (page - 1) * 10
        num_end = page * 10


        embed=discord.Embed(title=f"{ctx.guild.name}", description=f"**簽到天數排行榜** {num + 1} ～ {num_end}", color=ctx.author.color, timestamp=Setting.time_get(self))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"Page: {page}/{data_page + j}")
        for i in range(num, num_end):
            try:
                member = await MemberConverter().convert(ctx, data[i][0])
                embed.add_field(name=f"{i + 1}. {member.name}#{member.discriminator} ", value=f"總共簽到： **{data[i][1]}** 天", inline=False)
            except:
                pass
        message = await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await message.delete()






def setup(bot):
    bot.add_cog(Sign_Addon(bot))