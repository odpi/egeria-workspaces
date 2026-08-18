---
name: setup-git-signing
description: One-time setup for commit signing on a new machine for the egeria-workspaces repo — generating a per-machine SSH signing key, configuring 1Password's SSH agent (Linux snap package), and setting up git push over SSH. Use when commits are failing to sign on a machine that hasn't been configured yet, or when explicitly asked to set up git signing on a new machine.
---

# Setting up git commit signing on a new machine

Multiple machines commit to this repo (currently at least cray and hedwig). The
canonical author identity is `Dan Wolfson <dan.wolfson@pdr-associates.com>` —
confirm with `git log --format='%an <%ae>' | sort -u`. The **signing key is
per-machine, not shared** — generate a fresh one on each machine and register
it as its own GitHub **Signing Key** (Settings → SSH and GPG keys → New SSH
key → Signing Key). Multiple signing keys per account is normal and expected;
don't copy a private key between machines.

If signing via 1Password's SSH agent (the snap package, on Linux):
- `git config gpg.ssh.program` → `/snap/1password/current/app/op-ssh-sign` —
  use the `current` symlink, not a version-pinned path (snap revisions bump).
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
