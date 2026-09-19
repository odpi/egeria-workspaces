# Tinderbox export mechanics (DrEgeria-Specs-<Month>.tbx)

**Retired as of 2026-08-05 — historical reference only, not part of the
active workflow.** The user confirmed they will not maintain the Tinderbox
file going forward; all compact-spec edits (attributes/bundles/commands) go
through the Dr.Egeria Spec Editor's REST API instead (see SKILL.md Step 1),
and there is no mirroring step back into Tinderbox anymore. This document's
value now is purely as background — the document-structure conventions
described below may still be useful if a change is big enough to need
hand-crafting new cross-family structure directly in the compact JSON, but
Tinderbox itself is no longer touched.

The Tinderbox document gets copied to a new file each month —
`DrEgeria-Specs-June.tbx` was succeeded by `DrEgeria-Specs-July.tbx` (same
underlying content/UUID, just a new monthly filename). **Always confirm the
current filename with `mcp__tinderbox__get_document` before referencing a
path** — don't hardcode a month.

Everything below was discovered live from the open document via the
`mcp__tinderbox__*` tools — use those tools (`get_notes`, `evaluate`) to
re-verify any of this if the document structure has changed since (verified
against `DrEgeria-Specs-July.tbx` as of 2026-07-02).

## Document structure per family

```
/Command Specifications/<Family> - Refactored/
├── Common Attribute Definitions/   one note per attribute, Prototype: Attribute
├── Attribute Bundles/              one note per bundle, Prototype: Attribute Bundle
├── Commands/                       one note per command, Prototype: Element
├── Commands-Agent/                 agent for browsing commands
├── Egeria Types/                   reference notes for Egeria UML types
└── Docs/                           README + export notes for this family
```

Some families use slightly different sub-container names (e.g. Projects has
`Bundles - Projects` / `Commands - Projects` instead of the generic names) —
check the actual container's children before assuming.

## How export is wired

The family container note (e.g. `/Command Specifications/Governance Officer - Refactored`)
has `$HTMLExportTemplate` pointing at a per-family template under
`/Templates/`, named `JSON-Compact-Export-<Family>` (naming varies slightly:
`JSON-Compact-Export-Governance-Officer`, `JSON-Compact-Export-Collections`,
`JSON-Compact-Export-SolutionArchitect`, etc. — check
`$HTMLExportTemplate` on the container rather than guessing the template
note's name).

That template's `$Text` looks like:

```
{
"family": "Governance Officer",
"exported": "^value(date("today"))^",
"attribute_definitions": {
^include("/Command Specifications/Shared Attribute Definitions", "JSON-Compact-AttrDefs-Container")^,
^include("/Command Specifications/Governance Officer - Refactored/Family Attribute Definitions", "JSON-Compact-AttrDefs-Container")^
},
"bundles": {
^include("/Command Specifications/Common Bundles", "JSON-Compact-Bundles-Container")^,
^include("/Command Specifications/Governance Officer - Refactored/Attribute Bundles", "JSON-Compact-Bundles-Container")^
},
"commands": {
^include("/Command Specifications/Governance Officer - Refactored/Commands", "JSON-Compact-Commands-Container")^
}
}
```

`^include(path, "ContainerTemplate")^` applies a per-note template
(`JSON-Compact-AttrDef`, `JSON-Compact-Bundle`, `JSON-Compact-Command`) to
every child note at `path`, formatting each as one JSON entry.

**Verified ground truth on how each per-note template actually decides its
content** (read directly from each template's `$Text` action-code — don't
trust README prose over this, it's been wrong before):

- **`JSON-Compact-Bundle`** (one bundle → `own_attributes`):
  `if ($ChildCount > 0)` → iterates the bundle note's real alias children via
  `$Name(children)`. **Only when there are zero children** does it fall back
  to parsing `$BundleOwnAttributes` (text, comma-separated). So the
  authoritative source is the actual alias structure whenever any exists —
  `$BundleOwnAttributes` is a convenience shortcut for bundles with no
  aliases at all, not a general override. If a bundle has real children, its
  `$BundleOwnAttributes` text is simply ignored, whatever it says.
- **`JSON-Compact-Command`** (one command → its fields + `custom_attributes`):
  scalar fields (verb, family, display_name, qn_prefix, description,
  find_method, find_constraints, OM_TYPE, upsert, attach, level, ...) come
  from `$DisplayedAttributes($IDString)` — inherited via the `Element`
  prototype, so setting the attribute value is enough, no extra step needed.
  `custom_attributes` is `if ($HasCustomAttributes & $ChildCount > 0)` →
  children only. **There is no text-field fallback for commands at all** —
  if `$HasCustomAttributes=true` but the command note has zero children,
  `custom_attributes` exports as an empty `[]`, silently. Custom attributes
  on a command are real Tinderbox aliases, full stop.
- **`JSON-Compact-AttrDef`** (one attribute definition): same
  `$DisplayedAttributes($IDString)` pattern, inherited via the `Attribute`
  prototype.

Practical implication: when adding attributes to a bundle or custom
attributes to a command, create the real alias children (drag-with-option in
Tinderbox, or Note > Duplicate as Alias) — that's what actually gets
exported. Setting `$BundleOwnAttributes` text alongside is harmless
(descriptive, matches what a human reading the bundle note would expect) but
functionally inert once real children exist, and doesn't work at all for a
command's `custom_attributes` (no fallback exists there).

**`^include()` requires a literal string path — no dynamic expressions.**
This is why every family needs its own hardcoded export template instead of
one generic parameterized template (there is an experimental
`JSON-Compact-Export-Family` template using `$FamilyPath($IDString)`, but
per the in-document README this approach doesn't actually work for
`include()` — don't rely on it).

The per-family export template notes themselves have `$HTMLDontExport=true`
— they are not meant to be bulk-exported directly, only referenced as
another note's `$HTMLExportTemplate`.

## How to actually trigger export (GUI step, not scriptable via MCP)

1. Confirm the current month's file via `mcp__tinderbox__get_document` and
   open it in Tinderbox if it isn't already (e.g. `DrEgeria-Specs-July.tbx`).
2. Select the family container note, e.g.
   `/Command Specifications/Governance Officer - Refactored`.
3. View > Preview. The rendered JSON appears (resolved via the container's
   `$HTMLExportTemplate`).
4. Copy the JSON text out of the Preview pane.
5. Save it, overwriting the matching file in
   `egeria-python/md_processing/data/compact_commands/` (see mapping below).

The `mcp__tinderbox__evaluate` / `get_notes` tools can browse and verify the
note structure (confirm `$HTMLExportTemplate`, check bundle/attribute
values, spot typos) but **cannot render the final export text** —
`^include()`/`^value()` are export-code, resolved only by Tinderbox's own
export/preview engine, not by the action-code `evaluate` tool. So step 3-4
above has no MCP shortcut today; it's a manual copy from the GUI.

## Family → destination filename mapping

| Family (as it appears in the exported JSON's `"family"` field) | File in `md_processing/data/compact_commands/` |
|---|---|
| Actor Manager | `commands_actor_manager_compact.json` |
| Collections | `commands_collections_compact.json` |
| Data Designer | `commands_data_designer.json` (note: no `_compact` suffix, inconsistent with the rest) |
| Digital Products | `commands_digital_products_compact.json` |
| External References | `commands_external_references_compact.json` |
| Feedback | `commands_feedback_compact.json` |
| Glossary | `commands_glossary_compact.json` |
| Governance Officer | `commands_governance_officer_compact.json` |
| Projects | `commands_project_compact.json` (note: filename is singular "project", family name is plural "Projects") |
| Report | `commands_report_compact.json` |
| Solution Architect | `commands_solution_architect_compact.json` |

After overwriting the file, continue with Step 1 of `SKILL.md`
(`validate_compact_specs`).

## Adding a new command, attribute, or family (condensed from the in-document READMEs)

Full guides live in Tinderbox at
`/Command Specifications/Docs/README - How to Use This Structure` (general)
and the per-family `Docs/README - How to Use This Structure` (e.g.
Governance Officer's is more detailed). Condensed:

**New attribute:** create a note in `<Family>/Family Attribute Definitions/`
(newer families use this name; some older ones still say `Common Attribute
Definitions` — check the actual container) or the shared
`/Command Specifications/Shared Attribute Definitions/` if it's cross-family.
Set `$Prototype="Attribute"`, `variable_name`, `style`, `type` (see below —
easy to get wrong), `description`, `level`, `input_required`,
`min_cardinality`, `max_cardinality`, `default_value`, `isNullable`. To use
it in a bundle or command, create a real alias child there (see "how each
template actually decides its content" above) — a text-field shortcut only
works for bundles with zero other children, and doesn't exist at all for
commands.

`style` vs `type` — both exist and both matter, don't confuse them:
`style` is the human-facing attribute-editing hint (`Simple`, `Simple Int`,
`Bool`, `Simple List`, `Dictionary`, `Reference Name`, `Enum`); `type` is
Tinderbox's own value-type field, and it does **not** default sensibly —
new attributes default to `type: string` regardless of style, and need
setting explicitly to match: `Bool`→`boolean`, `Simple Int`→`int`,
`Dictionary`→`dictionary`, `Simple List`→`List[Str]`, `Reference Name`→
leave blank (confirmed against `Governance Control 1`). Check an existing
attribute of the same `style` for the exact `type` string rather than
guessing.

**New command:** create a note in `<Family>/Commands/`,
`$Prototype="Element"`, set `verb`, `display_name`, `qn_prefix`, `family`,
`description`, `level`, `find_method`, `find_constraints`, `upsert`,
`attach`, `bundle` (an existing bundle name — the live document's actual
attribute is `bundle`, lowercase; some READMEs say `$AttributeBundle`, but
that's not what's actually on real command notes). If it needs attributes
beyond the bundle, set `$HasCustomAttributes=true` and add real alias
children pointing at attributes in Family/Shared Attribute Definitions —
this is the only way custom_attributes reaches the export, there's no
fallback.

**New bundle:** create a note in `<Family>/Attribute Bundles/`, set
`$BundleInherits` (name of parent bundle, single inheritance). For its own
attributes, add real alias children (authoritative) — also set
`$BundleOwnAttributes` (comma-separated names) to match, for a human
reading the note, even though it's only actually read as a fallback when the
bundle has zero children.

**New family:** create a container under `/Command Specifications/`.
`$Prototype="Family Prototype"` exists and is used by every family
container, but **it does not auto-create anything** — it's a plain
prototype with no `OnAdd` action, purely cosmetic/organizational. Manually
create the substructure: `Family Attribute Definitions/`,
`Attribute Bundles/`, `Commands/`, `Docs/` (skip `Commands-Agent/`/
`Egeria Types/` unless you want them — they're not required for export).
Then copy an existing `JSON-Compact-Export-*` template, repoint its three
`^include()` paths + `"family"` field at the new family (remember bundles
often need a cross-family include too, e.g. Action Author includes
Governance Officer's Attribute Bundles for `Governance Control Base` — same
accepted pattern as Digital Products → Collections), and set the new
container's `$HTMLExportTemplate` to that new template.

As with everything else here — don't hand-build the compact JSON, make the
change in Tinderbox and export.
