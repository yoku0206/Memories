import discord
from discord.ext import commands, tasks
from discord import Object
from core.classes import Cog_Extension, Gloable_Func, Logger
from core import check
from utils import default
import datetime, asyncio, json, requests
from discord.ext.commands import MemberConverter, Greedy
from typing import Optional


jdata = default.Settings_Load()

class BannedUser(commands.Converter):
    async def convert(self, ctx, arg):
        if ctx.guild.me.guild_permissions.ban_members:
            if str(arg).isdigit():
                try:
                    member = await ctx.guild.fetch_ban(Object(id=int(arg))).user
                except discord.NotFound:
                    raise commands.BadArgument
            elif arg.startswith('<') and arg.endswith('>'):
                member = await ctx.guild_fetch_ban(Object(id=int(arg[3:-1]))).user
            else:
                member = arg

            member_name, member_discriminator = str(member).split('#')
            for ban in await ctx.guild.bans():
                user = ban.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    return user

class Mod(Cog_Extension):
    
    @commands.command(name='踢出成員', description='將成員從群組中踢出', aliases=['kick'])
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, targets: Greedy[discord.Member], *, reason: Optional[str] = '沒有原因！'):
        await ctx.message.delete()
        if not len(targets):
            await ctx.send(f"**[錯誤]** 缺少必要參數！\n正確用法：**`{jdata['PREFIX']}kick (成員) [原因]`**")
            pass
        try:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator and not target.id == jdata['Owner_id']:
                    await target.kick(reason=reason)

                    embed = discord.Embed(title='成員踢出', color=0xDD2222, timestamp=datetime.datetime.now())
                    embed.set_thumbnail(url=target.avatar_url)
                    embed.set_footer(text="簽到機器人 By 天夜Yoku#6529", icon_url=f"{ctx.bot.user.avatar_url}")
                    fileds = [
                        ("成  員", f"**`{target}`**", False),
                        ("執行人", f"**`{ctx.author.display_name}`**", False),
                        ("原  因", f"`{reason}`", False)
                    ]
                    for name, value, inline in fileds:
                        embed.add_field(name=name, value=value, inline=inline)

                    await ctx.send(embed= embed)
                else:
                    await ctx.send(f"[錯誤] 你不能對 {target.mention} 這麼做！ 壞壞 (≧∀≦)ゞ")

        except:
            await ctx.send("[錯誤] 指令錯誤！")
            pass
    
    @kick_member.error
    async def kick_command_error(self, ctx, exc):
        await ctx.message.delete()
        if isinstance(exc, commands.CheckFailure):
            await ctx.send("**[錯誤]** 你沒有權限這樣做！！")
    
    @commands.command(name='封禁成員', description='將成員從群組中封禁', aliases=['ban'])
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, targets: Greedy[discord.Member], *, reason: Optional[str]= '沒有原因！'):
        await ctx.message.delete()
        if not len(targets):
            await ctx.send(f"**[錯誤]** 缺少必要參數！\n正確用法：**`{jdata['PREFIX']}ban (成員) [原因]`**")
            pass
        try:
            for target in targets:
                if (ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator and not target.id == jdata['Owner_id']):
                    await target.ban(reason=reason, delete_message_days=0)

                    embed = discord.Embed(title='成員封鎖', color=0xDD2222, timestamp=datetime.datetime.now())
                    embed.set_thumbnail(url=target.avatar_url)
                    fileds = [
                        ("成  員", f"**`{target}`**"),
                        ("執行人", f"**`{ctx.author.display_name}`**"),
                        ("原  因", f"`{reason}`")
                    ]
                    for name, value in fileds:
                        embed.add_field(name=name, value=value, inline=False)
                    
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"[錯誤] 你不能對 {target.mention} 這麼做！ 壞壞 (≧∀≦)ゞ")
        except:
            await ctx.send("[錯誤] 指令錯誤！")
            pass

    @ban_member.error
    async def ban_command_error(self, ctx, exc):
        await ctx.message.delete()
        if isinstance(exc, commands.CheckFailure):
            await ctx.send("**[錯誤]** 你沒有權限這樣做！")
        else:
            await ctx.send(exc)

    @commands.command(name='解除封禁', description='從群組解除成員封禁', aliases=['unban'])
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban_member(self, ctx, targets: Greedy[BannedUser], *, reason: Optional[str] = '沒有原因！'):
        await ctx.message.delete()
        if not len(targets):
            await ctx.send(f"[錯誤] 缺少必要參數!\n正確用法：**`{jdata['PREFIX']}unban (成員) [原因]`**")
            pass
        try:
            for target in targets:
                await ctx.guild.unban(target, reason=reason)

                embed = discord.Embed(title='解除封鎖', color=0xDD2222, timestamp=datetime.datetime.now())
                embed.set_thumbnail(url=target.avatar_url)
                fileds = [
                    ("成  員", f"**`{target}`**"),
                    ("執行人", f"**`{ctx.author.display_name}`**"),
                    ("原  因", f"`{reason}`")
                ]
                for name, value in fileds:
                    embed.add_field(name=name, value=value, inline=False)
                
                await ctx.send(embed=embed)
        except:
            await ctx.send("[錯誤] 指令錯誤！")
            pass
    
    @unban_member.error
    async def unban_command_error(self, ctx, exc):
        await ctx.message.delete()
        if isinstance(exc, commands.CheckFailure):
            await ctx.send("**[錯誤]** 你沒有權限這樣做！")
        elif isinstance(exc, commands. BadArgument):
            await ctx.send(f"**[錯誤]** 請輸入正確的參數！\n正確用法：**`{jdata['PREFIX']}unban (成員) [原因]`**")
        else:
            await ctx.send(exc)
        
    @commands.command(name='清除', description='清除訊息', aliases=['clear', 'purge', 'cls'])
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, target: Optional[discord.Member] = None, number: Optional[int] = 1, *, reason: Optional[str] = '沒有原因！'):
        await ctx.message.delete()

        def check_msg(msg):
            if msg.author.id == target.id:
                return True
            else:
                return False
        
        if target == None:
            await ctx.channel.purge(limit=number, bulk= True)
            embed = discord.Embed(title='訊息清除資訊', color=ctx.author.color.random(), timestamp=default.time_get())
            embed.add_field(name="執行人", value=ctx.author.display_name, inline=False)
            embed.add_field(name="數  量", value=f"**{number}**", inline=False)
            embed.add_field(name="原  因", value=f"`{reason}`", inline=False)
            embed.set_footer(text="簽到機器人 By 天夜Yoku#6529", icon_url=f"{ctx.bot.user.avatar_url}")
            # msg = await ctx.send(f"已刪除 {number} 則訊息！")
            msg = await ctx.send(embed= embed)
        else:
            count = 0
            async for message in ctx.channel.history():
                if count == number:
                    break
                if message.author.id == target.id:
                    await message.delete()
                    count += 1
                else:
                    pass
            # await ctx.channel.purge(limit=number, bulk=True, check=check_msg)
            embed = discord.Embed(title='訊息清除資訊', color=ctx.author.color.random(), timestamp=default.time_get())
            embed.add_field(name="執行人", value=ctx.author.display_name, inline=False)
            embed.add_field(name="目  標", value=target.display_name, inline=False)
            embed.add_field(name="數  量", value=f"**{number}**", inline=False)
            embed.add_field(name="原  因", value=f"`{reason}`", inline=False)
            embed.set_footer(text="簽到機器人 By 天夜Yoku#6529", icon_url=f"{ctx.bot.user.avatar_url}")
            # msg = await ctx.send(f"已刪除 {target.display_name} {number} 則訊息！")
            msg = await ctx.send(embed= embed)

        await asyncio.sleep(10)
        await msg.delete()

    @clear_messages.error
    async def clear_command_error(self, ctx, exc):
        await ctx.message.delete()
        if isinstance(exc, commands.BadArgument):
            await ctx.send(f"**[錯誤]** 請輸入正確的參數！\n正確用法：**`{jdata['PREFIX']}clear [目標] [數量] [原因]`**")
        elif isinstance(exc, commands.CheckFailure):
            await ctx.send("**[錯誤]** 你沒有權限這樣做！")
        else:
            await ctx.send(exc)

        





def setup(bot):
    bot.add_cog(Mod(bot))