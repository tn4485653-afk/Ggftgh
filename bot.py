import discord
from discord.ext import commands
import requests
import json
import threading
from flask import Flask
import os
import asyncio

TOKEN = os.getenv("TOKEN")

# ===== UID LIST =====
UID_LIST = [
"7239185133","1947598925","4148416959","11057060967","13398513199",
"9404841062","14104403218","14200000765","14888888686","2791495541",
"14856789234","13813062157","14800000850","11976256727","14199999354"
]

# ===== WEB SERVER (FOR RENDER) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

# ===== DISCORD BOT =====
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot Online: {bot.user}")

# ===== SLASH COMMAND =====
@bot.tree.command(name="like", description="Send Free Fire Likes")
async def like(interaction: discord.Interaction, uid: str):

    await interaction.response.defer()

    url = f"https://ff.garena.cloud/like?uid={uid}&server=VN&key=FREE-FIRE-LIKE-API"

    try:
        r = requests.get(url, timeout=30)
        data = r.json()

        json_text = json.dumps(data, indent=2, ensure_ascii=False)

        await interaction.followup.send(f"```json\n{json_text}\n```")

    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# ===== AUTO LIKE =====
@bot.command()
async def auto(ctx):

    await ctx.send("🚀 AUTO LIKE STARTED")

    count = 1

    for uid in UID_LIST:

        url = f"https://ff.garena.cloud/like?uid={uid}&server=VN&key=FREE-FIRE-LIKE-API"

        try:
            r = requests.get(url, timeout=30)
            data = r.json()

            name = data.get("response", {}).get("PlayerNickname", "Unknown")

            await ctx.send(f"✅ {count}/{len(UID_LIST)} | UID: {uid} | Name: {name}")

        except Exception as e:
            await ctx.send(f"❌ UID {uid} Error: {e}")

        count += 1
        await asyncio.sleep(30)

    await ctx.send("🔥 AUTO LIKE FINISHED")

# ===== START WEB SERVER =====
threading.Thread(target=run_web, daemon=True).start()

# ===== RUN BOT =====
bot.run(TOKEN)