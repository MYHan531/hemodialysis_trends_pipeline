#!/bin/bash

# -------------------------------
# Airflow Restart Script (WSL-only)
# -------------------------------

# --- System Packages Checker ---
check_and_install_system() {
  PACKAGE=$1
  FRIENDLY_NAME=$2
  if ! command -v "$PACKAGE" &> /dev/null; then
    echo "📦 '$FRIENDLY_NAME' not found. Installing via apt..."
    sudo apt update && sudo apt install -y "$PACKAGE"
  else
    echo "✅ '$FRIENDLY_NAME' already installed."
  fi
}

# --- Python Packages Checker ---
check_and_install_python() {
  PACKAGE=$1
  FRIENDLY_NAME=$2
  if ! python3 -c "import $PACKAGE" &> /dev/null; then
    echo "📦 Python package '$FRIENDLY_NAME' not found. Installing via pip..."
    pip install "$PACKAGE"
  else
    echo "✅ Python package '$FRIENDLY_NAME' already installed."
  fi
}

echo "🔍 Checking required system packages..."
check_and_install_system curl "curl"
check_and_install_system lsof "lsof"
check_and_install_system netstat "net-tools"   # netstat comes from net-tools
check_and_install_system psql "PostgreSQL Client"
check_and_install_system gunicorn "gunicorn"

echo "🔍 Checking required Python packages..."
check_and_install_python psycopg2 "psycopg2-binary"
check_and_install_python pyspark "pyspark"
check_and_install_python sqlalchemy "sqlalchemy"

# --- CONFIGURATION ---
VENV_PATH="airflow_env/venv/bin/activate"
ENV_FILE=".env"
AIRFLOW_PORT=8080
SCHEDULER_PORT=8793

# --- current directory ---
AIRFLOW_DIR="$(cd "$(dirname "$0")" && pwd)"
export DAG_DIR="${AIRFLOW_DIR}/dags"
export LOG_DIR="${AIRFLOW_DIR}/airflow/logs"
WEB_LOG="$LOG_DIR/webserver.log"

# --- Helper function ---
print_section() {
  echo -e "\n🔹 $1\n---------------------------"
}

echo "Airflow directory = $AIRFLOW_DIR"
echo "DAG folder directory = $DAG_DIR"
echo "🚀 Restarting Airflow environment safely..."

# --- Activate virtualenv ---
print_section "Activating virtual environment"
if [ -f "$VENV_PATH" ]; then
  source "$VENV_PATH"
  echo "[✔] Virtualenv activated: airflow_env"
else
  echo "❌ Virtualenv not found at $VENV_PATH"
  exit 1
fi

# --- Load the environment variables ---
print_section "Loading environment variables"
if [ -f "$ENV_FILE" ]; then
  set -o allexport
  source "$ENV_FILE"
  set +o allexport
  echo "[✔] Loaded .env"
else
  echo "⚠️ .env not found. Continuing without it..."
fi

# --- Kill any processes on used ports incase if it has been already used ---
print_section "Freeing up Airflow ports"
for PORT in $AIRFLOW_PORT $SCHEDULER_PORT; do
    PIDS=$(lsof -ti :$PORT)
    if [ -n "$PIDS" ]; then
        echo "🛑 Port $PORT in use. Killing PID(s): $PIDS"
        kill -9 $PIDS
    else
        echo "✅ Port $PORT is free"
    fi
done

# --- Ensures log directory exists ---
print_section "Ensuring log directory"
LOG_DIR="${AIRFLOW_HOME}/logs"
if command -v mkdir >/dev/null 2>&1; then
  mkdir -p "$LOG_DIR"
  chmod -R 755 "$LOG_DIR"
  echo "[✔] Log directory ready: $LOG_DIR"
else
  echo "❌ 'mkdir' or 'chmod' not available"
  exit 1
fi

# --- DB MIGRATE ---
print_section "Migrating Airflow DB"
airflow db migrate

# # Start services
# # --- START WEBSERVER ---
# print_section "Starting Airflow Webserver"
# nohup airflow webserver --port $AIRFLOW_PORT > "$WEB_LOG" 2>&1 &

# MAX_WAIT=200
# ELAPSED=0
# until netstat -tuln | grep ":$AIRFLOW_PORT" > /dev/null; do
#     sleep 1
#     ELAPSED=$((ELAPSED+1))
#     if [ $ELAPSED -ge $MAX_WAIT ]; then
#         echo "❌ Timeout: Webserver failed to start within $MAX_WAIT seconds"
#         exit 1
#     fi
# done

# echo "✅ Webserver is now live on port $AIRFLOW_PORT (started in ${ELAPSED}s)"

# print_section "Starting Airflow Scheduler"
# airflow scheduler

# # --- START SCHEDULER ---
# print_section "Starting Airflow Scheduler"
# airflow scheduler

# # --- OPTIONAL: Open in browser (only on WSL) ---
# if grep -qEi "(Microsoft|WSL)" /proc/version &>/dev/null; then
#   echo "🌐 Opening Airflow UI at http://localhost:$AIRFLOW_PORT"
#   explorer.exe "http://localhost:$AIRFLOW_PORT"
# fi
