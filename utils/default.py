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