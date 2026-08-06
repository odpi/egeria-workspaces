#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
#
# Watches the Docker daemon (via the mounted socket) for "die" events on
# WATCH_CONTAINER and emails ALERT_EMAIL_TO through Resend when it happens.
# Runs the docker-events stream in a restart loop so a transient Docker
# Desktop restart (which drops the event stream) doesn't leave us silently
# unmonitored — see the July 30 OOM-kill this was built in response to.
set -eu

: "${WATCH_CONTAINER:=quickstart-egeria-main}"
: "${RESEND_API_KEY:=}"
: "${RESEND_FROM:=}"
: "${ALERT_EMAIL_TO:=}"

send_alert() {
    exit_code="$1"
    oom="$2"

    if [ -z "$RESEND_API_KEY" ] || [ -z "$RESEND_FROM" ] || [ -z "$ALERT_EMAIL_TO" ]; then
        echo "$(date -u +%FT%TZ) RESEND_API_KEY/RESEND_FROM/ALERT_EMAIL_TO not fully set - skipping alert email" >&2
        return 0
    fi

    ts="$(date -u +%FT%TZ)"
    if [ "$oom" = "true" ]; then
        subject="Egeria down: ${WATCH_CONTAINER} was OOM-killed (exit ${exit_code})"
        reason="The kernel OOM-killer terminated it - the container/VM ran out of memory."
    else
        subject="Egeria down: ${WATCH_CONTAINER} exited (code ${exit_code})"
        reason="It exited with code ${exit_code}. Check 'docker logs ${WATCH_CONTAINER}' for details."
    fi

    body="${WATCH_CONTAINER} stopped at ${ts}. ${reason}\n\nRestart policy should bring it back automatically if one is set; verify with 'docker ps -a --filter name=${WATCH_CONTAINER}'."

    payload=$(cat <<JSON
{"from":"${RESEND_FROM}","to":["${ALERT_EMAIL_TO}"],"subject":"${subject}","text":"${body}"}
JSON
)

    if curl -sf -m 15 -X POST https://api.resend.com/emails \
        -H "Authorization: Bearer ${RESEND_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "${payload}" >/tmp/resend-last-response.json 2>&1; then
        echo "$(date -u +%FT%TZ) alert email sent to ${ALERT_EMAIL_TO} for ${WATCH_CONTAINER} (exit ${exit_code}, oom=${oom})"
    else
        echo "$(date -u +%FT%TZ) FAILED to send alert email (see /tmp/resend-last-response.json)" >&2
    fi
}

echo "$(date -u +%FT%TZ) watching '${WATCH_CONTAINER}' for die events"

while true; do
    docker events \
        --filter "type=container" \
        --filter "container=${WATCH_CONTAINER}" \
        --filter "event=die" \
        --format '{{json .}}' \
    | while IFS= read -r line; do
        exit_code=$(echo "$line" | jq -r '.Actor.Attributes.exitCode // "unknown"')
        oom=$(docker inspect "${WATCH_CONTAINER}" --format '{{.State.OOMKilled}}' 2>/dev/null || echo "unknown")
        echo "$(date -u +%FT%TZ) die event: ${WATCH_CONTAINER} exit=${exit_code} oom=${oom}"
        send_alert "${exit_code}" "${oom}"
    done

    # docker events exits if the daemon connection drops (e.g. Docker Desktop
    # restarting); wait a bit and re-attach rather than leaving the watcher dead.
    echo "$(date -u +%FT%TZ) docker events stream ended - reconnecting in 10s" >&2
    sleep 10
done
