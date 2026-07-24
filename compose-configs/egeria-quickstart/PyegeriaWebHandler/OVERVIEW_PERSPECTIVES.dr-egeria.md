<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Overview — Perspective / Question Library

> Loadable **Dr.Egeria** document that materialises the Overview dashboard's
> per-perspective question sets as real Egeria elements: each **Perspective**
> (a viewpoint held by an actor) is linked via **ScopedBy** to its **Questions**
> (GlossaryTerms classified `IsQuestion`). Generated from `egeria-overview.html`
> `PERSPECTIVES` — the single source of truth. Regenerate with gen_perspectives.py.
>
> Starter questions scavenged from DAMA-DMBOK / EDM-Council DCAM / FAIR / DataOps.
> **Run with VALIDATE first, then PROCESS.** Create commands carry user-specified
> Qualified Names so the Link commands can cross-reference them within this doc.

---

# Data Governance Lead — perspective

# Create Perspective

## Display Name
Data Governance Lead

## Category
Overview Dashboard Perspective

## Description
Are we in control, and is it improving?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-governance

## Version Identifier
1.0

---

# Create Question

## Display Name
What share of critical assets is governed (owned, classified, certified)?

## Summary
What share of critical assets is governed (owned, classified, certified)?

## Usage
DCAM · Governance → Business value: regulatory exposure & audit-readiness

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-governance-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-governance

## Question Name
Question::overview-governance-01

## Label
ScopedBy

---

# Create Question

## Display Name
Is governance coverage improving period over period?

## Summary
Is governance coverage improving period over period?

## Usage
DAMA maturity → Business value: demonstrable program ROI to the board

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-governance-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-governance

## Question Name
Question::overview-governance-02

## Label
ScopedBy

---

# Create Question

## Display Name
Where is our regulatory exposure concentrated?

## Summary
Where is our regulatory exposure concentrated?

## Usage
FAIR + Privacy → Business value: avoided fines, breach-cost reduction

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-governance-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-governance

## Question Name
Question::overview-governance-03

## Label
ScopedBy

---

# Create Question

## Display Name
How many policy exceptions are open, and are they aging down?

## Summary
How many policy exceptions are open, and are they aging down?

## Usage
DCAM · Control → Business value: operational risk & SLA to remediation

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-governance-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-governance

## Question Name
Question::overview-governance-04

## Label
ScopedBy

---

# Create Question

## Display Name
Is the community actively curating & trusting the catalog?

## Summary
Is the community actively curating & trusting the catalog?

## Usage
Adoption → Business value: self-service, less steward toil

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-governance-05

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-governance

## Question Name
Question::overview-governance-05

## Label
ScopedBy

---

# Data Steward — perspective

# Create Perspective

## Display Name
Data Steward

## Category
Overview Dashboard Perspective

## Description
What in my domain needs my attention?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-steward

## Version Identifier
1.0

---

# Create Question

## Display Name
Which assets lack an owner, classification, or description?

## Summary
Which assets lack an owner, classification, or description?

## Usage
DAMA · Metadata → Value: trustable, findable catalog

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-steward-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-steward

## Question Name
Question::overview-steward-01

## Label
ScopedBy

---

# Create Question

## Display Name
Which glossary terms are unlinked or awaiting approval?

## Summary
Which glossary terms are unlinked or awaiting approval?

## Usage
FAIR · Findable → Value: semantic coverage

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-steward-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-steward

## Question Name
Question::overview-steward-02

## Label
ScopedBy

---

# Create Question

## Display Name
Which data stores have never been surveyed / profiled?

## Summary
Which data stores have never been surveyed / profiled?

## Usage
DataOps · quality → Value: known data quality

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-steward-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-steward

## Question Name
Question::overview-steward-03

## Label
ScopedBy

---

# Create Question

## Display Name
What changed in my domain since I last looked?

## Summary
What changed in my domain since I last looked?

## Usage
Observability → Value: stay ahead of drift

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-steward-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-steward

## Question Name
Question::overview-steward-04

## Label
ScopedBy

---

# Data Owner — perspective

# Create Perspective

## Display Name
Data Owner

## Category
Overview Dashboard Perspective

## Description
Is my data healthy, used, and trusted?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-owner

## Version Identifier
1.0

---

# Create Question

## Display Name
Who is using my data products, and how much?

## Summary
Who is using my data products, and how much?

## Usage
Data-as-product → Value: demonstrate impact

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-owner-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-owner

## Question Name
Question::overview-owner-01

## Label
ScopedBy

---

# Create Question

## Display Name
What is the quality & freshness of assets I own?

## Summary
What is the quality & freshness of assets I own?

## Usage
DataOps → Value: reliability

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-owner-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-owner

## Question Name
Question::overview-owner-02

## Label
ScopedBy

---

# Create Question

## Display Name
Are there open issues or low ratings on my assets?

## Summary
Are there open issues or low ratings on my assets?

## Usage
Feedback → Value: trust signal

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-owner-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-owner

## Question Name
Question::overview-owner-03

## Label
ScopedBy

---

# Create Question

## Display Name
Is my data properly classified & access-controlled?

## Summary
Is my data properly classified & access-controlled?

## Usage
DCAM → Value: compliance

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-owner-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-owner

## Question Name
Question::overview-owner-04

## Label
ScopedBy

---

# Data Consumer / Analyst — perspective

# Create Perspective

## Display Name
Data Consumer / Analyst

## Category
Overview Dashboard Perspective

## Description
Can I find and trust the data I need?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-consumer

## Version Identifier
1.0

---

# Create Question

## Display Name
What certified data products exist for my domain?

## Summary
What certified data products exist for my domain?

## Usage
FAIR · Findable → Value: faster time-to-data

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-consumer-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-consumer

## Question Name
Question::overview-consumer-01

## Label
ScopedBy

---

# Create Question

## Display Name
Where did this data come from, and how fresh is it?

## Summary
Where did this data come from, and how fresh is it?

## Usage
FAIR · lineage → Value: trust

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-consumer-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-consumer

## Question Name
Question::overview-consumer-02

## Label
ScopedBy

---

# Create Question

## Display Name
What do peers say — ratings, comments, most-used?

## Summary
What do peers say — ratings, comments, most-used?

## Usage
Collaboration → Value: social proof

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-consumer-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-consumer

## Question Name
Question::overview-consumer-03

## Label
ScopedBy

---

# Create Question

## Display Name
Which datasets are safe to use with an LLM/agent?

## Summary
Which datasets are safe to use with an LLM/agent?

## Usage
AI governance → Value: safe reuse

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-consumer-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-consumer

## Question Name
Question::overview-consumer-04

## Label
ScopedBy

---

# Data Engineer / Platform — perspective

# Create Perspective

## Display Name
Data Engineer / Platform

## Category
Overview Dashboard Perspective

## Description
Is the pipeline healthy and complete?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-engineer

## Version Identifier
1.0

---

# Create Question

## Display Name
Which assets are unsurveyed / missing schema?

## Summary
Which assets are unsurveyed / missing schema?

## Usage
DataOps → Value: coverage

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-engineer-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-engineer

## Question Name
Question::overview-engineer-01

## Label
ScopedBy

---

# Create Question

## Display Name
How complete is lineage — any orphan nodes?

## Summary
How complete is lineage — any orphan nodes?

## Usage
FAIR · lineage → Value: impact analysis

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-engineer-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-engineer

## Question Name
Question::overview-engineer-02

## Label
ScopedBy

---

# Create Question

## Display Name
What supply chains / blueprints do assets participate in?

## Summary
What supply chains / blueprints do assets participate in?

## Usage
Architecture → Value: change safety

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-engineer-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-engineer

## Question Name
Question::overview-engineer-03

## Label
ScopedBy

---

# Create Question

## Display Name
What structural change happened recently?

## Summary
What structural change happened recently?

## Usage
Observability → Value: detect drift

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-engineer-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-engineer

## Question Name
Question::overview-engineer-04

## Label
ScopedBy

---

# App / AI Builder — perspective

# Create Perspective

## Display Name
App / AI Builder

## Category
Overview Dashboard Perspective

## Description
How much governed context can I safely build on?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-builder

## Version Identifier
1.0

---

# Create Question

## Display Name
How much data is AI-ready — governed, documented, lineage-traced?

## Summary
How much data is AI-ready — governed, documented, lineage-traced?

## Usage
AI governance → Value: trustworthy AI faster

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-builder-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-builder

## Question Name
Question::overview-builder-01

## Label
ScopedBy

---

# Create Question

## Display Name
What context products can I consume via MCP / API?

## Summary
What context products can I consume via MCP / API?

## Usage
Context intelligence → Value: ship without re-plumbing

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-builder-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-builder

## Question Name
Question::overview-builder-02

## Label
ScopedBy

---

# Create Question

## Display Name
What is semantically grounded (glossary-linked)?

## Summary
What is semantically grounded (glossary-linked)?

## Usage
RAG grounding → Value: fewer hallucinations

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-builder-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-builder

## Question Name
Question::overview-builder-03

## Label
ScopedBy

---

# Create Question

## Display Name
What guardrails keep confidential data out of AI context?

## Summary
What guardrails keep confidential data out of AI context?

## Usage
AI safety → Value: defensible AI

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-builder-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-builder

## Question Name
Question::overview-builder-04

## Label
ScopedBy

---

# Privacy / Risk Officer — perspective

# Create Perspective

## Display Name
Privacy / Risk Officer

## Category
Overview Dashboard Perspective

## Description
Where is our risk and exposure?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-privacy

## Version Identifier
1.0

---

# Create Question

## Display Name
Where is PII / sensitive data, and is it in the right zones?

## Summary
Where is PII / sensitive data, and is it in the right zones?

## Usage
Privacy → Value: breach-cost reduction

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-privacy-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-privacy

## Question Name
Question::overview-privacy-01

## Label
ScopedBy

---

# Create Question

## Display Name
What is our retention / certification compliance posture?

## Summary
What is our retention / certification compliance posture?

## Usage
DCAM · Control → Value: avoided fines

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-privacy-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-privacy

## Question Name
Question::overview-privacy-02

## Label
ScopedBy

---

# Create Question

## Display Name
Who / what can access restricted data (incl. AI agents)?

## Summary
Who / what can access restricted data (incl. AI agents)?

## Usage
Access control → Value: least privilege

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-privacy-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-privacy

## Question Name
Question::overview-privacy-03

## Label
ScopedBy

---

# Create Question

## Display Name
Is confidential data blocked from AI training/RAG?

## Summary
Is confidential data blocked from AI training/RAG?

## Usage
AI safety → Value: defensible AI

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-privacy-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-privacy

## Question Name
Question::overview-privacy-04

## Label
ScopedBy

---

# Community Lead — perspective

# Create Perspective

## Display Name
Community Lead

## Category
Overview Dashboard Perspective

## Description
Is the community healthy and engaged?  (Egeria Overview dashboard perspective.)

## Qualified Name
Perspective::overview-community

## Version Identifier
1.0

---

# Create Question

## Display Name
Who are our most active contributors (karma leaders)?

## Summary
Who are our most active contributors (karma leaders)?

## Usage
Community Profile → Value: recognise curation

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-community-01

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-community

## Question Name
Question::overview-community-01

## Label
ScopedBy

---

# Create Question

## Display Name
Is engagement (comments, ratings, tags) growing?

## Summary
Is engagement (comments, ratings, tags) growing?

## Usage
Adoption → Value: trusted & used catalog

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-community-02

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-community

## Question Name
Question::overview-community-02

## Label
ScopedBy

---

# Create Question

## Display Name
Which communities / teams are most (and least) engaged?

## Summary
Which communities / teams are most (and least) engaged?

## Usage
Collaboration → Value: target enablement

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-community-03

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-community

## Question Name
Question::overview-community-03

## Label
ScopedBy

---

# Create Question

## Display Name
What questions are being asked but not answered?

## Summary
What questions are being asked but not answered?

## Usage
Q&A → Value: new views to build

## Category
Overview Dashboard Question

## Content Status
ACTIVE

## Qualified Name
Question::overview-community-04

## Version Identifier
1.0

# Link Perspective to Question

## Perspective Name
Perspective::overview-community

## Question Name
Question::overview-community-04

## Label
ScopedBy

---
