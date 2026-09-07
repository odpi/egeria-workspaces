---
name: setup-git-signing
description: One-time setup for commit signing on a new machine for the egeria-workspaces repo — generating a per-machine SSH signing key, configuring 1Password's SSH agent (Linux deb, snap or flatpak package), registering the machine in the allowed_signers roster, and setting up git push over SSH. Use when commits are failing to sign on a machine that hasn't been configured yet, when signature verification reports an unknown key, or when explicitly asked to set up git signing on a new machine.
---

# Setting up git commit signing on a new machine

Multiple machines commit to this repo — cray, hedwig, laz, and others. The
canonical author identity is `Dan Wolfson <dan.wolfson@pdr-associates.com>` —
confirm with `git log --format='%an <%ae>' | sort -u`.

**Check for an existing vault key before generating anything.** A signing key
held in 1Password is synced by the vault, so it is present on *every* machine
signed into that account — the "one key per machine" model does not apply to
it. This account has such a key (`SSH Key - dwolfson`), and as of 2026-09-06 it
had signed 790 of this repo's commits across machines and date ranges. On a new
machine, look first:

```bash
SSH_AUTH_SOCK=~/.1password/agent.sock ssh-add -L
```

If that returns a key, use it — no generation, no new GitHub Signing Key entry,
and no `allowed_signers` change on other machines, because they already trust
it. Compare its fingerprint against `list-signing-keys.sh` output to confirm it
is the one already in the history.

Only if there is no vault key does the per-machine model apply: generate a fresh
key on that machine and register it as its own GitHub **Signing Key** (Settings
→ SSH and GPG keys → New SSH key → Signing Key). Multiple signing keys per
account is normal; never copy a locally-generated private key between machines.

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
- **flatpak package** →
  `~/.local/share/flatpak/app/com.onepassword.OnePassword/current/active/files/extra/1Password/op-ssh-sign`
  — again the `current/active` symlink, not the commit-hash path underneath it,
  which changes on every update. **But prefer the deb: see the flatpak section
  below for why flatpak cannot support the `op` CLI at all.**

Migrating between packaging flavours changes both this path and the agent
socket path, and silently breaks signing until both are updated.

**A missing `op-ssh-sign` at the deb and snap paths does NOT mean 1Password is
absent.** Check the packaging before concluding anything:
`flatpak list | grep -i 1password`, `dpkg -l | grep -i 1password`,
`snap list | grep -i 1password`.

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

## The flatpak package: use the deb instead

Verified on pop-os (Pop!_OS 24.04, flatpak 1Password 8.12.12) on 2026-09-06.
**The flatpak cannot support the `op` CLI, so migrate to the deb.** The SSH
agent alone can be made to work, but only with the override below.

The flatpak publishes its integration sockets *inside its own mount namespace*.
`ss -xlp | grep 1password` lists paths that look ordinary and are not reachable
from the host at all — a sharper failure than snap's, where the socket merely
sits in an awkward but real location:

| Integration | Socket the app opens | Reachable from host? |
|---|---|---|
| SSH agent | `~/.1password/agent.sock` | No, until the override below |
| CLI (`op`) | `/run/user/<uid>/s.sock` | **No, and not fixable** |

The CLI socket sits in the sandbox's private `tmpfs` mount of
`/run/user/<uid>`, and flatpak has no supported way to share the host's
`XDG_RUNTIME_DIR`. The symptom is `op` reporting *"connecting to desktop app:
cannot connect to 1Password app, make sure it is running"* while the app is
plainly running. Confirm the diagnosis rather than guessing — compare the host
with the sandbox, using the app's pid:

```bash
ls -la /run/user/$(id -u)/s.sock                 # absent on the host
ls -la /proc/<pid>/root/run/user/$(id -u)/s.sock # present inside the sandbox
grep '/run/user' /proc/<pid>/mounts              # tmpfs, not a host bind
```

The agent socket *is* fixable, because its path is home-relative: grant the
sandbox write access to the real directory, then restart.

```bash
mkdir -p ~/.1password && chmod 700 ~/.1password
flatpak override --user --filesystem=~/.1password:create com.onepassword.OnePassword
```

**"Restart" means killing the background process — closing the window is not
enough.** 1Password keeps running after its window closes, so the sandbox
namespace survives and the new permission does not apply. The tell is that the
pid is unchanged. Force it with `flatpak kill com.onepassword.OnePassword`,
then relaunch. Confirm the fix took by checking that the directory is now a
host bind mount, not just that the socket exists:

```bash
grep '\.1password' /proc/<new-pid>/mounts   # expect an ext4 line, not absent
SSH_AUTH_SOCK=~/.1password/agent.sock ssh-add -l
```

### Migrating flatpak → deb

Installing the deb is not sufficient on its own; two things bite:

- **A leftover flatpak process keeps squatting on `~/.1password/agent.sock`**
  even after `flatpak uninstall`, so the deb app cannot own it and the agent
  serves the wrong instance. Check with `ss -xlp | grep agent.sock` and compare
  the owning pid against the deb app's; kill the flatpak tree if it is still
  there. Once it exits, the deb app takes the socket over on its own.
- **Undo the override** afterwards, so it does not linger for a reinstalled
  flatpak: `flatpak override --user --reset com.onepassword.OnePassword`.

### "failed to fill whole buffer" is also a first-use prompt

This error is documented above as a wrong-socket symptom, but it has a second
cause that looks identical: 1Password authorises each signing binary on first
use, and when the request comes from a non-interactive shell the prompt cannot
be answered and the connection closes. Distinguish the two by calling the
signer directly — if this succeeds, the socket is fine and it was authorisation:

```bash
printf 'test\n' > /tmp/sigtest
SSH_AUTH_SOCK=~/.1password/agent.sock <op-ssh-sign path> -Y sign -n git -f <pubkey file> /tmp/sigtest
```

A successful direct call clears the authorisation, after which `git commit`
signs normally.

### Telling the three failure modes apart by their symptom

Signing failures here look alike but are distinguishable. Measured on pop-os
2026-09-06 with a direct `op-ssh-sign` call:

| Symptom | Cause | Fix |
|---|---|---|
| Instant `1Password: agent returned an error` | `SSH_AUTH_SOCK` points at another agent | see below |
| **Hangs** until killed, empty stderr | 1Password is showing an approval dialog nobody has answered | approve it on screen |
| `1Password: failed to fill whole buffer` | the request was closed before a reply — a denied/cancelled approval, or a wrong socket path | approve, or fix the path |

Time the call to tell a hang from a fast failure — a hang means a prompt is
waiting, not that anything is misconfigured:

```bash
printf 'test\n' > /tmp/sigtest
time SSH_AUTH_SOCK=~/.1password/agent.sock timeout 10 \
  <op-ssh-sign path> -Y sign -n git -f <pubkey file> /tmp/sigtest
# exit 124 after the full timeout => blocked on an approval dialog
```

**The approval dialog is the one that wastes the most time**, because a
headless or backgrounded `git commit` cannot surface it: the commit fails with
`failed to write commit object` while the dialog sits unnoticed on the desktop.
If signing worked once and then stopped, suspect this before touching config.
Approve it once, and choose the option to stop asking for that application if
you intend to script commits.

**On the wrong-agent case:** on a GNOME/COSMIC desktop `SSH_AUTH_SOCK` is
preset to gnome-keyring (`/run/user/<uid>/gcr/ssh`) in every login shell, so
`op-ssh-sign` connects there instead of to 1Password.

```bash
echo $SSH_AUTH_SOCK   # /run/user/1000/gcr/ssh  -> wrong agent
```

Point it at 1Password persistently, e.g. in `~/.bashrc`:

```bash
export SSH_AUTH_SOCK=~/.1password/agent.sock
```

This is separate from the `IdentityAgent` line in `~/.ssh/config`: that governs
`ssh` itself, and `op-ssh-sign` does not read it. Non-interactive shells that
do not source `~/.bashrc` (automation, CI, agent tooling) still need it set
explicitly.

For `git push` over SSH: switch the remote
(`git remote set-url origin git@github.com:dwolfson/egeria-workspaces.git`),
add the same public key to GitHub *again* as an Authentication Key (separate
from the Signing Key entry), and point `~/.ssh/config`'s `Host github.com` at
the same agent via `IdentityAgent ~/.1password/agent.sock`.

Check `~/.ssh/config` before adding that stanza: the deb install writes a
`Host *` block with the same `IdentityAgent` line on first run, which already
covers github.com. Appending a second entry is harmless but redundant.

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

This file is **not** synced by git, so a *locally-generated* per-machine key
must be appended to `allowed_signers` on every *other* machine you verify from,
or that machine's commits read as unverified there. A key held in 1Password
needs this only once per machine's roster, since the same key is reused
everywhere. Keep each entry commented with which it is — machine name and
install flavour for a local key, or "primary vault key" for the shared one —
plus a commit-count/date range so an unfamiliar key can be traced later.

To see which keys have actually signed here and whether the local roster
covers them:

```bash
.claude/skills/setup-git-signing/list-signing-keys.sh
```

It flags each key `trusted` or `UNTRUSTED`; an `UNTRUSTED` key is a machine
missing from the roster, the shared vault key on a machine set up before this
note existed, or something that warrants a closer look. Before assuming an
unknown key belongs to an unidentified machine, check it against
`SSH_AUTH_SOCK=~/.1password/agent.sock ssh-add -L` — a match means it is the
vault key, not a stranger.

**`E` status on GitHub merge commits is normal and not a roster problem.** PRs
merged on github.com are signed with GitHub's *PGP* web-flow key, not SSH, so
git can only verify them if that key is in the local GPG keyring. Roughly a
third of this repo's history is such merges.
