# Feedback Analyst Guide

SQL recipes for querying the `demo.feedback` table in the shared Postgres instance (`coco_pharma` database, port 5442).

Connect: `psql -h localhost -p 5442 -U demo_user -d coco_pharma`

---

## Schema reference

```sql
SELECT column_name, data_type FROM information_schema.columns
WHERE table_schema = 'demo' AND table_name = 'feedback'
ORDER BY ordinal_position;
```

| Column | Type | Notes |
|---|---|---|
| id | varchar(36) | UUID primary key |
| session_id | varchar(36) | Browser session |
| user_id | varchar(200) | JWT sub (demo/freshstart) or email (local) |
| env | varchar(40) | `quickstart-demo` · `quickstart-local` · `freshstart` |
| persona | varchar(100) | Active Coco persona display name |
| page | varchar(200) | Tool section / route (e.g. `glossary`, `tech-catalog/apis`) |
| element_guid | varchar(36) | Egeria element in view, if any |
| rating | integer | 1–5 stars, nullable |
| category | varchar(40) | `bug` · `confusing` · `suggestion` · `praise` |
| message | text | Free-text |
| email | varchar(200) | For follow-up |
| wants_response | boolean | User requested a reply |
| consent_to_contact | boolean | User consented to contact |
| build_version | varchar(80) | Git SHA / `BUILD_VERSION` env var |
| user_agent | varchar(500) | Browser user-agent string |
| viewport | varchar(20) | e.g. `1920x1080` |
| locale | varchar(20) | e.g. `en-US` |
| triage_status | varchar(20) | `new` · `triaged` · `actioned` |
| created_at | timestamp | UTC submission time |

---

## Common queries

### Volume by day
```sql
SELECT date_trunc('day', created_at) AS day, COUNT(*) AS submissions
FROM demo.feedback
GROUP BY 1 ORDER BY 1 DESC;
```

### Volume by page (top 20)
```sql
SELECT page, COUNT(*) AS submissions, ROUND(AVG(rating), 1) AS avg_rating
FROM demo.feedback
GROUP BY page ORDER BY submissions DESC LIMIT 20;
```

### Volume by environment
```sql
SELECT env, COUNT(*) AS submissions,
       ROUND(AVG(rating), 1) AS avg_rating,
       SUM(CASE WHEN wants_response THEN 1 ELSE 0 END) AS wants_response
FROM demo.feedback
GROUP BY env ORDER BY submissions DESC;
```

### Category breakdown
```sql
SELECT category, COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM demo.feedback
WHERE category IS NOT NULL
GROUP BY category ORDER BY n DESC;
```

### Average rating by page (pages with ≥5 ratings)
```sql
SELECT page, COUNT(*) AS n, ROUND(AVG(rating), 2) AS avg_rating
FROM demo.feedback
WHERE rating IS NOT NULL
GROUP BY page HAVING COUNT(*) >= 5
ORDER BY avg_rating ASC;
```

### Response queue — needs reply
```sql
SELECT created_at, user_id, email, page, category, message, triage_status
FROM demo.feedback
WHERE wants_response = true
  AND triage_status = 'new'
ORDER BY created_at ASC;
```

### Bugs and confusing pages
```sql
SELECT page, category, COUNT(*) AS n, STRING_AGG(message, ' | ' ORDER BY created_at DESC) AS messages
FROM demo.feedback
WHERE category IN ('bug', 'confusing')
GROUP BY page, category ORDER BY n DESC;
```

### New submissions since a given date
```sql
SELECT * FROM demo.feedback
WHERE created_at >= '2026-06-01'
  AND triage_status = 'new'
ORDER BY created_at DESC;
```

### Submissions by persona (demo env)
```sql
SELECT persona, COUNT(*) AS submissions, ROUND(AVG(rating), 1) AS avg_rating
FROM demo.feedback
WHERE env = 'quickstart-demo' AND persona IS NOT NULL
GROUP BY persona ORDER BY submissions DESC;
```

### Unique active users (by env, last 30 days)
```sql
SELECT env, COUNT(DISTINCT user_id) AS unique_users
FROM demo.feedback
WHERE created_at >= NOW() - INTERVAL '30 days'
  AND user_id IS NOT NULL
GROUP BY env;
```

### Triage status overview
```sql
SELECT triage_status, COUNT(*) AS n,
       SUM(CASE WHEN wants_response THEN 1 ELSE 0 END) AS awaiting_reply
FROM demo.feedback
GROUP BY triage_status ORDER BY n DESC;
```

### Mark old new submissions as triaged (bulk triage)
```sql
UPDATE demo.feedback
SET triage_status = 'triaged'
WHERE triage_status = 'new'
  AND created_at < NOW() - INTERVAL '7 days';
```

---

## Admin panel

The Feedback tab in each environment's admin panel (`/admin`) provides a live view with status and environment filters and an inline triage dropdown. Use SQL directly for bulk operations, trend analysis, or cross-environment queries.
