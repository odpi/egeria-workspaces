# Coco Pharmaceuticals — Health and Safety Governance

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-23  
> **Description:** Governance definitions for the Health and Safety domain at Coco Pharmaceuticals, domain identifier `Health and Safety`. The file registers the domain identifier as a valid metadata value before any definition claims it, then defines the drivers, policies, and controls for the domain. Load `joint-governance-officer-definitions.md` and `manufacturing-governance-program.md` first.

---

## Overview

Health and safety is established here as a governance domain because the data it depends on has the same characteristics as the data governed elsewhere in this programme — it is evidential, it is retained for decades, it is inspected, and when it is wrong someone is harmed. What distinguishes it is the direction of protection. Every other control in the manufacturing environment protects the product from the people; these controls protect the people from the product.

That inversion is not merely rhetorical, and it produces the domain's most demanding governance problem. Coco Pharmaceuticals handles compounds that are pharmacologically active at very small doses, and the containment required to protect an operator can conflict directly with the conditions required to protect a sterile product. Airflow that pulls contamination away from an operator pushes it towards the product; gowning that protects the operator from a potent compound may shed particles; an isolator that contains a compound complicates the aseptic intervention it encloses. These conflicts are resolved by engineering judgement, but they must first be recognised, and a change assessed only for its GMP consequences will pass while creating an exposure risk that nobody evaluated.

The domain covers three bodies of data:

1. **Hazard and exposure data** — what substances and processes are hazardous, at what level, and what exposure people are actually receiving.
2. **Health surveillance data** — the medical monitoring of individuals working with those substances, which is health data of the most sensitive kind and must be retained for forty years.
3. **Incident and near miss data** — what has gone wrong or nearly gone wrong, and what was learned.

Its dependencies run through several domains. Competency and employment records come from Human Resource Management; occupational health data sits under the privacy framework and requires handling stricter than ordinary employee data; and the containment controls it specifies must be reconciled with the manufacturing controls governing the same rooms and the same processes.

---

## Part 1: Domain Registration

___

## Setup Valid Metadata Value

### Metadata Property Name
domainIdentifier

### Preferred Value
24

### Metadata Display Name
Health and Safety

### Metadata Description
The governance domain for health and safety encompasses the policies, practices and controls that protect workers, visitors and contractors from harm arising from the organisation's activities. It covers the identification and assessment of hazards, the control of occupational exposure to hazardous substances, the health surveillance of individuals working with them, and the recording, investigation and reporting of incidents. In a pharmaceutical manufacturing context it carries the additional requirement of reconciling containment measures that protect people with the sterility and quality measures that protect the product, since the two can impose conflicting demands on the same process.

___

---

## Part 2: Governance Drivers — Health and Safety

---

### 2.1 Business Imperatives

___

## Create Business Imperative

### Display Name
A Workforce Protected from the Compounds It Handles

### Qualified Name
CocoPharma::BusinessImperative::WorkforceProtectedFromExposure

### Domain Identifier
Health and Safety

### Summary
Coco Pharmaceuticals must know the hazard of every compound its people handle, control exposure to it, and be able to demonstrate that control from data rather than from assertion.

### Description
The company's move towards targeted and personalised therapies means the compounds it handles are becoming more potent, not less. A cytotoxic or highly active compound may have an occupational exposure limit measured in nanograms per cubic metre, a level at which the difference between adequate and inadequate containment cannot be perceived by the people working in the room and can only be established by measurement. This imperative treats exposure control as a data problem for that reason: without hazard characterisation, exposure monitoring, and health surveillance data that is complete and current, the company does not know whether its people are protected and neither do they. The consequences of getting it wrong are slow and often irreversible — occupational disease frequently presents years after the exposure that caused it, by which time the exposure records are the only evidence of what happened, and their absence has historically been decisive in litigation. The imperative also carries a workforce dimension: people will not do this work, and should not, without confidence that the exposure they are accepting is known and controlled.

### Implications
- Hazard must be characterised before a compound enters a facility, not after
- Control adequacy at low exposure limits can only be established by measurement
- Exposure records are the evidence base for disease presenting decades later
- Confidence in control is a condition of recruiting and retaining people for this work

### Outcomes
- Occupational exposure is known and controlled rather than assumed acceptable
- The company can answer questions about historical exposure from records
- People handling potent compounds do so with evidenced protection

### Importance
Critical

### Category
Health and Safety

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.2 Threats

___

## Create Threat

### Display Name
Occupational Exposure to Potent Compounds

### Qualified Name
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Domain Identifier
Health and Safety

### Summary
Workers may be exposed to pharmacologically active compounds above safe levels through containment failure, inadequate hazard characterisation, or activities where containment was never assessed.

### Description
Exposure rarely occurs through dramatic failure. It occurs through the activities that sit around the contained process — maintenance on equipment that has been cleaned but not verified clean, sampling and weighing steps performed outside the isolator because the isolator makes them awkward, cleaning of areas where residues accumulate, and waste handling downstream of every other control. These activities are frequently performed by people who are not the process operators, who may be contractors, and whose exposure was not considered when the containment strategy was designed for the process itself. A second route is inadequate hazard characterisation, which affects new compounds most: a molecule in early development may have no occupational exposure limit set, and in the absence of data the tendency is to handle it under general precautions rather than to band it conservatively. The harm is characteristically delayed and cumulative, which removes the feedback that would otherwise correct behaviour — nobody feels the exposure, nothing appears to go wrong, and the practice persists until surveillance detects an effect or a disease presents years later.

### Implications
- Maintenance, cleaning, sampling, and waste handling need separate exposure assessment
- Contractors performing these activities must be within the exposure control regime
- New compounds without an established limit must be banded conservatively, not handled generally
- Absence of perceptible harm provides no feedback, so control cannot rely on operator experience

### Importance
Critical

### Category
Health and Safety

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Threat

### Display Name
Under-reporting of Incidents and Near Misses

### Qualified Name
CocoPharma::Threat::IncidentUnderReporting

### Domain Identifier
Health and Safety

### Summary
Incidents and near misses may go unreported, removing the information the organisation needs to correct conditions before they cause serious harm.

### Description
Serious injuries are preceded by a much larger number of near misses arising from the same conditions, and the near misses are the affordable opportunity to intervene. Under-reporting destroys that opportunity, and it is driven by predictable causes: reporting that takes longer than the work it interrupts, a suspicion that reports lead to blame rather than to change, a belief that nothing will be done, and pressure on metrics that rewards low incident counts and therefore rewards silence. The last is the most damaging because it is self-reinforcing — a site with a falling incident rate and a falling near miss rate is usually not becoming safer but becoming quieter, and the metric that was supposed to detect the problem now conceals it. Contractor and agency workers under-report more than employees, having less job security and less confidence in the process, and they are disproportionately represented in exactly the maintenance and cleaning activities where exposure risk concentrates. The threat is invisible by construction: an organisation cannot see the reports it did not receive, and only the ratio between minor and serious events reveals that the base is missing.

### Implications
- Near miss volume is the leading indicator; its absence is a warning rather than a reassurance
- Reporting must be faster than the work it interrupts, or it will not happen
- Metrics rewarding low counts create an incentive to under-report
- Contractors and agency workers require particular attention and a route they trust

### Importance
High

### Category
Health and Safety

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.3 Regulations

___

## Create Regulation

### Display Name
Control of Substances Hazardous to Health Regulations 2002 (COSHH)

### Qualified Name
CocoPharma::Regulation::COSHH2002

### Domain Identifier
Health and Safety

### Summary
UK regulations requiring employers to assess the risk from hazardous substances, prevent or control exposure, monitor exposure, provide health surveillance where indicated, and retain the resulting records for forty years.

### Description
COSHH is the principal regulatory driver for this domain at the UK sites, and its requirements are unusually data-centred for health and safety legislation. An employer must assess the risk arising from every hazardous substance and every activity involving one, and the assessment must be suitable, sufficient, and kept current — an assessment that no longer describes how the work is done provides no protection and no defence. Where exposure cannot be prevented it must be adequately controlled, applying a hierarchy in which personal protective equipment is the last resort rather than the default. Exposure monitoring is required where the assessment indicates it, and health surveillance where an identifiable disease may result from exposure and valid techniques exist to detect it. The retention requirement is the striking one: health surveillance records must be kept for forty years from the last entry, and monitoring records for five, or forty where they relate to identifiable individuals under surveillance. Forty years exceeds the working life of the individual, the operating life of any facility, and the life of any system in which the records will initially be held.

### Regulation Source
Control of Substances Hazardous to Health Regulations 2002 (SI 2002/2677), as amended

### Regulators
- Health and Safety Executive (HSE) — UK
- Local authority environmental health departments

### Implications
- Assessments must remain current with how work is actually done, not as first written
- Personal protective equipment is the last resort in the control hierarchy, not the default
- Health surveillance records must be retained for forty years from the last entry
- Retention exceeds the life of the systems that will hold the records, requiring migration
- Monitoring must be conducted where the assessment indicates, not only where convenient

### Importance
Critical

### Category
Health and Safety

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Regulation

### Display Name
EU Occupational Safety and Health Framework Directive 89/391/EEC

### Qualified Name
CocoPharma::Regulation::EUOSHFrameworkDirective

### Domain Identifier
Health and Safety

### Summary
The EU directive establishing general principles for preventing occupational risk, requiring employers to assess risks, apply a defined hierarchy of prevention, document assessments, and consult workers on safety matters.

### Description
Directive 89/391/EEC is the foundation of occupational safety law across the EU subsidiaries, transposed into national legislation that adds detail and in several member states goes further than the directive requires. Its general principles of prevention set the order in which risk must be addressed — avoid the risk, evaluate what cannot be avoided, combat it at source, adapt the work to the individual, replace the dangerous with the less dangerous, and give collective protective measures priority over individual ones — and that ordering is legally operative rather than advisory, so a control strategy resting on personal protective equipment where engineering control was feasible is non-compliant regardless of whether exposure stayed within limits. The directive also requires worker consultation and participation on health and safety matters, and requires that workers designated to carry out protective activities have the necessary capability and means. Because national transpositions differ, the group operates to the strictest applicable standard across its sites rather than to each local minimum, which is simpler to govern and avoids a site-by-site defence of differing protection.

### Regulation Source
Council Directive 89/391/EEC on measures to encourage improvements in the safety and health of workers, as transposed in each member state

### Regulators
- National labour inspectorates in EU member states
- European Agency for Safety and Health at Work (EU-OSHA) — guidance

### Implications
- The hierarchy of prevention is legally operative, not advisory guidance
- Collective protective measures take priority over individual protection
- Risk assessments must be documented and available to inspectors
- Worker consultation on safety matters is a requirement, not a courtesy
- National transpositions differ, so the group works to the strictest applicable standard

### Importance
Critical

### Category
Health and Safety

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Policies — Health and Safety

---

### 3.1 Governance Principles

___

## Create Governance Principle

### Display Name
Control at Source Before Protection at the Person

### Qualified Name
CocoPharma::GovernancePrinciple::ControlAtSourceBeforeProtection

### Domain Identifier
Health and Safety

### Summary
Exposure is controlled by elimination, substitution, and engineering measures before any reliance is placed on personal protective equipment, and reliance on protective equipment is recorded as a residual rather than treated as a solution.

### Description
The hierarchy exists because the measures at its top work whether or not anyone does anything, while those at the bottom work only if a person does something correctly every time. An enclosed transfer protects everyone in the room continuously; a respirator protects one person if it is the right type, correctly fitted, worn throughout, and maintained. Personal protective equipment is therefore treated as evidence of unresolved risk rather than as risk control: where the assessment concludes that protective equipment is necessary, that conclusion is recorded with the reason engineering control was not reasonably practicable, and it is revisited when the process changes or the technology moves. The principle bites hardest on the activities that surround the contained process — maintenance, cleaning, sampling — where the engineering control was designed for the process and the ancillary tasks were left to protective equipment by default rather than by assessment. It also requires that the demands of containment and the demands of product protection be reconciled explicitly, since a measure protecting the operator may compromise the product and the resolution belongs to both domains rather than to whichever assesses the change first.

### Implications
- Reliance on protective equipment is recorded with the reason engineering control was rejected
- That reasoning is revisited on process change and as containment technology advances
- Ancillary activities require their own assessment, not inheritance of the process control
- Conflicts between containment and product protection are resolved jointly, not sequentially

### Outcomes
- Protection does not depend on correct individual behaviour every time
- Unresolved risk is visible as such rather than presented as controlled
- Containment and sterility conflicts surface at design rather than in operation

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Incidents Are Reported Without Blame

### Qualified Name
CocoPharma::GovernancePrinciple::IncidentsReportedWithoutBlame

### Domain Identifier
Health and Safety

### Summary
Reporting an incident or near miss carries no adverse consequence for the reporter, investigation addresses the conditions rather than the individual, and metrics are never constructed so that low reported counts are rewarded.

### Description
An organisation only learns about the conditions that cause harm if the people who encounter them say so, and they will only say so if reporting is safe. The principle therefore protects the reporter explicitly, directs investigation at the conditions that made the outcome possible rather than at the person closest to it, and — the part most often omitted — prohibits metric constructions that reward low counts. A site incentivised on incident rate has been given a reason to discourage reporting, and will do so through informal pressure that no policy statement counters. The protection is not unlimited: it covers error, omission, and the ordinary human variability that well-designed systems accommodate, and it does not extend to wilful disregard of a known control or to falsifying records, which is a distinction that must be stated so that the protection is credible rather than vague. Because contractors and agency workers report less readily than employees, and are disproportionately present in the higher-risk ancillary activities, the principle requires a reporting route available to them that does not run through the company staff supervising their work.

### Implications
- Metrics must never reward low reported counts, which creates pressure to under-report
- Investigation addresses conditions, and identifies the individual only where relevant to them
- The boundary excluding wilful disregard must be stated, or the protection reads as vague
- Contractors need a reporting route that bypasses the staff supervising their work

### Outcomes
- The organisation hears about conditions while they are still near misses
- Investigation produces changes to systems rather than to individuals
- Reported volume can be read as engagement rather than as deterioration

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Health Surveillance Data Serves the Worker First

### Qualified Name
CocoPharma::GovernancePrinciple::HealthSurveillanceServesWorker

### Domain Identifier
Health and Safety

### Summary
Health surveillance exists to protect the individual being monitored, their clinical data is held by occupational health and not by management, and the employer receives fitness conclusions rather than medical findings.

### Description
Health surveillance places the company in possession of medical information about its employees, and the arrangement is only defensible if the information flows in a way that serves the person it concerns. The principle separates the two roles: occupational health holds the clinical record and the findings within it, and the employer receives a conclusion about fitness for a role and any adjustment required, without the underlying medical detail. A manager needs to know that an individual should not work with a particular substance; they do not need to know the test result that led to that conclusion, and giving it to them converts a protective measure into a source of employment risk for the individual. The principle also requires that findings reach the individual first and in a form they can act on, and that a result indicating an effect triggers investigation of the workplace rather than only of the person — an individual's surveillance result is, among other things, a measurement of whether the control regime is working, and treating it solely as a personal medical matter loses that signal. Records outlive employment by decades, which makes their custody and eventual retrieval a governance matter in its own right.

### Implications
- Occupational health holds clinical detail; management receives fitness conclusions only
- Findings reach the individual first, in a form they can act on
- A result indicating an effect triggers workplace investigation, not only individual follow-up
- Custody arrangements must survive the forty-year retention and system changes within it

### Outcomes
- Individuals can participate in surveillance without creating employment risk for themselves
- Control failures are detected through surveillance results as well as through monitoring
- Records remain retrievable when a disease presents decades later

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.2 Governance Obligations

___

## Create Governance Obligation

### Display Name
Hazardous Substance Assessments Must Be Current for Every Substance and Task

### Qualified Name
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Domain Identifier
Health and Safety

### Summary
Every hazardous substance and every task involving one must have a current assessment covering the task as actually performed, reviewed on change and on a defined cycle.

### Description
The obligation attaches to the combination of substance and task rather than to the substance alone, because the same compound presents different exposure in weighing, in a closed transfer, and in cleaning the vessel afterwards. Assessments must describe the task as it is actually performed, which requires them to be written with the people who do the work and verified against practice rather than against the procedure — a divergence between the two is itself a finding, since it means either the assessment or the procedure does not describe reality. Currency is maintained through triggers as well as cycles: a process change, a facility change, a new substance, a change in supplier that alters physical form, an incident, or a monitoring result above expectation each require review, and change control must route to the assessment rather than leaving the connection to memory. Ancillary tasks are explicitly in scope, since the recurring failure is a thorough assessment of the manufacturing step accompanied by no assessment of the maintenance performed on the same equipment. Contractor activities require assessment on the same basis as employee activities.

### Implications
- Assessment covers substance and task in combination, not substance alone
- Assessments must describe practice, and divergence from procedure is itself a finding
- Change control must route to assessment review rather than relying on recall
- Maintenance, cleaning, sampling, and waste handling require their own assessments
- Contractor activities are assessed on the same basis as employee activities

### Outcomes
- Every hazardous activity has an assessment that describes what is actually done
- Process and facility changes do not silently invalidate the assessment basis
- The activities where exposure concentrates are covered rather than assumed

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Occupational Exposure Must Be Monitored Against Banded Limits

### Qualified Name
CocoPharma::GovernanceObligation::ExposureMonitoredAgainstBandedLimits

### Domain Identifier
Health and Safety

### Summary
Every compound must carry an occupational exposure band or limit before entering a facility, and actual exposure must be monitored against it where the assessment indicates, with results retained and trended.

### Description
No compound enters a Coco Pharmaceuticals facility without a hazard classification, and where toxicological data is insufficient to set a limit the compound is banded conservatively rather than handled under general precautions — the absence of data is a reason for caution rather than a reason for its absence. Monitoring is conducted where the assessment indicates, and the obligation requires the monitoring strategy to sample the activities that actually produce exposure rather than the ambient conditions that are easiest to measure: static area sampling in a corridor tells nothing about what a person received while breaking a containment seal. Results are compared against the band, retained for the required period, and trended, because a single result within limit says little and a rising trend within limit is the early warning the whole regime exists to produce. Results above limit require immediate action on the activity and investigation of the control failure, not merely a repeat measurement. Because the retention requirement extends to forty years where results relate to individuals under surveillance, results must be recorded against the individual and the activity in a form that will still be interpretable when the systems holding them have been replaced several times.

### Implications
- No compound enters a facility without a band or limit; missing data means conservative banding
- Monitoring must sample the exposing activities, not the ambient conditions
- Trending within limit is required, as a rising trend is the early warning
- Results above limit require action on the activity, not a repeat measurement
- Records must remain interpretable across forty years and several system generations

### Outcomes
- Exposure is known quantitatively rather than inferred from control design
- Deteriorating control is detected before a limit is exceeded
- Historical exposure can be reconstructed for an individual decades later

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Health Surveillance Must Be Provided and Its Records Retained for Forty Years

### Qualified Name
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Domain Identifier
Health and Safety

### Summary
Health surveillance must be provided where exposure may cause an identifiable disease, and records retained for forty years from the last entry in a form that remains retrievable and interpretable.

### Description
Surveillance is required where an identifiable disease may result from exposure and a valid technique exists to detect it, which for Coco Pharmaceuticals covers work with sensitising compounds, cytotoxics, and certain solvents. Provision is the straightforward part; retention is where the obligation becomes a governance problem. Forty years from the last entry means records created today will be required into the 2060s, long after the individual has left, the facility may have closed, and every system now holding the data has been replaced. Retention of the values alone is insufficient — the record must remain interpretable, which means retaining what was measured, by what method, against what limit in force at the time, and linked to the exposure history that explains why the individual was under surveillance at all. Migration between systems must preserve that linkage and be verified to have done so. The obligation also survives corporate change: records must transfer on divestment or closure rather than being lost with the entity, and where a site closes the arrangement for continued access must be established before it does rather than improvised afterwards.

### Implications
- Retention runs forty years from the last entry, outliving employment, systems, and facilities
- Records must retain method, limit in force, and the linked exposure history to stay interpretable
- Migrations must preserve linkage and be verified, not assumed
- Arrangements must survive site closure and corporate divestment
- Erasure is unavailable, and this must be explained to individuals at the point of surveillance

### Outcomes
- A disease presenting decades later can be assessed against real exposure records
- The company can discharge its obligations to former employees long after they leave
- Records survive the organisational changes that would otherwise destroy them

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Incidents and Near Misses Must Be Recorded, Investigated, and Reported

### Qualified Name
CocoPharma::GovernanceObligation::IncidentsRecordedAndReported

### Domain Identifier
Health and Safety

### Summary
Every incident and near miss must be recorded when it occurs, investigated proportionately to its potential rather than its actual outcome, and reported to the regulator where the reporting criteria are met.

### Description
Investigation depth is set by potential consequence rather than by what happened, which is the distinction that determines whether an organisation learns anything. A dropped component that struck nobody and the same component striking someone arise from identical conditions and warrant identical investigation; grading by actual outcome means the organisation investigates thoroughly only after it has been unlucky. Recording must be immediate and low-friction, since a report deferred to the end of a shift is frequently not made and is less accurate when it is. Statutory reporting criteria differ across the jurisdictions the group operates in — specified injuries, over-seven-day incapacitation, dangerous occurrences, and occupational diseases each carry their own thresholds and deadlines under the UK regime, with member state equivalents in the EU — and the obligation requires the assessment against those criteria to be made by someone competent to make it rather than by the person recording the event. Investigation findings must connect to action with an owner and a date, and the effectiveness of that action must be checked, on the same basis as the CAPA obligation in manufacturing.

### Implications
- Investigation depth follows potential consequence, not actual outcome
- Recording must be immediate and low-friction, or it will be deferred and degraded
- Statutory reportability is assessed by a competent person, not by the reporter
- Findings must connect to owned, dated actions whose effectiveness is verified
- Near misses are recorded on the same basis as incidents, not as an optional extra

### Outcomes
- The organisation learns from the events that could have been serious
- Regulatory reporting obligations are met within their deadlines
- Corrective action is verified to have worked rather than assumed

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Hazardous Substances Must Be Registered with a Current Safety Data Sheet

### Qualified Name
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Domain Identifier
Health and Safety

### Summary
Every hazardous substance held at any site must be recorded in the substance register with its location, quantity, hazard classification, and a current safety data sheet, before it is brought on site.

### Description
The assessment obligation requires an assessment for every hazardous substance and every task involving one, and that requirement has no denominator until the organisation knows what substances it holds. The register supplies it. Each entry records what the substance is, where it is held and in what quantity, how it is classified for hazard, and which supplier's safety data sheet applies — and the sheet is the upstream source for every assessment written against that substance, so a superseded sheet silently invalidates the assessments derived from it. Suppliers reclassify substances and reissue sheets without prompting, which makes currency an active obligation rather than a filing one. Research laboratories are the demanding case and the reason the register cannot be an annual stocktake: a laboratory may take delivery of a novel compound one week and consume it the next, and a register describing last quarter's holdings tells an emergency responder nothing useful about what is in the building tonight. Registration before arrival is therefore required, and reconciliation against procurement records is how substances that arrived outside the process are found.

### Implications
- Registration precedes arrival on site, not follows it
- Safety data sheet currency must be actively maintained, since suppliers reissue without prompting
- A superseded sheet invalidates the assessments derived from it and triggers their review
- Location and quantity must be current enough to inform emergency response
- Reconciliation against procurement finds substances that arrived outside the process

### Outcomes
- The assessment obligation has a known and complete population to work against
- Emergency responders can be told what is present and where
- Supplier reclassification reaches the assessments that depend on it

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Hazardous Waste Must Be Classified, Consigned, and Tracked to Final Disposal

### Qualified Name
CocoPharma::GovernanceObligation::HazardousWasteConsignedAndTracked

### Domain Identifier
Health and Safety

### Summary
Hazardous waste must be classified correctly at the point it arises, transferred only to authorised carriers and sites, and tracked through consignment records retained for the statutory period.

### Description
Duty of care over waste does not end when it leaves the site — it follows the waste to its final destination, and the company remains liable for a consignment misdescribed on the paperwork or delivered to a site not authorised to receive it. Classification at the point of arising is where accuracy is determined, because the person generating the waste knows what it is and the contractor collecting it does not; a drum described generically as laboratory waste cannot be treated correctly and may be refused, returned, or mishandled. Pharmaceutical waste carries categories that ordinary industrial classification handles poorly — cytotoxic and cytostatic residues, out-of-date controlled drugs, and material contaminated with biological agents each have their own route — and mixing them into a general stream is both a compliance failure and a hazard to the people handling it downstream. The records are the evidence: consignment notes and transfer notes must be retained for the statutory period and must reconcile against what the carrier reports receiving, since a discrepancy between the two is how illegitimate disposal is detected.

### Implications
- Classification happens where the waste arises, by the people who know what it is
- Carriers and receiving sites must be verified as authorised before transfer, and re-verified periodically
- Cytotoxic, controlled drug, and biologically contaminated streams must be segregated by route
- Consignment records must be retained for the statutory period and reconciled against carrier returns
- Discrepancies between consignment and receipt must be investigated, not filed

### Outcomes
- Waste reaches a destination authorised to receive it and is treated correctly
- The company can evidence its duty of care through to final disposal
- Downstream handlers are not exposed to hazards the paperwork did not declare

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Emergency Arrangements Must Match the Hazards Actually Present

### Qualified Name
CocoPharma::GovernanceObligation::EmergencyResponseMatchesHazards

### Domain Identifier
Health and Safety

### Summary
Spill, exposure, and release response arrangements must be derived from the substances actually held at each location, communicated to those who would respond, and exercised.

### Description
Emergency arrangements written generically protect nobody, because the correct response to a spill depends entirely on what was spilled — a solvent, a cytotoxic compound, and a biological agent each demand different containment, different protective equipment, different decontamination, and different medical follow-up, and the wrong response can be worse than none. The obligation therefore derives arrangements from the substance register for each location rather than from a template, and requires them to change when the holdings change. External responders are explicitly in scope: the fire service arriving at a research building at night needs to know what is inside before entering, and that information has to have been provided in advance and kept current, not assembled during the incident. Exposure response has a medical dimension that is frequently overlooked — some compounds require specific treatment within a short window, and the information has to reach occupational health and the local emergency department before it is needed rather than being looked up while someone waits. Arrangements are exercised, because a procedure never rehearsed is a document rather than a capability.

### Implications
- Arrangements are derived from the substance register per location, not from a template
- Holdings changes must trigger review of the response arrangements
- External responders must be given current information in advance of any incident
- Compound-specific medical treatment information must reach occupational health beforehand
- Arrangements must be exercised, not only written

### Outcomes
- The response to a spill or exposure matches what was actually released
- External responders enter buildings knowing what is inside
- Exposure treatment begins within the window that makes it effective

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.3 Governance Approaches

___

## Create Governance Approach

### Display Name
Occupational Exposure Banding

### Qualified Name
CocoPharma::GovernanceApproach::OccupationalExposureBanding

### Domain Identifier
Health and Safety

### Summary
Compounds are assigned to hazard bands from their toxicological and pharmacological data, and each band prescribes the containment, monitoring, and surveillance regime applied to any work with a compound in it.

### Description
Banding converts a compound-by-compound judgement into a systematic control decision, which matters most for the many compounds in development that will never accumulate enough data for a formal occupational exposure limit. A compound is assigned a band from what is known about its potency, its pharmacological effect, and any evidence of sensitisation, genotoxicity or reproductive toxicity, and the band then determines the containment standard required, whether monitoring is conducted, and whether health surveillance applies. Assignment happens before the compound arrives, is made by qualified toxicological judgement rather than by the receiving site, and is recorded with the reasoning and the data it rested on so that it can be revisited as data accumulates. Provisional assignments for early-stage compounds are conservative by design and are reviewed as toxicology develops, with reassignment downwards requiring the same rigour as assignment upwards. The banding record is the pivot on which the whole regime turns: it determines the containment engineering purchased, the monitoring conducted, and the individuals placed under surveillance, so an error in it propagates into every downstream control.

### Implications
- Assignment precedes arrival and is made by qualified toxicological judgement
- Provisional bands for early compounds are conservative and reviewed as data develops
- Reassignment downwards requires the same rigour as assignment upwards
- The band drives containment, monitoring, and surveillance, so errors propagate widely
- Assignment reasoning and its supporting data must be recorded, not only the result

### Outcomes
- Compounds without formal exposure limits are still controlled systematically
- Containment investment is matched to hazard rather than to intuition
- The basis for a control regime can be reconstructed and challenged

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Learning from Near Misses and Weak Signals

### Qualified Name
CocoPharma::GovernanceApproach::LearningFromNearMisses

### Domain Identifier
Health and Safety

### Summary
Near misses and low-level signals are actively sought, aggregated across sites, and analysed for the conditions they share, with reporting volume treated as a measure of engagement rather than of deterioration.

### Description
The approach treats near miss data as the organisation's principal safety intelligence and manages it accordingly. Reporting is made easier than not reporting, which in practice means a route that takes under a minute and does not require the reporter to classify or investigate anything. Reports are aggregated across sites, because a condition appearing once at each of four sites is invisible locally and obvious centrally, and analysed for shared conditions rather than counted. Feedback to reporters is treated as part of the mechanism rather than a courtesy: people stop reporting when nothing visibly follows, so what changed as a result is communicated back, including where the answer is that nothing changed and why. Reporting volume is deliberately interpreted as engagement, with a falling rate investigated as a possible reporting failure before being accepted as an improvement — the approach explicitly rejects the reading in which fewer reports means a safer site. Contractors are brought within the same system with a route that does not run through their supervising staff, since they perform much of the highest-exposure ancillary work.

### Implications
- Reporting must take under a minute and require no classification by the reporter
- Aggregation across sites is required, as shared conditions are invisible locally
- Feedback on what changed is part of the mechanism, not an optional courtesy
- A falling report rate is investigated as a reporting failure before being celebrated
- Contractors report through a route independent of their supervising staff

### Outcomes
- Conditions are corrected while they are still producing near misses
- Cross-site patterns are identified rather than repeatedly rediscovered locally
- Reporting culture is sustained by visible response

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Chemical Inventory and Safety Data Sheet Management

### Qualified Name
CocoPharma::GovernanceApproach::ChemicalInventoryManagement

### Domain Identifier
Health and Safety

### Summary
One substance register serves every downstream use — assessment, monitoring, waste routing, emergency response, and transport classification — populated at the point substances are ordered and maintained by the people who hold them.

### Description
The approach treats the substance register the way the data programme treats master data: one authoritative record, populated once, consumed by everyone who needs it. The alternative that organisations drift into is several partial lists — a procurement record, a laboratory's own spreadsheet, a fire safety schedule, a waste contractor's manifest — which disagree with each other and are each wrong in different ways. Population runs from ordering, so that a substance is registered before it arrives, with reconciliation against delivery and against periodic physical checks to find what bypassed the process. Safety data sheets are held against the register entry and refreshed on a cycle and on supplier notification, with a change in classification propagating to the assessments that depend on it rather than sitting unread. The approach differentiates by setting: manufacturing holds a small number of substances in large quantities with stable tasks, and a periodic cycle suits it, while research laboratories hold a large and changing variety in small quantities where registration must be immediate and lightweight or it will not happen. Applying the manufacturing rhythm to a research bench is how registers become fiction.

### Implications
- One register, populated from ordering, consumed by every downstream use
- Reconciliation against delivery and physical check finds what bypassed the process
- Classification changes propagate to dependent assessments rather than being filed
- Research settings need immediate lightweight registration; manufacturing suits a periodic cycle
- Register content must carry what transport, waste, and emergency response each need

### Outcomes
- Assessment, waste, emergency and transport decisions rest on the same substance data
- Substances present in research buildings are known while they are still there
- Supplier reclassification reaches the controls that depend on it

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 4: Governance Controls — Health and Safety

---

### 4.1 Governance Roles

___

## Create Governance Role

### Display Name
Head of Health and Safety (Governance Domain Lead)

### Qualified Name
CocoPharma::GovernanceRole::HeadOfHealthAndSafety

### Description
The Head of Health and Safety holds the domain lead role for identifier 24, accountable for hazard assessment, exposure control, health surveillance provision, and incident management across the group's sites. The role owns the exposure banding framework, approves the containment standard applied to each band, is the competent person for statutory reportability decisions, and reports exposure, surveillance, and incident measures to the governance leadership. It reports to the Head of Human Resources, who holds the domain, while retaining the independence to stop work it judges unsafe, and it is the counterparty to the Manufacturing Governance Lead when containment and product protection requirements conflict — a conflict that neither role may resolve unilaterally.

### Scope
Health and safety governance domain — hazard and exposure data, occupational exposure banding and monitoring, health surveillance provision, incident and near miss management, and contractor safety across all sites.

### Headcount
1

### Category
Governance Role

### Search Keywords
- health and safety
- occupational exposure
- containment
- incident management

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Role

### Display Name
Occupational Hygienist

### Qualified Name
CocoPharma::GovernanceRole::OccupationalHygienist

### Description
The Occupational Hygienist designs and conducts the exposure monitoring programme: determining which activities require monitoring, selecting sampling strategies that capture actual exposure rather than ambient conditions, interpreting results against the applicable band, and trending results to detect deteriorating control before a limit is exceeded. The role assesses containment performance during commissioning and after modification, advises on the hazardous substance assessments for ancillary activities, and is the technical authority on whether a proposed control measure will achieve the required exposure level. It works with occupational health on which individuals require surveillance based on their assessed exposure, and with engineering on containment design.

### Scope
Exposure monitoring strategy and interpretation, containment performance assessment, technical review of control measures, and identification of individuals requiring health surveillance.

### Headcount
3

### Category
Governance Role

### Search Keywords
- occupational hygiene
- exposure monitoring
- containment performance
- sampling strategy

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 4.2 Governance Metrics

___

## Create Governance Metric

### Display Name
Exposure Monitoring Coverage and Trend

### Qualified Name
CocoPharma::GovernanceMetric::ExposureMonitoringCoverage

### Domain Identifier
Health and Safety

### Summary
Measures the percentage of activities requiring monitoring that have a result within their sampling interval, reported with the proportion of results in the upper fraction of the applicable band.

### Description
Two figures are reported because coverage alone is uninformative. Coverage measures whether the monitoring programme is actually running — activities whose assessment requires monitoring but which have no current result are a gap, and they concentrate predictably in the ancillary tasks that were assessed late and scheduled last. The second figure reports results in the upper fraction of the band, typically above half the limit, because a programme reporting only exceedances is a lagging indicator: exposures drifting upward within limit are what precede an exceedance, and reporting them is what allows intervention beforehand. Results are reported by activity rather than by individual for control purposes, since the question is whether the control works, while individual attribution is retained separately for the surveillance and retention obligations. Contractor-performed activities are reported distinctly, as these are both higher risk and more likely to fall outside the monitoring schedule. Any single result above limit is reported individually and immediately rather than appearing in a periodic summary.

### Implications
- Coverage is measured against activities the assessment requires to be monitored
- Results in the upper fraction of the band must be reported, not only exceedances
- Reporting is by activity for control purposes, with individual attribution retained separately
- Contractor activities are reported distinctly, being higher risk and less well scheduled
- Above-limit results are escalated individually and immediately

### Outcomes
- Gaps in the monitoring programme are visible rather than assumed absent
- Deteriorating control is detected while exposures remain within limit
- Contractor exposure receives the same scrutiny as employee exposure

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Near Miss to Incident Ratio

### Qualified Name
CocoPharma::GovernanceMetric::NearMissToIncidentRatio

### Domain Identifier
Health and Safety

### Summary
Measures the ratio of reported near misses to reported incidents by site and by worker category, interpreted as a measure of reporting culture rather than of safety performance.

### Description
The ratio is the most reliable available indicator of whether the organisation is hearing about the conditions that precede harm. A healthy site reports many near misses for each incident; a low ratio means either that near misses are not occurring, which is implausible in an industrial environment, or that they are not being reported. The metric is therefore explicitly framed as a measure of reporting culture, and the framing is stated in the reporting so that it cannot be read as a safety score and optimised in the wrong direction. Reporting is broken down by worker category — employee, agency, contractor — because contractor under-reporting is both predictable and concentrated in the higher-exposure ancillary activities, and an aggregate ratio dominated by employees would conceal it. Site comparison is included, since a site with a materially lower ratio than comparable sites has a reporting problem rather than a safety advantage. A falling ratio triggers investigation of the reporting route before any conclusion is drawn about incident frequency, and the metric is never combined into a composite safety score.

### Implications
- Framed and reported as a measure of reporting culture, not of safety performance
- Broken down by worker category, since contractor under-reporting is predictable
- Site comparison is required, as a low ratio indicates a reporting problem
- A falling ratio triggers investigation of the reporting route first
- Never combined into a composite score where it could be optimised perversely

### Outcomes
- Under-reporting is detectable rather than appearing as improvement
- Contractor reporting failures are visible and addressable
- The organisation retains its supply of leading-indicator data

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Health Surveillance Completion and Record Integrity

### Qualified Name
CocoPharma::GovernanceMetric::HealthSurveillanceCompletion

### Domain Identifier
Health and Safety

### Summary
Measures the percentage of individuals requiring health surveillance who have a completed assessment within its interval, and the proportion of retained records passing periodic retrievability verification.

### Description
The first figure is a compliance and welfare measure: individuals identified as requiring surveillance who have not received it are both a regulatory breach and a person whose early indication of harm is not being looked for. It is computed from the exposure assessment rather than from surveillance attendance, since the population requiring surveillance is defined by exposure and an individual missing from the surveillance list entirely is the failure that attendance-based reporting cannot detect. The second figure addresses the forty-year retention obligation, which no other metric in this programme approaches in duration. A sample of retained records is periodically retrieved and checked for whether the values, the method, the applicable limit, and the linkage to exposure history all remain present and interpretable — because a record that has survived two system migrations with its linkage broken is retained in name only, and the failure is discoverable now or discovered by a claimant in forty years. Records for individuals who have left the company are sampled specifically, as those are the ones most likely to have been dropped in a migration.

### Implications
- The surveillance population is derived from exposure assessment, not from attendance lists
- Retrievability verification must test interpretability, not merely that a file opens
- Former employee records are sampled specifically, being most at risk in migrations
- Verification must cover linkage to exposure history, not only the surveillance values

### Outcomes
- Individuals requiring surveillance receive it within the interval
- Retention failures are found while they can still be remediated
- Records remain usable for the full forty-year obligation

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Substance Register Completeness and Data Sheet Currency

### Qualified Name
CocoPharma::GovernanceMetric::SubstanceRegisterCompleteness

### Domain Identifier
Health and Safety

### Summary
Measures the percentage of registered hazardous substances holding a current safety data sheet and a linked assessment, reported alongside substances found on site but not registered.

### Description
Three figures are reported because they fail for different reasons and have different owners. Data sheet currency is a maintenance measure and sits with the register owner. Assessment linkage — the proportion of registered substances that have an assessment covering the tasks they are used in — is the measure that tells the health and safety function whether the assessment obligation is actually being met across the estate rather than in the areas that were looked at. Unregistered substances found during physical checks or procurement reconciliation are reported separately and are the most consequential of the three, because a substance nobody registered is absent from assessment, from emergency arrangements, and from waste routing simultaneously. Research settings are reported apart from manufacturing, since their registers turn over far faster and a currency figure averaged across both conceals whichever is worse. Substances whose classification changed since their linked assessment was written are flagged distinctly, as those are assessments that are current by date and wrong in substance.

### Implications
- Currency, assessment linkage, and unregistered finds are reported as three separate figures
- Research and manufacturing settings are reported separately given their different turnover
- Substances reclassified since their assessment was written are flagged as stale-in-substance
- Requires physical checks and procurement reconciliation to generate the unregistered figure

### Outcomes
- Assessment coverage across the whole estate is measurable rather than sampled
- Substances bypassing registration are found while they are still on site
- Reclassification that invalidates an assessment is visible before an incident reveals it

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 4.3 Data Processing Purposes

The data processing purposes declared by this domain are defined in `6. data-privacy/data-processing-purposes.md`, together with those of every other domain and the links that connect them to the policies they implement. They remain owned by this domain and members of its folio; they are gathered there so that the lawful bases can be reviewed as a set.

## Part 5: Governance Links

---

### 5.1 Governance Responses — Drivers linked to Health and Safety Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::COSHH2002

### Policy
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Rationale
COSHH requires a suitable and sufficient assessment kept current. Attaching it to substance and task in combination is what makes it describe the work rather than the chemical.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::COSHH2002

### Policy
CocoPharma::GovernanceObligation::ExposureMonitoredAgainstBandedLimits

### Rationale
Monitoring is required where the assessment indicates it, and the results are the only evidence that control is adequate at limits below the threshold of perception.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::COSHH2002

### Policy
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Rationale
The forty-year retention requirement is the obligation's defining difficulty, since it outlives the systems, the facility, and the employment relationship.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::COSHH2002

### Policy
CocoPharma::GovernancePrinciple::ControlAtSourceBeforeProtection

### Rationale
COSHH requires exposure to be prevented or adequately controlled, with personal protective equipment as the last resort rather than the primary measure.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUOSHFrameworkDirective

### Policy
CocoPharma::GovernancePrinciple::ControlAtSourceBeforeProtection

### Rationale
The general principles of prevention give collective measures priority over individual protection, and that ordering is legally operative rather than advisory.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUOSHFrameworkDirective

### Policy
CocoPharma::GovernanceObligation::IncidentsRecordedAndReported

### Rationale
The directive and its national transpositions require incident recording and reporting, and require workers to be consulted on the safety matters those incidents reveal.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Policy
CocoPharma::GovernanceApproach::OccupationalExposureBanding

### Rationale
Banding controls the compounds that will never have a formal exposure limit, which is most of the development portfolio, and does so before the compound arrives.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Policy
CocoPharma::GovernanceObligation::ExposureMonitoredAgainstBandedLimits

### Rationale
Sampling the exposing activities rather than ambient conditions is what detects the maintenance and cleaning exposures through which the threat actually materialises.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Policy
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Rationale
The threat concentrates in ancillary activities that were never assessed. Requiring assessment per task, including maintenance and cleaning, closes that gap directly.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::IncidentUnderReporting

### Policy
CocoPharma::GovernancePrinciple::IncidentsReportedWithoutBlame

### Rationale
Under-reporting is driven by consequence and by metric pressure. Protecting the reporter and prohibiting metrics that reward low counts addresses both causes.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::IncidentUnderReporting

### Policy
CocoPharma::GovernanceApproach::LearningFromNearMisses

### Rationale
Making reporting faster than not reporting, and feeding back what changed, is what sustains the flow of information the organisation depends on.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::WorkforceProtectedFromExposure

### Policy
CocoPharma::GovernancePrinciple::HealthSurveillanceServesWorker

### Rationale
People accept work with potent compounds on the basis that exposure is known and controlled, which requires surveillance arranged so that participating carries no employment risk.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Policy
CocoPharma::GovernanceObligation::IncidentsRecordedAndReported

### Rationale
Incident and exposure records are subject to the same integrity expectations as manufacturing records: they are evidential, they are inspected, and they must be attributable and contemporaneous.

___

---

### 5.2 Governance Mechanisms — Health and Safety Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ExposureMonitoredAgainstBandedLimits

### Mechanism
CocoPharma::GovernanceMetric::ExposureMonitoringCoverage

### Rationale
Coverage against activities requiring monitoring, with upper-band results reported, measures both whether the programme runs and whether control is drifting.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::OccupationalExposureBanding

### Mechanism
CocoPharma::GovernanceMetric::ExposureMonitoringCoverage

### Rationale
Results interpreted against the assigned band tell the banding framework whether its assignments and the containment they specified are holding in practice.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::IncidentsReportedWithoutBlame

### Mechanism
CocoPharma::GovernanceMetric::NearMissToIncidentRatio

### Rationale
The ratio is the observable consequence of the principle: where reporting is genuinely safe the ratio is high, and where it is not the ratio collapses regardless of policy.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::LearningFromNearMisses

### Mechanism
CocoPharma::GovernanceMetric::NearMissToIncidentRatio

### Rationale
Broken down by site and worker category, the ratio shows the approach where its reporting routes are failing, particularly for contractors.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Mechanism
CocoPharma::GovernanceMetric::HealthSurveillanceCompletion

### Rationale
Retrievability verification is the only way a forty-year retention obligation can be tested now rather than discovered to have failed decades later.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::COSHH2002

### Policy
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Rationale
COSHH requires an assessment for every hazardous substance, which presupposes knowing what substances are held. The register is the population the assessment obligation works against.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::COSHH2002

### Policy
CocoPharma::GovernanceObligation::EmergencyResponseMatchesHazards

### Rationale
COSHH requires arrangements to deal with accidents, incidents and emergencies related to hazardous substances, and those arrangements only work if they match what is actually present.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUOSHFrameworkDirective

### Policy
CocoPharma::GovernanceObligation::EmergencyResponseMatchesHazards

### Rationale
The directive requires employers to arrange first aid, firefighting and evacuation appropriate to the nature of the activities, and to give responders the information they need.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Policy
CocoPharma::GovernanceObligation::HazardousWasteConsignedAndTracked

### Rationale
Waste handling is the last point in the chain and frequently the least controlled. Segregating cytotoxic and biologically contaminated streams protects the people handling them downstream, including contractors.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Policy
CocoPharma::GovernanceApproach::ChemicalInventoryManagement

### Rationale
Substances absent from the register are absent from assessment and monitoring, which is how exposure occurs in the research settings where holdings turn over fastest.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Mechanism
CocoPharma::GovernanceMetric::SubstanceRegisterCompleteness

### Rationale
Currency, assessment linkage, and unregistered finds measure the obligation from three angles, each with a different owner.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ChemicalInventoryManagement

### Mechanism
CocoPharma::GovernanceMetric::SubstanceRegisterCompleteness

### Rationale
Reporting research and manufacturing settings separately tells the approach whether its differentiated registration rhythm is working in both.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Mechanism
CocoPharma::GovernanceMetric::SubstanceRegisterCompleteness

### Rationale
Assessment linkage across the registered population is what shows whether the assessment obligation is met estate-wide rather than in the areas that were examined.

___

---

### 5.3 Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Governance Driver 2
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Description
Containment protects the person from the product and cleanroom control protects the product from the person, and the two impose conflicting demands on airflow, gowning, and enclosure. A change assessed against only one of them can create an exposure risk or a contamination risk that nobody evaluated.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::IncidentUnderReporting

### Governance Driver 2
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Description
Both threats concern information the organisation needs but does not automatically receive, and both are aggravated by the same conditions — pressure, blame, and the belief that speaking up changes nothing.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::WorkforceProtectedFromExposure

### Governance Driver 2
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Description
The transition brings more potent and more biologically active compounds into the facilities, raising the containment standard required at the same time as it increases the number of small-scale manual operations where exposure occurs.

___

---

### 5.4 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::ControlAtSourceBeforeProtection

### Governance Policy 2
CocoPharma::GovernancePrinciple::ValidatedStateMaintained

### Description
A containment change and a validated-state change are frequently the same change viewed from two domains. Neither the Head of Health and Safety nor the Manufacturing Governance Lead may resolve the conflict alone, and change control must route to both rather than to whichever is asked first.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Description
Health and safety states the forty-year statutory requirement; privacy incorporates it into the retention schedule and resolves it against erasure rights. The period is set by statute and neither domain may shorten it.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Governance Policy 2
CocoPharma::GovernanceApproach::ManufacturingChangeControl

### Description
Change control is the mechanism by which assessments stay current. A process or facility change that does not route to hazard assessment review leaves the assessment describing work that is no longer done.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::IncidentsRecordedAndReported

### Governance Policy 2
CocoPharma::GovernanceObligation::CAPAEffectivenessVerified

### Description
Safety investigation and manufacturing CAPA share the same failure mode — closure on completion of the action rather than on evidence of its effect — and the safety obligation adopts the manufacturing effectiveness standard rather than defining a weaker one.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::HealthSurveillanceServesWorker

### Governance Policy 2
CocoPharma::GovernancePrinciple::EmploymentDecisionsOnRecordedCriteria

### Description
A fitness restriction may bear on redeployment or capability decisions, and the boundary must hold in both directions: employment decisions may use the restriction, never the medical finding behind it.

___

---


___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Governance Policy 2
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Description
The register establishes what must be assessed and the assessment obligation establishes what the assessment must cover. Neither works alone — a register without assessments is an inventory, and assessments without a register cover whatever happened to be noticed.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::HazardousWasteConsignedAndTracked

### Mechanism
CocoPharma::CertificationType::ApprovedThirdPartyStatus

### Rationale
Waste carriers and disposal sites are third parties handling hazardous material on the company's behalf, so their authorisation to receive it is verified through the same approval process as any other supplier, with the waste-specific licences checked in addition.

___

---

## Part 6: Health and Safety Governance Folio

---

### 6.1 Folio Definition

___

## Create Folio

### Display Name
Head of Health and Safety — Governance Folio

### Qualified Name
CocoPharma::Folio::HeadOfHealthAndSafety

### Description
The governance definitions owned by the Head of Health and Safety in domain 24, authored by Faith Broker alongside the human resources and privacy programs. The folio covers the workforce protection imperative, the occupational exposure and under-reporting threats, COSHH and the EU OSH Framework Directive, the control hierarchy, blame-free reporting and surveillance principles, the assessment, monitoring, surveillance retention and incident obligations, and the controls that measure them.

### Purpose
Provides the Head of Health and Safety with a single view of the definitions governing protection of people from the compounds and processes the company operates. Several of these definitions stand in deliberate tension with manufacturing definitions governing the same rooms and processes, and holding them in a distinct folio keeps that tension visible rather than allowing one set to be read as a subset of the other.

### Category
Governance Folio

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::HeadOfHealthAndSafety

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::HeadOfHealthAndSafety

### Description
Assigns the Head of Health and Safety role responsibility for the governance definitions collected in this folio.

___

---

### 6.2 Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::BusinessImperative::WorkforceProtectedFromExposure

### Membership Rationale
Knowing and controlling occupational exposure is the central commitment of this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Membership Rationale
Exposure to potent compounds, particularly in ancillary activities, is owned by the Head of Health and Safety.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::Threat::IncidentUnderReporting

### Membership Rationale
Under-reporting removes the leading-indicator data this domain depends on and is owned here.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::Regulation::COSHH2002

### Membership Rationale
COSHH obligations at the UK sites are discharged by the health and safety function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::Regulation::EUOSHFrameworkDirective

### Membership Rationale
The EU framework obligations across the EU subsidiaries are discharged by the health and safety function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernancePrinciple::ControlAtSourceBeforeProtection

### Membership Rationale
The control hierarchy and the recording of residual reliance on protective equipment are set by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernancePrinciple::IncidentsReportedWithoutBlame

### Membership Rationale
Reporter protection and the prohibition on metrics rewarding low counts are owned here.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernancePrinciple::HealthSurveillanceServesWorker

### Membership Rationale
The separation between clinical findings and management information is defined and enforced by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Membership Rationale
Assessment currency per substance and task is maintained by the health and safety function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::ExposureMonitoredAgainstBandedLimits

### Membership Rationale
The monitoring programme is designed and operated by the Occupational Hygienist.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Membership Rationale
Surveillance provision and the forty-year retention obligation are owned by this domain with occupational health.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::IncidentsRecordedAndReported

### Membership Rationale
Incident recording, investigation, and statutory reportability decisions rest with the Head of Health and Safety.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceApproach::OccupationalExposureBanding

### Membership Rationale
The banding framework and its assignments are owned by this domain with toxicology.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceApproach::LearningFromNearMisses

### Membership Rationale
Near miss collection, cross-site aggregation, and feedback are operated by the health and safety function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceRole::OccupationalHygienist

### Membership Rationale
The technical role through which exposure monitoring and containment assessment are delivered.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceMetric::ExposureMonitoringCoverage

### Membership Rationale
Monitoring coverage and upper-band trends are reported to the Head of Health and Safety and to site management.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceMetric::NearMissToIncidentRatio

### Membership Rationale
The reporting culture measure is reported by site and worker category to this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceMetric::HealthSurveillanceCompletion

### Membership Rationale
Surveillance completion and record retrievability are reported to this domain and to occupational health.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Membership Rationale
The substance register underpins assessment, monitoring, waste routing and emergency response, and is maintained by the health and safety function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::HazardousWasteConsignedAndTracked

### Membership Rationale
Duty of care over hazardous waste through to final disposal is owned by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::EmergencyResponseMatchesHazards

### Membership Rationale
Emergency arrangements derived from actual holdings are set and exercised by the health and safety function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceApproach::ChemicalInventoryManagement

### Membership Rationale
The single substance register and its differentiated registration rhythm are operated by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceMetric::SubstanceRegisterCompleteness

### Membership Rationale
Register completeness, data sheet currency and unregistered finds are reported to the Head of Health and Safety and to site management.

### Membership Status
VALIDATED

___

---

### 6.3 Root Collection Membership

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Membership Rationale
The Health and Safety folio is part of the Coco Pharmaceuticals governance folios collection, making the domain discoverable alongside the others.

### Membership Status
VALIDATED

___

---

## Part 7: Corporate Regulation Library

Occupational safety regulation belonged to none of the existing library folders. It is closest to Employment Regulations, but that folder holds regulation of the employment relationship itself, while the regulations here govern the physical conditions of work and apply to contractors and visitors who are in no employment relationship with the company at all. A separate folder is created for that reason.

---

### 7.1 Folder Definition

___

## Create Collection Folder

### Display Name
Health and Safety Regulations

### Qualified Name
CollectionFolder::Coco::Health and Safety Regulations

### Purpose
Groups the occupational health and safety regulations governing the physical conditions under which people work at Coco Pharmaceuticals sites.

### Description
This folder holds regulation whose subject is the protection of people from harm arising from the company's activities — hazardous substance control, occupational exposure, health surveillance, machinery and workplace safety, and the recording and reporting of incidents. Its scope is defined by presence rather than by contract: it protects employees, agency workers, contractors, and visitors alike, which distinguishes it from Employment Regulations, whose subject is the employment relationship. National requirements differ substantially across the US parent and the UK and EU subsidiaries, so the folder holds parallel instruments addressing the same subject, and the group works to the strictest applicable standard rather than to each local minimum.

### Category
Regulation Category

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 7.2 Library Registration

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Corporate Regulation Library

### Element Id
CollectionFolder::Coco::Health and Safety Regulations

### Membership Rationale
Occupational health and safety regulation is a category of corporate regulatory obligation in its own right, distinct from employment regulation, and belongs in the library so that the full set of regulations the company is subject to is discoverable from one place.

### Membership Status
VALIDATED

___

---

### 7.3 Folder Members

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Health and Safety Regulations

### Element Id
CocoPharma::Regulation::COSHH2002

### Membership Rationale
COSHH is the principal occupational health regulation at the UK sites, governing hazardous substance assessment, exposure control, health surveillance, and the forty-year retention of the resulting records.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Health and Safety Regulations

### Element Id
CocoPharma::Regulation::EUOSHFrameworkDirective

### Membership Rationale
Directive 89/391/EEC is the foundation of occupational safety law across the EU subsidiaries, establishing the general principles of prevention that the group's control hierarchy implements.

### Membership Status
VALIDATED

___

---

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `manufacturing-governance-program.md` | MANUFACTURING-domain program. Governs the same rooms and processes from the product-protection side; containment and validated-state changes must be reconciled between the two |
| `human-resource-management.md` | HR domain program. Supplies competency and employment records; fitness restrictions from surveillance feed its authorisation records without the clinical findings behind them |
| `privacy-governance-program.md` | PRIVACY-domain program. Assures the lawful basis for occupational health data and holds the retention schedule into which the forty-year requirement is written |
| `corporate-governance-program.md` | CORPORATE-domain program. Third-party approval covers the contractors who perform much of the highest-exposure ancillary work |
| `joint-governance-officer-definitions.md` | Foundation definitions and the governance roles and folios framework |
