import discord
from discord.ext import commands
from discord import app_commands
import random

TOKEN = "Token"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers"))
    print(f"Watching {len(bot.guilds)} servers")
    print(f"Running as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
        
@bot.tree.command(name="sync", description="Resync slash commands")
@app_commands.default_permissions(administrator=True)
async def sync(interaction: discord.Interaction):
    try:
        synced = await bot.tree.sync()
        await interaction.response.send_message(f"synced {len(synced)} command(s)")
    except Exception as e:
        await interaction.response.send_message(e)

@bot.event
async def on_guild_join(guild: discord.Guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers"))
    print(f"Bot added to {guild.id}, Now watching {len(bot.guilds)} servers")

@bot.event
async def on_guild_remove(guild: discord.Guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers"))
    print(f"Bot removed from {guild.id}, Now watching {len(bot.guilds)} servers")

@bot.tree.command(name="customize", description="Personalize this Discord bot to cater to your needs!")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(bot_name="The new name for the bot (optional)",)
async def send_customize_request(interaction: discord.Interaction, bot_name: str = "Shitbot"):
    guild = interaction.guild
    try:
        if bot_name:
            if interaction.user.guild_permissions.administrator:
               await guild.me.edit(nick=bot_name)
               await interaction.response.send_message("Bot customization successful!")
            else:
                await interaction.response.send_message("You do not have permission to customize the bot.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to customize bot: {e}")

@bot.tree.command(name="help", description="List of commands and their usage.")
async def show_help(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot Commands", description="Here are all the available commands and their usage:", color=discord.Color.blurple())
    if interaction.user.guild_permissions.administrator:
        embed.add_field(name="/customize", value="Change the displayname of this bot.", inline=False)
    embed.add_field(name="/roast", value="Randomly roast a specified user.", inline=False)
    if interaction.user.guild_permissions.manage_messages:
        embed.add_field(name="/purge", value="Purge the channel.", inline=False)
    embed.add_field(name="/help", value="Show available commands and their usage.", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="roast", description="Roast someone.")
async def roast(interaction: discord.Interaction, person_to_roast: discord.Member):
    roasts = """{person_to_roast}, If I had a dollar for every brain cell you have, I'd have one dollar.
{person_to_roast}, Roses are red, violets are blue, I was looking for a joke, and then I found you.
{person_to_roast}, you're as useless as a screen door on a submarine.
Hey {person_to_roast}, I'm not saying you're ugly, but if you were a scarecrow, the birds would be laughing at you.
Roses are red, violets are blue, I'm sorry {person_to_roast}, but your IQ is lower than my shoe.
You should kill yourself {person_to_roast}
Hey {person_to_roast}, are you a magician? Because it seems like you made your dad disappear
{person_to_roast} If you were any more inbred, you'd be a sandwich.
{person_to_roast} You have the personality of a wet mop.
{person_to_roast} You're the reason why aliens won't talk to us.
{person_to_roast} Are you a parking ticket? Because you've got "fine" written all over you... and also, everyone hates you.
{person_to_roast} I'd call you a tool, but that implies you're useful in some way.
{person_to_roast} I'm jealous of all the people who haven't met you.
{person_to_roast} Roses are red, violets are blue, God made us beautiful, what happened to you?
{person_to_roast} You're the human equivalent of a participation trophy.
{person_to_roast} I bet your brain feels as good as new, seeing that you never use it.
{person_to_roast} If you were any more irrelevant, you'd be a white crayon.
{person_to_roast} I'd say you're dumb as a rock, but that would be an insult to rocks.
{person_to_roast} You're proof that evolution can go in reverse.
{person_to_roast} If ignorance is bliss, you must be the happiest person on Earth.
{person_to_roast} If stupidity was a crime, you'd be serving multiple life sentences.
{person_to_roast} I've met door knobs with more personality than you.
{person_to_roast} Did you fall from heaven? Because it looks like you landed on your face.
{person_to_roast} Even the Bermuda Triangle wouldn't swallow your ego.
{person_to_roast} I'd say you're a waste of oxygen, but I'm worried you'd take that as a compliment.
{person_to_roast} Is your personality a result of being dropped on your head as a child, or is it natural talent?
{person_to_roast} You're like a broken pencil - pointless.
{person_to_roast} Even an expired carton of milk has more potential than you.
{person_to_roast} Everyone who has ever loved you was wrong.
{person_to_roast} your mother's a whore.
{person_to_roast} your dad left you.
{person_to_roast} You are the best argument for post-term abortion.
{person_to_roast} I would explain it to you but I don't have the time or crayons.
{person_to_roast} Your birth certificate is an apology letter from the condom factory.
{person_to_roast} Everyone has the right to be stupid, but you're just abusing the privilege.
{person_to_roast} In any given situation, you are either correct or stupid. You are yet to be correct.
{person_to_roast} I'd call you a cunt, but you lack the warmth and depth.
{person_to_roast} Why don't you slip into something more comfortable, like a coma.
{person_to_roast} is a fucking pleb.
{person_to_roast} I'd call you an asshole but they serve a purpose.
{person_to_roast} I wish you were retarded. Then you'd have a valid excuse for your incompetence.
I may be drunk, {person_to_roast}, but in the morning I will be sober and you will still be ugly.
{person_to_roast} is a fuckstick"""
    await interaction.response.send_message(random.choice(roasts.split("\n")).format(person_to_roast=person_to_roast.mention))

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.tree.command(name="purge", description="Purges messages from the channel.")
@app_commands.default_permissions(manage_messages=True)
@app_commands.describe(limit="How many messages to purge, -1 for all")
async def say(interaction: discord.Interaction, limit: int):
    if interaction.user.guild_permissions.manage_messages:
        if limit > 0:
            await interaction.response.send_message(f"Purged {limit} messages!", ephemeral=True)
            await interaction.channel.purge(limit=limit)
        elif limit == -1:
            await interaction.response.send_message("Channel purged!", ephemeral=True)
            await interaction.channel.purge()
        else:
            await interaction.response.send_message("Invalid limit given!", ephemeral=True)
    else:
        await interaction.response.send_message("You are NOT allowed to do that!", ephemeral=True)

bot.run(TOKEN)