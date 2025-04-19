#!/bin/bash

# Check & install system deps
check_and_install() {
  PACKAGE=$1
  FRIENDLY_NAME=$2
  if ! command -v "$PACKAGE" &> /dev/null; then
    echo "📦 '$FRIENDLY_NAME' not found. Installing..."
    sudo apt update && sudo apt install -y "$PACKAGE"
  else
    echo "✅ '$FRIENDLY_NAME' already installed."
  fi
}

echo "🔍 Checking required system packages..."

check_and_install curl "curl"
check_and_install lsof "lsof"
check_and_install netstat "net-tools"   # netstat comes from net-tools
check_and_install psql "PostgreSQL Client"
check_and_install gunicorn "gunicorn"

# --- CONFIGURATION ---
VENV_PATH="airflow_env/venv/bin/activate"
ENV_FILE=".env"
AIRFLOW_PORT=8080
SCHEDULER_PORT=8793
AIRFLOW_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$AIRFLOW_DIR/logs"
WEB_LOG="$LOG_DIR/webserver.log"
SCHED_LOG="$LOG_DIR/scheduler.log"

echo "Airflow directory = $AIRFLOW_DIR"

echo "🚀 Restarting Airflow environment safely..."

# Activate virtual environment
if [ -f "$VENV_PATH" ]; then
    echo "🔄 Activating virtual environment..."
    source "$VENV_PATH"
else
    echo "❌ Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Load the environment variables
if [ -f "$ENV_FILE" ]; then
    echo "📦 Loading environment variables from $ENV_FILE..."
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
else
    echo "⚠️ No .env file found, continuing without loading..."
fi

# Kill any processes on used ports incase if it has been already used
for PORT in $AIRFLOW_PORT $SCHEDULER_PORT; do
    PIDS=$(lsof -ti :$PORT)
    if [ -n "$PIDS" ]; then
        echo "🛑 Port $PORT in use. Killing PID(s): $PIDS"
        kill -9 $PIDS
    else
        echo "✅ Port $PORT is free"
    fi
done

# Prepare log directory for logging
echo "📁 Ensuring log directory exists: $LOG_DIR"
mkdir -p "$LOG_DIR"
chmod -R 755 "$LOG_DIR"

# Start airflow webserver and airflow scheduler plus logging
echo "🚦 Starting Airflow webserver..."
nohup airflow webserver --port $AIRFLOW_PORT > "$WEB_LOG" 2>&1 &

echo "⏳ Waiting for webserver to be available on port $AIRFLOW_PORT..."

for i in {1..100}; do
    if ss -tuln | grep ":$AIRFLOW_PORT" > /dev/null; then
        echo "✅ Webserver is running on port $AIRFLOW_PORT"
        break
    fi
    sleep 1
done

if ! ss -tuln | grep ":$AIRFLOW_PORT" > /dev/null; then
    echo "❌ Webserver failed to start. Check $WEB_LOG for details"
    exit 1
fi

echo "📅 Starting Airflow scheduler..."
nohup airflow scheduler > "$SCHED_LOG" 2>&1 &

# Open in browser (only on WSL)
if grep -qEi "(Microsoft|WSL)" /proc/version &>/dev/null; then
    echo "🌐 Opening Airflow UI at http://localhost:$AIRFLOW_PORT"
    explorer.exe "http://localhost:$AIRFLOW_PORT"
fi
