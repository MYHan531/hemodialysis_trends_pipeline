# 💉 Haemodialysis Trends Data Pipeline (Airflow + Spark)

This project explores and monitors patterns in kidney disease and haemodialysis using a combination of robust data engineering tools — namely **PySpark**, **PostgreSQL**, and **Apache Airflow**. The pipeline takes raw clinical data, transforms it, and feeds it into predictive models and visual dashboards to offer meaningful insight.

---

## 🛠 Tech Stack

- **Python 3.11**  
- **Apache Spark** – scalable data transformation
- **PostgreSQL** – backend storage for processed data
- **Apache Airflow** – orchestrates and schedules the ETL and modelling workflows (requires WSL or Docker; avoid Windows CMD)
- **Power BI** – for rich, interactive data visualisation
- **Docker (future)** – planned containerisation once revisited

---

## 🗂 Project Layout

```
hemodialysis_trends_pipeline/
│
├── dags/                          # Airflow DAGs
│   └── spark_etl_dag.py          # ETL orchestration DAG
│
├── data/
│   ├── raw/                      # Original CSV dataset
│   │   └── kidney_disease.csv
│   └── clean/                    # Transformed data
│
├── models/                       # Machine learning model outputs
│   ├── anemia_scaler.joblib
│   ├── anemia_xgboost_model.joblib
│   ├── appetite_model.joblib
│   ├── appetite_scaler.joblib
│   ├── ckd_logistic_model.joblib
│   └── ckd_scaler.joblib
│
├── notebooks/                   # Jupyter notebooks for modelling
│   ├── predict_anemia_xgboost.ipynb
│   ├── predict_appetite_model.ipynb
│   └── predict_hypertension_model.ipynb
│
├── scripts/
│   ├── logs/
│   │   └── etl.log               # Logs generated during ETL
│   └── spark_transform.py        # Main data cleaning/transformation script
│
├── visualisations/               # Power BI dashboard assets
│   └── Haemodialysis Patient Trends - CKD Dataset.pbix
│
├── requirements.txt              # Python dependencies
└── README.md                     # You’re reading it
```

---

## ⚙️ Setup Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/MYHan531/hemodialysis_trends_pipeline.git
cd hemodialysis_trends_pipeline
```

### Step 2: Create and activate a virtual environment

```bash
python3 -m venv airflow_env/venv
source airflow_env/venv/bin/activate
```

### Step 3: Install required packages

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in your root directory:

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=your_port (default: 5432)
DB_NAME=your_db

export PROJECT_ROOT=$(pwd)
export AIRFLOW_HOME=$PROJECT_ROOT/airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_FOLDER=$PROJECT_ROOT/dags
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://your_username:yourpassword@your_port:5432/airflow"
```

### Step 5: Initialise the Airflow metadata database

```bash
airflow db init # or airflow db migrate
```

### Step 6: Create an Airflow admin user

```bash
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

### Step 7: Run the webserver and scheduler

```bash
airflow webserver --port 8080 &
airflow scheduler
```

Then head over to: [http://localhost:8080](http://localhost:8080)

---

## 💡 What This Project Does

- Automates the ETL process using Spark and Airflow
- Cleans and structures medical data from CSV to PostgreSQL
- Trains models to predict:  
  ✔ Anaemia  
  ✔ Appetite levels  
  ✔ Hypertension  
- Exports the results to CSV for visualisation

---

## 📊 Dashboarding

The Power BI report (`Haemodialysis Patient Trends - CKD Dataset.pbix`) showcases:

- CKD classification risk levels
- Model predictions (appetite, anaemia)
- Biomarker trends across patient age bands

---

## 🔮 What’s Coming Next

- [ ] Schedule training + exporting models via Airflow DAGs
- [ ] Alerting mechanisms (Slack/email for failed DAGs)
- [ ] Docker support for portability
- [ ] GitHub Actions CI/CD pipeline

---

## 📄 Licence

MIT Licence — free for both personal and commercial usage.

---

## ✍️ Maintainer

Crafted with care by [@MYHan531](https://github.com/MYHan531)  
If you find this useful, feel free to fork or reach out!

