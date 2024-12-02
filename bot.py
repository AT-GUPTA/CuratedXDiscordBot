import discord
from discord.ext import commands
import re
import os
from dotenv import load_dotenv

load_dotenv()

USER_COUNT = int(os.getenv("USER_COUNT", 2))
BOT_TOKEN = os.getenv("BOT_TOKEN","")
LINKS_ONLY_CHANNEL_ID = int(os.getenv("LINKS_ONLY_CHANNEL_ID",1312964005685362728))
CURATED_CHANNEL_ID = int(os.getenv("CURATED_CHANNEL_ID",1312965424446701628))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

link_reactions = {}
URL_REGEX = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.channel.id == LINKS_ONLY_CHANNEL_ID and not message.author.bot:
        links = re.findall(URL_REGEX, message.content)
        if links:
            link_reactions[message.id] = set()
            await message.add_reaction("👍")
        elif message.embeds:
            for embed in message.embeds:
                if embed.url and "http" in embed.url:
                    link_reactions[message.id] = set()
                    await message.add_reaction("👍")
                    break
        elif message.attachments:
            for attachment in message.attachments:
                if "http" in attachment.url:
                    link_reactions[message.id] = set()
                    await message.add_reaction("👍")
                    break
        else:
            await message.delete()
            await message.channel.send("Only links are allowed here!", delete_after=5)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message.id in link_reactions:
        link_reactions[reaction.message.id].add(user)
        if len(link_reactions[reaction.message.id]) == USER_COUNT:
            curated_channel = bot.get_channel(CURATED_CHANNEL_ID)
            original_message = reaction.message.content
            links = re.findall(URL_REGEX, original_message)
            if links:
                await curated_channel.send(f"Enjoy this hotness: {links[0]}")
            else:
                await curated_channel.send("No link was extracted!")

@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    if reaction.message.id in link_reactions:
        link_reactions[reaction.message.id].discard(user)

bot.run(BOT_TOKEN)