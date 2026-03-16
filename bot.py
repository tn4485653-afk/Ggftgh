import discord
from discord.ext import commands
import requests
import json
import threading
from flask import Flask
import os

TOKEN = os.getenv("TOKEN")

# WEB SERVER FOR RENDER
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

# DISCORD BOT
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot Online: {bot.user}")

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

threading.Thread(target=run_web).start()

bot.run(TOKEN)