from discord.ext import commands
from discord import Client
import re
from os import path
import xlrd
import pprint

# Open specified excel file and read data from file.
# Warning: when files are updated and their names get changed, you
#   must update the hard coded file name in DataBuilder.py
def dict_builder(path=""):
    location = path
    book = xlrd.open_workbook(location)
    sheet = book.sheet_by_index(0)
    sheet.cell_value(0, 0)
    data_dictionary = dict()

    for rownum in range(1, sheet.nrows):
        tempdict = dict()
        for cn, values in zip(sheet.row_values(0, 0), sheet.row_values(rownum, 0)):
            if (values != ""):
                tempdict[cn] = values
        if (re.match(r".*Root Table.*", location, re.IGNORECASE)):
            data_dictionary[str(sheet.cell_value(rownum, 0))] = tempdict
        else:
            data_dictionary[str(sheet.cell_value(rownum, 0)).lower()] = tempdict

    return data_dictionary


try:
    from sys import _MEIPASS
    MEI = True
    tblpath = path.join(_MEIPASS, "DataFiles")
except ImportError:
    # this prepends the absolute file path of the calling script
    #   to the virtual path passed as a param - GreenKnight5
    bundle_dir = path.dirname(path.abspath(__file__))
    tblpath = path.join(bundle_dir, "DataFiles")

    MEI = False

# Probably not needed
def open_mei_fallback(filename, mode='r'):
    # this prepends the absolute file path of the calling script
    #   to the file passed as a param - GreenKnight5
    filename = path.join(path.dirname(path.abspath(__file__)), filename)

    if not MEI:
        return open(filename, mode)

    try:
        f = open(filename, mode)
    except IOError:
        f = open(path.join(_MEIPASS, filename), mode)
    return f

print(tblpath)
# Make RE read/do this in the future for any version
BOSS_MOVES_TABLE = path.join(tblpath, "Boss Moves v7.xls")
CODES_TABLE = path.join(tblpath, "Codes_v6.xls")
ITEM_TABLE = path.join(tblpath, "Item Table v2.xls")
RANDOM_SKILLSETS_TABLE = path.join(tblpath, "Random Skillsets v2.xls")
ROOT_TABLE = path.join(tblpath, "Root Table v4.xls")
SKILL_PARAMETERS_TABLE = path.join(tblpath, "Skill Parameters v3.xls")
SPECIAL_EQUIPMENT_TABLE = path.join(tblpath, "Special Equipment v3.xls")
SPECIAL_WEAPONS_TABLE = path.join(tblpath, "Special Weapons v4.xls")
STATUS_EFFECTS_TABLE = path.join(tblpath, "Status Effects v3.xls")
COMMANDS_TABLE = path.join(tblpath, "Commands v1.xls")



class Data:
    def __init__(self):
        self.boss_moves = dict_builder(BOSS_MOVES_TABLE)
        self.codes = dict_builder(CODES_TABLE)
        self.item_table = dict_builder(ITEM_TABLE)
        self.random_skillsets = dict_builder(RANDOM_SKILLSETS_TABLE)
        self.root_table = dict_builder(ROOT_TABLE)
        self.skill_parameters = dict_builder(SKILL_PARAMETERS_TABLE)
        self.special_equipment = dict_builder(SPECIAL_EQUIPMENT_TABLE)
        self.special_weapons = dict_builder(SPECIAL_WEAPONS_TABLE)
        self.status_effects = dict_builder(STATUS_EFFECTS_TABLE)
        self.commands = dict_builder(COMMANDS_TABLE)

data = Data()

class DiscordCecilBot(commands.Cog):
    def __init__(self, client):
        """
        The init function will always take a client, which represents the particular bot that is using the cog.
        """
        self.client = client
        self._last_member = None
        self.printer = pprint.PrettyPrinter(indent=4)


    def command_lookup(self, author, message):
	    #Data lookup patterns
	    rchaospattern = r"\A!r-?chaos"
	    rcommandpattern = r"\A!r-?\w*"
	    wcommandpattern = r"\A![w|?|3x]-\w*"
	    skillpattern = r"\A!skill\s.*"
	    bosspattern = r"\A!boss\s.*"
	    codepattern = r"\A!code[s]?\s\w*"
	    itempattern = r"\A!item\s.*"
	    specialequipmentpattern = r"\A!specialequipment\s.*"
	    specialweaponpattern = r"\A!specialweapon\s.*"
	    statuseffectpattern = r"\A!statuseffect\s\.*"
	    rootpattern = r"\A!base\s.*"
	    communitycommandpattern = r"\A!.*"

	    #General command patterns
	    hellopattern = r"\A!hello"
	    commandspattern = r"\A!command[s]?"
	    beyondchaospattern = "\A!beyondchaos"
	    discordpattern = r"\A!discord"
	    getbcpattern = r"\A!getbc"
	    permadeath = r"\A!permadeath"
	    aboutpattern = r"\A!about"


	    if re.search(rchaospattern, message, re.IGNORECASE):
	        return "It's literally every spell/skill in the game in one spellset. Threat:(8/255)"

	    elif re.search(rcommandpattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!", "", message).lower()
	            anothertemp = re.sub("r-", "r", temp).lower()
	            return (data.random_skillsets[anothertemp])
	        except:
	            #in case someone enteres a community command that starts with "r"
	            try:
	                temp = re.sub("!", "", message).lower()
	                return (data.commands[temp])
	            except:
	                return "Null"

	    elif re.search(wcommandpattern, message, re.IGNORECASE):
	        return "W-/?-/3x-[spellset] is just like r-[spellset] but " \
	               "gets cast more than once. NOTE: These spellsets that " \
	               "include Spiraler, Quadra Slam, and/or Quadra Slice will " \
	               "not cast those spells!"

	    elif re.search(skillpattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!skill ", "", message).lower()
	            return (data.skill_parameters[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif re.search(bosspattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!boss ", "", message).lower()
	            return (data.boss_moves[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif re.search(codepattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!code ", "", message).lower()
	            return (data.codes[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif re.search(itempattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!item ", "", message).lower()
	            return (data.item_table[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif re.search(specialequipmentpattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!specialequipment ", "", message).lower()
	            return (data.special_equipment[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif re.search(specialweaponpattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!specialweapon ", "", message).lower()
	            return (data.special_weapons[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif re.search(statuseffectpattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!statuseffect ", "", message).lower()
	            return (data.status_effects[temp])
	        except:
	            pass
	    elif re.search(rootpattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!base ", "", message)
	            return (data.root_table[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again. REMEBER: capitalization matters!")


	    elif re.search(hellopattern, message, re.IGNORECASE):
	        return f"Hello {author}!"
	    elif re.search(commandspattern, message, re.IGNORECASE):
	        return "Basic commands: !hello, !about, !getBC, !discord, !beyondchaos, !permadeath " \
	               "<!R[spell] commands: ex.'!RTime'> " \
	               "<!Skill [SkillName] commands: ex.'!skill fire 3'> " \
	               "<!Boss [BossName] commands: ex. '!boss Kefka3'> " \
	               "<!Code [CodeName] commands: ex. '!code capslockoff'> " \
	               "<!Item [ItemName] commands: ex. '!item potion'> " \
	               "<!StatusEffect [EffectName] commands: ex: '!statuseffect poison'> " \
	               "<!Base [SkillBase] commands: ex. '!base Fir'> " \
	               "<!SpecialEquipment [EquipName] commands: ex. '!specialequipment red duster'> " \
	               "<!SpecialWeapons [WeaponName] commands: ex. '!specialweapon portal gun'>"
	    elif re.search(beyondchaospattern, message, re.IGNORECASE):
	        return "Originally developed by Abyssonym, but now maintained by SubtractionSoup, " \
	               "Beyond Chaos is a randomizer, a program that remixes game content randomly, " \
	               "for FF6. Every time you run Beyond Chaos, it will generate a completely unique, " \
	               "brand-new mod of FF6 for you to challenge and explore. There are over 10 billion " \
	               "different possible randomizations! Nearly everything is randomized, " \
	               "including treasure, enemies, colors, graphics, character abilities, and more."
	    elif re.search(getbcpattern, message, re.IGNORECASE):
	        return "Current EX version by SubtractionSoup: https://github.com/subtractionsoup/beyondchaos/releases/latest"
	    elif re.search(discordpattern, message, re.IGNORECASE):
	        return "Check out the Beyond Chaos Barracks - https://discord.gg/S3G3UXy"
	    elif re.search(permadeath, message, re.IGNORECASE):
	        return "Permadeath means starting a new randomized game upon game over"
	    elif re.search(aboutpattern, message, re.IGNORECASE):
	        return "CecilBot is a program to help players by providing a list of skills and " \
	               "spells within each skill-set. CecilBot was made by GreenKnight5 and inspired by " \
	               "FF6Rando community member Cecil188, and uses databases authored by Cecil188. " \
	               "Please PM any questions, comments, concerns to @GreenKnight5 or @Cecil188."
	    elif re.search(communitycommandpattern, message, re.IGNORECASE):
	        try:
	            temp = re.sub("!", "", message).lower()
	            return (data.commands[temp])
	        except:
	            return "Null"
	    else:
	        return "Null"


    @commands.Cog.listener()
    async def on_ready(self):
        """
        Any listeners you add will be effectively merged with the global listeners,
        which means you can have multiple cogs listening for the same events and
        taking actions based on those events.
        """
        print("CecilBot extension has been loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        channels = ["ask-cecilbot"]
        if message.author == self.client.user:
            return
        if channel.name in channels:
            if message.content.startswith('!'):
                # await channel.send(message.content)
                # Pprint pretiffies everything, and then calls GK's command_lookup function
                to_send = self.command_lookup(message.author, message.content)
                pretty_message = self.printer.pformat(to_send)
                await channel.send(pretty_message)

    @commands.command()
    async def hello(self, ctx,):
        """Says hello"""
        member = ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
            await ctx.send(ctx.message)
            await ctx.send(ctx.message.content)
            print(type(ctx.message.content))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member
    '''
    @commands.command(name='r-')
    async def _r(self, ctx, argument):
        print(argument)
        if '-' in argument:
            argument = argument[1:]
        await ctx.send(data.random_skillsets['r' + argument.lower()])
    '''

def setup(client):
    """
    This setup function must exist in every cog file and will ultimately have a
    nearly identical signature and logic to what you're seeing here.
    It's ultimately what loads the Cog into the bot.
    """
    client.add_cog(DiscordCecilBot(client))
