import discord
from discord.ext import commands
import json, os, datetime
from datetime import timedelta, timezone, datetime
import keep_alive

intens = discord.Intents.all()

with open("settings.json", mode= 'r', encoding= 'utf8') as jfile:
    jdata = json.load(jfile)


Token = os.getenv("DISCORD_TOKEN")

def time_get():
    dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    local_dt = dt.astimezone(timezone(timedelta(hours=8)))
    return local_dt

bot = commands.Bot(command_prefix=jdata["PREFIX"], intents= intens)

@bot.event
async def on_ready():
    print(">>Bot is ready!!<<")
    print("Bot info: \nname: {} \nid: {} \n當前時間：{}".format(bot.user.name, bot.user.id, time_get().strftime("%Y/%m/%d %H:%M")))
    game = discord.Game(f"輸入 {jdata['PREFIX']}sign 來簽到喔！ OuO")
    await bot.change_presence(status=discord.Status.online, activity=game)

for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        bot.load_extension(f"cmds.{filename[:-3]}")

if __name__ == "__main__":
    # keep_alive.keep_alive()
    bot.run(Token)