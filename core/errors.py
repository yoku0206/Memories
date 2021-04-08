import discord
from discord.ext import commands
from core.classes import Cog_Extension, Logger
from cmds.main import Main
import json, asyncio

with open('settings.json', mode= 'r', encoding= 'utf8') as jfile:
    jdata = json.load(jfile)

class Errors():
    async def default_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg = await ctx.send(self, error)
            Logger.log(self, ctx, error)
            await asyncio.sleep(5)
            await msg.delete()
            
        else:
            msg = await ctx.send(f"未知錯誤: {error}")
            Logger.log(self, ctx, error)
            await asyncio.sleep(5)
            await msg.delete()
            
    