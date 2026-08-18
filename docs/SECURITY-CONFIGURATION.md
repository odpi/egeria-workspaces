<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Configuring Security

How TLS/HTTPS and authentication are configured across the three deployment modes in this repo
— quickstart (local/multi-host), quickstart `--demo`, and freshstart. For **reporting a security
vulnerability**, see [`SECURITY.md`](../SECURITY.md) at the repo root instead — this document is
an operator's configuration guide, not a disclosure policy.

---

## At a glance

| | Quickstart (non-demo) | Quickstart `--demo` | Freshstart |
|---|---|---|---|
| HTTPS | always on, self-signed by default | always on, **real cert required** | always on, self-signed by default |
| Default HTTPS port | 8843 | 443 | 7843 |
| HTTP port (301-redirects to HTTPS) | 8885 | 8885 | 7885 |
| Cert source | self-signed (auto) or `CERT_DIR` | `CERT_DIR` (supplied) or Let's Encrypt (automatic fallback) | self-signed (auto) or `CERT_DIR` |
| Auth gating | none — opens straight to the portal | JWT + Postgres, registration + email verification | Egeria-backed login (`bootstrap`/`secret` initially) |
| Multi-host variant | `quick-start-multi-host` — same TLS mechanism | n/a (`--demo` is `quick-start-local`-only) | `fresh-start-multi-host` — same TLS mechanism |

Every mode's plain-HTTP port always 301-redirects to the HTTPS one — there is no way to reach
the portal over plain HTTP for actual use, only as a redirect hop. (`curl -L` follows it
automatically; without `-L` you'll see a `301` and a `Location:` header instead of content.)

---

## HTTPS / TLS

### Self-signed by default (quickstart, freshstart — both local and multi-host)

`./quick-start-local`, `./quick-start-multi-host`, `./fresh-start-local`, and
`./fresh-start-multi-host` all bring up Apache's HTTPS listener on every run. If no certificate
is configured, each auto-generates a self-signed one on first run via `generate-certs.sh`:

| Script(s) | Self-signed cert location | Default HTTPS port |
|---|---|---|
| `quick-start-local`, `quick-start-multi-host` | `runtime-volumes/certs-quickstart/` | 8843 |
| `fresh-start-local`, `fresh-start-multi-host` | `runtime-volumes/certs-freshstart/` | 7843 |

Your browser will warn about the self-signed cert — accept it once. The cert is regenerated
only if the files at that path are missing; once created, it's reused across runs so you don't
have to re-accept the warning every restart.

To get rid of that warning entirely for local development (or to fix a hard cert error rather
than just a warning — the auto-generated cert doesn't carry Subject Alternative Names, so some
browsers reject it outright depending on which hostname you use to reach it), drop in a
locally-trusted cert via `mkcert` instead: see
[`MKCERT-SETUP.md`](MKCERT-SETUP.md) (macOS/Linux/Windows). Same `CERT_DIR` mechanism below —
mkcert output drops straight into that three-file layout.

**To use a real certificate instead**, create `.env.ssl` (gitignored) in the relevant
`compose-configs/egeria-quickstart/` or `compose-configs/egeria-freshstart/` directory:

```ini
CERT_DIR=/absolute/path/to/dir/containing/server.crt+server.key+server-ca.crt
HTTPS_PORT=8843        # optional — omit to keep the mode's default
SITE_URL=https://your.domain.com   # optional — omit to derive from HOST_FQDN:HTTPS_PORT
```

`CERT_DIR` must contain exactly `server.crt`, `server.key`, and `server-ca.crt` — the same
layout `generate-certs.sh` produces, so nothing downstream (Apache's `fastapi-ssl.conf`) needs
to know whether the cert is self-signed or real.

**Renewal** (real certificates): replace the three files at `CERT_DIR` and restart Apache — no
rebuild required:

```bash
docker restart quickstart-web-server    # or freshstart-web-server
```

### Quickstart `--demo` — real certificate required

Demo mode (`./quick-start-local --demo`) is meant for a real public deployment, so it does not
fall back to a self-signed certificate. On first run you're prompted for a certificate
directory (same `server.crt`/`server.key`/`server-ca.crt` layout):

- **Supply a path** to a cert you already have, or
- **Leave it blank** to have Let's Encrypt obtain one automatically (see below).

The answer is saved to `.env.demo` (gitignored) and reused on subsequent `--demo` runs.

### Let's Encrypt (automatic, quickstart `--demo` only)

Leaving the cert-directory prompt blank in `--demo` mode triggers automatic Let's Encrypt
acquisition:

1. **Requirements**: `SITE_URL`'s domain must already resolve (DNS) to this host, and **port 80**
   must be reachable from the internet on that domain — Let's Encrypt's HTTP-01 challenge
   protocol hardcodes port 80, it isn't configurable.
2. A temporary self-signed cert is generated first so Apache's HTTPS vhost can start at all.
3. Apache comes up with `egeria-quickstart-letsencrypt.yaml` applied — port 80 mapped, and an
   ACME webroot mounted. The plain-HTTP vhost exempts `/.well-known/acme-challenge/` from its
   redirect-to-HTTPS rule specifically so Let's Encrypt's validator can reach it.
4. `letsencrypt-cert.sh` runs `certbot` (via the official `certbot/certbot` container image —
   nothing to install on the host) against the now-live webroot, and installs the result into
   the same `server.crt`/`server.key`/`server-ca.crt` layout.
5. Apache restarts to load the real cert (it doesn't hot-reload cert files).
6. If any step fails — domain not resolving yet, port 80 blocked — a warning is logged and the
   demo **keeps running on the temporary self-signed cert** rather than aborting.

The contact email Let's Encrypt uses for expiry notices is the same `ADMIN_BOOTSTRAP_EMAIL` you
already provide for the admin account — no separate prompt.

**Renewal**: Let's Encrypt certificates expire after 90 days. Schedule `renew-certs.sh` via cron
or a systemd timer on the demo host:

```cron
0 3 * * * cd /path/to/egeria-workspaces && ./renew-certs.sh >> runtime-volumes/letsencrypt/renew.log 2>&1
```

It's safe to run as often as daily: `certbot` only actually reissues a certificate once it's
within 30 days of expiry, and `renew-certs.sh` only restarts Apache when the certificate file on
disk actually changed — a no-op check causes no service interruption. It exits early (without
touching anything) if the deployment isn't using Let's Encrypt (i.e. `CERT_DIR` in `.env.demo`
isn't the Let's Encrypt output path).

### Cookie security

Cookies are set with `Secure=true` automatically whenever `SITE_URL` starts with `https://` —
true by default in every mode now that HTTPS is always on. No manual configuration needed.

---

## Authentication models

The three modes intentionally use **different** auth models — this is by design, not drift
(see `BACKLOG.md`'s SHARE-1/SHARE-2/SHARE-3 notes for the shared-vs-per-env code convention
behind it):

### Quickstart, non-demo (default)

No auth gating at all. The portal opens straight through — appropriate for local, single-user
development against pre-loaded Coco Pharmaceuticals data.

### Quickstart `--demo`

Full registration/login flow, backed by Postgres (`demo_auth` schema in the shared
`coco_pharma` database) — JWT session cookies, email verification via Resend (optional; leave
`RESEND_API_KEY` blank to require manual verification via `/admin` instead), persona picker,
admin bootstrap account. Full reference:
[`compose-configs/egeria-quickstart/PyegeriaWebHandler/demo-mode.md`](../compose-configs/egeria-quickstart/PyegeriaWebHandler/demo-mode.md)
(see its own **Security checklist** section before making a demo deployment public).

### Freshstart

No SQLite/Postgres user store — Egeria itself is the user store, via its SecurityOfficer API.
Initial login is `bootstrap` / `secret` (forces a password change on first use); the portal
admin creates further accounts through the Admin panel. `EGERIA_ADMIN_USERS` (comma-separated
Egeria user IDs) controls who gets portal admin access. Full reference:
[`compose-configs/egeria-freshstart/README.md`](../compose-configs/egeria-freshstart/README.md#portal-and-authentication).

---

## What's exposed on which port

| Port | Service | Exposed by default? |
|---|---|---|
| 8885 / 7885 | Apache HTTP (redirect-only) | yes |
| 8843 / 7843 | Apache HTTPS (self-signed unless `CERT_DIR` set) | yes |
| 443 | Apache HTTPS, quickstart `--demo` only | only in `--demo` |
| 80 | ACME HTTP-01 challenge, quickstart `--demo` + Let's Encrypt only | only when using the automatic Let's Encrypt fallback |
| 8000 / 7000-range | FastAPI (`pyegeria-web`), direct | **no** — only reachable inside the Docker network; all external traffic goes through Apache |
| 9443 / 8443 | Egeria platform (OMAG server's own HTTPS) | yes — unrelated to the Apache-fronted portal, Egeria terminates its own TLS |

---

## Multi-host deployments

`quick-start-multi-host` and `fresh-start-multi-host` use the exact same TLS mechanism as their
`-local` counterparts (same `CERT_DIR`/`.env.ssl`/self-signed-fallback logic — they're the same
Docker Compose project, just with a cluster network overlay instead of the local one). They have
no `--demo` equivalent, so no Let's Encrypt automation — supply a real `CERT_DIR` via `.env.ssl`
if you need a browser-trusted certificate for a multi-host deployment reachable by real DNS.
