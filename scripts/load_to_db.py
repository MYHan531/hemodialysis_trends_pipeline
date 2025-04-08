# === IMPORT LIBRARIES ===
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import getpass
import os

# Load variables from .env
load_dotenv()

# Prompt for connection details, requires pgAdmin
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME')

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# === Import Cleaned Data ===
CLEANED_CSV_PATH = '../data/clean/kidney_disease_cleaned.csv'

# === Load Cleaned Data ===
df = pd.read_csv(CLEANED_CSV_PATH)

# Load to PostgreSQL table
df.to_sql(
    name='dialysis_cleaned',
    con=engine,
    if_exists='replace',
    index=False,
    method='multi'  # allows batching
)

print("[SUCCESS] Cleaned dialysis data loaded into PostgreSQL table 'dialysis_cleaned'")
