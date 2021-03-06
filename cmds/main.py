import discord
from discord.ext import commands, tasks
from core.classes import Cog_Extension, Gloable_Func, Logger
from core import check
import datetime, asyncio, json
from discord.ext.commands import MemberConverter
from datetime import datetime, timezone, timedelta


with open('settings.json', mode= 'r', encoding= 'utf8') as jfile:
    jdata = json.load(jfile)

def Admin_Check():
    def Check_Admin(ctx):
        with open('guild.json', mode='r', encoding=' utf8') as gfile:
            gdata = json.load(gfile)
        user_id = int(ctx.message.author.id)
        return user_id in gdata[str(ctx.guild.id)]['settings']['admin'] or user_id == 480906273026473986
    return commands.check(Check_Admin)

class Setting():
    def __init__(self, bot):
        self.bot = bot

    def Guild_Json_Load(self):
        with open('guild.json', mode='r', encoding=' utf8') as gfile:
            gdata = json.load(gfile)
        return gdata

    def Guild_Json_Write(self, gdata):
        with open('guild.json', mode= 'w', encoding=' utf8') as gfile:
            json.dump(gdata, gfile, indent=4, ensure_ascii=False)
    
    def time_get(self):
        dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        local_dt = dt.astimezone(timezone(timedelta(hours=8)))
        return local_dt


    async def Guild_Info(self, ctx):
        async for guilds in self.bot.fetch_guilds():
            gdata = Setting.Guild_Json_Load(self)
            guild = self.bot.get_guild(guilds.id)
            guild_id = str(guild.id)
            print("="*20)
            print("\n檢查中...\n")
            print(f"群組名稱： {guild.name}")
            print(f"群組ID： {guild.id}\n")

            if guild_id not in gdata:
                print(f"找不到 {guild.name} 新增中...")
                gdata[guild_id] = {
                    "name": guild.name,
                    "settings": {
                        "ann_time": "0",
                        "admin": [480906273026473986],
                        "stop": 0,
                        "channel": 0
                    },
                    "user": {}
                }
                Setting.Guild_Json_Write(self, gdata)
                print("新增完成！")
            else:
                print(f"{guild.name} 檢查中...")
                gdata[guild_id]['name'] = guild.name
                try:
                    for i in gdata[guild_id]['settings']['admin']:
                        if guild.get_member(int(i)) == None:
                            print(f"找不到 {i}")
                            gdata[guild_id]['settings']['admin'].remove(i)
                        else:
                            member = guild.get_member(int(i))
                            print(f"成功找到 {member.name}！")
                            pass
                except KeyError:
                    print("找不到此資料...建立中...")
                    gdata[guild_id]['settings']['admin'] = [480906273026473986]
                try:
                    for i in gdata[guild_id]['user']:
                        if guild.get_member(int(i)) == None:
                            print(f"找不到 {i}")
                            del gdata[guild_id]['user'][str(i)]
                        else:
                            member = guild.get_member(int(i))
                            print(f"成功找到 {member.name}！")
                except KeyError:
                    print("找不到此資料...建立中...")
                    gdata[guild_id]['user'] = {}
                try:
                    if guild.get_channel(gdata[guild_id]['settings']['channel']) == None:
                        print(f"找不到 {gdata[guild_id]['settings']['channel']}")
                        gdata[guild_id]['settings']['channel'] = 0
                    else:
                        channel = guild.get_channel(gdata[guild_id]['settings']['channel'])
                        print(f"成功找到 {channel.name}！")
                except KeyError:
                    print("找不到此資料...建立中...")
                    gdata[guild_id]['settings']['channel'] = 0

            Setting.Guild_Json_Write(self, gdata)
            print("檢查完成...資料儲存完成...\n")
            

class Main(Cog_Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_preset.start()


    @tasks.loop(seconds=1)
    async def user_preset(self):
        gdata = Setting.Guild_Json_Load(self)
        now_time = Setting.time_get(self)
        
        datetime_format = now_time.strftime("%d")
        now_month = now_time.strftime("%B")

        for guilds in gdata:
            if gdata[guilds]['settings']['stop'] == 0 and datetime_format != gdata[guilds]['settings']['ann_time']:
                print("\n偵測符合條件！\n")

                gdata[guilds]['settings']['stop'] = 1
                gdata[guilds]['settings']['ann_time'] = datetime_format

                guild = self.bot.get_guild(int(guilds))

                try:
                    channel = guild.get_channel(int(gdata[guilds]['settings']['channel']))
                    await channel.send("**各位早安！又是美好的一天呢XD**")
                except:
                    print(f"{guild.name} 頻道錯誤！")
                    pass
                
                if now_month in jdata['month'] and now_month != jdata['Now_Month']:
                    print("偵測到月份改變...修正中...\n")
                    jdata['Now_Month'] = now_month
                    for guilds in gdata:
                        for user in gdata[guilds]['user']:
                            gdata[guilds]['user'][user]['month'] = 0
                            gdata[guilds]['user'][user]['today'] = "False"
                    print("修正完成...")
                    with open('settings.json', mode='w', encoding= 'utf8') as jfile:
                        json.dump(jdata, jfile, indent=4, ensure_ascii=False)
                else:
                    print("月份相同...更新本日簽到記錄中...\n")
                    for user in gdata[guilds]['user']:
                        gdata[guilds]['user'][user]['today'] = "False"
                    print("更新完成...")
                        
                Setting.Guild_Json_Write(self, gdata)
                gdata = Setting.Guild_Json_Load(self)

            elif gdata[guilds]['settings']['stop'] == 1 and datetime_format == gdata[guilds]['settings']['ann_time']:
                print("\n偵測符合條件！\n")

                gdata[guilds]['settings']['stop'] = 0
                
                Setting.Guild_Json_Write(self, gdata)
                gdata = Setting.Guild_Json_Load(self)



    @user_preset.before_loop
    async def wait_user_preset(self):
        await self.bot.wait_until_ready()
        print("迴圈開始！")

    @commands.command(aliases=["pstart"])
    async def preset_start(self, ctx):
        await ctx.message.delete()
        try:
            self.user_preset.start()
            await ctx.send("迴圈開始！")
        except:
            await ctx.send("執行失敗！")
    
    @commands.command(aliases=["pstop"])
    async def preset_stop(self, ctx):
        await ctx.message.delete()
        try:
            self.user_preset.cancel()
            await ctx.send("迴圈停止！")
        except:
            await ctx.send("停止失敗！")

    @commands.command()
    async def ping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f'{round(self.bot.latency*1000)} (毫秒)')

    @commands.command()
    async def sign(self, ctx):
        await ctx.message.delete()

        await Setting.Guild_Info(self, ctx)

        gdata = Setting.Guild_Json_Load(self)

        if str(ctx.author.id) not in gdata[str(ctx.guild.id)]['user']:
            print(f"{ctx.author.name} 資料不存在...建立中...\n")
            gdata[str(ctx.guild.id)]['user'][str(ctx.message.author.id)] = {
                "name": ctx.author.name,
                "today": "False",
                "month": 0,
                "total": 0
            }
            Setting.Guild_Json_Write(self, gdata)
            print("資料建立完成\n")

        gdata = Setting.Guild_Json_Load(self)

        if gdata[str(ctx.guild.id)]['user'][str(ctx.author.id)]['today'] == "False":
            print(f"更新 {ctx.author.name} 本日簽到記錄中...\n")

            gdata[str(ctx.guild.id)]['user'][str(ctx.author.id)]['today'] = "True"
            gdata[str(ctx.guild.id)]['user'][str(ctx.author.id)]['month'] += 1
            gdata[str(ctx.guild.id)]['user'][str(ctx.author.id)]['total'] += 1

            Setting.Guild_Json_Write(self, gdata)
            print(f"{ctx.author.name} 紀錄更新完成！")

            gdata = Setting.Guild_Json_Load(self)

            days = str(gdata[str(ctx.guild.id)]['user'][str(ctx.author.id)]['total'])

            embed = discord.Embed(title="**簽到成功**", description=f"你已成功簽到 **{days}** 天", 
            color=ctx.author.color, timestamp=Setting.time_get(self))
            embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif gdata[str(ctx.guild.id)]['user'][str(ctx.author.id)]['today'] == "True":
            print(f"{ctx.author.name} 已經完成簽到！")

            embed = discord.Embed(title="**簽到失敗**", description="你今天已經簽到過了喔！", 
            color= 0xff1a1a, timestamp=Setting.time_get(self))
            embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("發生錯誤！請立即通知管理員喔！")

    @commands.command()
    async def check(self, ctx, *, mem = None):
        await ctx.message.delete()
        if mem == None:
            member = ctx.author
        else:
            try:
                member = await MemberConverter().convert(ctx, mem)
            except:
                await ctx.send("請輸入正確的成員！")
        await Setting.Guild_Info(self, ctx)
        gdata = Setting.Guild_Json_Load(self)

        with open('settings.json', mode='r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        
        now_month = jdata['Now_Month']
        now_month_name = jdata['month'][now_month]['name']
        now_month_day = jdata['month'][now_month]['day']
        now_day = int(Setting.time_get(self).strftime("%d"))
        month_sign = gdata[str(ctx.guild.id)]['user'][str(member.id)]['month']
        total_sign = gdata[str(ctx.guild.id)]['user'][str(member.id)]['total']

        if gdata[str(ctx.guild.id)]['user'][str(member.id)]['today'] == "True":
            today_sign = "已簽到！"
        else:
            today_sign = "尚未簽到喔！"

        embed = discord.Embed(title=f"{member.name}#{member.discriminator} **簽到記錄**", color=member.color, timestamp=Setting.time_get(self))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="本日簽到", value=f"**`{today_sign}`**", inline=False)
        embed.add_field(name=f"{now_month_name} 簽到天數", value=f"**`{month_sign}`**", inline=True)
        embed.add_field(name=f"{now_month_name} 未簽到天數", value=f"**`{now_month_day - month_sign}`**", inline=True)
        embed.add_field(name=f"{now_month_name} 剩餘天數", value=f"**`{now_month_day - now_day}`**", inline=True)
        embed.add_field(name="總簽到天數", value=f"**`{total_sign}`**", inline=True)
        embed.set_footer(text=f"使用 {jdata['PREFIX']}sign 來簽到，{jdata['PREFIX']}check 查看自己的簽到狀況")
        await ctx.send(embed=embed)

    @commands.group()
    @Admin_Check()
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send("請輸入正確的參數！")
            pass
        else:
            pass

    @admin.group(aliases=["add"])
    async def admin_add(self, ctx, *, mem = None):
        await ctx.message.delete()
        try:
            if mem == None:
                await ctx.send("確用法：**`s!admin add @(user)`**")
                pass
            else:
                try:
                    member = await MemberConverter().convert(ctx, mem)
                    await Setting.Guild_Info(self, ctx)
                    gdata = Setting.Guild_Json_Load(self)
                    if member in gdata[str(ctx.guild.id)]['settings']['admin']:
                        await ctx.send("[錯誤] 此成員已經是管理員了!\n使用 **`s!admin list`** 來查看目前的管理員!")
                    else:
                        gdata[str(ctx.guild.id)]['settings']['admin'].append(member.id)
                        await ctx.send(f"[資訊] 成功新增 {member.mention}!")
                    Setting.Guild_Json_Write(self, gdata)
                except:
                    await ctx.send("正確用法：**`y!ticket admin add @(user)`**")
                    pass
        except:
            await ctx.send("[錯誤] 指令錯誤!!")
            pass
    
    @admin.command(aliases=['remove'])
    async def admin_remove(self, ctx, mem = None):
        await ctx.message.delete()
        try:
            if mem == None:
                await ctx.send("正確用法：**`s!admin remove @(user)`**")
                pass
            else:
                try:
                    member = await MemberConverter().convert(ctx, mem)
                    await Setting.Guild_Info(self, ctx)
                    gdata = Setting.Guild_Json_Load(self)
                    if member.id not in gdata[str(ctx.guild.id)]['settings']['admin']:
                        await ctx.send("[錯誤] 此成員不是管理員!!\n使用 **`s!admin list`** 來查看目前的管理員!")
                    else:
                        gdata[str(ctx.guild.id)]['settings']['admin'].remove(member.id)
                        await ctx.send(f"[資訊] 成功移除 {member.mention}!")
                    Setting.Guild_Json_Write(self, gdata)
                except:
                    await ctx.send("正確用法：**`s!admin remove @(user)`**")
                    pass
        except:
            await ctx.send("[錯誤] 指令錯誤!!")
            pass
    
    @admin.command(aliases=['list'])
    async def admin_list(self, ctx):
        await ctx.message.delete()
        try:
            await Setting.Guild_Info(self, ctx)
            gdata = Setting.Guild_Json_Load(self)
            members = ""
            if gdata[str(ctx.guild.id)]['settings']['admin']:
                for i in gdata[str(ctx.guild.id)]['settings']['admin']:
                    user = await MemberConverter().convert(ctx, str(i))
                    members = members + "\n" + user.name
                await ctx.send(f"[資訊] 管理員：\n```{members}```")
            else:
                await ctx.send("[錯誤] 沒有任何管理員!!")
                pass
        except:
            await ctx.send("[錯誤] 指令錯誤!!")
            pass


    @admin.command(aliases=["time"])
    async def time_set(self, ctx, num, time):
        await ctx.message.delete()
        gdata = Setting.Guild_Json_Load(self)
        if num == "1":
            gdata[str(ctx.guild.id)]['settings']['ann_time_1'] = time
        elif num == "2":
            gdata[str(ctx.guild.id)]['settings']['ann_time_2'] = time
        elif num == "3":
            gdata[str(ctx.guild.id)]['settings']['ann_time_3'] = time
        else:
            await ctx.send("請輸入正確的數值！")
        Setting.Guild_Json_Write(self, gdata)
        await ctx.send(f'時間設定: {time}')
        datetime_format = Setting.time_get(self).strftime("%H%M")
        await ctx.send(f"現在時間： {datetime_format}")

    @admin.group()
    async def user(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send("[錯誤] 請輸入有效的參數！")
            pass
    
    @user.command(aliases=["preset"])
    async def user_preset_command(self, ctx, mem = "*"):
        await ctx.message.delete()
        if mem == "*":
            gdata = Setting.Guild_Json_Load(self)
            gdata[str(ctx.guild.id)]['settings']['stop'] = 0
            for user in gdata[str(ctx.guild.id)]['user']:
                gdata[str(ctx.guild.id)]['user'][user]['today'] = "False"

            Setting.Guild_Json_Write(self, gdata)
            gdata = Setting.Guild_Json_Load(self)

            await ctx.send("**處理完成！！**")
        else:
            try:
                member = MemberConverter().convert(ctx, mem)
                gdata = Setting.Guild_Json_Load(self)
                gdata[str(ctx.guild.id)]['settings']['stop'] = 0
                gdata[str(ctx.guild.id)]['user'][str(member.id)]['today'] = "False"
                    
                Setting.Guild_Json_Write(self, gdata)
                gdata = Setting.Guild_Json_Load(self)

                await ctx.send("**處理完成！！**")
            except:
                pass

def setup(bot):
    bot.add_cog(Main(bot))