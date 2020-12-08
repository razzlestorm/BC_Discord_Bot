from sqlalchemy import Column, Table, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index, Metadata

metadata = MetaData()

boss_moves = Table('BossMoves', metadata,
    Column('boss_id', Integer, primary_key=True),
    Column('boss_name', String(32), nullable=False),
    Column('level', Integer),
    Column('hp', Integer),
    Column('mp', Integer),
    Column('skills', String(255)),
    Column('statuses', String(255)),
    Column('absorbs', String(255)),
    Column('nullifies', String(255)),
    Column('weaknesses', String(255)),
)

codes = Table('Codes', metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String(255), nullable=False),
    Column('effect', String(255)),
)

items = Table('Items', metadata,
    Column('id', Integer, primary_key=True),
    Column('item', String(255), nullable=False),
    Column('effect', String(255)),
)

skillsets = Table('Skillsets', metadata,
    Column('id', Integer, primary_key=True),
    Column('skillset', String(255), nullable=False),
    Column('spellist', String(2400)),
    Column('danger_odds', String(255)),
)

root_table = Table('RootTable', metadata,
    Column('id', Integer, primary_key=True),
    Column('root', String(255), nullable=False),
    Column('effect', String(255)),
)

special_equipment = Table('SpecialEquipment', metadata
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('type', String(255)),
    Column('def', Integer),
    Column('mdef', Integer),
    Column('stats', String(255)),
    Column('evade', Integer),
    Column('mevade', Integer),
    Column('element_null', String(255)),
    Column('element_absorb', String(255)),
    Column('element_weak', String(255)),
    Column('breaks', String(255)),
    Column('learn', String(255)),
    Column('equip', String(255)),
    Column('statuses', String(255)),
    Column('immunities', String(255)),
    Column('specials', String(255))
)

special_weapons = Table('SpecialWeapons', metadata
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('power', Integer),
    Column('stats', String(255)),
    Column('evade', Integer),
    Column('mevade', Integer),
    Column('elements', String(255)),
    Column('breaks', String(255)),
    Column('learn', String(255)),
    Column('procs', String(255)),
    Column('hitrate', Integer)
    Column('equip', String(255)),
    Column('statuses', String(255)),
    Column('immunities', String(255)),
    Column('specials', String(255))
)

status_effects = Table('StatusEffects', metadata,
    Column('id', Integer, primary_key=True),
    Column('status_name', String(32), nullable=False),
    Column('buff_ailment', String(255)),
    Column('appearance', String(255)),
    Column('duration', String(255)),
    Column('description', String(255)),
    Column('inflicted_by', String(255)),
    Column('healed_by', String(255)),
    Column('prevented_by', String(255)),
)

tools = Table('Tools', metadata,
    Column('id', Integer, primary_key=True),
    Column('tool_name', String(32), nullable=False),
    Column('power', Integer),
    Column('elements', String(255)),
    Column('statuses', String(255)),
    Column('physical', String(32)),
    Column('ignores_defense', String(32)),
    Column('instant_death', String(32)),
    Column('special_effects', String(255)),
)
