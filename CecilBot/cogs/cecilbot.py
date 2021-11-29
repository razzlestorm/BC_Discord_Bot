from discord.ext import commands
from discord import Client
import re
from os import path
import xlrd
import pprint
from configparser import ConfigParser

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
# Potentially create a database for this
BOSS_DISAMBIGUATIONS = path.join(tblpath, "Boss Disambiguations v1.xls")
BOSS_MOVES_TABLE = path.join(tblpath, "Boss Moves v7.2.xls")
CODES_TABLE = path.join(tblpath, "Codes v5.2.xls")
ITEM_TABLE = path.join(tblpath, "Item Table v2.xls")
RANDOM_SKILLSETS_TABLE = path.join(tblpath, "Random Skillsets v2.1.xls")
ROOT_TABLE = path.join(tblpath, "Root Table v4.xls")
SKILL_PARAMETERS_TABLE = path.join(tblpath, "Skill_Parameters_v3.3.xls")
SPECIAL_EQUIPMENT_TABLE = path.join(tblpath, "Special Equipment v3.xls")
SPECIAL_WEAPONS_TABLE = path.join(tblpath, "Special Weapons v4.xls")
STATUS_EFFECTS_TABLE = path.join(tblpath, "Status Effects v3.xls")
COMMANDS_TABLE = path.join(tblpath, "Commands v1.xls")
TOOLS_TABLE = path.join(tblpath, "Tools List v1.xls")


# Create a class to pull from DB
class Data:
    def __init__(self):
        self.boss_moves = dict_builder(BOSS_MOVES_TABLE)
        # Updates the boss_moves table with boss_disambiguations instead of
        # individually handling it in the command logic
        self.boss_moves.update(dict_builder(BOSS_DISAMBIGUATIONS))
        self.codes = dict_builder(CODES_TABLE)
        self.item_table = dict_builder(ITEM_TABLE)
        self.random_skillsets = dict_builder(RANDOM_SKILLSETS_TABLE)
        self.root_table = dict_builder(ROOT_TABLE)
        self.skill_parameters = dict_builder(SKILL_PARAMETERS_TABLE)
        self.special_equipment = dict_builder(SPECIAL_EQUIPMENT_TABLE)
        self.special_weapons = dict_builder(SPECIAL_WEAPONS_TABLE)
        self.status_effects = dict_builder(STATUS_EFFECTS_TABLE)
        self.commands = dict_builder(COMMANDS_TABLE)
        self.tools = dict_builder(TOOLS_TABLE)

class Entry:
    def __init__(self, entry, desc):
        self.entry = entry
        self.desc = desc

class Boss:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.level = kwargs.get('level')
        self.HP = kwargs.get('HP')
        self.MP = kwargs.get('MP')
        self.skills = kwargs.get('skills')
        self.statuses = kwargs.get('statuses')
        self.absorbs = kwargs.get('absorbs')
        self.nullifies = kwargs.get('nullifies')
        self.weaknesses = kwargs.get('weaknesses')

class Random:
    def __init__(self, entry, spell_list, danger):
        self.entry = entry
        self.spell_list = spell_list
        self.danger = danger

class Skill:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.MP_cost = kwargs.get('MP_cost')
        self.power = kwargs.get('power')
        self.acc = kwargs.get('acc')
        self.elements = kwargs.get('elements')
        self.statuses = kwargs.get('statuses')
        self.healing = kwargs.get('healing')
        self.runic = kwargs.get('runic')
        self.split = kwargs.get('split')
        self.reflects = kwargs.get('reflects')
        self.phys = kwargs.get('phys')
        self.ignores_def = kwargs.get('ignores_def')
        self.unblockable = kwargs.get('unblockable')
        self.instant_death = kwargs.get('instant_death')
        self.special_effects = kwargs.get('special_effects')

class SWeapon:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.power = kwargs.get('power')
        self.stats = kwargs.get('stats')
        self.evade = kwargs.get('evade')
        self.MEvade = kwargs.get('MEvade')
        self.elements = kwargs.get('elements')
        self.learn = kwargs.get('learn')
        self.break_for = kwargs.get('break_for')
        self.proc = kwargs.get('proc')
        self.hit_rate = kwargs.get('hit_rate')
        self.equip = kwargs.get('equip')
        self.statuses = kwargs.get('statuses')
        self.immunities = kwargs.get('immunities')
        self.specials = kwargs.get('specials')

class SEquipment:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.defense = kwargs.get('defense')
        self.MDef = kwargs.get('MDef')
        self.stats = kwargs.get('stats')
        self.evade = kwargs.get('evade')
        self.MEvade = kwargs.get('MEvade')
        self.elenull = kwargs.get('elenull')
        self.elehalve = kwargs.get('elehalve')
        self.eleabsorb = kwargs.get('eleabsorb')
        self.eleweak = kwargs.get('eleweak')
        self.break_for = kwargs.get('break_for')
        self.learn = kwargs.get('learn')
        self.equip = kwargs.get('equip')
        self.statuses = kwargs.get('statuses')
        self.immunities = kwargs.get('immunities')
        self.specials = kwargs.get('specials')

class Status:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.appearance = kwargs.get('appearance')
        self.duration = kwargs.get('duration')
        self.desc = kwargs.get('desc')
        self.source = kwargs.get('source')
        self.healedby = kwargs.get('healedby')
        self.prevent = kwargs.get('prevent')

class Tool:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.power = kwargs.get('power')
        self.element = kwargs.get('element')
        self.status = kwargs.get('status')
        self.phys = kwargs.get('phys')
        self.ignores_def = kwargs.get('ignores_def')
        self.instant_death = kwargs.get('instant_death')
        self.special_effects = kwargs.get('special_effects')



data = Data()

class DiscordCecilBot(commands.Cog):
    def __init__(self, client):
        """
        The init function will always take a client, which represents the particular bot that is using the cog.
        """
        self.client = client
        self._last_member = None
        self.printer = pprint.PrettyPrinter(indent=2, width=105)

    def command_lookup(self, author, message):
	    #Data lookup patterns
	    rchaospattern = re.compile(r"\A!r-?chaos", re.IGNORECASE)
	    rcommandpattern = re.compile(r"\A!r-?\w*", re.IGNORECASE)
	    wcommandpattern = re.compile(r"\A![w|?|3x]-?\w*", re.IGNORECASE)
	    skillpattern = re.compile(r"\A!skill\s.*", re.IGNORECASE)
	    bosspattern = re.compile(r"\A!boss\s.*", re.IGNORECASE)
	    codepattern = re.compile(r"\A!code[s]?\s\w*", re.IGNORECASE)
	    itempattern = re.compile(r"\A!item\s.*", re.IGNORECASE)
	    toolpattern = re.compile(r"\A!tool\s.*", re.IGNORECASE)
	    specialequipmentpattern = re.compile(r"\A!specialequipment\s.*", re.IGNORECASE)
	    specialweaponpattern = re.compile(r"\A!specialweapon\s.*", re.IGNORECASE)
	    statuseffectpattern = re.compile(r"\A!statuseffect\s\.*", re.IGNORECASE)
	    rootpattern = re.compile(r"\A!base\s.*", re.IGNORECASE)

	    #General command patterns
	    hellopattern = re.compile(r"\A!hello", re.IGNORECASE)
	    commandspattern = re.compile(r"\A!command[s]?", re.IGNORECASE)
	    beyondchaospattern = re.compile("\A!beyondchaos", re.IGNORECASE)
	    getbcpattern = re.compile(r"\A!getbc", re.IGNORECASE)
	    discordpattern = re.compile(r"\A!(bcdiscord|bc|discord)", re.IGNORECASE)
	    permadeath = re.compile(r"\A!permadeath", re.IGNORECASE)
	    aboutpattern = re.compile(r"\A!about", re.IGNORECASE)
	    helppattern = re.compile(r"\A!help", re.IGNORECASE)
	    communitycommandpattern = re.compile(r"\A!.*", re.IGNORECASE)


	    if rchaospattern.search(message):
	        return "It's literally every spell/skill in the game in one spellset. Threat:(8/255)"

	    elif rcommandpattern.search(message):
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

	    elif wcommandpattern.search(message):
	        return "W-/?-/3x-[spellset] is just like r-[spellset] but " \
	               "gets cast more than once. NOTE: These spellsets that " \
	               "include Spiraler, Quadra Slam, and/or Quadra Slice will " \
	               "not cast those spells!"

	    elif skillpattern.search(message):
	        try:
	            temp = re.sub("!skill ", "", message, flags=re.IGNORECASE).lower()
	            return (data.skill_parameters[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif bosspattern.search(message):
	        try:
	            temp = re.sub("!boss ", "", message, flags=re.IGNORECASE).lower()
	            return (data.boss_moves[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif codepattern.search(message):
	        try:
	            temp = re.sub("!code ", "", message, flags=re.IGNORECASE).lower()
	            return (data.codes[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif itempattern.search(message):
	        try:
	            temp = re.sub("!item ", "", message, flags=re.IGNORECASE).lower()
	            return (data.item_table[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif toolpattern.search(message):
	        try:
	            temp = re.sub("!tool ", "", message, flags=re.IGNORECASE).lower()
	            return (data.tools[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif specialequipmentpattern.search(message):
	        try:
	            temp = re.sub("!specialequipment ", "", message, flags=re.IGNORECASE).lower()
	            return (data.special_equipment[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif specialweaponpattern.search(message):
	        try:
	            temp = re.sub("!specialweapon ", "", message, flags=re.IGNORECASE).lower()
	            return (data.special_weapons[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again.")
	    elif statuseffectpattern.search(message):
	        try:
	            temp = re.sub("!statuseffect ", "", message, flags=re.IGNORECASE).lower()
	            return (data.status_effects[temp])
	        except:
	            pass
	    elif rootpattern.search(message):
	        try:
	            temp = re.sub("!base ", "", message, flags=re.IGNORECASE)
	            return (data.root_table[temp])
	        except:
	            return (f"Sorry, could not find {temp}. Please check your spelling "
	                  f"and try again. REMEMBER: Bases are only up to "
                      f"four letters long, and capitalization matters!")


	    elif hellopattern.search(message):
	        return f"Hello {author}!"
	    elif commandspattern.search(message):
	        return "Basic commands: !hello, !about, !getBC, !discord, !beyondchaos, !permadeath \n" \
	               "<!R[spell] commands: ex.'!RTime'> \n" \
	               "<!Skill [SkillName] commands: ex.'!skill fire 3'> \n" \
	               "<!Boss [BossName] commands: ex. '!boss Kefka3'> \n" \
	               "<!Code [CodeName] commands: ex. '!code capslockoff'> \n" \
	               "<!Item [ItemName] commands: ex. '!item potion'> \n" \
	               "<!StatusEffect [EffectName] commands: ex: '!statuseffect poison'> \n" \
	               "<!Base [SkillBase] commands: ex. '!base Fir'> \n" \
	               "<!SpecialEquipment [EquipName] commands: ex. '!specialequipment red duster'> \n" \
	               "<!SpecialWeapons [WeaponName] commands: ex. '!specialweapon portal gun'> \n"
	    elif beyondchaospattern.search(message):
	        return "Originally developed by Abyssonym, but now maintained by SubtractionSoup, " \
	               "Beyond Chaos is a randomizer, a program that remixes game content randomly, " \
	               "for FF6. Every time you run Beyond Chaos, it will generate a completely unique, " \
	               "brand-new mod of FF6 for you to challenge and explore. There are over 10 billion " \
	               "different possible randomizations! Nearly everything is randomized, " \
	               "including treasure, enemies, colors, graphics, character abilities, and more."
	    elif getbcpattern.search(message):
	        return "Current CE version by DarkSlash: https://github.com/FF6BeyondChaos/BeyondChaosRandomizer/releases/latest"
	    elif discordpattern.search(message):
	        return "Check out the Beyond Chaos Barracks - https://discord.gg/S3G3UXy"
	    elif permadeath.search(message):
	        return "Permadeath means starting a new randomized game upon game over"
	    elif aboutpattern.search(message):
	        return "CecilBot is a program to help players by providing a list of skills and " \
	               "spells within each skill-set. CecilBot was made by GreenKnight5 and inspired by " \
	               "FF6Rando community member Cecil188, and uses databases authored by Cecil188. " \
	               "Please PM any questions, comments, concerns to @GreenKnight5,  @Cecil188, or @RazzleStorm."
	    elif helppattern.search(message):
	        text = "The Discord Cecilbot should function almost exactly " \
	        "like your familiar Twitch Cecilbot. Type !commands to see " \
	        "the most common commands and their syntax. Check the pins in " \
	        "this channel for a more detailed explanation."
	        return text
	    elif communitycommandpattern.search(message):
	        try:
	            temp = re.sub("!", "", message).lower()
	            return (data.commands[temp])
	        except:
	            return "That command didn't work, check your spelling and try again!"
	    else:
	        return "That command didn't work, check your spelling and try again!"

### Start discord.py Bot functionality ###

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
                if isinstance(to_send, dict):
                    pretty_message = self.printer.pformat(to_send)
                    if "response" in to_send:
                        pretty_message = to_send["response"]
                    await channel.send(pretty_message)
                else:
                    pretty_message = eval(self.printer.pformat(to_send))
                    await channel.send(pretty_message)

    @commands.command()
    async def add(self, ctx, *args):
        '''
        Parameters
        -----------
        args : These args are expected in the following order:
            [Command (e.g. Skill, Boss, Item, etc.)][EntryName][Entry]
        Possible tables to add an entry to are:
        BOSS_MOVES_TABLE
        CODES_TABLE
        ITEM_TABLE
        RANDOM_SKILLSETS_TABLE
        ROOT_TABLE
        SKILL_PARAMETERS_TABLE
        SPECIAL_EQUIPMENT_TABLE
        SPECIAL_WEAPONS_TABLE
        STATUS_EFFECTS_TABLE
        COMMANDS_TABLE
       "<!R[spell] commands: ex.'!RTime'> \n" \
       "<!Skill [SkillName] commands: ex.'!skill fire 3'> \n" \
       "<!Boss [BossName] commands: ex. '!boss Kefka3'> \n" \
       "<!Code [CodeName] commands: ex. '!code capslockoff'> \n" \
       "<!Item [ItemName] commands: ex. '!item potion'> \n" \
       "<!StatusEffect [EffectName] commands: ex: '!statuseffect poison'> \n" \
       "<!Base [SkillBase] commands: ex. '!base Fir'> \n" \
       "<!SpecialEquipment [EquipName] commands: ex. '!specialequipment red duster'> \n" \
       "<!SpecialWeapons [WeaponName] commands: ex. '!specialweapon portal gun'>

        '''
        member = ctx.author
        print(member.roles)
        print(args)



    @commands.command()
    async def hello(self, ctx,):
        """Says hello"""
        member = ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
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
