import discord
from discord.ext import commands
from discord import app_commands
import shelve
import json
import random

def get_config(key):
    db = shelve.open("databases/settings/config")
    config_dict = db["configkey"]
    db.close()
    config_dict = json.loads(str(config_dict))
    value = config_dict.get(key, None)
    if isinstance(value, (list, tuple)):
        return value
    return value

TOKEN = "Token"


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_config("ckprefix"), intents=intents)

async def fetch_image(url: str):
    async with bot.http._HTTPClient__session.get(url) as response:
        return await response.read()

@bot.tree.command(name="customize", description="Personalize this Discord bot to cater to your needs!")
@app_commands.describe(
    bot_name="The new name for the bot (optional)",
    bot_icon="URL to the new icon for the bot (optional)"
)
async def send_customize_request(interaction: discord.Interaction, bot_name: str = None, bot_icon: str = None):
    try:
        if bot_name:
            await bot.user.edit(username=bot_name)
        
        if bot_icon:
            avatar_data = await fetch_image(bot_icon)
            await bot.user.edit(avatar=avatar_data)

        await interaction.response.send_message("Bot customization successful!")
    except Exception as e:
        await interaction.response.send_message(f"Failed to customize bot: {e}")


@bot.tree.command(name="help", description="Need help? No problem, this command is here for you!")
async def show_help(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot Commands", description="Here are all the available commands and their usage:", color=discord.Color.blurple())

    embed.add_field(name="/customize [bot_name] [bot_icon]", value="Personalize this Discord bot with a new name and/or icon.", inline=False)
    embed.add_field(name="/roast", value="Randomly roast a specified user", inline=False)
    embed.add_field(name="/purge", value="Purge the channel.", inline=False)
    embed.add_field(name="/help", value="Show available commands and their usage.", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="roast", description="Roast someone.")
async def roast(interaction: discord.Interaction, person_to_roast: discord.Member):
    await interaction.response.send_message(random.choice(get_config("roasts").split("\n")).format(person_to_roast=person_to_roast.mention))

@bot.event
async def on_ready():
    print(f"Running as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.tree.command(name="purge", description="Purges messages from the channel.")
@app_commands.describe(limit="How many messages to purge, -1 for all")
async def say(interaction: discord.Interaction, limit: int):
    if interaction.user.guild_permissions.manage_messages:
        if limit > 0:
            await interaction.response.send_message(f"Purged {limit} messages!", ephemeral=True)
            await interaction.channel.purge(limit=limit)\
            
        elif limit == -1:
            await interaction.response.send_message("Channel purged!", ephemeral=True)
            await interaction.channel.purge()
        else:
            await interaction.response.send_message("Invalid limit given!", ephemeral=True)
    else:
        await interaction.response.send_message("You are NOT allowed to do that!", ephemeral=True)

bot.run(TOKEN)