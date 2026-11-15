# Dr.Egeria: techniques and best practices

[Writing commands](overview.md#writing-commands) shows the basic shape of a command. This page covers what trips people up once a document grows: prose around the commands, examples that shouldn't run, files that are loaded again and again, and filters that have changed meaning.

Most of it follows from one fact about how Dr.Egeria reads a document, so that comes first.

---

## How Dr.Egeria reads a document

Dr.Egeria cuts the document into **blocks**. A new block starts at every line that begins with `# ` or `## `, and at every line that is only `___` or `---`. Nothing else starts a block.

A block is a **command** if its first non-blank line is a command verb followed by an object. A `## ` in front is optional. Everything else is prose, and is copied to the output unchanged.

The verbs are Add, Attach, Cancel, Classify, Clear, Count, Create, Declassify, Delete, Detach, Display, Find, Import, Initiate, Link, Process, Provenance, Publish, Reclassify, Remove, Run, Search, Set, Setup, Unlink, Update, Validate and View. Matching ignores case.

Inside a command, every `### ` heading up to the end of the block is an attribute, and the lines below it are its value.

The rules below follow from this.

---

## Close every command with `___`

A command's block runs until the next `#`, `##`, `___` or `---` line. If prose follows a command, any `###` heading in that prose becomes an attribute of the command:

```text
## Create Glossary Term
### Display Name
Customer

### How we chose this name        <- read as an attribute of the term
We looked at three candidates...
```

Dr.Egeria then reports an unknown attribute, or worse, accepts it. End each command with a line containing only `___`, and the prose after it is safe:

```text
## Create Glossary Term
### Display Name
Customer

___

### How we chose this name        <- prose
```

Between two commands the separator is optional, since the next `##` already starts a new block. Put it in anyway: it's what keeps the document safe when someone later adds prose between them.

## Don't start prose with a command verb

The block rule works the other way too. A `##` heading, or the first line after a separator or heading, that happens to begin with a verb is read as a command:

```text
___

## Process Parameter Time Series      <- read as the command "Process" "Parameter Time Series"
```

Dr.Egeria logs `No processor registered for 'Process Parameter Time Series'` and carries on. The same happens to a sentence like "Find the owner in the table below." if it's the first line after a `___`.

Reword the heading ("## The Process Parameter Time Series product"), make it `#` or `###`, which aren't read as commands, or put another line of prose before the sentence. Only the first non-blank line of a block is checked, so the same sentence further down a paragraph is fine.

## Code fences don't hide commands

Dr.Egeria ignores code fences. A command inside a ```` ```markdown ```` block (or a fence of any other language) runs like any other:

````text
```markdown
## Create Glossary Term          <- this runs
### Display Name
Customer
```
````

This is useful: a tutorial can show a command in a fence and have readers run the tutorial itself. Two things to watch:

- **End a runnable fenced command with `___` before the closing fence.** Otherwise the closing ```` ``` ```` line is part of the block, and ends up in the value of the command's last attribute.
- **A fenced example that is *not* meant to run will run too.** To show a command without running it, use a placeholder the verb list can't match, such as `## <Verb> <Object>`, or make the heading `###`. Indenting it works only if a line of prose comes first in the same block: an indented command straight after a `___` is still a command.

Check with **validate**: every command Dr.Egeria found is listed, so an example that shouldn't be there shows up.

## Write attributes as headings, not `Key: value`

An attribute is a `### ` heading with its value on the lines below. A `Key: value` line is just text. Before the first attribute it is ignored; after one, it becomes part of that attribute's value:

```text
## Create Report
Report Spec: Collections          <- ignored
### Display Name
Next Steps
Output Format: DICT               <- the display name is now "Next Steps\nOutput Format: DICT"
### Report Spec
Collections                       <- this is how to set it
```

For a multi-valued attribute, give the values as a bullet list or as one comma-separated line.

## Validate first, and expect forward references

Run a document with `validate` before `process`. Validate checks every command against Egeria without changing anything, and reports unknown attributes, missing required ones, values that aren't valid, and references it can't resolve.

A reference to an element that an **earlier command in the same document** creates, such as a Link to a term created above it, shows in validate as not found, because validate hasn't created it. That's expected. On `process` the commands run in order, so the element exists by the time the reference is resolved.

Anything else validate reports is worth fixing before you process.

---

## Make documents safe to load again

Documents in `dr-egeria-inbox` are run again and again: by auto-heal after Egeria is reset, by **Run Now** and **Run All Enabled**, and by people re-running a tutorial. See [Data Initialization](../data-initialization.md).

- **Create, Update and their synonyms are upserts.** Dr.Egeria looks the element up by its qualified name, which it derives from the display name and type unless you give one, and updates it if it exists. Running them twice is harmless.
- **Changing the display name makes a new element.** Running the document again then leaves the old element in place next to the new one. The same happens if you change the command's type, for example from `Create Agreement` to `Create Digital Subscription`, because the type is part of the qualified name. On a repository that is already loaded, delete or rename the old element first.
- **Link and Add commands are not all safe to repeat.** Some look for an existing relationship first (`Add Member to Collection`; `Link Governance Results` skips a pair that is already linked); others are not proven to. A batch counts as safe to re-run only when every Link and Add kind in it is proven to check first; otherwise its `_batch.json` should say `"idempotent": false`, so Run Now asks before running it. The rule, and the commands proven so far, are in [Manifest and ordering file specs](../data-initialization-manifests.md).
- **Give the batch a canary** that the **last** document creates, so a run that stops partway through is noticed and retried.

## Limit Result by Status means element status, not lifecycle

`Limit Result by Status` (on View Report and Create Report) filters on an element's **element status**. Egeria accepts `UNKNOWN`, `ACTIVE`, `INVALID`, `DELETED` and `OTHER`, but in practice an element is `ACTIVE` or `DELETED`:

| Value | Returns |
|---|---|
| empty, or `ACTIVE` (the default) | elements that aren't deleted |
| `DELETED` | soft-deleted elements only |
| `ACTIVE, DELETED` | both |

Values such as `DRAFT`, `APPROVED` or `DEPRECATED` used to be element statuses. They now live in each element's own lifecycle property. Egeria rejects them here, and Dr.Egeria (pyegeria 6.3.0 and later) warns and drops them before sending the request. To filter on lifecycle, use:

- **Limit Result by Content Status** for authored content: glossary terms, governance definitions, data assets (`DRAFT`, `PREPARED`, `PROPOSED`, `APPROVED`, `REJECTED`, `ACTIVE`, `DEPRECATED`, `OBSOLETE`, `OTHER`)
- **Limit Result by Deployment Status** for infrastructure (`PROPOSED`, `UNDER_DEVELOPMENT`, `DEVELOPMENT_COMPLETE`, `APPROVED_FOR_DEPLOYMENT`, `REJECTED`, `STANDBY`, `ACTIVE`, `DISABLED`, `FAILED`, `OTHER`)
- **Limit Result by Activity Status** for processes and actions (`REQUESTED`, `APPROVED`, `WAITING`, `ACTIVATING`, `IN_PROGRESS`, `PAUSED`, `FOR_INFO`, `COMPLETED`, `INVALID`, `IGNORED`, `FAILED`, `CANCELLED`, `ABANDONED`, `OTHER`)

These only take effect on reports whose underlying search supports that filter. For the others, Dr.Egeria warns that the filter was dropped and runs the report without it.

---

## Further reading

- [Dr. Egeria overview](overview.md): directives, writing commands, output
- [Basic Templates](templates-basic.md) and [Advanced Templates](templates-advanced.md): every command and attribute
- [Data Initialization](../data-initialization.md): how inbox documents are loaded and re-loaded
- [Running notebooks during Data Initialization](../data-initialization-notebooks.md#techniques-and-best-practices): the same kind of advice for notebooks
