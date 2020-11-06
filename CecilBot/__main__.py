from pathlib import Path

from decouple import config
from discord.ext import commands

ROOT_DIR = Path(__file__).resolve(strict=True).parent

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
    client.load_extension(f"cogs.{cog.name[:-3]}")


client.run(config("DISCORD_BOT_KEY"))
