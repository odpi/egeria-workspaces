# Quickstart — Demo Environment

Demo mode enables public access to the Quickstart stack with user registration, persona selection, and a managed Obsidian session. It is designed for running structured demonstrations to external audiences.

---

## Enabling demo mode

In `compose-configs/egeria-quickstart/.env`:

```
DEMO_MODE=true
JWT_SECRET=<long-random-string>         # change before going public
ADMIN_BOOTSTRAP_EMAIL=you@example.com
ADMIN_BOOTSTRAP_PASSWORD=<strong-password>
```

Optionally configure email notifications (magic-link registration):
```
RESEND_API_KEY=re_...
RESEND_FROM=noreply@yourdomain.com
```

---

## User flow

1. Visitor arrives at the portal → redirected to `/login`
2. They register with email + password → receive a verification email
3. After verifying → they reach the portal and choose a persona
4. The persona sets their Egeria credentials for Explorer and Dr. Egeria

---

## Personas

Each persona represents a [Coco Pharmaceuticals](../coco/overview.md) employee with a different role and focus. Choosing a persona sets:
- The Egeria user ID and password used for all API calls
- The Dr. Egeria plugin credentials (auto-populated when acquiring Obsidian)
- The highlighted tools shown in the bio card

See [Coco Pharmaceuticals personas](../coco/personas.md) for the full list.

---

## Obsidian in demo mode

The containerised Obsidian instance is shared among all demo users. The portal manages access with a session lock:

- Users acquire a timed session (default 20 min) before Obsidian opens
- Credentials are injected automatically from the selected persona
- Admins can reserve blocks, evict current holders, and view the audit log

See [Obsidian session management](obsidian-sessions.md) for full details.

---

## Admin responsibilities

- Monitor and manage registered users in the [Admin panel](admin-guide.md)
- Set the Egeria reset schedule if you want the metadata store refreshed periodically
- Create Obsidian reservations before scheduled presentations
