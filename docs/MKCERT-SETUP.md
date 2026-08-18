<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Trusting local HTTPS certs with mkcert

How to get rid of the "your connection is not private" browser warning on quickstart/freshstart's
self-signed HTTPS, for local development. This replaces the auto-generated self-signed cert
(`generate-certs.sh`) with one that's actually trusted by your OS/browser — no more clicking
through the interstitial (or, worse, hitting a hard `ERR_CERT_COMMON_NAME_INVALID` if the
auto-generated cert has no Subject Alternative Names for the hostname you're using).

This is a per-machine, local-dev-only setup. It is **not** an alternative to Let's Encrypt for a
real public deployment — see [`SECURITY-CONFIGURATION.md`](SECURITY-CONFIGURATION.md#lets-encrypt-automatic-quickstart---demo-only)
for that. mkcert only works because it installs a *private* CA that only your machine trusts;
Let's Encrypt requires a publicly-resolvable domain name and validates ownership of it over the
open internet (HTTP-01/DNS-01/TLS-ALPN-01) — an email address does not substitute for that, and
it cannot issue for `localhost`, private IPs, or `.local` hostnames at all.

## How it works

1. `mkcert -install` creates a private CA (once per machine) and adds it to your OS's system
   trust store (and, separately, to Firefox/NSS-based browsers' trust store if the `nss` tooling
   is present).
2. `mkcert <hostnames...>` mints a leaf certificate signed by that CA for whichever hostnames you
   list — `localhost`, `127.0.0.1`, `::1`, and your machine's hostname are the ones this repo's
   Apache config needs (see `HOST_FQDN` in `compose-configs/egeria-quickstart/.env`).
3. Drop the resulting cert into `CERT_DIR` in the same three-file layout (`server.crt`,
   `server.key`, `server-ca.crt`) that `generate-certs.sh` already produces, and restart Apache —
   see [`SECURITY-CONFIGURATION.md`](SECURITY-CONFIGURATION.md#https--tls) for exactly where
   `CERT_DIR` is configured per deployment mode.

## macOS

```bash
brew install mkcert
mkcert -install          # prompts for your password (adds the CA to the System keychain)
```

If `mkcert -install` fails with `sudo: a terminal is required...`, it's being run non-interactively
(e.g. through a script or another program's shell-out) — `sudo` needs an actual TTY to prompt for
your password. Run it directly in Terminal.app/iTerm instead.

If you'd rather avoid the terminal/sudo prompt entirely, trust the CA through the GUI instead:

1. Open **Keychain Access**.
2. File → Import Items… → select `~/Library/Application Support/mkcert/rootCA.pem` → import into
   the **System** keychain (macOS prompts for your password here, which works fine since it's a
   GUI app, not a headless shell).
3. Find "mkcert development CA" in the list, double-click it, expand **Trust**, set "When using
   this certificate" to **Always Trust**, close, and confirm with your password.

Then generate and install the cert:

```bash
cd /path/to/dir/for/certs
mkcert -cert-file server.crt -key-file server.key localhost 127.0.0.1 ::1 <your-hostname>
cp "$(mkcert -CAROOT)/rootCA.pem" server-ca.crt

# point CERT_DIR at that directory (.env.ssl / .env.demo — see SECURITY-CONFIGURATION.md),
# or copy the three files directly into the existing CERT_DIR, then:
docker restart quickstart-web-server   # or freshstart-web-server
```

## Linux

```bash
# Debian/Ubuntu:
sudo apt install libnss3-tools
# Fedora/RHEL:
sudo dnf install nss-tools
# Arch:
sudo pacman -S nss

# then install mkcert itself — either your distro's package (if available) or the prebuilt binary:
#   https://github.com/FiloSottile/mkcert#installation
mkcert -install
```

`libnss3-tools`/`nss-tools` is what lets `mkcert -install` also trust the CA for Firefox and other
NSS-based browsers; without it, mkcert still creates and system-trusts the CA (so Chrome/Chromium,
which use the OS store, work fine), it just can't reach into Firefox's separate NSS database.
`mkcert -install` here does its own `sudo` internally when it needs to touch the system trust
store — same TTY requirement as macOS: run it in a real terminal, not through a non-interactive
script.

Cert generation and installation into `CERT_DIR` are identical to the macOS steps above:

```bash
cd /path/to/dir/for/certs
mkcert -cert-file server.crt -key-file server.key localhost 127.0.0.1 ::1 <your-hostname>
cp "$(mkcert -CAROOT)/rootCA.pem" server-ca.crt
docker restart quickstart-web-server   # or freshstart-web-server
```

## Windows

```powershell
choco install mkcert
# or: scoop bucket add extras; scoop install mkcert

mkcert -install
```

`mkcert -install` adds the CA to the Windows certificate store via `certutil`, which Chrome and
Edge pick up automatically (they use the OS store on Windows). Firefox needs the NSS tooling too —
mkcert's installer prints a warning and skips Firefox trust if it isn't found; see mkcert's own
README for the NSS package needed on Windows if you use Firefox.

Run from an elevated (Administrator) PowerShell or Command Prompt — same underlying reason as the
`sudo` requirement on macOS/Linux: writing to the system trust store needs admin rights, and that
prompt needs an interactive session to answer.

```powershell
cd C:\path\to\dir\for\certs
mkcert -cert-file server.crt -key-file server.key localhost 127.0.0.1 ::1 <your-hostname>
copy "$(mkcert -CAROOT)\rootCA.pem" server-ca.crt
docker restart quickstart-web-server   # or freshstart-web-server
```

(If you're running the Docker host itself inside WSL2 rather than Windows directly, treat that as
the Linux case above — WSL2 has its own filesystem and trust store, separate from Windows'.)

## Renewing / adding a hostname later

Certs `mkcert` generates are valid for about 2.5 years (no separate renewal automation like
Let's Encrypt's `renew-certs.sh`). If you need to add another hostname, or the cert expires, just
rerun the `mkcert -cert-file ... <hostnames>` command with the updated list and restart Apache —
the CA itself (from `mkcert -install`) doesn't need to be recreated or re-trusted.
