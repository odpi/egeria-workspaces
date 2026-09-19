<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Perspective / Question Scoping — Options for Discussion

Written 2026-09-02, following BACKLOG.md's NEXT-10 P3 item 4 (Overview's
Perspectives/Questions document, generated 2026-07-26, never processed).
Investigating that item surfaced a bigger question this document is about:
Egeria Overview, Resource Explorer (RE), and Egeria Advisor (EA) all use
**Perspectives** and **Questions**, and should share one consistent model
rather than each growing its own. This document is a discussion paper, not
a decision — it lays out what's actually live in Egeria today, three
distinct scoping problems that got tangled together in conversation, what
real Egeria mechanisms exist for each, and open options with trade-offs.
No implementation should start from this document alone; it's the input to
a team conversation.

**Everything below marked "confirmed live" was checked directly against
the running `quickstart-egeria-main` platform (Coco Pharmaceuticals demo
data) on 2026-09-02, not inferred from documentation.** Numbers will drift
as demo data changes; the *shape* of the findings is what should be
trusted, not the exact counts.

---

## 1. Why this surfaced now

`OVERVIEW_PERSPECTIVES.dr-egeria.md` (generated 2026-07-26 by
`gen_perspectives.py`) was written to materialize the Overview dashboard's
hardcoded `PERSPECTIVES` JavaScript object as real Egeria elements: 8
Perspectives, 33 Questions, linked via `ScopedBy`. It was never run — as of
the July 28 backlog note, only one pre-existing Perspective
(`Security Officer`, original Coco demo data) existed.

Checking before running it (rather than after) found the live picture has
moved on substantially since July: **Resource Explorer has since created
its own Perspective/Question set**, and it doesn't look like Overview's.

## 2. What's actually live today (confirmed 2026-09-02)

- **13 Perspectives** exist (not 1). 12 are Resource Explorer's own —
  `Admin`, `Architecture`, `Security`, `Data Expert`, `Community`,
  `Privacy`, `App/AI Builder`, `Consumer`, `Data Owner`, `Steward`,
  `Financial`, `Governance` — plus the original `Security Officer`.
  `createdBy: erinoverview`, `createTime: 2026-09-02T13:27` — created
  roughly 90 minutes before this check, almost certainly an automated
  `bootstrap.check_and_heal()` re-run after a platform restart earlier the
  same session, not long-settled data.
- **51 Questions** exist (`GlossaryTerm` + `Question` classification), all
  clearly Resource Explorer's own repo-scouting vocabulary — *"Are there
  outstanding CVEs?"*, *"Who maintains this repository?"*, *"Does it hold
  an OpenSSF Best Practices (CII) badge?"* — plus 2 unrelated questions
  from a separate "Jacquard" subsystem. **Zero textual overlap** with
  Overview's planned 33 questions (different domain — repo evaluation vs.
  data-asset governance — and a different `qualifiedName` scheme:
  `Coco Pharmaceuticals::Term::<text>::1.0` vs. Overview's planned
  `Question::overview-<perspective>-<NN>`).
- **170 `ScopedBy` relationships** connect those 51 Questions to the 13
  Perspectives (Question = scoped element, Perspective = scope — this is
  RE's own `Link Perspective to Question` Dr.Egeria command, whose
  template description literally says *"Links a Perspective to a Question
  via a ScopedBy relationship."*). **None of the 170 have any property
  set** — the relationship supports optional `Label`/`Description`/
  `Journal Entry` fields (per the Dr.Egeria template) and every single
  live instance has them empty.
- `Perspective` and `ScopedBy` are both **native Egeria types**, not
  invented for this project. `Perspective` (`Actor` → `Referenceable` →
  `OpenMetadataRoot`) is described in the type system as *"a context for
  an actor and how they are likely to process information based on their
  skills, current context, and background."* `ScopedBy`'s own description:
  *"Link between a scope — such as a digital product, infrastructure
  element, or organization — and an element restricted the scope."*

**Implication:** Overview's plan to reuse RE's existing Perspective
elements (linking new questions to `Perspective::Governance` etc. by
qualified name, per the doc's own header note) is *structurally* sound —
the mechanism was built for exactly this kind of sharing. But the two
questions sets serve genuinely different purposes under the same label:
RE's `Perspective::Governance` questions are about whether a *repository*
fits governance frameworks; Overview's would be about whether a *data
asset* is governed. Same node, two different domains hanging off it.

## 3. Three scoping problems, not one

Conversation exploring this kept sliding between three genuinely different
questions. Separating them is the main point of this document.

### 3.1 Which app/product does a Question belong to?

*(RE's repo-scouting questions vs. Overview's asset-governance questions
vs. whatever EA needs.)*

Two real options, both grounded in what's live:

- **(a) Populate the unused `Label` field** on each `ScopedBy` link with
  an owning-app tag (e.g. `"Resource Explorer"` / `"Overview Dashboard"`).
  Cheapest — the field already exists on every one of the 170 live links,
  currently empty. No new elements, fully additive, works today.
- **(b) A real scope element per app**, e.g. model Resource Explorer /
  Overview / Egeria Advisor each as a `DigitalProduct`, and give each
  Question a *second* `ScopedBy` link to its owning app-product alongside
  its link to the shared Perspective. `ScopedBy`'s own description
  explicitly names "digital product" as a typical scope type — this is
  idiomatic, not a stretch. Costs more (new elements, a second link per
  Question) but makes "show me every Question RE owns" a direct,
  independently queryable relationship rather than a string tag.

Not mutually exclusive — (a) is cheap enough to do regardless of whether
(b) also happens later.

### 3.2 What breadth does an answer apply over?

*(Is "Architecture" being asked about everything Egeria knows, one
organization, one project?)*

**`scope` is a valid-value-backed string attribute, not a type or a
relationship** — this distinction matters and was worth stating precisely
mid-conversation. It classifies breadth-of-coverage with a controlled
vocabulary; it does not link to another element the way `ScopedBy` does.

Confirmed live: a registered `scope` property exists with **12 values** —
`Individual`, `Within Team`, `Within Discipline`, `Within Project`,
`Within Business Capability`, `Within digital product`,
`Within organization`, `Within Site`, `Within Facility`, `Within Country`,
`Within Region`, `Within agreement`, `The world` — maps directly onto
"everything Egeria knows" (`The world`), "a specific organization"
(`Within organization`), "a project's scope" (`Within Project`).

It's formally attached (in the type model) to `GovernanceDefinition` and
close kin — `ActorRole`, `InformationSupplyChain`, `SubjectArea`,
`ValidValueDefinition` — and to the `Regulator` relationship. **Neither
`Perspective` nor `Question` carries it today.**

The open question worth the team's attention: is breadth-of-coverage a
property of the *Question itself* (static — this Question only ever makes
sense at organization scope), or a property of *asking* it (a per-view
runtime parameter — today viewing Architecture through a project lens,
tomorrow through the whole organization)? This mirrors a pattern already
built in this app: `as_of_time` isn't stored on elements, it's a query
parameter every relevant endpoint accepts. If `scope` behaves the same
way — a filter Overview passes when asking "give me Architecture's
questions, scoped to X," backed by the real Egeria vocabulary for a UI
dropdown — the whole benefit lands with **zero new persistent links**.
Static modeling (attaching `scope` permanently) is only needed if some
Questions are *intrinsically* scoped and shouldn't be offered outside it —
worth asking whether concrete examples of that exist before assuming they
do.

### 3.3 Which Organization/Business Capability does a *resource* belong to?

*(So a query can be limited to "the user's organization," not just
answer "which organization is the user in.")*

This one has a confirmed real gap, not just an open design choice.

**Resolving the user's own organization is solid and already populated**:
`UserIdentity` → `ProfileIdentity` → `Person` → `PersonRoleAppointment` →
`PersonRole`/`TeamRole` → `TeamRoleAppointment` → `Team`/`Organization`
(`Organization` is a native `Team` subtype), with `TeamStructure` for
reporting hierarchy if a team rolls up into a larger org. Confirmed live:
**21 `Organization` elements, 67 `Team`s, 17 `TeamRoleAppointment`s**
already populated in the Coco Pharmaceuticals dataset (Bushy Mead
Hospital, Oak Dene Hospital, TravelPlanner Cloud Provider, Coco
Pharmaceuticals Ltd itself, etc.) — this traversal is answerable today,
not hypothetical.

**Filtering *resources* (assets, and anything Overview would count/query)
by that organization has no existing precedent anywhere in this platform.**
Every live `ScopedBy` relationship was enumerated (345 total, as of the
last check) and grouped by type pair — the full list is
`GlossaryTerm→Perspective` (170), `GovernanceActionProcess→GlossaryTerm`
(87), `GlossaryTerm→GlossaryTerm` (54), `ExternalId→MetadataCollection`
(12), `Community→DigitalProductFamily` (8), `CertificationType→Project`
(6), `PropertyFacet→MetadataCollection` (3),
`InformationSupplyChain→Project` (3), plus two singletons. **Nothing
connects an Asset to an Organization or a BusinessCapability, anywhere.**
`AssignmentScope` (720 live relationships) is heavily used but for a
different purpose entirely — who is *responsible for managing* something
(`PersonRole→Notification/Team/ToDo/Community/DigitalProduct/Project`,
`GovernanceRole→BusinessCapability/Location/Folio`), not which
organization a resource belongs to. `DigitalSupport`
(`BusinessCapability`→any `Referenceable`, the type-system's own
general-purpose "this capability is supported by this thing" link) has
**zero live usage** anywhere on the platform.

**A tempting shortcut was checked and ruled out.** Governance zones look
superficially like they might double as organizational boundaries — they
don't. Zones are entirely internal, functional/departmental (`Sales Zone`,
`Finance Zone`, `Manufacturing`, `Clinical Trials`, `IT Infrastructure`,
...); Organizations are external entities Coco Pharma does business with
(hospitals as customers, cloud providers as vendors, a consultancy), with
`Coco Pharmaceuticals Ltd` itself as just one of 21 entries. Zero name or
conceptual overlap — confirmed by listing both sets side by side, not
assumed from the names alone.

**Candidate approaches, none proven out yet:**

1. **Ownership traversal at query time** — walk each Asset's `Contributor`/
   owner back through `PersonRoleAppointment`/`TeamRoleAppointment` to
   their `Organization`, the same chain as §3.3's user-resolution path,
   run per-asset. Correct in principle; only as good as ownership data
   completeness, and potentially expensive as a live filter over a large
   asset population (would need a materialized/cached version, not a
   per-request graph walk, for anything beyond a handful of assets).
2. **A new, explicit `ScopedBy` link**, Asset → `Organization`, populated
   once as real metadata (via a survey step, a bulk load, or manual
   curation) then queried directly and cheaply. Real modeling/authoring
   work, but reuses the exact mechanism already established for
   Question↔Perspective — same shape of solution as §3.1's option (b).
3. **`DigitalSupport` (BusinessCapability → Referenceable)** — genuinely
   built for "this capability is supported by this resource," unused
   today. Business-capability scoping (one of the 12 `scope` valid values
   is literally `Within Business Capability`) might be the more natural
   fit than organization scoping for some questions — e.g. "Architecture"
   might more usefully mean "within this Business Capability" than "within
   this Organization" for certain resources. Worth deciding per-Perspective
   rather than assuming one scoping axis fits all Perspectives.

## 4. Open decisions for team discussion

1. **§3.1** — Populate `Label` on existing/new `ScopedBy` links now (cheap,
   backward-compatible), model per-app `DigitalProduct` scope elements
   later, or both? Does EA need a third label in the mix, and does it have
   its own Questions/Perspectives already (worth checking before this
   conversation happens, same way RE's state was checked here)?
2. **§3.2** — Is breadth-of-coverage (`scope`) a static property of a
   Question, or a runtime view parameter (the `as_of_time` pattern)? Are
   there concrete Questions today that are *intrinsically* scoped and
   shouldn't be askable outside that scope, or is every Question in
   principle askable at any breadth?
3. **§3.3** — Given no existing precedent, which candidate (query-time
   traversal, explicit `ScopedBy` to Organization, `DigitalSupport` to
   BusinessCapability, some combination, or something not listed here) is
   worth prototyping first? Does this depend on the demo-data organization/
   business-capability correlators Dan is currently loading in — worth
   revisiting this document once that lands, since it may change what's
   "confirmed live" throughout §2–§3.
4. Should Overview's own Perspectives (currently a hardcoded
   `PERSPECTIVES` object in `egeria-overview.html`, not yet materialized
   in Egeria at all) reuse RE's 12 Perspectives by qualified name as
   originally planned, or does the domain mismatch found in §2 argue for
   Overview minting its own smaller, differently-scoped set instead of
   overloading shared labels?

## 5. Explicitly out of scope for this document

- No code changes, no Egeria writes, no decisions. This is a survey of
  what's live and what mechanisms exist, for the team conversation to
  work from.
- `OVERVIEW_PERSPECTIVES.dr-egeria.md` itself was not re-examined
  line-by-line against the current 13/51/170 state — that's a follow-up
  once §4's decisions are made, not before.
