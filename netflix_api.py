from datetime import date
import this
from venv import create
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import and_, delete, update, insert, func
from sqlalchemy import asc
from sqlalchemy import desc
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os

# Initialize Objects and load .env
app = FastAPI()
meta = MetaData()
load_dotenv()

# Grab environment variables from .env
db_user = os.environ['DB_USERNAME']
db_pass = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_address = os.environ['DB_ADDRESS']
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

# Connect to Cloud SQL with environment variables
if os.environ['WHERE_AM_I'] == 'localhost':
    engine = create_engine(
        f'postgresql://{db_user}:{db_pass}@{db_address}/{db_name}', echo=False)
else:
    # on Cloud Run
    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{instance_connection_name}")

# Define and Describe Netflix table
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

# meta.create_all(engine)
# meta.drop_all(engine)
# session = Session(engine, future=True)

# Index page
@app.get("/")
async def root():
    return {"msg": "Hello! Please refer to /docs page for documentations!"}


# Dynamic search, use multiple or none filters
@app.get("/search")
async def search_optional(request: Request, show_id=None, type=None, title=None, director=None, cast=None, country=None,
                          date_added=None, release_year=None, rating=None, duration=None, listed_in=None, description=None,
                          sort_by=None, sort_order=None, page=1):

    # Table Headers
    header = netflix.columns

    # Select all from table
    query = sa.select(netflix)

    # Filtering
    if show_id:
        query = query.where(header['show_id'] == show_id)
    if type:
        query = query.where(header['type'] == type)
    if title:
        query = query.where(header['title'] == title)
    if director:
        query = query.where(header['director'] == director)
    if cast:
        query = query.where(header['cast'] == cast)
    if country:
        query = query.where(header['country'] == country)
    if date_added:
        query = query.where(header['date_added'] == date_added)
    if release_year:
        query = query.where(header['release_year'] == release_year)
    if rating:
        query = query.where(header['rating'] == rating)
    if duration:
        query = query.where(header['duration'] == duration)
    if listed_in:
        query = query.where(header['listed_in'] == listed_in)
    if description:
        query = query.where(header['description'] == description)

    # Sorting
    if sort_by:
        if sort_order == 'asc':
            query = query.order_by(asc(header[sort_by]))
        elif sort_order == 'desc':
            query = query.order_by(desc(header[sort_by]))

    # Limit/Offsetting
    page = int(page)
    query = query.limit(5).offset((page-1)*5)

    # Executing Database Query
    connection = engine.connect()
    result = connection.execute(query)
    data = result.fetchall()

    # JSON Pagination's next page
    if len(data) == 5:
        page += 1
        current_url = request.url._url
        if "?" in current_url:
            next_url = current_url + f"&page={page}"
        else:
            next_url = current_url + f"?page={page}"

        data.append({"next": next_url})

    # Response
    return data

# post for create/insert
@app.get("/create/{show_id}")
async def creating(show_id, title=None, type=None, director=None, cast=None, country=None,
                   date_added=None, release_year=None, rating=None, duration=None, listed_in=None, description=None):
    query = netflix.insert().values(show_id=show_id)
    print(query)
    connection = engine.connect()
    connection.execute(query)
    return {"created": show_id}

# put for updating
@app.get("/update/{show_id}")
async def updating(show_id, type=None, title=None, director=None, cast=None, country=None,
                   date_added=None, release_year=None, rating=None, duration=None, listed_in=None, description=None):
    query = netflix.update().where(netflix.columns['show_id'] == show_id)
    if title:
        query = query.values(title=title)
    if director:
        query = query.values(director=director)
    print(query)
    connection = engine.connect()
    connection.execute(query)
    return {"updated": show_id}

# delete
@app.get("/delete")
async def deleting(show_id=None, type=None, title=None, director=None, cast=None, country=None,
                   date_added=None, release_year=None, rating=None, duration=None, listed_in=None, description=None):
    query = netflix.delete().where(netflix.columns['show_id'] == show_id)
    print(query)
    connection = engine.connect()
    connection.execute(query)
    return {"deleted": show_id}


# if __name__ == "__main__":
#     uvicorn.run("cloud:app", host="0.0.0.0", port=int(
#         os.environ.get("PORT", 8080)), log_level="info")
