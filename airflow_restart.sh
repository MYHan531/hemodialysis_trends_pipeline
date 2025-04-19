#!/bin/bash

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
sleep 5

if netstat -tuln | grep ":$AIRFLOW_PORT" > /dev/null; then
    echo "✅ Webserver is running on port $AIRFLOW_PORT"
else
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
