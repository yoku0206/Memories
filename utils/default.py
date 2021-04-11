import discord
import json, requests, datetime
from datetime import timezone, timedelta, datetime


def Settings_Load():
    with open('settings.json', mode= 'r', encoding= 'utf8') as jfile:
        return json.load(jfile)

def Settings_Write(jdata):
    with open('settings.json', mode= 'w', encoding= 'utf8') as jfile:
        json.dump(jdata, jfile, indent=4, ensure_ascii=False)

def Guild_Load():
    response = requests.get('https://jsonstorage.net/api/items/', {
            "id": "3202bdcb-5212-4789-822a-5864caa6e62e"
        })
    data = response.json()
    return data

def Guild_Write(data):
    update = requests.put('https://jsonstorage.net/api/items/', 
        params = {"id": "3202bdcb-5212-4789-822a-5864caa6e62e"},
        json = data
    )

def time_get():
    dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    local_dt = dt.astimezone(timezone(timedelta(hours=8)))
    return local_dt

def time_convert(time):
    pos = ["s", "m", "h", "d"]
    time_dict = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 3600*24
    }
    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    
    return val * time_dict[unit]

def check(ctx):
    user_id = int(ctx.message.author.id)
    gdata = Guild_Load()
    admin_list = gdata[str(ctx.guild.id)]['settings']['admin']
    return user_id in admin_list or user_id == 480906273026473986