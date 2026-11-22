#!/usr/bin/env bash
# Prune Airflow per-run log directories older than N days (default 1).
# Airflow has no built-in file-log retention; unchecked, logs grow to >1M dirs,
# which exhausts inotify watches for IDEs (PyCharm fsnotifier) watching the repo.
# Runs inside the worker container because the files are owned by uid 50000.
# Cron example (hourly): 17 * * * * /path/to/prune-airflow-logs.sh 1 >> /tmp/prune-airflow-logs.log 2>&1
set -euo pipefail
DAYS="${1:-1}"
docker exec airflow-marquez-airflow-worker-1 sh -c \
  "find /opt/airflow/logs -mindepth 2 -maxdepth 2 -type d -name 'run_id=*' -mtime +${DAYS} -exec rm -rf {} +"
