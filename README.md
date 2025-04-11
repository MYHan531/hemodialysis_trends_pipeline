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
├── dags/ # Airflow DAGs 
│     └── dialysis_pipeline.py 
│ 
├── data/ 
│     ├── raw/ # Original CSV 
│     └── clean/ # Cleaned output 
│ 
├── scripts/ 
│      └── spark_transform.py # Data cleaning transformation 
│ 
├── requirements.txt 
└── README.md