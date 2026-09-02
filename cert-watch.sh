#!/usr/bin/env bash
# Cert expiry watchdog for the public demo.
#
# Why this exists: renewal is HTTP-01 and needs inbound port 80, which is
# normally kept CLOSED on the router and opened on demand. A plain daily
# `renew-certs.sh` cron therefore fails every night and — critically — would
# fail silently in the renewal window too. That is exactly how the cert
# reached expiry day on 2026-08-22 with nobody noticing.
#
# So instead of blindly renewing, this:
#   days > NOTIFY_DAYS            -> silent, exit 0 (the normal case)
#   RENEW_DAYS < days <= NOTIFY   -> heads-up email: renewal window opens soon,
#                                    please open port 80. certbot won't act yet
#                                    (--keep-until-expiring only renews inside
#                                    30 days), so we do NOT attempt a renewal.
#   days <= RENEW_DAYS            -> attempt renew-certs.sh:
#                                      changed  -> success email, state reset
#                                      no change-> "open port 80" email
#
# Notification is rate-limited via a state file so you don't get 30 identical
# mails: at most once every REMIND_EVERY_DAYS, except inside URGENT_DAYS where
# it mails every run. Success and failure-after-success always notify.
#
# Schedule daily, e.g.:
#   0 3 * * * cd /path/to/egeria-workspaces && ./cert-watch.sh >> runtime-volumes/letsencrypt/cert-watch.log 2>&1
set -euo pipefail
cd "$(dirname "$0")"

NOTIFY_DAYS="${NOTIFY_DAYS:-35}"        # start warning this far out
RENEW_DAYS="${RENEW_DAYS:-30}"          # certbot's own --keep-until-expiring window
URGENT_DAYS="${URGENT_DAYS:-7}"         # inside this, mail every run
REMIND_EVERY_DAYS="${REMIND_EVERY_DAYS:-5}"

ENV_MAIN="compose-configs/egeria-quickstart/.env"
ENV_DEMO="compose-configs/egeria-quickstart/.env.demo"
STATE_DIR="runtime-volumes/letsencrypt"
STATE_FILE="${STATE_DIR}/cert-watch.state"

log() { echo "$(date -u +%FT%TZ) [cert-watch] $*"; }

_get() { # _get KEY FILE
  [[ -f "$2" ]] || return 0
  grep -E "^$1=" "$2" | head -n1 | cut -d= -f2- || true
}

CERT_DIR="$(_get CERT_DIR "$ENV_DEMO")"
[[ -n "$CERT_DIR" ]] || CERT_DIR="$(_get CERT_DIR "$ENV_MAIN")"
CERT="${CERT_DIR}/server.crt"

if [[ ! -r "$CERT" ]]; then
  log "ERROR: cert not readable at ${CERT:-<unset>} — cannot check expiry."
  exit 1
fi

_end="$(openssl x509 -in "$CERT" -noout -enddate | cut -d= -f2)"
_end_epoch="$(date -d "$_end" +%s)"
DAYS=$(( (_end_epoch - $(date +%s)) / 86400 ))
DOMAINS="$(openssl x509 -in "$CERT" -noout -ext subjectAltName 2>/dev/null \
           | tr ',' '\n' | sed -n 's/.*DNS://p' | tr -d ' ' | paste -sd, -)"

log "cert ${DOMAINS:-?} expires ${_end} (${DAYS} days)"

mkdir -p "$STATE_DIR"

send_mail() { # send_mail SUBJECT BODY
  local subject="$1" body="$2"
  local key from to
  # Env overrides win over .env — lets you test delivery (or deliberately
  # disable it) without editing the file.
  key="${RESEND_API_KEY-$(_get RESEND_API_KEY "$ENV_MAIN")}"
  from="${RESEND_FROM-$(_get RESEND_FROM "$ENV_MAIN")}"
  to="${ALERT_EMAIL_TO-$(_get ALERT_EMAIL_TO "$ENV_MAIN")}"
  if [[ -z "$key" || -z "$from" || -z "$to" ]]; then
    log "WARN: RESEND_API_KEY/RESEND_FROM/ALERT_EMAIL_TO not all set — cannot email: ${subject}"
    return 1
  fi
  # Build JSON with python so subject/body are escaped correctly.
  local payload
  payload="$(FROM="$from" TO="$to" SUBJ="$subject" BODY="$body" python3 -c '
import json, os
print(json.dumps({"from": os.environ["FROM"], "to": [os.environ["TO"]],
                  "subject": os.environ["SUBJ"], "text": os.environ["BODY"]}))')"
  if curl -sf -m 20 -X POST https://api.resend.com/emails \
       -H "Authorization: Bearer ${key}" \
       -H "Content-Type: application/json" \
       -d "$payload" >/dev/null 2>&1; then
    log "emailed ${to}: ${subject}"
    return 0
  fi
  log "ERROR: failed to email ${to}: ${subject}"
  return 1
}

# --test-email: prove the alert path actually delivers, without waiting for a
# real expiry. Alerting on this host was silently broken for months once
# already (ALERT_EMAIL_TO unset), so being able to check is worth a flag.
if [[ "${1:-}" == "--test-email" ]]; then
  if send_mail "[TEST] cert-watch alerting is working" \
"This is a test from cert-watch.sh on $(hostname).

Current certificate:
  domains: ${DOMAINS}
  expires: ${_end}  (${DAYS} days)

No action needed — this message only confirms that alert delivery works."; then
    log "test email sent OK"; exit 0
  fi
  log "test email FAILED"; exit 1
fi

should_notify() {
  (( DAYS <= URGENT_DAYS )) && return 0
  [[ -f "$STATE_FILE" ]] || return 0
  local last now
  last="$(cut -d' ' -f1 "$STATE_FILE" 2>/dev/null || echo 0)"
  now="$(date +%s)"
  (( (now - last) >= REMIND_EVERY_DAYS * 86400 ))
}

mark_notified() { echo "$(date +%s) days=${DAYS}" > "$STATE_FILE"; }

# ── Case 1: comfortably valid — stay quiet ────────────────────────────────────
if (( DAYS > NOTIFY_DAYS )); then
  log "OK — ${DAYS} days left (> ${NOTIFY_DAYS}); nothing to do."
  rm -f "$STATE_FILE"
  exit 0
fi

SITE="$(_get SITE_URL "$ENV_DEMO")"; [[ -n "$SITE" ]] || SITE="$(_get SITE_URL "$ENV_MAIN")"

# ── Case 2: approaching, but certbot won't renew yet — heads-up only ──────────
if (( DAYS > RENEW_DAYS )); then
  if should_notify; then
    send_mail "TLS cert for ${SITE:-the demo} renews in $(( DAYS - RENEW_DAYS )) days — port 80 needed" \
"The Let's Encrypt certificate for ${DOMAINS} expires in ${DAYS} days (${_end}).

Certbot will not renew until it is within ${RENEW_DAYS} days, so nothing has
been attempted yet. When that window opens, renewal needs inbound port 80:

  router 192.168.0.1:  external TCP :80  ->  cray (192.168.0.173) :80

Please open it around then. The daily cert-watch job will renew automatically
once port 80 is reachable, and email you to confirm." && mark_notified
  else
    log "approaching (${DAYS} days) but notified recently; staying quiet."
  fi
  exit 0
fi

# ── Case 3: inside the renewal window — actually try ──────────────────────────
log "within ${RENEW_DAYS} days — attempting renewal..."
_before="$(cksum "$CERT" 2>/dev/null || true)"
_out="$(./renew-certs.sh 2>&1 || true)"
echo "$_out"
_after="$(cksum "$CERT" 2>/dev/null || true)"

if [[ "$_before" != "$_after" ]]; then
  _newend="$(openssl x509 -in "$CERT" -noout -enddate | cut -d= -f2)"
  send_mail "TLS cert for ${SITE:-the demo} renewed successfully" \
"The certificate for ${DOMAINS} was renewed and now expires ${_newend}.

apache-web was restarted to load it. You can close port 80 again." || true
  rm -f "$STATE_FILE"
  log "renewed; new expiry ${_newend}"
  exit 0
fi

if should_notify; then
  send_mail "ACTION NEEDED: TLS cert for ${SITE:-the demo} expires in ${DAYS} days — open port 80" \
"Renewal ran but the certificate did NOT change, so it has not been renewed.

  domains: ${DOMAINS}
  expires: ${_end}  (${DAYS} days)

The usual cause is that inbound port 80 is closed, which HTTP-01 requires:

  router 192.168.0.1:  external TCP :80  ->  cray (192.168.0.173) :80

Open it, then either wait for tomorrow's 03:00 run or execute now:

  cd $(pwd) && ./cert-watch.sh

Last renewal output:
${_out}" && mark_notified
else
  log "not renewed (${DAYS} days) but notified recently; staying quiet."
fi
exit 0
