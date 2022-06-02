from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import sqlalchemy as sa
import os


user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
address = os.environ['DB_ADDRESS']
database = os.environ['DB_NAME']

engine = create_engine(
    f'postgresql://{user}:{password}@{address}/{database}', echo=False)

meta = MetaData()

netflix = Table(
    'netflix', meta,
    Column('show_id', String),
    Column('type', String),
    Column('title', String),
    Column('director', String),
    Column('cast', String),
    Column('country', String),
    Column('date_added', String),
    Column('release_year', String),
    Column('rating', String),
    Column('duration', String),
    Column('listed_in', String),
    Column('description', String)
)

# print(netflix.c['show_id'])
meta.create_all(engine)

# meta.drop_all(engine)

# insp = sa.inspect(engine)
# db_list = insp.get_table_names()
# print(db_list)

# connection = engine.connect()
# connection.execute("DROP TABLE some_table, netflix, netflix2;")

# conn = engine.connect()
# conn.execute("CREATE TABLE some_table (x int, y int)")

insp = sa.inspect(engine)
db_list = insp.get_schema_names()
print(db_list)

insp = sa.inspect(engine)
db_list = insp.get_table_names()
print(db_list)
