#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
#
# Restarts shared-infra containers that report an "unhealthy" healthcheck while
# still running, and emails through Resend when it does.
#
# WHY THIS EXISTS
# ---------------
# Docker's `restart:` policies only act when a container's main process exits.
# They do nothing for a container that stays up while the service inside it is
# dead. That is not hypothetical here: on 2026-08-16 Kafka's broker hit an
# OutOfMemoryError and shut down, but the JVM never exited, so `restart: always`
# never fired. The broker listener (9192) was gone while the controller listener
# stayed bound, and the container sat unhealthy for five days before a
# deploy-time healthcheck surfaced it.
#
# The quickstart stack's watchdog (compose-configs/egeria-quickstart/watchdog)
# does not cover this: it watches `die` events, so by construction it only sees
# containers that exit. It also lives in the quickstart stack, which
# redeploy-demo tears down on every run, whereas shared-infra is the long-lived
# tier. Hence a separate, small healer that lives with the services it watches.
#
# RELATIONSHIP TO THE KAFKA JVM FLAG
# ----------------------------------
# shared-infra.yaml also sets -XX:+ExitOnOutOfMemoryError for Kafka, which makes
# that specific failure a clean exit that `restart: always` handles on its own.
# This service is the backstop for unhealthy-but-alive states with other causes
# (deadlock, wedged disk, GC death spiral) where the process never exits.
#
# WHY POLLING RATHER THAN `docker events`
# ---------------------------------------
# `docker events --filter event=health_status` is the obvious approach, but
# health_status events could not be observed firing on this host even across a
# real starting->healthy transition. Polling `docker inspect` reflects the
# daemon's current truth and cannot miss a transition that happened while the
# event stream was reconnecting.

set -eu

: "${AUTOHEAL_LABEL:=egeria.autoheal}"
: "${POLL_SECONDS:=30}"
# Minimum gap between restarts of the same container. Bounds the damage if a
# container is persistently unhealthy — without it, a service that cannot become
# healthy would be restarted every POLL_SECONDS forever, which is worse than
# leaving it down for a human to look at.
: "${RESTART_COOLDOWN_SECONDS:=600}"
: "${RESEND_API_KEY:=}"
: "${RESEND_FROM:=}"
: "${ALERT_EMAIL_TO:=}"

STATE_DIR=/tmp/autoheal
mkdir -p "$STATE_DIR"

log() { echo "$(date -u +%FT%TZ) $*"; }

send_alert() {
    container="$1"
    outcome="$2"
    detail="$3"

    if [ -z "$RESEND_API_KEY" ] || [ -z "$RESEND_FROM" ] || [ -z "$ALERT_EMAIL_TO" ]; then
        log "RESEND_API_KEY/RESEND_FROM/ALERT_EMAIL_TO not fully set - skipping alert email"
        return 0
    fi

    ts="$(date -u +%FT%TZ)"
    subject="autoheal: ${container} was unhealthy (${outcome})"
    body="${container} reported an unhealthy healthcheck at ${ts} while still running, so Docker's restart policy would not have acted on it.\n\nOutcome: ${outcome}\n${detail}\n\nCheck 'docker logs ${container}' and 'docker inspect --format {{json .State.Health}} ${container}'."

    payload=$(cat <<JSON
{"from":"${RESEND_FROM}","to":["${ALERT_EMAIL_TO}"],"subject":"${subject}","text":"${body}"}
JSON
)

    if curl -sf -m 15 -X POST https://api.resend.com/emails \
        -H "Authorization: Bearer ${RESEND_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "${payload}" >/tmp/resend-last-response.json 2>&1; then
        log "alert email sent to ${ALERT_EMAIL_TO} for ${container} (${outcome})"
    else
        log "FAILED to send alert email for ${container} (see /tmp/resend-last-response.json)"
    fi
}

log "autoheal watching containers labelled ${AUTOHEAL_LABEL}=true (poll ${POLL_SECONDS}s, cooldown ${RESTART_COOLDOWN_SECONDS}s)"

while true; do
    # `|| true` so a daemon hiccup pauses this cycle rather than killing the
    # loop via `set -e` and leaving everything unmonitored.
    containers=$(docker ps --filter "label=${AUTOHEAL_LABEL}=true" --format '{{.Names}}' 2>/dev/null || true)

    for c in $containers; do
        status=$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$c" 2>/dev/null || echo "gone")

        # "starting" means the healthcheck's start_period is still in play —
        # restarting then would guarantee an unbootable loop for any service
        # that legitimately takes a while to come up.
        [ "$status" = "unhealthy" ] || continue

        now=$(date +%s)
        stamp_file="$STATE_DIR/${c}.last-restart"
        last=0
        [ -f "$stamp_file" ] && last=$(cat "$stamp_file" 2>/dev/null || echo 0)
        age=$((now - last))

        if [ "$age" -lt "$RESTART_COOLDOWN_SECONDS" ]; then
            log "${c} still unhealthy but restarted ${age}s ago (cooldown ${RESTART_COOLDOWN_SECONDS}s) - leaving it alone"
            continue
        fi

        streak=$(docker inspect --format '{{if .State.Health}}{{.State.Health.FailingStreak}}{{else}}?{{end}}' "$c" 2>/dev/null || echo "?")
        log "${c} is unhealthy (failing streak ${streak}) - restarting"
        echo "$now" > "$stamp_file"

        if docker restart "$c" >/dev/null 2>&1; then
            log "${c} restart issued"
            send_alert "$c" "restarted" "Failing streak was ${streak}. autoheal issued a restart; it will not retry for ${RESTART_COOLDOWN_SECONDS}s."
        else
            log "${c} restart FAILED"
            send_alert "$c" "restart failed" "Failing streak was ${streak}. autoheal could not restart it - manual intervention needed."
        fi
    done

    sleep "$POLL_SECONDS"
done
