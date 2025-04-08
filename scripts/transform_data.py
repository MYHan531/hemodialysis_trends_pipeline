# === IMPORT LIBRARIES ===
import pandas as pd
import numpy as np
import os

# === Load raw dataset & Set new output path ===
INPUT_PATH = '../data/raw/kidney_disease.csv'
OUTPUT_PATH = '../data/clean/kidney_disease_cleaned.csv'

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Read raw data
df = pd.read_csv(INPUT_PATH)

# Drop ID column (not useful for analysis)
df.drop(columns=['id'], inplace=True)

# Convert object-number columns to actual numeric types
for col in ['pcv', 'wc', 'rc']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Clean yes/no or categorical columns
binary_cols = ['htn', 'dm', 'cad', 'appet', 'pe', 'ane']
df[binary_cols] = df[binary_cols].applymap(lambda x: 1 if str(x).strip().lower() == 'yes' else 0 if str(x).strip().lower() == 'no' else np.nan)

# Convert 'classification' to binary (1 = CKD, 0 = Not CKD)
df['classification'] = df['classification'].apply(lambda x: 1 if 'ckd' in str(x).lower() else 0)

# Fill remaining numeric nulls with column medians
for col in df.select_dtypes(include=[np.number]).columns:
    df[col].fillna(df[col].median(), inplace=True)

# Fill categorical nulls with mode
for col in df.select_dtypes(include='object').columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Create age bands
# df['age_band'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 65, 100], 
#                         labels=['0-18', '19-35', '36-50', '51-65', '65+'])

# Save cleaned dataset
df.to_csv(OUTPUT_PATH, index=False)
print(f"[SUCCESS] Cleaned data saved to: {OUTPUT_PATH}")