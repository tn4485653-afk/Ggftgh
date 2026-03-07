import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import time
import os
from flask import Flask
import threading

TOKEN = os.getenv("TOKEN")

API_URL = "https://sikibidilike.onrender.com/like"
API_KEY = "luciferr7x"
SERVER_NAME = "VN"

COOLDOWN_FILE = "cooldown.json"
LOG_CHANNEL_ID = 1234567890

# ===== WEB SERVER FOR RENDER =====

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ===== DISCORD BOT =====

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# load cooldown
if os.path.exists(COOLDOWN_FILE):
    with open(COOLDOWN_FILE, "r") as f:
        cooldown = json.load(f)
else:
    cooldown = {}

def save():
    with open(COOLDOWN_FILE, "w") as f:
        json.dump(cooldown, f, indent=4)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

spam_control = {}

@bot.tree.command(name="like", description="Gửi like cho UID")
async def like(interaction: discord.Interaction, uid: str):

    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ Không được dùng trong DM.",
            ephemeral=True
        )
        return

    user_id = str(interaction.user.id)
    now = time.time()

    # anti spam
    if user_id in spam_control:
        if now - spam_control[user_id] < 5:
            await interaction.response.send_message(
                "⚠️ Bạn đang dùng quá nhanh.",
                ephemeral=True
            )
            return

    spam_control[user_id] = now

    # owner unlimited
    if interaction.user == interaction.guild.owner:

        r = requests.get(API_URL, params={
            "uid": uid,
            "server_name": SERVER_NAME,
            "key": API_KEY
        })

        data = r.json()

        embed = discord.Embed(
            title="👑 Server Owner Used Like",
            color=0x00ff00
        )

        embed.add_field(name="UID", value=uid)

        embed.add_field(
            name="Response",
            value=f"```json\n{json.dumps(data,indent=2)}\n```",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

        return

    # cooldown
    if user_id in cooldown:

        last = cooldown[user_id]
        remain = 86400 - (now - last)

        if remain > 0:

            h = int(remain // 3600)
            m = int((remain % 3600) // 60)
            s = int(remain % 60)

            embed = discord.Embed(
                title="⏳ Cooldown",
                description=f"Đợi **{h}h {m}m {s}s** nữa.",
                color=0xff0000
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    try:

        r = requests.get(API_URL, params={
            "uid": uid,
            "server_name": SERVER_NAME,
            "key": API_KEY
        })

        data = r.json()

        cooldown[user_id] = now
        save()

        embed = discord.Embed(
            title="✅ Like Sent",
            color=0x2ecc71
        )

        embed.add_field(name="UID", value=uid)

        embed.add_field(
            name="Response",
            value=f"```json\n{json.dumps(data,indent=2)}\n```",
            inline=False
        )

        embed.set_footer(text=f"Used by {interaction.user}")

        await interaction.response.send_message(embed=embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ API Error",
            description=str(e),
            color=0xff0000
        )

        await interaction.response.send_message(embed=embed)

bot.run(TOKEN)