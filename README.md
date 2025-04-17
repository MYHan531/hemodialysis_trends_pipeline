# 💉 Haemodialysis Trends Data Pipeline (Airflow + Spark)

This project analyses and tracks trends related to kidney disease and haemodialysis using data engineering tools like **PySpark**, **PostgreSQL**, and **Apache Airflow**. It transforms raw medical data into insights you can visualise and monitor.

---

## 🚀 Tech Stack

- **Python 3.11**
- **Apache Spark** for scalable data transformation
- **PostgreSQL** for storing cleaned data
- **Apache Airflow** for scheduling and monitoring the pipeline (requires Docker or WSL; DO NOT USE Windows Command Prompt)
- **Power BI** (external) for dashboarding and visualization
- **Future Implementation**: Will consider containerizing the project using Docker

---

## 📁 Project Structure

```
hemodialysis_trends_pipeline/
│
├── dags/                          # Airflow DAGs
│   └── spark_etl_dag.py          # Linked to spark_transform.py
│
├── data/
│   ├── raw/                     # Original CSV
│   │   └── kidney_disease.csv  # Original dataset
│   └── clean/                   # Cleaned output
│
├── models/                        # Trained models and scalers
│   ├── anemia_scaler.joblib
│   ├── anemia_xgboost_model.joblib
│   ├── appetite_model.joblib
│   ├── appetite_scaler.joblib
│   ├── ckd_logistic_model.joblib
│   └── ckd_scaler.joblib
│
├── notebooks/                     # Jupyter Notebooks for model dev
│   ├── predict_anemia_xgboost.ipynb
│   ├── predict_appetite_model.ipynb
│   └── predict_hypertension_model.ipynb
│
├── scripts/
│   ├── logs/
│   │   └── etl.log
│   └── spark_transform.py     # Cleans data and loads to PostgreSQL
│
├── visualisations/                # Power BI dashboard
│   └── Haemodialysis Patient Trends - CKD Dataset.pbix
│
├── requirements.txt               # Python dependencies
└── README.md                   # Project documentation (You are here)
```

---

## 🔧 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/hemodialysis_trends_pipeline.git
cd hemodialysis_trends_pipeline
```

### 2. Create a Virtual Environment

```bash
python3 -m venv airflow_env/venv
source airflow_env/venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```bash
# .env example
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kidney_disease_db

export PROJECT_ROOT=$(pwd)
export AIRFLOW_HOME=$PROJECT_ROOT/airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_FOLDER=$PROJECT_ROOT/dags
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:yourpassword@localhost:5432/airflow"
```

### 5. Initialize Airflow Metadata DB

```bash
airflow db init
```

### 6. Create Airflow Admin User

```bash
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

### 7. Start the Web UI & Scheduler

```bash
airflow webserver --port 8080 &
airflow scheduler
```

Go to: [http://localhost:8080](http://localhost:8080)

---

## 🤔 Use Cases

- Automate data transformation and loading into a database
- Predict medical indicators like anemia, appetite, and hypertension using ML models
- Export results for Power BI dashboarding

---

## 📊 Dashboard

The Power BI dashboard `Haemodialysis Patient Trends - CKD Dataset.pbix` uses cleaned + predicted outputs to visualize:

- CKD risk bands
- Anemia likelihood
- Appetite levels
- Blood cell trends over age groups

---

## 🚀 Next Steps

- [ ] Schedule model training and export
- [ ] Add Slack/email alerts for DAG failures
- [ ] Containerize with Docker
- [ ] CI/CD pipeline via GitHub Actions

---

## 🚗 License

MIT — free for personal and commercial use.

---

## ✨ Author

Built with care by @your-username

