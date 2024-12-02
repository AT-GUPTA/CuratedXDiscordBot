import discord
from discord.ext import commands
import re
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configuration
USER_COUNT = int(os.getenv("USER_COUNT", 2))
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LINKS_ONLY_CHANNEL_ID = int(os.getenv("LINKS_ONLY_CHANNEL_ID", 0))
CURATED_CHANNEL_ID = int(os.getenv("CURATED_CHANNEL_ID", 0))
REACTION_EMOJI = os.getenv("REACTION_EMOJI", "👍")  # Configurable reaction emoji

# Regex for URL detection
URL_REGEX = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("CuratedXBot")

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Global state
link_reactions = {}

# Utility function: Extract and clean a link from a message
def extract_links(content):
    links = re.findall(URL_REGEX, content)
    return [link.strip() for link in links]

# Event: Bot is ready
@bot.event
async def on_ready():
    logger.info(f"Bot is online as {bot.user}")

# Event: Handle messages in the links-only channel
@bot.event
async def on_message(message):
    if message.channel.id == LINKS_ONLY_CHANNEL_ID and not message.author.bot:
        links = extract_links(message.content)
        if links:
            link_reactions[message.id] = set()
            await message.add_reaction(REACTION_EMOJI)
            logger.info(f"Detected link: {links[0]} from {message.author}")
        else:
            await message.delete()
            await message.channel.send("Only links are allowed in this channel!", delete_after=5)
            logger.warning(f"Deleted non-link message from {message.author}")

# Event: Handle reaction additions
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot or reaction.emoji != REACTION_EMOJI:
        return
    if reaction.message.id in link_reactions:
        link_reactions[reaction.message.id].add(user)
        if len(link_reactions[reaction.message.id]) >= USER_COUNT:
            curated_channel = bot.get_channel(CURATED_CHANNEL_ID)
            links = extract_links(reaction.message.content)
            if links:
                embed = discord.Embed(
                    title="New Curated Link",
                    description=f"[{links[0]}]({links[0]})",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Shared by {reaction.message.author.display_name}")
                await curated_channel.send(embed=embed)
                logger.info(f"Curated link: {links[0]} posted to #{curated_channel.name}")

# Event: Handle reaction removals
@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot or reaction.emoji != REACTION_EMOJI:
        return
    if reaction.message.id in link_reactions:
        link_reactions[reaction.message.id].discard(user)

# Command: Show bot stats
@bot.command(name="stats")
async def stats(ctx):
    await ctx.send(f"Currently tracking {len(link_reactions)} messages for reactions.")
    logger.info(f"Stats command executed by {ctx.author}")

# Command: Reset tracked messages
@bot.command(name="reset")
@commands.has_permissions(administrator=True)
async def reset(ctx):
    link_reactions.clear()
    await ctx.send("All tracked messages have been reset!")
    logger.info("Link reactions reset by an administrator.")

# Command: Update the required user count dynamically
@bot.command(name="set_user_count")
@commands.has_permissions(administrator=True)
async def set_user_count(ctx, count: int):
    global USER_COUNT
    USER_COUNT = count
    await ctx.send(f"User count updated to {USER_COUNT}.")
    logger.info(f"User count updated to {USER_COUNT} by {ctx.author}")

# Command: Update the reaction emoji dynamically
@bot.command(name="set_reaction")
@commands.has_permissions(administrator=True)
async def set_reaction(ctx, emoji: str):
    global REACTION_EMOJI
    REACTION_EMOJI = emoji
    await ctx.send(f"Reaction emoji updated to {REACTION_EMOJI}.")
    logger.info(f"Reaction emoji updated to {REACTION_EMOJI} by {ctx.author}")

# Command: Help
@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="CuratedX Bot Help",
        description="Manage and curate links with reactions!",
        color=discord.Color.green()
    )
    embed.add_field(name="!stats", value="Show the number of tracked messages.", inline=False)
    embed.add_field(name="!reset", value="Reset all tracked messages (Admin only).", inline=False)
    embed.add_field(name="!set_user_count <count>", value="Set the number of reactions required (Admin only).", inline=False)
    embed.add_field(name="!set_reaction <emoji>", value="Set the reaction emoji dynamically (Admin only).", inline=False)
    await ctx.send(embed=embed)

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command!")
        logger.warning(f"Unauthorized command attempt by {ctx.author}")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument for this command.")
    else:
        await ctx.send("An error occurred while processing the command.")
        logger.error(f"Unexpected error: {error}")

# Run the bot
bot.run(BOT_TOKEN)