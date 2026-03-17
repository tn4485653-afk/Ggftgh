import discord
from discord.ext import commands
import requests
import asyncio
from flask import Flask
import threading
import os
import json

# ===== ENV =====
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ Missing TOKEN")

# ===== KEY để thẳng =====
VISIT_KEY = "skibidiexe"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# ===== WEB KEEP ALIVE =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    threading.Thread(target=run_web).start()

# ===== EMOTES =====
EMOTES_RD = [
"909042007","909049006","909050009","909051009","909000002",
"909051005","909000006","909000014","909000010","909000048",
"909000034","909000020","909000021","909000012","909000015",
"909000069"
]

EMOTES_S7 = [
"909000063","909000068","909000075","909040010","909000081",
"909039011","909000085","909000090","909000098","909035007",
"909042008","909041005","909033001","909038010","909038012",
"909045001","909049010","909051003"
]

API_URL = "https://tui-3yue7eisiskksjs.onrender.com/join"
VISIT_API = "https://cosmos-visit-api.vercel.app/visit"

# ===== CALL JOIN =====
def call_api(tc, group, emote):
    params = {
        "tc": tc,
        "uid1": group[0] if len(group) > 0 else "",
        "uid2": group[1] if len(group) > 1 else "",
        "uid3": group[2] if len(group) > 2 else "",
        "uid4": group[3] if len(group) > 3 else "",
        "uid5": group[4] if len(group) > 4 else "",
        "uid6": "",
        "emote_id": emote
    }

    try:
        requests.get(API_URL, params=params, timeout=10)
    except:
        pass

# ===== AUTO =====
async def run_auto(ctx, tc, uids, emotes):
    if isinstance(ctx.channel, discord.DMChannel):
        return

    await ctx.send(f"🚀 Running {len(uids)} UID...")

    groups = [uids[i:i+5] for i in range(0, len(uids), 5)]

    for emote in emotes:
        for group in groups:
            call_api(tc, group, emote)

        await asyncio.sleep(8)

    await ctx.send("✅ Done!")

# ===== RD =====
@bot.command()
async def rd(ctx, tc, *uids):
    if isinstance(ctx.channel, discord.DMChannel):
        return

    if not uids:
        await ctx.send("❌ Missing UID!")
        return

    bot.loop.create_task(run_auto(ctx, tc, list(uids), EMOTES_RD))

# ===== S7 =====
@bot.command()
async def s7(ctx, tc, *uids):
    if isinstance(ctx.channel, discord.DMChannel):
        return

    if not uids:
        await ctx.send("❌ Missing UID!")
        return

    bot.loop.create_task(run_auto(ctx, tc, list(uids), EMOTES_S7))

# ===== VISIT =====
@bot.command()
async def visit(ctx, region, uid):
    if isinstance(ctx.channel, discord.DMChannel):
        return

    params = {
        "api_key": VISIT_KEY,  # 🔑 key nằm đây
        "region": region,
        "uid": uid
    }

    try:
        r = requests.get(VISIT_API, params=params, timeout=40)
        data = r.json()

        formatted = json.dumps(data, indent=2, ensure_ascii=False)

        if len(formatted) > 1900:
            await ctx.send("📄 JSON quá dài, xem log Render!")
            print(formatted)
        else:
            await ctx.send(f"```json\n{formatted}\n```")

    except requests.exceptions.Timeout:
        await ctx.send("⏱ Timeout 40s!")
    except Exception as e:
        await ctx.send("❌ API lỗi!")
        print(e)

# ===== START =====
keep_alive()
bot.run(TOKEN)