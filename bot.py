import json
import threading
from flask import Flask
import os
import asyncio

TOKEN = os.getenv("TOKEN")

# ===== 70 UID CÀI SẴN =====
UID_LIST = [
"7239185133","1947598925","4148416959","11057060967","13398513199","9404841062","14104403218","14200000765","14888888686","2791495541",
"14856789234","13813062157","14800000850","11976256727","14199999354","UID16","UID17","UID18","UID19","UID20",
"UID21","UID22","UID23","UID24","UID25","UID26","UID27","UID28","UID29","UID30",
"UID31","UID32","UID33","UID34","UID35","UID36","UID37","UID38","UID39","UID40",
"UID41","UID42","UID43","UID44","UID45","UID46","UID47","UID48","UID49","UID50",
"UID51","UID52","UID53","UID54","UID55","UID56","UID57","UID58","UID59","UID60",
"UID61","UID62","UID63","UID64","UID65","UID66","UID67","UID68","UID69","UID70"
]

# ===== WEB SERVER (HOST RENDER) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

# ===== DISCORD BOT =====
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== BOT READY =====
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot Online: {bot.user}")

# ===== SLASH COMMAND LIKE =====
@bot.tree.command(name="like", description="Send Free Fire Likes")
async def like(interaction: discord.Interaction, uid: str):

    await interaction.response.defer()

    url = f"https://ff.garena.cloud/like?uid={uid}&server=VN&key=FREE-FIRE-LIKE-API"

    try:
        r = requests.get(url, timeout=30)
        data = r.json()

        if "response" in data and "OWNERS" in data["response"]:
            del data["response"]["OWNERS"]

        json_text = json.dumps(data, indent=2, ensure_ascii=False)

        await interaction.followup.send(f"```json\n{json_text}\n```")

    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# ===== AUTO COMMAND =====
@bot.command()
async def auto(ctx):

    await ctx.send("🚀 AUTO LIKE STARTED (70 UID)")

    count = 1

    for uid in UID_LIST:

        url = f"https://ff.garena.cloud/like?uid={uid}&server=VN&key=FREE-FIRE-LIKE-API"

        try:
            r = requests.get(url, timeout=30)
            data = r.json()

            name = "Unknown"

            if "response" in data:
                name = data["response"].get("PlayerNickname", "Unknown")

            await ctx.send(f"✅ {count}/70 | UID: {uid} | Name: {name}")

        except Exception as e:
            await ctx.send(f"❌ {count}/70 | UID {uid} | Error: {e}")

        count += 1

        await asyncio.sleep(30)  # delay 30 giây

    await ctx.send("🔥 AUTO LIKE FINISHED")

# ===== RUN WEB SERVER =====
threading.Thread(target=run_web).start()

# ===== START BOT =====
bot.run(TOKEN)