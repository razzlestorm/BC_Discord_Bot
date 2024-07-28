from pathlib import Path

import asyncio
import logging
from pathlib import Path
import sys
import time

import discord

from decouple import config
from discord.ext import commands

ROOT_DIR = Path(__file__).resolve(strict=True).parent

"""
client = commands.Bot(command_prefix=config("DISCORD_PREFIX"))

@client.event
async def on_ready():
    print("CecilBot is here to party!")


@client.command()
async def ping(ctx):
    await ctx.send("PONG")


# Register Cogs with bot
for cog in (ROOT_DIR / "cogs").glob("*.py"):
    print(f"Found cog: 'cog.{cog.name[:-3]}'")
    # If run as a Python module with -m, this path will need to be changed to "CecilBot/cogs."
    client.load_extension(f"cogs.{cog.name[:-3]}")


client.run(config("DISCORD_BOT_KEY"))

"""


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = config("DISCORD_PREFIX"), intents = discord.Intents.default())

    async def on_ready(self):
        print(f"CecilBot is here to party!")

bot = Bot()

async def load_cogs(b):
    init = ROOT_DIR/"cogs"/"__init__.py"
    cogs = [cog for cog in (ROOT_DIR / "cogs").glob("*.py") if cog != init]
    for cog in cogs:
        print(f"Found cog: 'cog.{cog.name[:-3]}'")
        await b.load_extension(f"CecilBot.cogs.{cog.name[:-3]}")

@bot.event
async def on_ready():
    # Register Cogs with bot
    commands = await bot.tree.sync()
    # bot.tree.clear_commands(guild=discord.Object(id="740310401001980036"))
    print(f"CecilBot synced these commands: {commands}")
    print("CecilBot is finished loading!")

async def main():
    async with bot:
        await load_cogs(bot)
        await bot.start(config("DISCORD_BOT_KEY"))

asyncio.run(main())

# bot.run(config("DISCORD_BOT_KEY"))
