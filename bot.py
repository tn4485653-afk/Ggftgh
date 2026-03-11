import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import os
from flask import Flask
import threading

TOKEN = os.getenv("TOKEN")

API_URL = "https://nine7yttt67uggdev.onrender.com"
API_KEY = "luciferr7x"
SERVER_NAME = "VN"

LOG_CHANNEL_ID = 1234567890

# ===== WEB SERVER (PORT FOR RENDER) =====

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ===== DISCORD BOT =====

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

@bot.tree.command(name="like", description="Send like to UID")
async def like(interaction: discord.Interaction, uid: str):

    await interaction.response.defer()

    try:

        r = requests.get(API_URL, params={
            "uid": uid,
            "server_name": SERVER_NAME,
            "key": API_KEY
        })

        data = r.json()

        embed = discord.Embed(
            title="✅ Like Sent",
            color=0x2ecc71
        )

        embed.add_field(name="UID", value=uid)

        embed.add_field(
            name="API Response",
            value=f"```json\n{json.dumps(data,indent=2)}\n```",
            inline=False
        )

        embed.set_footer(text=f"Used by {interaction.user}")

        await interaction.followup.send(embed=embed)

        # LOG
        log_channel = bot.get_channel(LOG_CHANNEL_ID)

        if log_channel:
            await log_channel.send(f"!like {uid}")

    except Exception as e:

        await interaction.followup.send(f"❌ Error: {e}")

bot.run(TOKEN)