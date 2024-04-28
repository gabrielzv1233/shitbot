import discord
from discord.ext import commands
import shelve
import json
import os

if not os.path.isfile(".env"):
    with open(".env", "w") as file:
        file.write("TOKEN=Your_Bot_Token_here\n")

from dotenv import load_dotenv
load_dotenv()

def get_config(key):
    db = shelve.open("databases/settings/config")
    config_dict = db["configkey"]
    db.close()
    config_dict = json.loads(str(config_dict))
    value = config_dict.get(key, None)
    if isinstance(value, (list, tuple)):
        return value
    return value

TOKEN = os.environ['TOKEN']


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_config("ckprefix"), intents=intents)

@bot.event
async def on_ready():
    print(f"Discord bot running as {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=get_config("watching_status")))

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(aliases=get_config("purge_aliases"))
async def purge(ctx):
    allowed_roles_ids = [str(role_id) for role_id in get_config("allowed_purge_roles")]
    user_role_ids = [str(role.id) for role in ctx.author.roles]

    if any(role_id in allowed_roles_ids for role_id in user_role_ids):
        await ctx.channel.purge()
        await ctx.send(f"{ctx.author.display_name}, Messages purged!", delete_after=5)
    else:
        await ctx.send(f"{ctx.author.display_name}, You are NOT allowed to do that!", delete_after=5)

bot.run(TOKEN)