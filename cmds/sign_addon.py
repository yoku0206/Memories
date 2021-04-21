import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension, Gloable_Func, Logger
from core import check
from cmds.main import Setting
from utils import default
import datetime, asyncio, json
from discord.ext.commands import MemberConverter


with open('settings.json', mode= 'r', encoding= 'utf8') as jfile:
    jdata = json.load(jfile)

class Sign_Addon(Cog_Extension):
    
    @commands.command(name='簽到排行榜', description='簽到排行榜', aliases=['ranks'])
    async def sign_scoreboard(self, ctx):
        await ctx.message.delete()
        await Setting.Guild_Info(self, ctx)
        gdata = default.Guild_Load()

        temp = {}
        for i in gdata[str(ctx.guild.id)]['user']:
            temp[i] = gdata[str(ctx.guild.id)]['user'][i]['total']
        data = sorted(temp.items(), key= lambda x: x[1], reverse=True)

        data_page = len(data) // 10
        if len(data) % 10 > 0:
            data_page += 1

        em = []
        for page in range(data_page):
            embed = discord.Embed(title= f"{ctx.guild.name}", description= f"**簽到天數排行榜**",
            color=ctx.author.color.random(), timestamp=default.time_get())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f"Page: {page + 1}/{data_page}", icon_url=f"{ctx.bot.user.avatar_url}")
            for i in range((page) * 10, ((page + 1) * 10)):
                try:
                    member = await MemberConverter().convert(ctx, data[i][0])
                    embed.add_field(name= f"{i + 1}. {member.name}#{member.discriminator} ", 
                    value= f"總共簽到： **{data[i][1]}**", inline=False)
                except:
                    pass
            em.append(embed)

        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        current = 0
        msg = await ctx.send(embed=em[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add",
                 check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, 
                 timeout=60.0)

            except asyncio.TimeoutError:
                await msg.delete()
                return

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0
                    
                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                        
                elif reaction.emoji == u"\u27A1":
                    if current < len(em)-1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(em)-1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=em[current])
        
        




def setup(bot):
    bot.add_cog(Sign_Addon(bot))