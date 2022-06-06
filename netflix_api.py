# SQLalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import sqlalchemy as sa
from sqlalchemy import asc, desc, func
from sqlalchemy.sql import func
# Environment variable
from dotenv import load_dotenv
import os
# Fastapi & Security
import secrets
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials



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
if os.getenv('GAE_ENV', '').startswith('standard'):
    # Production in the standard environment
    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{instance_connection_name}")
else:
    # Local execution.
    engine = create_engine(
        f'postgresql://{db_user}:{db_pass}@{db_address}/{db_name}', echo=False)
        

# Define and Describe Netflix table
netflix = Table('netflix_pandas', meta,
                Column('show_id', Integer, primary_key=True, unique=True),
                Column('type', String),
                Column('title', String),
                Column('director', String),
                Column('cast', String),
                Column('country', String),
                Column('date_added', String),
                Column('release_year', Integer),
                Column('rating', String),
                Column('duration', String),
                Column('listed_in', String),
                Column('description', String),
                sqlite_autoincrement=True,
                autoload_with=engine)


# Authentication to access API
# Fastapi HTTP Basic Auth
security = HTTPBasic()
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, os.environ['API_USERNAME'])
    correct_password = secrets.compare_digest(
        credentials.password, os.environ['API_PASSWORD'])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Index page
@app.get("/")
async def root(username: str = Depends(get_current_username)):
    return {"msg": "Hello! Please refer to /docs page for documentations!"}


# Dynamic search, use multiple or none filters
@app.get("/search")
async def search_optional(request: Request, show_id:int=None, type=None, title=None, director=None, cast=None, country=None,
                          date_added=None, release_year:int=None, rating=None, duration=None, listed_in=None, description=None,
                          sort_by=None, sort_order=None, page=1, username: str = Depends(get_current_username)):

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
@app.get("/create/{show_id}/{title}")
async def creating(show_id:int=None, title=None, type=None, director=None, cast=None, country=None,
                   date_added=None, release_year: int = None, rating=None, duration=None, listed_in=None, description=None,
                   username: str = Depends(get_current_username)):
    
    # Initial insert statement
    query = netflix.insert()

    # Additional values
    if show_id:
        query = query.values(show_id=show_id)
    if type:
        query = query.values(type=type)
    if title:
        query = query.values(title=title)
    if director:
        query = query.values(director=director)
    if cast:
        query = query.values(cast=cast)
    if country:
        query = query.values(country=country)
    if date_added:
        query = query.values(date_added=date_added)
    if release_year:
        query = query.values(release_year=release_year)
    if rating:
        query = query.values(rating=rating)
    if duration:
        query = query.values(duration=duration)
    if listed_in:
        query = query.values(listed_in=listed_in)
    if description:
        query = query.values(description=description)

    # Execute query
    connection = engine.connect()
    connection.execute(query)

    return {show_id: title}


# put for updating: multiple options
@app.get("/update/{show_id}")
async def updating(show_id: int, type=None, title=None, director=None, cast=None, country=None,
                   date_added=None, release_year: int = None, rating=None, duration=None, listed_in=None, description=None,
                   username: str = Depends(get_current_username)):
            
    # Initial update query
    query = netflix.update().where(netflix.columns['show_id'] == show_id)

    # Options
    if type:
        query = query.values(type=type)
    if title:
        query = query.values(title=title)
    if director:
        query = query.values(director=director)
    if cast:
        query = query.values(cast=cast)
    if country:
        query = query.values(country=country)
    if date_added:
        query = query.values(date_added=date_added)
    if release_year:
        query = query.values(release_year=release_year)
    if rating:
        query = query.values(rating=rating)
    if duration:
        query = query.values(duration=duration)
    if listed_in:
        query = query.values(listed_in=listed_in)
    if description:
        query = query.values(description=description)

    # Execute query
    connection = engine.connect()
    connection.execute(query)

    # Response
    return {"updated": show_id}


# Delete: multiple options or none
@app.get("/delete")
async def deleting(show_id: int = None, type=None, title=None, director=None, cast=None, country=None,
                   date_added=None, release_year: int = None, rating=None, duration=None, listed_in=None, description=None,
                   username: str = Depends(get_current_username)):

    # # Initial Delete query
    query = netflix.delete()

    header = netflix.columns

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

    # Executing query
    connection = engine.connect()
    connection.execute(query)

    # Response
    return {"deleted": "okay" }


@app.get("/summary/type")
async def summary_type(username: str = Depends(get_current_username)):
    header = netflix.columns
    query = sa.select([header['type'],
                        func.count(header['type'])]).group_by(header['type'])

    # get all the records
    result = engine.execute(query).fetchall()
    return result

@app.get("/summary/title")
async def summary_title(username: str = Depends(get_current_username)):
    header = netflix.columns
    query = func.count(header['title'])

    # get all the records
    result = engine.execute(query).fetchall()
    return result

@app.get("/summary/date_added")
async def summary_date_added(username: str = Depends(get_current_username)):
    header = netflix.columns
    query = sa.select([header['date_added'],
                        func.count(header['date_added'])]).group_by(header['date_added'])

    # get all the records
    result = engine.execute(query).fetchall()
    return result


@app.get("/summary/rating")
async def summary_rating(username: str = Depends(get_current_username)):
    header = netflix.columns
    query = sa.select([header['rating'],
            func.count(header['rating'])]).group_by(header['rating'])

    # get all the records
    result = engine.execute(query).fetchall()
    return result


@app.get("/summary/release_year")
async def summary_release_year(username: str = Depends(get_current_username)):
    header = netflix.columns
    return_list = list()

    # Average
    query = func.avg(header['release_year'])
    avg_result = engine.execute(query).fetchall()
    return_list.append(avg_result[0])
    # Max
    query = func.max(header['release_year'])
    max_result = engine.execute(query).fetchall()
    return_list.append(max_result[0])
    # Min
    query = func.min(header['release_year'])
    min_result = engine.execute(query).fetchall()
    return_list.append(min_result[0])
    # Count
    query = func.count(header['release_year'])
    count_result = engine.execute(query).fetchall()
    return_list.append(count_result[0])

    return return_list


@app.get("/summary/duration")
async def summary_duration(username: str = Depends(get_current_username)):
        header = netflix.columns
        query = sa.select([header['duration'],
            func.count(header['duration'])]).group_by(header['duration'])

        # get all the records
        result = engine.execute(query).fetchall()
        return result


 