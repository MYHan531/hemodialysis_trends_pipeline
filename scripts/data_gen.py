import pandas as pd
import numpy as np
import random
from faker import Faker

# Initialise Faker to make random generations
fake = Faker()

# Load original dataset(act as template)
template_path = "../data/raw/kidney_disease2.csv" 
original = pd.read_csv(template_path)

# Number of rows to generate
TARGET_ROWS = 1_000_000

# Helper functions to generate slightly varied data
def vary_numeric(val, variation=0.1):
    if pd.isna(val):
        return np.nan
    try:
        val = float(val)
        return round(val * (1 + random.uniform(-variation, variation)), 2)
    except ValueError:
        return val  # If it can't be converted to float, return original


def vary_categorical(val, choices, prob_miss=0.01):
    if not choices:  # only if choices list is empty
        return np.nan
    if random.random() < prob_miss:
        return np.nan
    try:
        return random.choice(choices)
    except (IndexError, TypeError):
        return np.nan

# Create dataframe
synthetic_data = []

print("🚀 Generating synthetic data...")

# Prebuild unique categories from original
categorical_columns = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']
category_choices = {col: original[col].dropna().unique().tolist() for col in categorical_columns}

# row samples
for _ in range(TARGET_ROWS):
    row = {}
    for col in original.columns:
        if col in categorical_columns:
            row[col] = vary_categorical(None, category_choices[col])
        elif col == 'classification':
            row[col] = random.choice(['ckd', 'notckd'])
        elif col == 'age':
            row[col] = round(random.uniform(2, 90), 1)
        elif col == 'bp':
            row[col] = round(random.uniform(50, 180), 0)
        else:
            row[col] = vary_numeric(original[col].dropna().sample(1).values[0])
    synthetic_data.append(row)

# Save to csv
synthetic_df = pd.DataFrame(synthetic_data)
out_path = "../data/raw/kidney_disease_synthetic.csv"
synthetic_df.to_csv(out_path, index=False)

print(f"✅ Synthetic data with {TARGET_ROWS} rows saved to {out_path}")
