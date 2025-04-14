# 💉 Hemodialysis Trends Data Pipeline (Airflow + Spark)

This project analyzes and tracks trends related to kidney disease and hemodialysis using data engineering tools like **PySpark**, **PostgreSQL**, and **Apache Airflow**. It transforms raw medical data into insights you can visualize and monitor.

---

## 🚀 Tech Stack

- **Python 3.11**
- **Apache Spark** for scalable data transformation
- **PostgreSQL** for storing cleaned data
- **Apache Airflow** for scheduling and monitoring the pipeline
- **Power BI** (external) for dashboarding and visualization

---

## 📁 Project Structure

hemodialysis_trends_pipeline/ 
│ 
├── dags/ # Airflow DAGs (unused as of now)
│     └── dialysis_pipeline.py 
│ 
├── data/ 
│     ├── raw/ # Original CSV
|     |     └── kidney_disease.csv # Original Dataset
|     |
│     └── clean/ # Cleaned output 
│ 
├── scripts/
│     |── logs/ # Log folder
|     |     └── etl.log # Created by spark_transform.py
│     |── spark_transform.py # Data cleaning transformation, loads into PostgresSQL (requires pgAdmin)
|     |── load_to_db.py # Deprecated, replaced by spark_transform.py
|     └── transform_data.py # Also deprecated, replaced by spark_transform.py
│
|── visualisations/
|     └── Haemodialysis Patient Trends - CKD Dataset.pbix # Data Visualiser used to chart the cleaned data
|  
├── requirements.txt 
└── README.md