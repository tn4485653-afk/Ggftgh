import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import time
import os

TOKEN = os.getenv("TOKEN")

API_URL = "https://sikibidilike.onrender.com/like"
API_KEY = "luciferr7x"
SERVER_NAME = "VN"

COOLDOWN_FILE = "cooldown.json"
LOG_CHANNEL_ID = 1427614982782189568

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

    # anti spam 5s
    if user_id in spam_control:
        if now - spam_control[user_id] < 5:
            await interaction.response.send_message(
                "⚠️ Bạn đang dùng quá nhanh. Đợi vài giây.",
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

        embed.set_footer(text=f"Used by {interaction.user}")

        await interaction.response.send_message(embed=embed)

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

        return

    # cooldown 24h
    if user_id in cooldown:

        last = cooldown[user_id]
        remain = 86400 - (now - last)

        if remain > 0:

            hours = int(remain // 3600)
            minutes = int((remain % 3600) // 60)
            seconds = int(remain % 60)

            embed = discord.Embed(
                title="⏳ Cooldown",
                description=f"Bạn phải đợi **{hours}h {minutes}m {seconds}s** nữa.",
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

        embed.add_field(name="UID", value=uid, inline=False)

        embed.add_field(
            name="Response",
            value=f"```json\n{json.dumps(data,indent=2)}\n```",
            inline=False
        )

        embed.set_footer(text=f"Used by {interaction.user}")

        await interaction.response.send_message(embed=embed)

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:

            log_embed = discord.Embed(
                title="📜 Like Command Used",
                color=0x3498db
            )

            log_embed.add_field(
                name="User",
                value=interaction.user.mention
            )

            log_embed.add_field(
                name="UID",
                value=uid
            )

            log_embed.add_field(
                name="Server",
                value=interaction.guild.name
            )

            log_embed.set_footer(
                text=time.strftime("%Y-%m-%d %H:%M:%S")
            )

            await log_channel.send(embed=log_embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ API Error",
            description=str(e),
            color=0xff0000
        )

        await interaction.response.send_message(embed=embed)

bot.run(TOKEN)