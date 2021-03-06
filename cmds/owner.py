import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio, os, datetime

with open('settings.json', mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Owner(Cog_Extension):
    
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'載入 **{extension}** 成功')
        print(f"載入 {extension} 成功\n資訊: {ctx.guild} {ctx.channel} {ctx.author}")
        
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'卸載 **{extension}** 成功')
        print(f"卸載 {extension} 成功\n資訊: {ctx.guild} {ctx.channel} {ctx.author}")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        await ctx.message.delete()
        if extension == '*':
            for filename in os.listdir('./cmds'):
                if filename.endswith('.py'):
                    self.bot.reload_extension(f'cmds.{filename[:-3]}')
            msg = await ctx.send(f'成功重新載入所有指令')
            print(f"成功載入 所有指令\n資訊: {ctx.guild} {ctx.channel} {ctx.author}")
        else:
            self.bot.reload_extension(f'cmds.{extension}')
            msg = await ctx.send(f'重新載入 **{extension}** 成功')
            print(f"重新載入 {extension} 成功\n資訊: {ctx.guild} {ctx.channel} {ctx.author}")
        await asyncio.sleep(1)
        await msg.delete()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.message.delete()
        await ctx.send("Shutting down...")
        await asyncio.sleep(1)
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))