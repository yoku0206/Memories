import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension, Gloable_Func, Logger
from core import check
from cmds.main import Setting
import datetime, asyncio, json, requests
from discord.ext.commands import MemberConverter


with open('settings.json', mode= 'r', encoding= 'utf8') as jfile:
    jdata = json.load(jfile)

class Mod(Cog_Extension):
    
    pass

def setup(bot):
    bot.add_cog(Mod(bot))