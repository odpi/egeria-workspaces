# Keeping Safe

The scenarios in this directory focus on security and the IT infrastructure that underpins it.  They rest on the systems inventory that [Gary Geeke](https://egeria-project.org/practices/coco-pharmaceuticals/personas/gary-geeke/) built in [1. coco-data-hub](../1.%20coco-data-hub/README.md) — first from his own spreadsheet, to support the mapping of the strategic information supply chains to real systems, and then extended with the systems of the Austin and Bucharest acquisitions.  The security team took that inventory up to scope the ISMS.

- [it-governance-program.md](it-governance-program.md) is Gary's governance program for the `IT Infrastructure` domain, built on that inventory and structured around the ITIL practices his team already works to.  IT infrastructure is a *serving* domain: it owns no regulatory obligation of its own, and almost all of its governance is expressed as commitments to obligations belonging to security, manufacturing, privacy, drug development and corporate governance.
- [Understanding Martyn's Law](martyns-law/README.md) looks at managing a physical security situation.
- [onboarding-simon-burr.md](onboarding-simon-burr.md) records the arrival of Simon Burr as Coco Pharmaceuticals' first Chief Information Security Officer, reporting to Ivor Padlock as Chief Security Officer: his profile, the CISO role and his appointment, his governance folio, and his plan for his first ninety days - including setting up continuous penetration testing across the company.
- [security-glossary.md](security-glossary.md) is the vocabulary that security people use - the goals and principles of security, the language of the ISMS, identity and access, kinds of attack, security testing and monitoring, and incident response.  Simon Burr wrote it with Ivor Padlock and Sidney Seeker when he found that words such as *threat*, *risk* and *vulnerability* meant different things to different people.  It underpins the security awareness training.
- [risk-scopes.md](risk-scopes.md) is the security team's threat modelling output: it links the risks in the [risk register](../0.%20data-governance-program/risk-register.md) to the solution components of the strategic information supply chains that they threaten, using the `ScopedBy` relationship.  Since the components are linked to the systems that implement them in all three estates, scoping a risk to a component scopes it to every system that implements it.  It also lists the risks that have nothing to be scoped to yet.

## Loading the IT governance program

The definitions carry Domain Identifier `IT Infrastructure` and link to definitions across the domain programs, so load the whole of `0. data-governance-program` first, then the systems inventory notebooks in `1. coco-data-hub`, then this file.

1. From Obsidian - open the `it-governance-program.md` file and click the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the command:

    ```
    dr_egeria --directive process --userid garygeeke --user_pass secret it-governance-program.md
    ```

## Onboarding Simon Burr

`onboarding-simon-burr.md` links to the Chief Security Officer folio and the security definitions in `0. data-governance-program`, so load that first.  Load it before the files that Si authors - the security glossary and the risk scopes:

```
dr_egeria --directive process --userid simonburr --user_pass secret onboarding-simon-burr.md
```

## Loading the security glossary

`security-glossary.md` links the glossary to the security governance principle in `0. data-governance-program/data-security-strategy.md`, so load that first.  It is loaded as Simon Burr:

```
dr_egeria --directive process --userid simonburr --user_pass secret security-glossary.md
```

## Loading the risk scopes

`risk-scopes.md` links definitions from `0. data-governance-program/risk-register.md` to the components from `1. coco-data-hub/strategic-supply-chain-analysis.md`, so load both of those first.  It is the output of Simon Burr's threat modelling, so it is loaded as Simon Burr:

```
dr_egeria --directive process --userid simonburr --user_pass secret risk-scopes.md
```

The Martyn's Law definitions load after this file.


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.