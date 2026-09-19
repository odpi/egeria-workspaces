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
: "${RESET_MARKER:=/demo-data/reset-marker}"
: "${RESET_GRACE_SEC:=300}"
: "${RESEND_API_KEY:=}"
: "${RESEND_FROM:=}"
: "${ALERT_EMAIL_TO:=}"

# The nightly demo reset (PyegeriaWebHandler/demo_reset_handler.py) stops the
# platform container deliberately, and that reaches us as exactly the same
# `die` event (exit 143) a real crash would - so before this, every reset
# emailed an "Egeria down" alert, which only teaches the reader to ignore the
# one that eventually matters. The reset stamps RESET_MARKER with the epoch
# seconds of the stop just before issuing it; a die within RESET_GRACE_SEC of
# that stamp is expected and stays quiet. Anything older - or no marker at all,
# e.g. the mount is missing or the reset path itself broke - still alerts, so
# the failure mode here is a spurious email, never a silent outage.
is_scheduled_reset() {
    marker_age=""
    [ -r "$RESET_MARKER" ] || return 1
    marker=$(cat "$RESET_MARKER" 2>/dev/null) || return 1
    # busybox `sh` has no regex; reject anything that is not a bare integer so a
    # truncated or half-written marker can never be read as "reset in progress".
    case "$marker" in
        ''|*[!0-9]*) return 1 ;;
    esac
    marker_age=$(( $(date -u +%s) - marker ))
    [ "$marker_age" -ge 0 ] && [ "$marker_age" -le "$RESET_GRACE_SEC" ]
}

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
        # An OOM kill is never "expected", so it alerts even inside the reset
        # window - suppressing that would hide the exact failure this watchdog
        # was built for (see the July 30 OOM-kill noted above).
        if [ "$oom" != "true" ] && is_scheduled_reset; then
            echo "$(date -u +%FT%TZ) die event: ${WATCH_CONTAINER} exit=${exit_code} oom=${oom} - scheduled demo reset ${marker_age}s ago, not alerting"
        else
            echo "$(date -u +%FT%TZ) die event: ${WATCH_CONTAINER} exit=${exit_code} oom=${oom}"
            send_alert "${exit_code}" "${oom}"
        fi
    done

    # docker events exits if the daemon connection drops (e.g. Docker Desktop
    # restarting); wait a bit and re-attach rather than leaving the watcher dead.
    echo "$(date -u +%FT%TZ) docker events stream ended - reconnecting in 10s" >&2
    sleep 10
done
