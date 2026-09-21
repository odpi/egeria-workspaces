<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# The Sixty-Day Review — Jules Keeper's Script

> **Author:** Jules Keeper (Chief Data Officer)  
> **Version:** 1.1  
> **Status:** DRAFT  
> **Date:** 2026-09-19  
> **Description:** The script for Jules Keeper's sixty-day review with the founders — Zach Now, Terri Daring and Steve Starter — reporting the strategic information supply chain work at the close of the Initiation Phase: what was found, what it is worth, and the decisions that shape the final thirty days.  A speaking script, not a Dr.Egeria command file.

---

## How to use this script

Thirty-five minutes with the founders, no deck of forty slides.  Three screens shown live from Egeria Explorer, two documents, one slide, and the rest is talking.

This is the checkpoint at the end of the [Initiation Phase](../0.%20data-governance-program/jules-90-day-plan.md) — day sixty of ninety.  The work being reported is the *Identify key information supply chains* task and everything that fell out of it.  The Impact Phase has not started, and the five decisions at the end are what it needs in order to start well.

| | Section | Minutes | On screen |
|---|---|---|---|
| 1 | Where we are at day sixty | 2 | nothing |
| 2 | Sixteen flows | 4 | the register |
| 3 | From a list to something that runs | 4 | one supply chain's implementation graph |
| 4 | Which machines actually do this | 6 | the gap report |
| 5 | Products instead of integrations | 4 | one product and its specification |
| 6 | What it buys us in quality | 5 | nothing |
| 7 | What it buys us in the way we work | 3 | nothing |
| 8 | The gaps are the acquisition plan | 5 | the three-estate table |
| 9 | What I need from you | 3 | one slide, five decisions |

### Before the room

Nothing here is a screenshot — three of the six screens are live, and one of the documents does not exist until somebody runs a notebook.  Work down this list the day before, not the hour before.

| On screen | Where it comes from | What must be true first |
|---|---|---|
| The register (§2) | Egeria Explorer, Strategic Information Supply Chains collection | `0. data-governance-program/` loaded in full — the register loads nineteenth and last, after every domain file |
| Implementation graph (§3) | Egeria Explorer, Solution Architect card → Batch Manufacturing and Release | [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md) loaded, as `erinoverview` |
| **The gap report (§4)** | [mapping-the-systems/system-mapping-report.md](mapping-the-systems/system-mapping-report.md) — **generated, gitignored, not in a fresh clone** | Run `mapping-the-systems/mapping-the-systems.ipynb` as `peterprofile`, after the acquisition systems are loaded by [extending-the-systems-inventory/](extending-the-systems-inventory/README.md) |
| A product and its spec (§5) | Egeria Explorer, Strategic Digital Product Catalog | [strategic-digital-products/](strategic-digital-products/README.md) loaded in `_batch.json` order, as `erinoverview` |
| Three-estate table (§8) | [strategic-supply-chain-system-matches.md](strategic-supply-chain-system-matches.md), Part 1 | Committed — nothing to run |
| Five decisions (§9) | One slide, made by hand | — |

**Do not drive Explorer signed in as Jules.**  Jules and Erin are in none of the infrastructure zone groups, so they see nine of the parent's twenty-nine systems and the rest simply look missing — which is a spectacular thing to discover in front of the founders while claiming to have mapped the estate.  Sign in as `peterprofile`, who can read all twenty-nine.  The reasoning is in [mapping-the-systems/README.md](mapping-the-systems/README.md).

If the notebook cannot be run in time, §4 still works from the numbers in this script — but say the report is generated and offer it afterwards rather than promising a screen that is not there.

**Rules for the room.** Never say "framework".  Never say "maturity".  If asked what this is called, the answer is "a map of how data gets from where it happens to where it matters" — not "an information supply chain register".  Every claim in this script is backed by a file; the backing is in the appendix, not in the talk.

**Things to have open but not show unless asked:** the eight components with no system anywhere; the seventeen the parent might cover but nobody will confirm; the three ledgers.

---

## 1. Where we are at day sixty

> You gave me ninety days.  This is day sixty, and I have come a month early on purpose — because what the last thirty days turned up changes what I should spend the final thirty doing, and some of that is your call rather than mine.
>
> I want to be straight about the shape of it first, because you have all three told me, in different words, that you did not build this company to fill in forms.  What my team has spent the last two months doing is not writing rules.  It is drawing a map.  We took the question *how does data get from where something happens to where somebody decides something*, and we answered it, for the sixteen flows where getting it wrong costs us a patient, a licence or a quarter.
>
> The map turned out to be more interesting than the map-making.  It told us three things we did not know: where our product quality actually depends on a spreadsheet, what the two acquisitions are really worth, and which four or five things we do not have at all.
>
> Thirty-five minutes.  Five decisions at the end, and then I will go and spend the last thirty days on whatever you tell me matters most.

---

## 2. Sixteen flows

*Show: the Strategic Information Supply Chains register.*

> Coco runs many hundreds of data flows.  We named sixteen.
>
> Erin set the entry test, and the discipline is in what it excludes.  A flow gets on this list only if it passes one of four questions.  If it stopped for a day, would we stop making, selling or shipping something?  Does a regulator expect this data to arrive somewhere, correct and on time?  Could a fault in it reach a patient?  And the one I argued hardest for — once the wrong data has travelled this flow, can we undo it?
>
> That fourth test is the one that matters to a manufacturer.  Most data problems are recoverable.  You reissue the report, you restate the figure, you apologise.  A serial number issued twice is not recoverable.  A pack decommissioned in error is not recoverable.  A patient-derived material that has lost its identity is not recoverable.  Those flows have to be watched *before* the fault propagates, and that is a completely different engineering problem from reporting on it afterwards.
>
> Seven of the sixteen already existed in our metadata — clinical trials, treatment ordering, inventory, product details and a few others were mapped years ago and nobody had built on them.  We adopted those rather than redrawing them.  We added nine: batch manufacturing and release, serialisation, cold chain and dangerous goods, adverse events, financial close, third party payment, workforce qualification, occupational health, and data subject rights.
>
> Sixteen.  Not four hundred.  If somebody proposes a seventeenth, they have to say which of the four tests it passes.

**If Zach asks "who decides what's on the list":** the four tests decide.  I do not, and neither does any one domain.  The test is public and anybody can argue a flow onto it.

---

## 3. From a list to something that runs

*Show: the Batch Manufacturing and Release implementation graph.*

> A list of sixteen flows is a poster.  This is the part that makes it operational.
>
> Peter and Erin took each of the sixteen and said what actually carries it: eighty-two components, and a hundred and thirty connections between them.  Sixty-eight of those components are things we run.  The rest are hospitals, carriers, the national verification systems and the third-party screening service — outside the company, but on the map, because a flow that ends at our boundary is not a flow.
>
> Every connection records what crosses it and which of the sixteen flows it serves.  That last bit is why this is not a diagram somebody drew in a meeting.  Because each connection knows which flows it belongs to, the picture of any one flow can be assembled from the parts rather than maintained by hand.  When a connection changes, every flow that uses it changes with it.  Nobody has to remember to update the poster.
>
> Here is the first thing that fell out, and it is the small kind of finding that pays for the work.  The hazardous material inventory turns out to serve three of the sixteen flows: occupational health, dangerous goods transport, and inventory tracking.  It was recorded as serving one.  Nobody was wrong — each of the three teams knew about its own use.  Nobody had ever seen all three at once.  That system now has three sets of people who care whether it is up, and the next time somebody proposes changing it, all three get asked.

---

## 4. Which machines actually do this

*Show: the gap report, headline table only.*

> Then we asked the blunt question: for each of those sixty-eight components, which actual system runs it?  Gary joined us for this, because it is his inventory.
>
> We got this wrong the first time, and the way we got it wrong is the most useful thing in the analysis.
>
> Version one matched everything against Gary's inventory — twenty-nine systems — and concluded that the regulated half of this business had no systems at all.  No LIMS.  No quality management.  No batch record.  No equipment qualification.  That conclusion was alarming and it was wrong, for two reasons.
>
> The first is that Gary's twenty-nine are the servers under Gary's care.  Equipment a department bought for itself was never in scope.  So it is the integrated surface of the parent company, not everything the parent runs.
>
> The second is that we had forgotten to look at what we bought.  Austin has forty-five systems.  Bucharest has thirty.  And when you put those inventories next to the sixteen flows, the regulated layer is there — twice.  LabWare LIMS, Waters Empower, Veeva Vault QMS, Trackwise, Siemens Opcenter, Rockwell FactoryTalk, IBM Maximo, SAP S/4HANA, Workday.  In both of them.  Almost system for system.
>
> So the corrected picture, across all three estates, is this.  Twenty-three components the parent clearly covers.  Seventeen where the only candidate is a system somebody thinks probably does it, and no owner has confirmed.  Twenty that exist only at the acquisitions.  And eight that nothing anywhere in this group does.
>
> Eight.  Down from twenty-eight before we looked at Austin and Bucharest.  I want to name them, because a list of eight is a shopping list and a list of twenty-eight is a crisis:
>
> - four of them are serialisation — generating serial numbers, storing them, uploading them to the national registers, and triaging the alerts that come back;
> - one is medical coding of adverse events, which is a human job today and arguably should stay one;
> - three are the machinery of answering a data subject's request — verifying who they are, knowing what we hold, and actually going and doing it.
>
> Nothing serialises.  Not the parent, not Austin, not Bucharest.  And nothing does pharmacovigilance — both acquisitions can take a product complaint and route an adverse event into a quality system, but a quality system is not a safety system and it does not run the statutory reporting clock.

**If Steve asks how confident we are:** every match carries a confidence.  *Strong* means a system's own description or a recorded interaction between two systems names the function.  *Probable* means it plainly lives there but nothing says so.  *Possible* means it could, and we have not linked it — we have written down the question instead.  The seventeen unconfirmed are all Possible, and they are the first thing I want owners for.

---

## 5. Products instead of integrations

*Show: one digital product and its specification — Batch Execution Records will do.*

> One more piece, and then I get to what it is worth.
>
> Every one of those hundred and thirty connections carries data.  Until this year that data existed only as an arrangement between the two systems at either end — a file, a feed, a nightly job that two people understood and nobody had written down.  When one of those two people leaves, the arrangement becomes a risk; when a third team wants the same data, they build a second arrangement beside the first.
>
> Erin's team turned all of it into **eighty-two products**.  A product here is a named, described, catalogued thing: it says what it contains, who owns it, what kind of data it is — master data, transactional record, event stream, time series, evidence record, reference data, regulatory submission, insight — and it carries a specification listing exactly which fields a subscriber receives.  One thousand and twenty-seven field names across the eighty-two, and every one of them built from the same agreed vocabulary, so that *batch identifier* means the same thing in manufacturing, in quality and in the warehouse.  That vocabulary check was done name by name.  It is the least glamorous part of the whole exercise and it is the part that stops the next argument before it starts.
>
> Ownership follows production.  The group whose system produces the data owns the product: eleven folders, one per business area — quality systems own fifteen products, finance thirteen, manufacturing eleven, people systems eleven, and so on down.  Nobody had to negotiate that, because it falls straight out of the map.
>
> And the products know what they depend on.  A hundred and twenty-five dependencies, one for every connection where both ends have a product.  Which means you can follow any number back to its origin.  *Where did this figure come from* stops being a two-week investigation and becomes a click.
>
> Why I think this is the commercially interesting part: today, when a team wants data another team holds, they negotiate an integration.  Weeks of work, bespoke, and somebody maintains it forever.  Eighty-two products with published specifications means they subscribe instead.  The cost of the second consumer of a piece of data drops to near zero, and that is the thing that decides whether people bother to use data at all.
>
> Honest caveat, because you three build things for a living and will ask.  These are **proposals**.  The catalogue describes what each product contains and where it will be read from once the Data Hub exists.  Nothing is flowing yet.  What we have done is the design and the agreement — which is the part that normally takes eighteen months and three restarts.  The build is the easy half.

---

## 6. What it buys us in quality

> Three things, and I will be specific rather than inspirational.
>
> **Product quality.** Take batch release.  Fourteen components sit between a material arriving and a batch being certified.  We can now say, for each of the three estates, which system holds each step, which steps have no system, and where a step is held in more than one place with nothing connecting them.  At Austin the manufacturing execution system raises a deviation into the quality system, the quality system's disposition goes back to the electronic batch record, and all of that is recorded.  At the parent, the equivalent of all three is a homegrown control system at each site and somebody's judgement.  That is not a criticism of the sites — it is what a shoestring builds, and it worked.  It is a statement of where a release decision can currently be defended to an inspector and where it rests on a person.
>
> Two connections we did not have but plainly should: an out-of-specification laboratory result raising a deviation, and an overdue calibration raising a quality event.  Both of those exist as real traffic at both acquisitions.  Neither was in our design.  The equipment qualification gate was enforcing itself and nobody had written it down.
>
> **Research quality.** Terri, this one is yours and it is not comfortable.  The clinical trials flow is the best-modelled thing in our whole metadata estate — it has components, roles, wires, the lot, and it has had for years.  And when we asked which systems implement it, the answer for the research components is: none are in any inventory.  Not the parent's, not Austin's, not Bucharest's.  The lab runs on equipment and software that has never been catalogued as systems at all.
>
> That means two things.  It means when a trial result is questioned we cannot trace it back to the instrument the way we can trace a batch back to a line.  And it means the research estate is invisible to every control we have built — security zones, retention, access review, the lot.
>
> The opportunity is on the other side of the same coin.  Austin's data lake holds five years of process and sensor telemetry, and there is a Spark environment sitting on it that today is used for anomaly scores.  That is a research asset the research function does not know it owns.  Five years of what actually happened on a production line, at fifteen-minute resolution, is the kind of thing Terri's people would normally have to run a study to obtain.
>
> **Patient safety.** Adverse event reporting has nine components.  One of them the parent covers.  Five exist only at Austin.  One exists nowhere.  The safety intake gateway — the thing that catches a complaint that turns out to be an adverse event — is Austin's ServiceNow feeding Austin's quality system, and it is a *Strong* match because the traffic is recorded and running.  We bought a working safety intake and did not notice.

---

## 7. What it buys us in the way we work

> Our governance leaders spent the past two months writing down what their domains need.  Six of them — Ivor, Faith, Stew, Tessa, Reggie and me — covering ten domains between us: data, security, privacy, manufacturing, drug development, corporate, human resources, health and safety, distribution, and diversity and inclusion.  Twelve documents.  Several hundred obligations.
>
> The natural end of that is ten programmes, ten sets of reporting, and ten people asking the same site manager for slightly different things.  That is exactly the bureaucracy you three have always resisted, and you would have been right to resist it.
>
> What stopped it was the sixteen flows.  Every obligation any of those teams wrote down is now attached to the flow it constrains, not to a policy binder.  Which means when Stew's team changes something in batch release, the system can tell them — before they change it — that this touches a manufacturing obligation, a data obligation and a distribution obligation, and here are the three people to talk to.  One conversation instead of three audits.
>
> The concrete effect, already: the register links to definitions owned by every single domain, and the whole set loads in one pass with no unresolved references.  That sounds technical.  What it means is that ten domains, working separately, produced work that fits together without anybody having to reconcile it afterwards.  That has not happened here before.
>
> One detail that tells the story better than the principle.  Where two domains needed to reference each other, the link had to be written by whichever team finished second — and in every case they did it, without being asked, because they could see the other team's definition.  On the day I joined they could not see each other's work at all.
>
> And it goes the other way.  The hazardous material inventory now has three owners who know about each other.  The employee flow and the financial close flow share the payroll posting and now know they share it.  When one of them wants to change it, the other finds out.

---

## 8. The gaps are the acquisition plan

*Show: the three-estate table.*

> Now the part I actually came to say.
>
> We bought Austin for its capacity and we bought Bucharest for its European footprint.  What the map says is that we also bought, twice, a complete regulated pharmaceutical operating stack — and that the parent does not have one.
>
> Look at what they run.  Austin and Bucharest were bought independently, from two different companies, in two different regulatory jurisdictions, years apart.  And they run near-identical estates: Opcenter, FactoryTalk, LabWare, Empower, Veeva quality, Trackwise, Maximo, S/4HANA, Workday, Splunk.  That convergence is not a coincidence and it is not fashion.  It is what a small-batch pharmaceutical manufacturer buys when it has to pass inspection.
>
> Which reframes the integration question completely.  For a year we have been asking *how do we absorb Austin into Coco*.  The map says the better question is *which of Austin's systems becomes the group standard*.  We are the outlier, not them.
>
> And they complete each other.  Austin has the electronic batch record, master data management pushing golden product, supplier, customer and employee records to four systems already, the five-year data lake, transport management, and a learning system that tracks GMP training compliance.  Bucharest has regulatory information management — dossier authoring and health authority tracking — a long-term archive built for GMP retention, cold-chain sensors, and electronic signature.  Between the two of them they cover almost the whole of our sixteen flows.  Neither covers it alone, and the parent covers the regulated half not at all.
>
> So the integration programme writes itself, and it is a shorter programme than the one we were planning:
>
> 1. **Adopt rather than build.** Every capability on the eight-component shopping list that we were going to procure — check first whether one of the acquisitions already runs it.  Most of what we thought was missing was not missing, it was unlooked-at.
> 2. **Pick the standard per capability, not per site.** Austin's batch record and master data, Bucharest's regulatory information management and archive.  We are not choosing a winner; we are choosing eight or ten winners, and both sites win some.
> 3. **The acquisitions get something too.** Neither of them has a group view of anything — not of product, not of supplier, not of financial position.  They have each been running as a complete company inside ours.  The map is the first artefact that shows either of them how their work connects to the group's.
> 4. **The eight real gaps get funded once, for the group.** Serialisation is the big one: four components, no system anywhere, and a regulatory deadline that does not care that we are mid-integration.  Pharmacovigilance is the second.  Both are group capabilities, so building them three times would be the worst outcome available.
>
> One more, and it is the finding that most deserves your attention.  We have three ledgers — the parent's, Austin's and Bucharest's — and no recorded flow between any of them.  For a US-listed group, consolidated statements are being produced somewhere, and that somewhere is in nobody's inventory.  I am not raising that as a control failure.  I am raising it because it is the clearest possible illustration of what this map does: it does not find things that are broken, it finds things that are *unaccounted for*, which is the category that hurts you in an audit.

---

## 9. What I need from you

*Show: five decisions.*

> Five things, and none of them is a budget line today.
>
> 1. **Owners for seventeen components.** Seventeen capabilities where the parent *might* be covered and nobody will say. I need a named person per capability to say yes or no.  Two weeks of somebody's diary, not a project.
> 2. **A ruling on four systems.** Gary's inventory has four systems labelled Austin that do not appear in Austin's own forty-five.  Either they are the interfaces we built to talk to Austin, or they are an old simplification of the same things.  The answer changes what we connect to what.  Stew and Gary can settle it in a room.
> 3. **Agreement in principle that the group standard can come from an acquisition.** This is the only genuinely political one.  If the answer is no, the integration plan is twice as long and I would rather know now.
> 4. **Serialisation and pharmacovigilance funded as group capabilities.** Not as Austin projects, not as parent projects.  Group.
> 5. **One person to own the research systems question.** Somebody to go and catalogue what the labs actually run, so that the best-designed flow we have stops resting on systems nobody has written down.
>
> That is it.  No new committee, no new policy, and nothing in this needs a process that did not already exist.
>
> What you are getting for it is the ability to answer, for any of the sixteen things that could stop this company, the question *what does that depend on, who owns it, and what happens if it breaks* — in about a minute, from a screen, rather than in three weeks from a working group.
>
> And what I will do with my last thirty days depends on your answers.  If you want the seventeen unknowns closed, that is a month of chasing owners and I will have you a clean map by day ninety.  If you want the serialisation gap costed, that is a different month.  I have a view — I would close the unknowns, because the shopping list is not trustworthy until somebody has confirmed what we already have — but you are the ones who know which of these keeps you awake.

---

## Prepared answers

**"This sounds like a lot of documentation."**
> It is one map and it maintains itself.  Every connection on it knows which flows it serves, so when a connection changes the flows change with it.  Nobody redraws anything.  The reason we can say eight things are missing today is that nobody had to remember to keep a list — we asked the map.

**"What did it cost?"**
> Erin, Peter and Gary, about two months, alongside their day jobs.  No procurement, no consultants, no new tooling — it runs on the metadata platform we already had.  The most expensive part was the two days we spent being wrong about the acquisitions.

**"Why didn't we know about Austin's systems already?"**
> Because nobody had ever asked the question in a form that required an answer per capability.  Due diligence valued the plant.  The integration plan listed the systems.  Neither of them asked *does this system do the thing our batch release depends on*, and that is the only question that would have surfaced it.

**"Is this a compliance exercise?"**
> It started as one and it stopped being one about six weeks in.  Compliance was the reason we could get six busy governance leaders and their teams to write down what they need.  The map is what we got out of it, and the map is worth more than the compliance.

**"What happens if we do nothing with it?"**
> It goes stale in about a year, and we find out about serialisation from a regulator instead of from a spreadsheet.  I would rather not test that.

**"You've catalogued eighty-two products that don't exist."**
> Correct, and I would rather be told that now than after we had built them.  What exists is the agreement on what each one contains, who owns it and what the fields mean — across eleven business areas and three estates.  That agreement is the part that normally fails.  The eighty-two schemas are a fortnight's work once somebody says go.

**"You've told us what's broken. What's actually good?"**
> Three things.  The sites run better than their systems deserve — the parent has been passing inspection on judgement and discipline, and that is a real asset, it is just not a scalable one.  The acquisitions are worth more than we paid for, because we valued capacity and got a regulated operating model.  And six governance leaders who had never worked together produced twelve pieces of work that fitted together first time.  That last one is the one I did not expect.

---

## Appendix: Where every number comes from

| Claim | Source |
|---|---|
| Sixteen flows; the four tests; seven adopted, nine new | [`0. data-governance-program/strategic-information-supply-chains.md`](../0.%20data-governance-program/strategic-information-supply-chains.md) |
| 82 components, 130 connections, membership and wiring | [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md) |
| Three estates; 29 / 45 / 30 systems; the convergent stacks; the reconciliation question on the four Austin entries; three ledgers | [strategic-supply-chain-system-matches.md](strategic-supply-chain-system-matches.md) |
| 23 covered / 17 unconfirmed / 20 acquisitions-only / 8 nowhere; the eight with nothing anywhere; per-group and per-flow coverage | [mapping-the-systems/system-mapping-report.md](mapping-the-systems/system-mapping-report.md) — generated by `mapping-the-systems.ipynb`, gitignored, so run the notebook before quoting it |
| 128 lineage rows over 87 system hops, 39 carrying more than one flow | `mapping-the-systems/supply-chain-lineage.ipynb` |
| Ten governance domains, twelve documents, six leaders; the no-forward-references property | [`0. data-governance-program/README.md`](../0.%20data-governance-program/README.md) |
| 82 products, 156 structures, 1,027 fields, 125 dependencies | [strategic-digital-products/README.md](strategic-digital-products/README.md) |
| Austin's five-year telemetry lake; the LIMS and Maximo connections we were missing | [strategic-supply-chain-system-matches.md](strategic-supply-chain-system-matches.md), Findings |

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
