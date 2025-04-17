def install_if_missing(package, import_name=None):
    try:
        __import__(import_name or package)
    except ImportError:
        import subprocess
        import sys
        print(f"📦 Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_if_missing("pandas")
install_if_missing("pyspark", "pyspark")
install_if_missing("sqlalchemy")
install_if_missing("python-dotenv", "dotenv")

import os
import glob
import shutil
import pandas as pd
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "etl.log")

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE_PATH, "a") as f:
        f.write(full_message + "\n")

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
log("Starting Spark session...")
spark = SparkSession.builder \
    .appName("DialysisDataTransform") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()

# Load and clean data
log("Reading raw CSV data...")
df = spark.read.option("header", True).option("inferSchema", True).csv(RAW_DATA_PATH)
df = df.drop("id")

log("Cleaning binary columns...")
binary_cols = ['htn', 'dm', 'cad', 'pe', 'ane']
for col_name in binary_cols:
    df = df.withColumn(
        col_name,
        when(col(col_name) == "yes", 1)
        .when(col(col_name) == "no", 0)
        .otherwise(None)
    )

log("Casting numeric columns...")
cast_cols = ['pcv', 'rc', 'wc']
for col_name in cast_cols:
    df = df.withColumn(col_name, col(col_name).cast("double"))

log("Encoding target classification column...")
df = df.withColumn("classification", when(col("classification").like("%ckd%"), 1).otherwise(0))

log("Creating age bands...")
df = df.withColumn(
    "age_band",
    when(col("age") <= 18, "0-18")
    .when(col("age") <= 35, "19-35")
    .when(col("age") <= 50, "36-50")
    .when(col("age") <= 65, "51-65")
    .otherwise("65+")
)

log("Writing temporary CSV...")
os.makedirs(os.path.dirname(TMP_OUTPUT_DIR), exist_ok=True)
df.coalesce(1).write.mode("overwrite").option("header", True).csv(TMP_OUTPUT_DIR)

# Move the part-00000 file to the final cleaned path
log("Moving CSV to final location...")
csv_files = glob.glob(os.path.join(TMP_OUTPUT_DIR, "part-*.csv"))
if csv_files:
    shutil.move(csv_files[0], FINAL_CSV_PATH)
    log(f"CSV cleaned and saved to: {FINAL_CSV_PATH}")
else:
    log("Output CSV file not found.")
    exit()

# Load into pandas and rename columns
log("Loading cleaned CSV into pandas...")
df_cleaned = pd.read_csv(FINAL_CSV_PATH)

log("Renaming columns to descriptive names...")
column_renames = {
    'age': 'Age',
    'bp': 'Blood_Pressure',
    'sg': 'Specific_Gravity',
    'al': 'Albumin',
    'su': 'Sugar',
    'rbc': 'Red_Blood_Cells',
    'pc': 'Pus_Cells',
    'pcc': 'Pus_Cell_Clumps',
    'ba': 'Bacteria',
    'bgr': 'Blood_Glucose_Random',
    'bu': 'Blood_Urea',
    'sc': 'Serum_Creatinine',
    'sod': 'Sodium',
    'pot': 'Potassium',
    'hemo': 'Hemoglobin',
    'pcv': 'Packed_Cell_Volume',
    'wc': 'White_Blood_Cell_Count',
    'rc': 'Red_Blood_Cell_Count',
    'htn': 'Hypertension',
    'dm': 'Diabetes_Mellitus',
    'cad': 'Coronary_Artery_Disease',
    'appet': 'Appetite',
    'pe': 'Pedal_Edema',
    'ane': 'Anemia',
    'classification': 'Kidney_Disease_Classification',
    'age_band': 'Age_Band'
}
df_cleaned.rename(columns=column_renames, inplace=True)

# if you need a new local copy, uncomment this segment
# df_cleaned.to_csv(FINAL_CSV_PATH, index=False)
# log(f"Renamed CSV saved to: {FINAL_CSV_PATH}")

# Load to PostgreSQL
log("Connecting to PostgreSQL database...")
db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

log(f"Uploading data to PostgreSQL table '{DB_TABLE}'...")
df_cleaned.to_sql(DB_TABLE, engine, if_exists="replace", index=False, method="multi")
log(f"Data loaded into PostgreSQL table: {DB_TABLE}")

log("ETL job completed successfully.")
