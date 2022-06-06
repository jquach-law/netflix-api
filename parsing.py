import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
address = os.environ['DB_ADDRESS']
database = os.environ['DB_NAME']

# Connect to Database
engine = create_engine(
    f'postgresql://{user}:{password}@{address}/{database}', echo=False)

# .csv to pandas Dataframe
netflix_csv = "../netflix_titles/netflix_titles.csv"
df = pd.read_csv(netflix_csv)

# Strip first letter in "show_id", convert to int for primary key
df['show_id'] = df['show_id'].str[1:]
df['show_id'] = df['show_id'].astype(int)


# Export to Database
df.to_sql("netflix_pandas", engine, if_exists="replace", index=False)


