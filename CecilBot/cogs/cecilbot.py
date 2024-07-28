import discord
from discord.ext import commands
from discord import Client, app_commands
import re
from os import path
import pprint
from collections import Counter
from configparser import ConfigParser
from typing import List
from pathlib import Path
from CecilBot.utils import *
import logging


EXCELS = [x for x in Path("CecilBot", "cogs", "DataFiles").glob("*.xls*")]


class DiscordCecilBot(commands.Cog):
    def __init__(self, client):
        """
        The init function will always take a client, which represents the particular bot that is using the cog.
        """
        self.client = client
        self._last_member = None
        self.printer = pprint.PrettyPrinter(indent=2, width=105)
        self.logger = logging.getLogger(__name__)
        self.logger.info("CecilBot Cog instance created")
        self.data = build_mega_dict(EXCELS)

    @app_commands.describe(
        table="Any of Base, Boss, Code, Command, Item, R, Skill, SpecialEquipment, SpecialWeapons, StatusEffect, or Tool.",
        query="any word, like 'Ultros1', 'Bolt 3', etc.",
    )
    @app_commands.command()
    async def lookup(self, interaction: discord.Interaction, table: str, query: str):
        """
        Look up anything! Just use a slash command and then fill in the fields. They will autocomplete as you type!
        """

        if table not in self.data.keys():
            await interaction.response.send_message(
                f"{table} isn't one of the available tables to look things up in."
            )
            return

        elif query not in self.data[table]:
            await interaction.response.send_message(
                f"Sorry, could not find {query}. Try using the autocomplete feature. It might take a second or two to populate."
            )
            return

        else:
            await interaction.response.send_message(self.data[table][query])

    @lookup.autocomplete("table")
    async def query_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:

        return [
            app_commands.Choice(name=key, value=key)
            for key in self.data.keys()
            if current.lower() in key.lower()
        ]

    @lookup.autocomplete("query")
    async def query_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        ns = interaction.namespace
        return [
            app_commands.Choice(name=key, value=key)
            for key in self.data[ns.table].keys()
            if current.lower() in key.lower()
        ]

    @app_commands.command()
    async def beyondchaos(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "Originally developed by Abyssonym, but now maintained by SubtractionSoup, "
            "Beyond Chaos is a randomizer, a program that remixes game content randomly, "
            "for FF6. Every time you run Beyond Chaos, it will generate a completely unique, "
            "brand-new mod of FF6 for you to challenge and explore. There are over 10 billion "
            "different possible randomizations! Nearly everything is randomized, "
            "including treasure, enemies, colors, graphics, character abilities, and more."
        )
        return

    @app_commands.command()
    async def w(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "W-/?-/3x-[spellset] is just like r-[spellset] but "
            "gets cast more than once. NOTE: These spellsets that "
            "include Spiraler, Quadra Slam, and/or Quadra Slice will "
            "not cast those spells!"
        )
        return

    @app_commands.command()
    async def get_bc(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "Current CE version by DarkSlash: https://github.com/FF6BeyondChaos/BeyondChaosRandomizer/releases/latest"
        )
        return

    @app_commands.command()
    async def permadeath(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "Permadeath means starting a new randomized game upon game over"
        )
        return

    @app_commands.command()
    async def about(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "CecilBot is a program to help players by providing a list of skills and "
            "spells within each skill-set. CecilBot was made by GreenKnight5 and inspired by "
            "FF6Rando community member Cecil188, and uses databases authored by Cecil188. "
            "Please PM any questions, comments, concerns to @GreenKnight5,  @Cecil188, or @RazzleStorm."
        )
        return

    @app_commands.command()
    async def permadeath(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "Check out the Beyond Chaos Barracks - https://discord.gg/S3G3UXy"
        )
        return

    ### Start discord.py Bot functionality ###

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Any listeners you add will be effectively merged with the global listeners,
        which means you can have multiple cogs listening for the same events and
        taking actions based on those events.
        """
        print("CecilBot extension has been loaded")

    """
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        channels = ["ask-cecilbot"]
        if message.author == self.client.user:
            return
        if channel.name in channels:
            if message.content.startswith("!"):
                # await channel.send(message.content)
                # Pprint pretiffies everything, and then calls GK's command_lookup function
                to_send = self.command_lookup(message.author, message.content)
                if isinstance(to_send, dict):
                    pretty_message = self.printer.pformat(to_send)
                    if "response" in to_send:
                        pretty_message = to_send["response"]
                    await channel.send(pretty_message)
                else:
                    pretty_message = eval(self.printer.pformat(to_send))
                    await channel.send(pretty_message)
    """

    @commands.command()
    async def hello(
        self,
        ctx,
    ):
        """Says hello"""
        member = ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send("Hello {0.name}~".format(member))
        else:
            await ctx.send("Hello {0.name}... This feels familiar.".format(member))
        self._last_member = member

    """
    @commands.command(name='r-')
    async def _r(self, ctx, argument):
        print(argument)
        if '-' in argument:
            argument = argument[1:]
        await ctx.send(data.random_skillsets['r' + argument.lower()])
    """

    @app_commands.command()
    async def github(self, interaction: discord.Interaction) -> None:
        """Display link to the GitHub, so you can read or contribute to my code!"""
        embed = discord.Embed()
        embed.description = (
            "My code is available to peruse and contribute to on"
            " [GitHub](https://github.com/razzlestorm/BC_Discord_Bot). You"
            " can also visit my "
            "[Discussions Page]"
            "(https://github.com/razzlestorm/BC_Discord_Bot/issues)"
            " to make suggestions or flesh out ideas."
        )
        await interaction.response.send_message(embed=embed)


async def setup(client):
    """
    This setup function must exist in every cog file and will ultimately have a
    nearly identical signature and logic to what you're seeing here.
    It's ultimately what loads the Cog into the bot.
    """
    await client.add_cog(DiscordCecilBot(client))
