import pandas as pd
from schema_models import *
from sqlalchemy import create_engine
engine = create_engine('sqlite:///BCfiles.db')

boss_moves = pd.read_excel("Boss Moves v7.1.xls")

# boss_moves.to_sql('boss_moves', con=engine, if_exists='replace')

show_all = engine.execute("SELECT * FROM boss_moves").fetchall()
print(show_all)
