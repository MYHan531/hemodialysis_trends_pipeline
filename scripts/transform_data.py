# === IMPORT LIBRARIES ===
import pandas as pd
from sqlalchemy import create_engine
import getpass
import os

# === Import Cleaned Data ===
CLEANED_CSV_PATH = '../data/clean/kidney_disease_cleaned.csv'

# === Load Cleaned Data ===
df = pd.read_csv(CLEANED_CSV_PATH)

# Prompt for connection details, requires pgAdmin
db_user = input("Enter PostgreSQL username (default: postgres): ") or 'postgres'
db_password = getpass.getpass("Enter PostgreSQL password: ")
db_host = input("Enter host (default: localhost): ") or 'localhost'
db_port = input("Enter port (default: 5432): ") or '5432'
db_name = input("Enter database name (default: books_db): ") or 'books_db'

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Load to PostgreSQL table
df.to_sql(
    name='dialysis_cleaned',
    con=engine,
    if_exists='replace',
    index=False,
    method='multi'  # Speeds up insert
)

print("[SUCCESS] Cleaned dialysis data loaded into PostgreSQL table 'dialysis_cleaned'")