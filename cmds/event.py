import discord
from discord.ext import commands
from core.classes import Cog_Extension
from core.errors import Errors
import json, datetime, asyncio

with open('settings.json', mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_command = '{0}_error'.format(ctx.command)
        try:
            if hasattr(Errors, error_command):
                await Errors.error_command()
                return
            elif isinstance(error, commands.errors.CommandNotFound):
                await ctx.message.delete()
                embed = discord.Embed(title="錯誤資訊", description="請檢查你所輸入的指令!", color=0xff1a1a)
                embed.add_field(name="使用者", value=f"{ctx.author.mention}", inline= False)
                embed.add_field(name="指令", value=f"```{ctx.message.content[2:]}```", inline=False)
                embed.add_field(name="錯誤內容", value="你所輸入的指令不存在", inline=False)
                # embed.set_footer(text="")
                await ctx.send(embed=embed)
                return
            elif isinstance(error, commands.errors.CheckFailure):
                await ctx.message.delete()
                embed = discord.Embed(title="錯誤資訊", description="你沒有權限這麼做!", color=0xff1a1a)
                embed.add_field(name="使用者", value=f"{ctx.author.mention}", inline= False)
                embed.add_field(name="指令", value=f"```{ctx.message.content[2:]}```", inline=False)
                embed.add_field(name="錯誤內容", value="你的權限不夠大!", inline=False)
                # embed.set_footer(text="")
                await ctx.send(embed=embed)
                return
            else:
                await Errors.default_error(self, ctx, error)
                pass
        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(Event(bot))