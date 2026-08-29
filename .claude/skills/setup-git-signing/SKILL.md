---
name: setup-git-signing
description: One-time setup for commit signing on a new machine for the egeria-workspaces repo — generating a per-machine SSH signing key, configuring 1Password's SSH agent (Linux deb or snap package), registering the machine in the allowed_signers roster, and setting up git push over SSH. Use when commits are failing to sign on a machine that hasn't been configured yet, when signature verification reports an unknown key, or when explicitly asked to set up git signing on a new machine.
---

# Setting up git commit signing on a new machine

Multiple machines commit to this repo — cray, hedwig, laz, and others. The
canonical author identity is `Dan Wolfson <dan.wolfson@pdr-associates.com>` —
confirm with `git log --format='%an <%ae>' | sort -u`. The **signing key is
per-machine, not shared** — generate a fresh one on each machine and register
it as its own GitHub **Signing Key** (Settings → SSH and GPG keys → New SSH
key → Signing Key). Multiple signing keys per account is normal and expected;
don't copy a private key between machines.

Signing config belongs in **global** config (`~/.gitconfig`), not a repo's
`.git/config` — `~/.gitconfig` is already per-machine, so a per-machine
`user.signingkey` lives there correctly, and every clone on the machine then
signs without per-repo setup:

```bash
git config --global user.name       "Dan Wolfson"
git config --global user.email      "dan.wolfson@pdr-associates.com"
git config --global user.signingkey "ssh-ed25519 AAAA...<this machine's key>"
git config --global gpg.format      ssh
git config --global gpg.ssh.program <op-ssh-sign path, see below>
git config --global commit.gpgsign  true
```

This repo additionally needs `git config --local core.hooksPath .githooks`
(repo-local by nature) to activate the DCO `commit-msg` hook. It is not
inherited from a clone — set it in every fresh clone, or commits will skip
the `Signed-off-by` check locally and only fail in CI.

If signing via 1Password's SSH agent on Linux, the `gpg.ssh.program` path
depends on how 1Password was installed:
- **deb package** (cray, as of 2026-08) → `/opt/1Password/op-ssh-sign`.
- **snap package** → `/snap/1password/current/app/op-ssh-sign` — use the
  `current` symlink, not a version-pinned path (snap revisions bump).

Migrating snap → deb changes both this path and the agent socket path, and
silently breaks signing until both are updated.

The snap-specific socket workaround below applies only to snap installs:
- The snap sandbox can't create the usual `~/.1password/agent.sock`
  compatibility symlink. If `op-ssh-sign` fails with "Could not connect to
  socket" or "failed to fill whole buffer", find the real agent socket with
  `ss -xlp | grep 1password` — it's
  `~/snap/1password/current/.1password/agent.sock`, **not** the other
  `s.sock` under `/run/user/<uid>/snap.1password/` (that one exists too but
  isn't the agent-protocol socket). Symlink it:
  `ln -sf ~/snap/1password/current/.1password/agent.sock ~/.1password/agent.sock`.
- Enable 1Password's SSH Agent first (Settings → Developer → "Use the SSH
  Agent"), and create/import the key there as an SSH Key item.

For `git push` over SSH: switch the remote
(`git remote set-url origin git@github.com:dwolfson/egeria-workspaces.git`),
add the same public key to GitHub *again* as an Authentication Key (separate
from the Signing Key entry), and point `~/.ssh/config`'s `Host github.com` at
the same agent via `IdentityAgent ~/.1password/agent.sock`.

First connection to any new host (GitHub, or a Tailscale peer) fails
non-interactively on host key verification — accept once with
`ssh -o StrictHostKeyChecking=accept-new <host>` before scripting anything
against it.

## Verifying signatures — the allowed_signers roster

Signing works without it, but `git log --show-signature` (and `%G?`) will fail
with `gpg.ssh.allowedSignersFile needs to be configured and exist` until each
machine has a local roster of the keys it should trust:

```bash
mkdir -p ~/.config/git
git config --global gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers
```

One line per trusted key, restricted to the `git` namespace:

```
dan.wolfson@pdr-associates.com namespaces="git" ssh-ed25519 AAAA...
```

Because signing keys are per-machine and this file is **not** synced by git,
adding a new machine means appending its public key to `allowed_signers` on
every *other* machine you verify from — otherwise that machine's commits read
as unverified there. Keep each entry commented with the machine name, install
flavour, and commit-count/date range so an unfamiliar key can be traced later.

To see which keys have actually signed here and whether the local roster
covers them:

```bash
.claude/skills/setup-git-signing/list-signing-keys.sh
```

It flags each key `trusted` or `UNTRUSTED`; an `UNTRUSTED` key is either a
machine missing from the roster or something that warrants a closer look.

**`E` status on GitHub merge commits is normal and not a roster problem.** PRs
merged on github.com are signed with GitHub's *PGP* web-flow key, not SSH, so
git can only verify them if that key is in the local GPG keyring. Roughly a
third of this repo's history is such merges.
