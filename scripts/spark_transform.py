import os
import glob
import shutil
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PostgreSQL credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_TABLE = "dialysis_cleaned"

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "../data/raw/kidney_disease.csv")
TMP_OUTPUT_DIR = os.path.join(BASE_DIR, "../data/clean/tmp_csv")
FINAL_CSV_PATH = os.path.join(BASE_DIR, "../data/clean/kidney_disease_cleaned.csv")

# Start Spark
spark = SparkSession.builder \
    .appName("DialysisDataTransform") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()

# Load and clean data
df = spark.read.option("header", True).option("inferSchema", True).csv(RAW_DATA_PATH)
df = df.drop("id")

binary_cols = ['htn', 'dm', 'cad', 'pe', 'ane']
for col_name in binary_cols:
    df = df.withColumn(
        col_name,
        when(col(col_name) == "yes", 1)
        .when(col(col_name) == "no", 0)
        .otherwise(None)
    )

cast_cols = ['pcv', 'rc', 'wc']
for col_name in cast_cols:
    df = df.withColumn(col_name, col(col_name).cast("double"))

df = df.withColumn("classification", when(col("classification").like("%ckd%"), 1).otherwise(0))

df = df.withColumn(
    "age_band",
    when(col("age") <= 18, "0-18")
    .when(col("age") <= 35, "19-35")
    .when(col("age") <= 50, "36-50")
    .when(col("age") <= 65, "51-65")
    .otherwise("65+")
)

# Ensure output dir exists
os.makedirs(os.path.dirname(TMP_OUTPUT_DIR), exist_ok=True)

# Write to single CSV file in temp folder
df.coalesce(1).write.mode("overwrite").option("header", True).csv(TMP_OUTPUT_DIR)

# Move the part-00000 file to the final cleaned path
csv_files = glob.glob(os.path.join(TMP_OUTPUT_DIR, "part-*.csv"))
if csv_files:
    shutil.move(csv_files[0], FINAL_CSV_PATH)
    print(f"[✅] CSV cleaned and saved to: {FINAL_CSV_PATH}")
else:
    print("[❌] Output CSV file not found.")

# Load cleaned CSV into PostgreSQL using pandas
df_cleaned = pd.read_csv(FINAL_CSV_PATH)

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

df_cleaned.to_sql(DB_TABLE, engine, if_exists="replace", index=False, method="multi")
print(f"[✅] Data loaded into PostgreSQL table: {DB_TABLE}")
