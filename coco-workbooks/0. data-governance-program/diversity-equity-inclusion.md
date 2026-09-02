# Coco Pharmaceuticals — Diversity, Equity and Inclusion Governance

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-23  
> **Description:** Governance definitions for the Diversity, Equity and Inclusion domain at Coco Pharmaceuticals, domain identifier `Diversity, Equity and Inclusion`. The file registers the domain identifier as a valid metadata value before any definition claims it, then defines the drivers, policies, and controls for the domain. Load `joint-governance-officer-definitions.md` and `human-resource-management.md` first.

---

## Overview

Diversity, equity and inclusion is established here as a governance domain distinct from Human Resource Management, and the distinction is deliberate rather than organisational tidiness. HR owns the employment relationship: how decisions about individuals are made, recorded, and defended. This domain owns something broader and, for a pharmaceutical company, more consequential — whether the medicines the company develops actually work for the populations that will take them.

That is not a workforce question. A trial enrolling participants who differ systematically from the patients who will eventually be prescribed the product yields evidence that does not describe those patients, and the gap is discovered after approval, in practice, by people for whom the dose or the safety profile turns out to be different. The same failure recurs in a more modern form as the company builds models to guide personalised treatment: a model trained on the population that happened to be enrolled will perform worst for the groups that were least represented, and will do so silently.

The domain therefore spans three areas that share one logic — that unrepresentative data produces confident conclusions which are wrong for some people:

1. **Clinical evidence** — whether trial populations reflect disease epidemiology, and whether subgroup differences are looked for rather than assumed absent.
2. **Patient-affecting models and information** — whether analytical models perform equitably across groups, and whether patient information is usable by people with disabilities and lower health literacy.
3. **Organisational representation** — whether the company reflects the communities it serves, which is the area that overlaps with HR.

The boundary with Human Resource Management is drawn at the employment decision. HR owns hiring, pay, promotion, and the statutory pay gap reporting that follows from employment law; this domain owns the aggregate representation outcomes those decisions produce, and the equity analysis that spans employment, clinical, and product dimensions together. Where this file needs employment data it consumes HR's, and the equality monitoring processing purpose declared in `human-resource-management.md` is not duplicated here.

---

## Part 1: Domain Registration

___

## Setup Valid Metadata Value

### Metadata Property Name
domainIdentifier

### Preferred Value
23

### Metadata Display Name
Diversity, Equity and Inclusion

### Metadata Description
The governance domain for diversity, equity and inclusion encompasses the policies, practices and controls that ensure the organisation's work serves all the populations affected by it. In a pharmaceutical context this extends beyond workforce representation to the representativeness of clinical evidence, the equitable performance of models that influence patient care, and the accessibility of patient information. It exists to detect and correct the systematic disadvantage that arises when data, evidence or decisions reflect some groups better than others, and to ensure that inequity is identified through deliberate measurement rather than discovered through harm.

___

---

## Part 2: Governance Drivers — Diversity, Equity and Inclusion

The inconsistent employment decisions threat (`CocoPharma::Threat::InconsistentEmploymentDecisions`) and the UK Equality Act (`CocoPharma::Regulation::UKEqualityAct2010`) are defined in `human-resource-management.md` and are responded to here rather than restated.

---

### 2.1 Business Imperatives

___

## Create Business Imperative

### Display Name
Medicines Evidenced in the Populations That Will Use Them

### Qualified Name
CocoPharma::BusinessImperative::RepresentativeClinicalEvidence

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Coco Pharmaceuticals must generate clinical evidence in trial populations that reflect the patients who will be prescribed its products, so that efficacy and safety conclusions hold for those patients.

### Description
A clinical trial answers a question about the people who were in it. Where those people differ systematically from the eventual patient population — in ancestry, age, sex, comorbidity, or body composition — the answer may not transfer, and the difference is often material: drug metabolism varies with genetic variants distributed unevenly across ancestral populations, and dosing established in one group can be wrong for another. Historically the shortfall has been treated as a recruitment difficulty rather than an evidence defect, which is the error this imperative corrects. Enrolment that does not reflect epidemiology is a limitation on what the trial can support, and it should be visible as such when the results are read. The commercial case runs the same direction as the ethical one: regulators increasingly require enrolment plans with demographic targets, payers ask whether evidence covers their populations, and a post-approval finding of differential safety is far more expensive than enrolling representatively in the first place. For the personalised medicine programme the stakes rise further, since a therapy targeted on genomic characteristics cannot be developed on a population in which those characteristics are unevenly sampled.

### Implications
- Enrolment targets must be derived from disease epidemiology, not from recruitment convenience
- Site selection determines who can enrol, so it is an evidence decision rather than an operational one
- Shortfalls against targets must be reported as limitations on the evidence, not omitted
- Genomic and pharmacogenomic work requires representative sampling to be valid at all

### Outcomes
- Efficacy and safety conclusions transfer to the patients who receive the product
- Regulatory diversity requirements are met by design rather than explained afterwards
- Post-approval differential safety findings become rare

### Importance
Critical

### Category
Diversity, Equity and Inclusion

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Business Imperative

### Display Name
An Organisation That Reflects the Communities It Serves

### Qualified Name
CocoPharma::BusinessImperative::RepresentativeOrganisation

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Coco Pharmaceuticals must be able to measure representation across its workforce, its clinical investigators, and its suppliers, and to act on the disparities that measurement reveals.

### Description
Representation matters instrumentally as well as ethically, and the instrumental case is the one most often left unstated. Trial recruitment succeeds or fails substantially on whether investigators and site staff are trusted by the communities they recruit from, which is affected by who those investigators are. Product and information design reflects the assumptions of the people who design it, and assumptions that go unchallenged in a homogeneous group produce leaflets nobody in the intended population can follow. Decisions about which conditions to research reflect whose experience is represented in the room. This imperative requires representation to be measured across all three populations the company influences — its own workforce, the investigators it selects, and the suppliers it engages — rather than only the first, and requires the measurement to be actionable, which means broken down where decisions are made rather than reported as a single organisational figure. The employment half of this rests on HR's data and analysis; what this domain adds is the extension beyond the workforce and the connection to the evidence and product consequences.

### Implications
- Measurement must cover investigators and suppliers, not only employees
- Figures must be reported where decisions are made, not only at organisational level
- Employment representation data is consumed from HR rather than separately collected
- Disparities require an owner and a response, not only publication

### Outcomes
- Community trust in the company's research is built on visible representation
- Design assumptions are challenged before they reach patients
- The company can substantiate its representation claims with data

### Importance
High

### Category
Diversity, Equity and Inclusion

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
Unrepresentative Trial Evidence

### Qualified Name
CocoPharma::Threat::UnrepresentativeTrialEvidence

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Trial populations that differ systematically from the eventual patient population may produce efficacy and safety conclusions that do not hold for the groups least represented.

### Description
The threat materialises quietly and late. A trial completes, the analysis is sound, the product is approved, and the divergence only becomes apparent when patients outside the studied population are treated and respond differently — in efficacy, in adverse event rate, or in the dose required. By then the evidence base cannot be corrected without new studies, the label may need restricting, and the people harmed are those who were underrepresented in the first place. Several mechanisms drive it and none involves anyone deciding to exclude: sites are chosen for enrolment speed and prior performance, which favours centres serving populations already well represented in research; eligibility criteria exclude comorbidities and concomitant medications that are more prevalent in some groups; trial visit schedules assume flexible working hours and private transport; and consent materials are written at a reading level that filters participation. Each choice is defensible in isolation and the aggregate is a population that does not look like the patients. The threat is compounded when trial data is later reused to build models, because the sampling bias is inherited and amplified.

### Implications
- Site selection choices determine the achievable population and must be assessed as such
- Eligibility criteria must be reviewed for differential exclusion, not only for scientific necessity
- Practical trial burden filters participation by circumstance rather than by clinical suitability
- Sampling bias propagates into every downstream reuse of the trial data

### Importance
Critical

### Category
Diversity, Equity and Inclusion

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
Differential Model Performance Affecting Patient Care

### Qualified Name
CocoPharma::Threat::DifferentialModelPerformance

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Analytical models used to guide treatment selection, dosing, or eligibility may perform worse for groups underrepresented in their training data, producing systematically poorer decisions for those patients.

### Description
As the personalised medicine programme grows, models increasingly stand between patient data and clinical decisions — predicting response, stratifying risk, selecting candidates for a therapy. A model learns the population it was trained on, and where that population underrepresents a group its predictions for that group are less accurate while carrying exactly the same appearance of confidence. Aggregate performance metrics conceal this completely: a model that is highly accurate overall can be little better than chance for a subgroup forming a small fraction of the training data, and nothing in the headline figure reveals it. The mechanism is worse than simple noise, because models also learn proxies — a postcode, a referral pattern, a prior treatment history that reflects historical access rather than clinical need — and reproduce the inequity encoded in those proxies as though it were a clinical finding. Because the output is a number rather than a judgement, it tends to be trusted more than the human decision it replaced, and challenged less.

### Implications
- Aggregate accuracy conceals subgroup failure and cannot be relied on alone
- Training data representativeness must be assessed before a model is deployed, not after
- Models learn proxies for group membership even when the characteristic is excluded
- Model outputs attract more trust than the judgements they replace, so errors propagate further

### Importance
High

### Category
Diversity, Equity and Inclusion

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
FDA Clinical Trial Diversity Action Plan Requirements

### Qualified Name
CocoPharma::Regulation::FDADiversityActionPlan

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
US requirements obliging sponsors of pivotal clinical trials to submit a Diversity Action Plan setting enrolment goals by demographic subgroup, with rationale and the measures that will achieve them.

### Description
The Food and Drug Omnibus Reform Act of 2022 introduced a statutory requirement for sponsors of certain pivotal studies to submit a Diversity Action Plan to the FDA, converting what had been guidance and encouragement into a filed commitment. The plan must state enrolment goals disaggregated by race, ethnicity, sex, and age group; explain the rationale for those goals by reference to the epidemiology of the condition; and describe the concrete measures — site selection, community engagement, reduction of participation burden, trial design choices — by which the sponsor intends to meet them. The governance significance is that the goals become a commitment against which actual enrolment is measured and must be explained. A sponsor that files a plan and misses its goals without having taken the measures it described is in a materially worse position than one that never filed, which makes the accuracy of the demographic data collected during the trial, and the ability to monitor enrolment against target while the trial is running, a compliance matter rather than an analytical convenience.

### Regulation Source
Food and Drug Omnibus Reform Act of 2022, section 3602, with FDA guidance on Diversity Action Plans

### Regulators
- Food and Drug Administration (FDA) — United States

### Implications
- Enrolment goals must be derived from and justified by disease epidemiology
- The measures described in the plan must actually be implemented and evidenced
- Enrolment against goals must be monitored during the trial, not assessed at its end
- Demographic data collection must be accurate and consistently categorised across sites

### Importance
Critical

### Category
Diversity, Equity and Inclusion

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
European Accessibility Act (EU) 2019/882

### Qualified Name
CocoPharma::Regulation::EuropeanAccessibilityAct

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
EU directive requiring specified products and services, including e-commerce and digital services, to meet accessibility requirements so that people with disabilities can use them on an equal basis.

### Description
The Accessibility Act sets functional accessibility requirements for products and services placed on the EU market, and reaches Coco Pharmaceuticals principally through its digital patient-facing services — patient support portals, digital companion applications for personalised therapies, and the e-commerce channels through which products and services are offered. Its requirements are expressed functionally rather than as a technical checklist: information must be available through more than one sensory channel, presented in ways users can perceive and understand, and made compatible with assistive technologies. For a pharmaceutical company the important consequence is that accessibility of patient information is not confined to the regulated package leaflet, which has its own readability requirements under medicines law, but extends to every digital surface through which a patient interacts with the company. Because personalised therapies increasingly depend on patients using an application to report symptoms or schedule collection, an inaccessible application does not merely inconvenience the patient — it excludes them from the treatment pathway.

### Regulation Source
Directive (EU) 2019/882 on the accessibility requirements for products and services

### Regulators
- National market surveillance authorities in EU member states
- European Commission

### Implications
- Digital patient-facing services must meet functional accessibility requirements
- Accessibility must be designed in, as retrofitting a service is substantially harder
- Where treatment depends on a digital tool, inaccessibility excludes patients from therapy
- Requirements apply alongside, not instead of, medicines law readability obligations

### Importance
High

### Category
Diversity, Equity and Inclusion

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Policies — Diversity, Equity and Inclusion

---

### 3.1 Governance Principles

___

## Create Governance Principle

### Display Name
Evidence Is Generated in Populations That Reflect Intended Use

### Qualified Name
CocoPharma::GovernancePrinciple::RepresentativeEvidenceRequired

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Trial populations are planned against the epidemiology of the condition, and any divergence between the enrolled population and the intended patient population is stated as a limitation on the evidence.

### Description
The principle establishes representativeness as a property of the evidence rather than a target for the recruitment function. It requires the intended patient population to be characterised at protocol design — from disease epidemiology in the markets where the product will be used, not from the populations of previous trials, which would perpetuate the existing distribution — and enrolment planned against that characterisation. Where the achieved population diverges, the divergence is reported alongside the results and its implications for generalisability stated, rather than being noted in a recruitment report nobody reads with the efficacy data. This is deliberately a disclosure obligation as well as a planning one, because the discipline that changes behaviour is knowing that the shortfall will appear next to the conclusions. The principle does not require every trial to be perfectly representative, which is often not achievable within a feasible timeline; it requires the company to know what it has, to say what it has, and not to claim more than the population supports.

### Implications
- Intended population is characterised from epidemiology, not from prior trial populations
- Divergence between planned and achieved enrolment is reported with the results
- Generalisability limits must be stated rather than left to the reader to infer
- Achieving representativeness may extend timelines, and that trade-off is made explicitly

### Outcomes
- Conclusions are qualified by the population that actually supports them
- Recruitment shortfalls become visible to the people interpreting the evidence
- Claims made for a product match the evidence base behind them

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
Demographic Data Detects Inequity and Never Determines Access

### Qualified Name
CocoPharma::GovernancePrinciple::DemographicDataForEquityNotAccess

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Demographic and protected characteristic data is collected to measure whether outcomes differ between groups, and is structurally prevented from influencing any decision about an individual's treatment, enrolment, or employment.

### Description
Measuring inequity requires collecting exactly the characteristics that must not drive decisions, and the resolution is not to avoid collection — which makes inequity invisible rather than absent — but to separate measurement from decision by design. Demographic data is held so that it is available for aggregate analysis and unavailable at the point of individual decision: not shown on the screens where enrolment eligibility is assessed, not present in the records used for employment decisions, and not supplied as a feature to models that influence patient care. The last case needs the most care, since a model deprived of the characteristic will often reconstruct it from correlated variables, which is why the principle requires models to be tested for differential performance rather than merely be denied the field. Where a characteristic is genuinely clinically relevant — as ancestry can be for pharmacogenomic variants — it is used as the specific clinical variable it stands for rather than as the social category, and the distinction is recorded so that clinical use cannot expand quietly into demographic use.

### Implications
- Demographic data is separated from the systems and screens used for individual decisions
- Excluding the characteristic from a model is insufficient; differential testing is required
- Clinically relevant use must be expressed as the specific variable, not the social category
- Aggregate outputs require minimum group sizes to avoid identifying individuals

### Outcomes
- Inequity can be measured without creating a route to discriminate
- Clinical use of ancestry is precise rather than a proxy
- Individuals can supply demographic data without risk to how they are treated

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
Patient Information Must Be Usable by the Patients Who Need It

### Qualified Name
CocoPharma::GovernancePrinciple::PatientInformationAccessible

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Information a patient needs in order to use a product safely must be accessible in perceivability, comprehension, and language, and tested with the people who will rely on it.

### Description
Information that is technically complete but practically unusable does not discharge the obligation to inform, and in a treatment context the consequence is a patient taking a medicine incorrectly. The principle covers three dimensions that are commonly confused. Perceivability is the accessibility question the Accessibility Act addresses — whether a person using a screen reader or with limited vision can obtain the information at all. Comprehension is the health literacy question — whether a person of average reading ability can follow it, which for medicines information is frequently not the case despite readability testing being a regulatory requirement. Language is the question of which populations are served at all, and it interacts directly with trial representativeness, since materials available only in the majority language of a market restrict who can meaningfully consent. The principle requires testing with representative users rather than assessment against a formula, because reading-level scores measure sentence length rather than whether anyone understood the instruction.

### Implications
- Perceivability, comprehension, and language must each be addressed, not conflated
- Testing must involve representative users, not only formulaic readability scoring
- Digital tools required for a therapy must meet accessibility requirements before launch
- Language coverage decisions determine who can meaningfully consent and are recorded as such

### Outcomes
- Patients can act correctly on the information they are given
- Digital treatment pathways do not exclude patients with disabilities
- Consent is meaningful across the populations a trial intends to enrol

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
Trial Enrolment Targets Must Be Set Against Epidemiology and Monitored During Recruitment

### Qualified Name
CocoPharma::GovernanceObligation::TrialEnrolmentTargetsAgainstEpidemiology

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Every pivotal trial must set demographic enrolment targets derived from disease epidemiology, monitor actual enrolment against them while recruitment is open, and act on divergence rather than reporting it afterwards.

### Description
Targets are only useful while something can still be done about them. This obligation requires targets to be established at protocol design from epidemiology in the intended markets, and enrolment to be monitored against them continuously so that divergence triggers intervention during recruitment — opening additional sites, revisiting eligibility criteria, adjusting visit burden — rather than appearing as a limitation in the clinical study report. Monitoring requires demographic data to be captured consistently across sites, which is less straightforward than it appears: categories differ between jurisdictions, self-identification and observer assignment give different answers, and a site recording ethnicity in local categories cannot be aggregated without a mapping that is agreed in advance. The obligation therefore includes the categorisation standard as part of what must be defined at protocol design. Where a target will not be met, the obligation requires the decision to proceed to be taken explicitly and recorded with its rationale, since accepting an unrepresentative population is a decision about the evidence and belongs with the people accountable for it.

### Implications
- Targets derive from epidemiology in the intended markets and are set at protocol design
- Demographic categorisation must be standardised across sites and agreed in advance
- Monitoring runs during recruitment, with divergence triggering intervention
- A decision to proceed despite unmet targets is recorded with its rationale

### Outcomes
- Recruitment shortfalls are corrected while correction is still possible
- Demographic data can be aggregated across sites and jurisdictions
- Accepting an unrepresentative population becomes a visible, accountable decision

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
Subgroup Analyses Must Be Pre-specified and Reported Whatever They Show

### Qualified Name
CocoPharma::GovernanceObligation::SubgroupAnalysesPrespecified

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Analyses of efficacy and safety by demographic subgroup must be pre-specified in the statistical analysis plan and reported in full, including where the subgroup was too small to support a conclusion.

### Description
Pre-specification protects subgroup analysis from the two failure modes that otherwise destroy its value. Analyses chosen after seeing the data can be selected to support a preferred conclusion, and analyses not planned at all are usually not conducted, so a differential effect goes unlooked-for rather than unfound. The obligation requires the subgroups, the analytical method, and the interpretive approach to multiplicity to be set out before unblinding. Reporting is required regardless of outcome, and this includes the uncomfortable case where a subgroup was enrolled in numbers too small to support any conclusion — which must be stated as an absence of evidence rather than allowed to read as evidence of absence. That distinction is the one most often lost in practice: a safety profile described as consistent across subgroups, when one subgroup contained eleven participants, misleads without containing a false statement. The obligation therefore requires subgroup sizes and the resulting precision to be reported alongside the estimates.

### Implications
- Subgroups, methods, and multiplicity approach are fixed before unblinding
- Results are reported whatever they show, including inconclusive subgroups
- Subgroup sizes and precision must be reported alongside estimates
- Absence of evidence must not be characterised as evidence of consistency

### Outcomes
- Differential effects are looked for rather than discovered post-approval
- Readers can distinguish a subgroup that was studied from one that was not
- Subgroup claims are constrained by the data actually supporting them

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
Patient-Affecting Models Must Be Tested for Differential Performance Before Deployment

### Qualified Name
CocoPharma::GovernanceObligation::ModelsTestedForDifferentialPerformance

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Any model whose output influences patient treatment, eligibility, or prioritisation must have its performance measured separately for each relevant subgroup before deployment and monitored after it.

### Description
The obligation makes subgroup performance a release criterion rather than an evaluation topic. Before deployment, the model's performance is measured within each subgroup of clinical relevance, the training data composition is documented, and subgroups too sparsely represented for performance to be estimated are identified as limitations on the scope of use — a model that cannot be shown to work for a group should not be applied to that group silently. Testing must extend to proxy effects, examining whether excluded characteristics are being reconstructed from correlated variables, since a model formally blind to ancestry may reproduce ancestral differences through variables that track it. Monitoring continues after deployment because populations shift and performance degrades unevenly. The obligation also requires the intended scope of use to be recorded and enforced, as the most common route to harm is a model validated for one population being applied to another on the assumption that a good model is good everywhere.

### Implications
- Subgroup performance is a release criterion, not a post-deployment evaluation
- Training data composition must be documented and its gaps declared as scope limits
- Proxy reconstruction of excluded characteristics must be tested for explicitly
- Intended scope of use must be recorded and enforced, not left to the deploying team
- Performance monitoring continues after deployment, disaggregated by subgroup

### Outcomes
- Models are not deployed for populations they cannot be shown to serve
- Proxy discrimination is detected rather than assumed absent
- Degradation affecting one group is visible before it accumulates harm

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
Inclusive Trial Design and Site Selection

### Qualified Name
CocoPharma::GovernanceApproach::InclusiveTrialDesign

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Trial design decisions are assessed for their effect on who can participate, with site selection, eligibility criteria, and participation burden treated as determinants of the achievable population.

### Description
The approach intervenes at the point where representativeness is actually decided, which is design rather than recruitment. Three sets of decisions are examined. Site selection determines the catchment population, so sites are chosen partly for the communities they serve rather than solely for enrolment speed and prior performance — which requires accepting that a site new to research needs more support and may enrol more slowly. Eligibility criteria are reviewed for differential exclusion: an upper limit on body mass index, an exclusion for controlled hypertension, or a requirement for a particular baseline organ function each remove a larger fraction of some populations than others, and each must be justified by trial-specific scientific necessity rather than by inherited convention. Participation burden is examined for what it filters — visit frequency and timing, travel requirements, whether time off work is needed, whether materials exist in the languages the catchment speaks — with decentralised and hybrid elements considered as a means of widening participation rather than only of accelerating it. Decisions are recorded with their expected effect on the achievable population, so that the eventual enrolment can be assessed against the design that produced it.

### Implications
- Sites are selected partly for the communities they serve, accepting slower start-up
- Every eligibility criterion requires trial-specific justification, not inherited convention
- Participation burden is assessed for what it filters, not only for feasibility
- Design decisions are recorded with their expected effect on the achievable population

### Outcomes
- The achievable population is widened at the point where it is determined
- Enrolment shortfalls can be traced to the design decisions that caused them
- Decentralised elements are used to widen access rather than only to speed recruitment

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
Equity Impact Assessment

### Qualified Name
CocoPharma::GovernanceApproach::EquityImpactAssessment

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Decisions with foreseeable differential effects on groups — trial designs, model deployments, patient-facing digital services, and access programmes — are assessed for those effects before commitment, on a proportionate basis.

### Description
The approach applies a consistent method across decisions that would otherwise be examined in unconnected ways, and it deliberately mirrors the privacy impact assessment process so that the two can run together where a decision engages both. An assessment identifies who is affected, which groups may be affected differently and why, what data exists to test that expectation, what would be done if the differential effect proved real, and what will be monitored after the decision. It is proportionate: a change to a patient portal's language coverage does not warrant the depth applied to deploying a model that selects patients for a therapy. Assessments are conducted before commitment, since their purpose is to change the decision rather than to document it, and they are revisited when the thing assessed changes materially. Where an assessment identifies a differential effect the organisation decides to accept, the acceptance is recorded with its reasoning and owner — the approach exists to make such trade-offs explicit and attributable, not to prohibit them.

### Implications
- Assessment precedes commitment, or it documents rather than informs
- Depth is proportionate to the foreseeable effect, not uniform across decisions
- Assessments run jointly with privacy impact assessments where both are engaged
- Accepted differential effects are recorded with reasoning and a named owner
- Monitoring commitments made in the assessment are tracked after the decision

### Outcomes
- Differential effects are identified while the decision can still change
- Trade-offs are made by identifiable people rather than emerging from process
- The organisation has a consistent method across clinical, digital, and access decisions

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 4: Governance Controls — Diversity, Equity and Inclusion

---

### 4.1 Governance Roles

___

## Create Governance Role

### Display Name
Head of Diversity, Equity and Inclusion (Governance Domain Lead)

### Qualified Name
CocoPharma::GovernanceRole::HeadOfDiversityEquityInclusion

### Description
The Head of Diversity, Equity and Inclusion holds the domain lead role for identifier 23, accountable for the representativeness of clinical evidence, the equitable performance of patient-affecting models, the accessibility of patient information, and organisational representation across workforce, investigators, and suppliers. The role owns the equity impact assessment process, approves Diversity Action Plans before filing, and reports representation and representativeness measures to the governance leadership. It draws on employment representation data owned by the Head of Human Resources rather than collecting it separately, and works with the Drug Development Lead on enrolment targets and with the Chief Data Officer on model governance. The appointment is not yet made; pending appointment the role is discharged by the Head of Human Resources, and that interim arrangement is recorded rather than left implicit because it places two domains with a deliberate boundary in one pair of hands.

### Scope
Diversity, equity and inclusion governance domain — clinical evidence representativeness, model equity, patient information accessibility, and representation across workforce, investigators, and suppliers.

### Headcount
1

### Category
Governance Role

### Search Keywords
- diversity equity inclusion
- clinical trial diversity
- model equity
- accessibility

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Role

### Display Name
Clinical Trial Diversity Lead

### Qualified Name
CocoPharma::GovernanceRole::ClinicalTrialDiversityLead

### Description
The Clinical Trial Diversity Lead is responsible for the representativeness of enrolment across the trial portfolio. The role derives enrolment targets from disease epidemiology, drafts the Diversity Action Plans filed with the FDA, maintains the demographic categorisation standard used across sites and jurisdictions, monitors enrolment against target during recruitment, and escalates divergence to the study team and the Drug Development Lead while intervention is still possible. It advises on site selection and on eligibility criteria review, and maintains the community engagement relationships that make recruitment from underrepresented populations feasible. It reports to the Head of Diversity, Equity and Inclusion and works day to day with the clinical operations and biostatistics functions.

### Scope
Trial enrolment representativeness across the portfolio — epidemiological target setting, Diversity Action Plans, demographic categorisation standards, enrolment monitoring, and site and criteria advice.

### Headcount
2

### Category
Governance Role

### Search Keywords
- trial diversity
- enrolment targets
- diversity action plan
- community engagement

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
Trial Enrolment Representativeness Against Epidemiology

### Qualified Name
CocoPharma::GovernanceMetric::TrialEnrolmentRepresentativeness

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Measures, per trial and per demographic subgroup, enrolment as a proportion of the epidemiologically derived target, reported during recruitment rather than at its close.

### Description
The comparison is against the epidemiological target rather than against a population average, because the relevant question is whether the trial reflects who has the condition and not who lives in the country. Reporting is per subgroup and never aggregated into a single index: a composite score can look adequate while one group is absent entirely, and the absent group is the finding. Reporting cadence is deliberately during recruitment, since a measure produced at database lock informs nothing that can still be changed, and the metric therefore carries a projection — enrolment at the current rate against the target — as its most actionable element. Trials filing a Diversity Action Plan are reported separately, because for those the target is a commitment made to a regulator rather than an internal goal, and divergence carries a different consequence. Subgroups where the achieved number is too small to support subgroup analysis are flagged distinctly from those merely below target, since that threshold is what determines whether the trial can say anything about the group at all.

### Implications
- Comparison is against epidemiological target, not general population distribution
- Reported per subgroup, never composited into a single representativeness score
- A projection against current enrolment rate is required for the metric to drive action
- Trials with filed Diversity Action Plans are reported separately
- Subgroups below the threshold for meaningful analysis are flagged distinctly

### Outcomes
- Enrolment gaps prompt intervention during recruitment
- Regulatory enrolment commitments are tracked against actual performance
- Trials that will be unable to support subgroup conclusions are identified early

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
Model Subgroup Performance Disparity

### Qualified Name
CocoPharma::GovernanceMetric::ModelSubgroupPerformanceDisparity

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Measures, for each deployed patient-affecting model, the gap between best and worst performing subgroup on the model's primary performance measure, reported alongside training data composition.

### Description
The metric reports the disparity rather than the aggregate, because the aggregate is precisely what conceals the problem. It is computed on whatever measure is primary for the model's purpose — sensitivity where the cost of a missed case dominates, calibration where the output is used as a probability — since a disparity in one can coexist with parity in another and reporting the wrong one gives false assurance. Training data composition is reported alongside, as the usual explanation for a disparity is representation in training, and pairing the two makes the remedy visible rather than leaving the disparity as an unexplained property of the model. Subgroups too small to estimate performance for are reported as unestimable rather than omitted, since omission reads as parity. Trend over time is tracked, because the more common failure after deployment is not a model that was always unequal but one that degrades faster for a group as the population shifts. Models exceeding a defined disparity threshold are escalated to the Head of Diversity, Equity and Inclusion and the model owner for a scope-of-use decision.

### Implications
- The primary measure must be chosen for the model's purpose, not for convenience
- Training data composition is reported with the disparity to make the remedy visible
- Unestimable subgroups are reported as such, never omitted
- Trend tracking is required, since post-deployment degradation is uneven
- Threshold breaches trigger a scope-of-use decision, not only a note

### Outcomes
- Subgroup failure is visible where aggregate accuracy would hide it
- Disparities are connected to their most likely cause at the point of reporting
- Models degrading for a particular group are caught before harm accumulates

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

### 5.1 Governance Responses — Drivers linked to DEI Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDADiversityActionPlan

### Policy
CocoPharma::GovernanceObligation::TrialEnrolmentTargetsAgainstEpidemiology

### Rationale
The Act requires enrolment goals justified by epidemiology and the measures to achieve them. The obligation makes those goals monitorable during recruitment rather than assessable only afterwards.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDADiversityActionPlan

### Policy
CocoPharma::GovernanceApproach::InclusiveTrialDesign

### Rationale
A Diversity Action Plan must describe concrete measures. Site selection, eligibility review, and burden reduction are those measures, and the approach is where they are decided.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDADiversityActionPlan

### Policy
CocoPharma::GovernancePrinciple::RepresentativeEvidenceRequired

### Rationale
Filing enrolment goals converts representativeness from an aspiration into a commitment against which the company will be measured, which is what the principle states internally.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EuropeanAccessibilityAct

### Policy
CocoPharma::GovernancePrinciple::PatientInformationAccessible

### Rationale
The Act sets functional accessibility requirements for digital services. The principle extends the same standard across all patient information, including where medicines law rather than the Act applies.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKEqualityAct2010

### Policy
CocoPharma::GovernanceApproach::EquityImpactAssessment

### Rationale
Indirect discrimination requires objective justification of a criterion that disadvantages a group. Assessing differential effect before commitment is how that justification is established rather than reconstructed.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnrepresentativeTrialEvidence

### Policy
CocoPharma::GovernancePrinciple::RepresentativeEvidenceRequired

### Rationale
The threat is unrepresentative evidence read as though it generalised. Requiring divergence to be stated with the results prevents the conclusion travelling further than the population supports it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnrepresentativeTrialEvidence

### Policy
CocoPharma::GovernanceApproach::InclusiveTrialDesign

### Rationale
Representativeness is determined by design decisions about sites, criteria, and burden. Intervening there addresses the cause rather than the symptom.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnrepresentativeTrialEvidence

### Policy
CocoPharma::GovernanceObligation::SubgroupAnalysesPrespecified

### Rationale
Where a trial does enrol a subgroup, pre-specified analysis is what ensures a differential effect is looked for rather than left undiscovered until post-approval use.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::DifferentialModelPerformance

### Policy
CocoPharma::GovernanceObligation::ModelsTestedForDifferentialPerformance

### Rationale
Subgroup testing before deployment is the only point at which differential performance can be found before it affects patients, since aggregate metrics will not reveal it afterwards.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::DifferentialModelPerformance

### Policy
CocoPharma::GovernancePrinciple::DemographicDataForEquityNotAccess

### Rationale
The principle permits the demographic data needed to test a model while structurally preventing it becoming an input, which is the arrangement the threat requires.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::RepresentativeClinicalEvidence

### Policy
CocoPharma::GovernanceObligation::TrialEnrolmentTargetsAgainstEpidemiology

### Rationale
Targets derived from epidemiology and monitored during recruitment are how the imperative is made operational rather than aspirational.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::RepresentativeOrganisation

### Policy
CocoPharma::GovernanceApproach::EquityImpactAssessment

### Rationale
Representation across workforce, investigators, and suppliers is affected by decisions taken in each area; the assessment is the common method applied across them.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernanceObligation::ModelsTestedForDifferentialPerformance

### Rationale
Personalised medicine places models between patient data and treatment decisions, which makes their equitable performance a precondition of the transition rather than a refinement of it.

___

---

### 5.2 Governance Mechanisms — DEI Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::TrialEnrolmentTargetsAgainstEpidemiology

### Mechanism
CocoPharma::GovernanceMetric::TrialEnrolmentRepresentativeness

### Rationale
Per-subgroup enrolment against epidemiological target, with a projection, measures the obligation at the point action is still possible.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::RepresentativeEvidenceRequired

### Mechanism
CocoPharma::GovernanceMetric::TrialEnrolmentRepresentativeness

### Rationale
Flagging subgroups below the threshold for meaningful analysis shows where the evidence will not support conclusions, which is the limitation the principle requires to be stated.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ModelsTestedForDifferentialPerformance

### Mechanism
CocoPharma::GovernanceMetric::ModelSubgroupPerformanceDisparity

### Rationale
Best-to-worst subgroup disparity reported with training data composition measures the obligation and points at its usual cause in the same view.

___

---

### 5.3 Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::UnrepresentativeTrialEvidence

### Governance Driver 2
CocoPharma::Threat::DifferentialModelPerformance

### Description
The second inherits from the first. A model trained on trial data carries that data's sampling bias forward and amplifies it, so unrepresentative enrolment years ago produces inequitable predictions today — which is why the two must be governed as one chain rather than as separate concerns.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::RepresentativeClinicalEvidence

### Governance Driver 2
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Description
The FDA regulations govern how trial data must be captured and evidenced; the imperative governs whose data it is. Both bear on whether a submission supports the conclusions drawn from it, from different directions.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::RepresentativeOrganisation

### Governance Driver 2
CocoPharma::Threat::InconsistentEmploymentDecisions

### Description
Organisational representation is the aggregate outcome of the employment decisions the HR threat concerns. The threat describes the mechanism; the imperative describes the result and extends it beyond employees to investigators and suppliers.

___

---

### 5.4 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::TrialEnrolmentTargetsAgainstEpidemiology

### Governance Policy 2
CocoPharma::GovernanceApproach::RiskBasedClinicalQualityManagement

### Description
Enrolment representativeness is a quality attribute of the trial in the sense E6(R3) uses: it affects the reliability of results, and it belongs among the critical factors identified at design rather than being managed separately from trial quality.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::EquityImpactAssessment

### Governance Policy 2
CocoPharma::GovernanceApproach::PrivacyImpactAssessmentProcess

### Description
The two assessments examine the same decisions from adjacent angles and are designed to run together: privacy asks whether the processing is lawful and proportionate, equity asks whether its effects fall evenly. A decision engaging both should be assessed once.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::PatientInformationAccessible

### Governance Policy 2
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Description
Consent that a participant cannot read is not informed consent. Accessibility of trial materials is therefore a condition of the protection the drug development principle promises, not a separate courtesy.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::SubgroupAnalysesPrespecified

### Governance Policy 2
CocoPharma::GovernancePrinciple::ResearchDataReproducibility

### Description
Pre-specification and reproducibility defend against the same failure from opposite ends: analyses chosen after seeing data, and analyses that cannot be rerun to check what was chosen.

___

---


## Part 6: Diversity, Equity and Inclusion Governance Folio

---

### 6.1 Folio Definition

___

## Create Folio

### Display Name
Head of Diversity, Equity and Inclusion — Governance Folio

### Qualified Name
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Description
The governance definitions owned by the Head of Diversity, Equity and Inclusion in domain 23. The folio covers the representative evidence and representative organisation imperatives, the unrepresentative trial evidence and differential model performance threats, the FDA Diversity Action Plan requirements and the European Accessibility Act, the evidence, demographic data and accessibility principles, the enrolment, subgroup analysis and model testing obligations, and the controls that measure them.

### Purpose
Provides a single view of the definitions governing whether the company's evidence, models, and information serve all the populations they affect. The folio is kept separate from the Head of Human Resources folio even while one person discharges both roles, so that the boundary between employment governance and equity of evidence remains visible.

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
CocoPharma::GovernanceRole::HeadOfDiversityEquityInclusion

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Description
Assigns the Head of Diversity, Equity and Inclusion role responsibility for the governance definitions collected in this folio.

___

---

### 6.2 Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::BusinessImperative::RepresentativeClinicalEvidence

### Membership Rationale
Whether evidence transfers to the patients who will receive the product is the central concern of this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::BusinessImperative::RepresentativeOrganisation

### Membership Rationale
Representation across workforce, investigators, and suppliers is measured and acted on from this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::Threat::UnrepresentativeTrialEvidence

### Membership Rationale
The evidence defect arising from unrepresentative enrolment is owned here, jointly managed with the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::Threat::DifferentialModelPerformance

### Membership Rationale
Inequitable model performance affecting patient care is owned here with the Chief Data Officer on model governance.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::Regulation::FDADiversityActionPlan

### Membership Rationale
Diversity Action Plans are drafted and approved within this domain before filing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::Regulation::EuropeanAccessibilityAct

### Membership Rationale
Accessibility of patient-facing digital services is owned by this domain with the Senior Software Manager.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernancePrinciple::RepresentativeEvidenceRequired

### Membership Rationale
The standard applied to evidence generation and its disclosure is set here.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernancePrinciple::DemographicDataForEquityNotAccess

### Membership Rationale
The separation between measuring inequity and deciding on individuals is defined and enforced from this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernancePrinciple::PatientInformationAccessible

### Membership Rationale
Accessibility across perceivability, comprehension, and language is owned here.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceObligation::TrialEnrolmentTargetsAgainstEpidemiology

### Membership Rationale
Enrolment targets and their monitoring are set by the Clinical Trial Diversity Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceObligation::SubgroupAnalysesPrespecified

### Membership Rationale
Pre-specification and full reporting of subgroup analyses is required by this domain and delivered with biostatistics.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceObligation::ModelsTestedForDifferentialPerformance

### Membership Rationale
Subgroup testing as a model release criterion is required by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceApproach::InclusiveTrialDesign

### Membership Rationale
Design and site selection advice is provided by the Clinical Trial Diversity Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceApproach::EquityImpactAssessment

### Membership Rationale
The assessment method is owned here and applied across clinical, digital, and access decisions.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceRole::ClinicalTrialDiversityLead

### Membership Rationale
The delegated role through which trial representativeness is managed.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceMetric::TrialEnrolmentRepresentativeness

### Membership Rationale
Per-subgroup enrolment against epidemiological target is reported from this domain to study teams.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::GovernanceMetric::ModelSubgroupPerformanceDisparity

### Membership Rationale
Model disparity is reported to this domain and to model owners for scope-of-use decisions.

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
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Membership Rationale
The Diversity, Equity and Inclusion folio is part of the Coco Pharmaceuticals governance folios collection, making the domain discoverable alongside the others.

### Membership Status
VALIDATED

___

---

## Part 7: Corporate Regulation Library

---

### 7.1 Clinical Trial Regulations Membership

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Clinical Trial Regulations

### Element Id
CocoPharma::Regulation::FDADiversityActionPlan

### Membership Rationale
The Diversity Action Plan requirement governs the conduct of pivotal clinical trials and belongs with the other clinical trial regulations, which are themselves reachable from the pharmaceutical industry folder.

### Membership Status
VALIDATED

___

---

### 7.2 Product and Service Regulations Folder

The European Accessibility Act governs products and services rather than employment, finance, clinical trials, medicines, privacy, or security, and no existing library folder covered that category. The folder created here is deliberately broader than this domain: it is intended to hold consumer-facing, digital service, and medical device regulation as those arise, whichever domain owns them.

___

## Create Collection Folder

### Display Name
Product and Service Regulations

### Qualified Name
CollectionFolder::Coco::Product and Service Regulations

### Purpose
Groups the regulations governing the products and services Coco Pharmaceuticals places on the market, as distinct from the regulations governing how they are manufactured, tested, or sold.

### Description
This folder holds regulation whose subject is the product or service as the user encounters it — its accessibility, its safety in use, its digital characteristics, and the information supplied with it. It is distinct from the Pharmaceutical Industry Regulations folder, which governs how medicinal products are developed and manufactured, and from Financial Regulations, which governs how they are sold and accounted for. The distinction matters because product and service regulation frequently applies horizontally across sectors rather than to pharmaceuticals specifically, and is enforced by market surveillance authorities rather than by medicines regulators. As Coco Pharmaceuticals extends into digital companion applications and connected devices supporting personalised therapies, this category is expected to grow.

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

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Corporate Regulation Library

### Element Id
CollectionFolder::Coco::Product and Service Regulations

### Membership Rationale
Product and service regulation is a category of corporate regulatory obligation distinct from the manufacturing, financial, and clinical categories already in the library, and belongs alongside them so that the full set of regulations the company is subject to is discoverable from one place.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Product and Service Regulations

### Element Id
CocoPharma::Regulation::EuropeanAccessibilityAct

### Membership Rationale
The Accessibility Act sets functional requirements for the digital services through which patients interact with the company, making it a regulation of the service as the user encounters it.

### Membership Status
VALIDATED

___

---


## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `human-resource-management.md` | HR domain program. Owns employment decisions, pay equity, and workforce equality monitoring; this domain consumes its representation data rather than re-collecting it |
| `drug-development-governance.md` | Drug Development domain program. Enrolment targets and subgroup analyses are delivered through its trial processes |
| `privacy-governance-program.md` | PRIVACY-domain program. Assures the lawful basis for demographic data processing and owns the privacy impact assessment this domain's equity assessment runs alongside |
| `data-governance-program.md` | DATA-domain program. Lineage for critical data elements is what makes model training data composition verifiable |
| `joint-governance-officer-definitions.md` | Foundation definitions and the governance roles and folios framework |
