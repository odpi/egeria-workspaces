# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
#
# Sourced (not run) by the scripts that start Airflow: exports PROVISIONER_PASSWORD from
# compose-configs/shared-infra/.env (written by gen-env.sh) unless it is already set, so that
# airflow-marquez.yaml's AIRFLOW_CONN_COCO_DATA_HUB signs in as provisioner with the same password the
# shared Postgres has (TR-28). The value is read, never printed, and the file is never sourced.
_epp_env="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.env"
if [[ -z "${PROVISIONER_PASSWORD:-}" && -f "$_epp_env" ]]; then
  PROVISIONER_PASSWORD="$(grep -E '^PROVISIONER_PASSWORD=' "$_epp_env" | head -n1 | cut -d= -f2- || true)"
  PROVISIONER_PASSWORD="${PROVISIONER_PASSWORD%\'}"; PROVISIONER_PASSWORD="${PROVISIONER_PASSWORD#\'}"
  PROVISIONER_PASSWORD="${PROVISIONER_PASSWORD%\"}"; PROVISIONER_PASSWORD="${PROVISIONER_PASSWORD#\"}"
fi
if [[ -z "${PROVISIONER_PASSWORD:-}" ]]; then
  echo "[airflow] WARNING: PROVISIONER_PASSWORD is not set (compose-configs/shared-infra/.env); run compose-configs/shared-infra/gen-env.sh first." >&2
fi
export PROVISIONER_PASSWORD
unset _epp_env
