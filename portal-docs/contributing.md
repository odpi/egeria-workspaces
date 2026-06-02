# Adding Documentation

This guide explains how the portal-docs system works and how to add new pages.

---

## How it works

The `portal-docs/` directory in the repository is bind-mounted into the Apache container at `/usr/local/apache2/htdocs/docs`, making it available at the `/docs/` URL. Changes to files in `portal-docs/` take effect immediately — no container restart needed.

Two special files drive the documentation hub:

| File | Purpose |
|------|---------|
| `index.html` | The card grid hub at `/docs/` |
| `viewer.html` | Markdown renderer — fetches and renders any `.md` file within `portal-docs/` |

The viewer is accessed as `viewer.html?src=path/to/file.md` where the path is relative to `portal-docs/`.

---

## Directory structure

```
portal-docs/
  index.html            ← documentation hub (edit to add cards)
  viewer.html           ← markdown renderer (do not edit for content)
  contributing.md       ← this file
  tools/                ← docs that apply to both environments
    dr-egeria/
      overview.md
      templates-basic.md
      templates-advanced.md
    egeria-explorer.md
    obsidian.md
    jupyter.md
    egeria-advisor.md
  quickstart/           ← Quickstart-specific docs
    overview.md
    local/
    demo/
    coco/
  freshstart/           ← Freshstart-specific docs
    overview.md
    getting-started.md
```

---

## Adding a new page

**Step 1** — Create a Markdown file in the appropriate subdirectory:

- `tools/` — applies to both Quickstart and Freshstart
- `quickstart/` — Quickstart-specific
- `freshstart/` — Freshstart-specific

**Step 2** — Add a card to `index.html`:

```html
<a class="card" href="viewer.html?src=tools/my-topic.md">
  <div class="card-icon">📄</div>
  <div class="card-name">My Topic</div>
  <div class="card-desc">One-line description shown on the card.</div>
  <span class="card-tag tag-tool">Tool</span>
</a>
```

Available tag styles:

| Class | Colour | Use for |
|-------|--------|---------|
| `tag-tool` | Blue | Both environments |
| `tag-qs` | Green | Quickstart only |
| `tag-fs` | Purple | Freshstart only |

**Step 3** — Add the page slug to `_LABELS` in `viewer.html` so the breadcrumb renders correctly:

```javascript
'my-topic': 'My Topic',
```

That's it. No server restart needed.

---

## Markdown features

The viewer supports:

- Standard GitHub-flavoured Markdown (tables, task lists, fenced code blocks)
- Mermaid diagrams in ` ```mermaid ``` ` blocks
- Syntax highlighting for code blocks (via highlight.js)
- Auto-generated table of contents (when the page has ≥ 2 headings)
- Internal links to other `.md` files — write them as relative paths and the viewer rewrites them automatically: `[see also](../tools/obsidian.md)`

**Important:** Do not use `../` to escape `portal-docs/` — the viewer strips `../` from `src` parameters as a security measure.

---

## Template file locations

The Dr. Egeria command templates in `templates/` (repo root) are mounted into both environments:

| Environment | URL path | Obsidian vault path |
|-------------|----------|---------------------|
| Quickstart | `/Dr-Egeria-Samples/templates/` | `Dr-Egeria-Samples/templates/` |
| Freshstart | `/Dr-Egeria-Samples/templates/` | *(no Obsidian container)* |

Templates are organised as `templates/basic/<Category>/` and `templates/advanced/<Category>/`. Both levels are browsable via Apache directory listing and directly openable in Obsidian.

The portal-docs pages `tools/dr-egeria/templates-basic.md` and `tools/dr-egeria/templates-advanced.md` are narrative summaries. The live browsable files are at the paths above.

---

## Apache fetch behaviour

The Apache rewrite rule redirects bare `.md` requests to the SSI markdown renderer. The viewer bypasses this by sending `X-Requested-With: XMLHttpRequest` with its fetch, which matches the rewrite skip condition — Apache then serves the raw file directly. Any new fetch of a `.md` file outside the viewer should include this header.
