from sqlalchemy import create_engine
import sqlalchemy as sa
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
address = os.environ['DB_ADDRESS']
database = os.environ['DB_NAME']

# Connect to Cloud SQL
engine = create_engine(
    f'postgresql://{user}:{password}@{address}/{database}', echo=False)

# Print current tables in Cloud SQL
insp = sa.inspect(engine)
db_list = insp.get_table_names()
print(db_list)
