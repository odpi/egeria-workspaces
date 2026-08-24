<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**People and Organizations**

Dr.Egeria commands for the design patterns in Chapter 3, "People and Organizations", of *Patterns of
Information Management* by Mandy Chessell and Harald C. Smith (IBM Press, 2013).
The book sets each pattern's identifier in small capitals; those small-capital names are used
here as the display names, and as the reference names in [poim-pattern-links.md](poim-pattern-links.md).

Patterns marked as summarised below are described in the book by a patlet table only
(icon, name, problem, solution) rather than a full pattern description, so they carry a
Description, Problem Statement and Solution Description but no Context, Forces, examples
or consequences.

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Centric Organization

### Qualified Name

DesignPattern::Information Centric Organization

### Category

Information Centric Organization Patterns

### Description

Make the management of information a strategic priority. Develop systems and practices that nurture and exploit information to maximum effect.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization exists for a purpose. It has targets to achieve and long-term aspirations.

### Problem Statement

An organization needs to make good use of its information to achieve its goals.

This seems a simple, obvious statement, but in practice it is very hard to achieve. Information is not a physical thing that can be controlled. It is ever changing and conveys different meanings depending on the context in which it is used. The absence of information can be as misleading as information that is out of date or just plain wrong. Too much information can be overwhelming and unhelpful.

It costs money to store and maintain information. Some information is required for regulatory reasons and keeping some types of information, such as personal information, imposes legal responsibilities to keep it safe and to retain it for a specified period of time. The management of information must be purposeful and continuous.

How does an organization collect, maintain, and distribute the right information to support its activities?

### Problem Example

MCHS Trading is a trading company that has four channels to market for the goods and services it offers: physical stores, an Internet site, mail order, and a customer call center where people can phone in orders.

MCHS owns a number of applications, each supporting different parts of the business. Information must flow between its order taking, shipping, and invoicing applications to receive and fulfill customer's orders. Any failures in this flow of information could affect the organization's ability to serve its customers, or collect money for goods sent out.

### Forces

- Conflicting business imperatives and obligations—The same information may be subjected to conflicting requirements across different lines of business or from diverse obligations.
- Information not seen as an asset—Information is considered secondary or merely supportive to the "real" business.
- No one takes ownership—Ownership of information implies responsibility for its management and many individuals or groups do not want responsibility for what they can't control.
- Information not tracked or measured—The organization has limited insight into what information is being stored, how it is being managed, and where and how it is being used.
- Limited means to ensure information management practices are understood—The organization does not have clear or effective channels to ensure everyone understands how information is managed.
- Duplicated information—The same information may be stored in many places in an organization's systems.
- Many formats for each type of information—Each copy of information tends to have its own unique format and there are differences in validation rules and the use of the information.
- Inconsistent information—The set of valid values for an information attribute may not be consistent throughout the organization.
- Information comes from many sources—An employee receiving new information may not be a direct user of any of the information processes within the information supply chain.
- People make mistakes—They may enter incorrect information into a user interface, either through lack of attention, lack of training, or because the values they have are not correct.
- Information quality varies—Information coming in from outside of the organization can arrive through many channels and can have differing levels of quality.
- Access and privacy controls require constant scrutiny—Information is regularly distributed and dispersed through the organization for varied uses, often with insufficient controls.
- Storage costs money—Each copy of information costs money to store and maintain.

### Solution Description

Make the management of information a strategic priority. Develop systems and practices that nurture and exploit information to maximum effect.

This does not mean information is kept for no reason. The essence of information management is to only keep information that is necessary for the running of the organization and to manage it throughout its life cycle—from creation, through maintenance, and eventual archival and deletion.

The characteristics of an information centric organization are as follows:

- Appropriate information is delivered to individuals as and when they need it to perform their jobs.
- Information is protected and only available to those who need it.
- The organization can demonstrate that it is meeting its legal and ethical obligations (see Information Management Obligation).
- Information is only kept as long as it is needed. After that, it is destroyed.
- The use of information and any opportunities to make use of new sources of information are actively sought to continuously improve the organization's effectiveness. Delivering these characteristics requires four patterns to be in place:
- An Information Governance Process ensures information has an owner and people have a clear understanding of their responsibility toward the management and protection of information.
- Information Provisioning ensures Information Processes operate on information from authoritative sources.
- Information is moved between systems (Information Nodes) along well-defined and managed pathways called Information Supply Chains.
- Information is managed appropriately throughout its life cycle according to the kind of Information Element it is.

### Solution Example

In MCHS Trading, order records are created in the order-taking applications and passed to the Shipping application. The Shipping application controls the dispatch of goods. When all of the goods on the order are sent to the customer, a copy of the order record is sent to the Invoicing application. The Invoicing application controls the process for invoicing the customer and collecting the payment. This is shown in Figure 3.3.

Each information node (application) supporting the order-processing activity maintains an information collection of order records. These records reflect the work performed on the order within the information node. When the work for an order moves to a new information node, the order record in the original information node is no longer updated.

Each information node also needs information collections that describe the customers and products that are referenced by the orders. Additional information processes must maintain this information and distribute any changes because the values should be consistent in each information node. When MCHS Trading embarked on becoming an information centric organization, the update of customer and product details was handled manually in each information node. It also had no ability to create management reports on customer trends and which products were the most profitable. MCHS Trading created an Information Governance Program and implemented a number of Information Solutions to improve how it was managing information, including the following:

- Centralized Master for product details
- Synchronized Masters for customer details
- Distributed Activity Status for order processing
- Historical Reporting for their management reports
- Partner Collaboration to connect to their suppliers to replenish the stock The result is an efficient and effective management and distribution of information between its systems. Figure 3.4 summarizes many of MCHS Trading's information supply chains.

### Benefits

- An information centric organization knows what actions it is taking, where, when, by whom, and why.

### Liabilities

- Becoming an information centric organization requires a willingness to constantly review, refine, and develop the breadth and depth of information available to decision makers in the organization because the world, and its expectations, are continuously changing as people become more sophisticated in their use of information. It also requires the organization to see information as not only important, but also as a strategic asset, and not simply as an adjunct to the business.

### Usage

In many industries, we see successful organizations making information a key asset and using it to deliver better value and customer service by treating people and issues in a holistic way. The business leadership in an organization is responsible for driving focus on information within the business strategy and plan. This is referred to as their Information Agenda.

### Search Keywords

- Patterns of Information Management
- Information Centric Organization
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Management Obligation

### Qualified Name

DesignPattern::Information Management Obligation

### Category

Information Centric Organization Patterns

### Description

Review the regulations and policies that apply to the organization, and extract and document the specific requirements that relate to information management as information management obligations that define where the requirement came from and how the organization operations comply.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization operates within one or more legal frameworks (depending on the number of countries it operates in). These legal frameworks define certain requirements that the organization must meet in order to continue its operations. Failure to do so can lead to fines and other prosecutions.

### Problem Statement

An organization has an obligation to operate in a legal and ethical manner according to the regulations covering its type of operation. This includes the way information is managed.

How does it keep track of the regulations and its response to them, in order to demonstrate it is operating legally and ethically?

### Problem Example

MCHS Trading operates its stores throughout North America and Europe. It has an Internet presence, which means it is selling to people from all over the world. The goods that it sells come from small-scale producers who are located in many difference countries. How can it be sure that it is managing the information that supports its operation correctly? Different countries have different accounting, privacy, import/export rules to name but a few of the regulations it needs to respect.

### Forces

- An organization is a collection of freethinking individuals—Their actions when working on behalf of the organization must be in compliance with the regulations. However, very few will have read these regulations, or could really understand them if they tried and rely on specialized education and guidance from co-workers and the information systems they use to operate in the right way.
- Many industries are seeing a growth in the number of regulations that apply to them—These regulations overlap in content, and where an organization spans the boundaries of different legal frameworks, it can find itself subject to conflicting regulations.
- It is not enough to be compliant with a regulation—An organization must be able to demonstrate its compliance. This means that everyone in the organization should comply with the regulations in a consistent way and keep records of this compliance.

### Solution Description

Review the regulations and policies that apply to the organization and extract and document the specific requirements that relate to information management as information management obligations that define where the requirement came from and how the organization operations comply.

The aim of this exercise is threefold:

- To understand what is required.
- To document what is required in a language that is meaningful to the organization.
- To make decisions on how the organization will conform, or not, as the case may be. This way, the organization is purposeful in its response to the regulations and individuals understand what they need to do. Regulations evolve over time and are created for specific purposes by different groups of people. There is often duplication and inconsistency within the regulations. The clauses of the regulations need to be linked to similar and contradicting clauses from other regulations. Then a response to each of the uniquely identified requirement or obligation is created. This will define how the organization will implement the obligation and also provide the evidence that it is doing so. See Figure 3.5.

### Solution Example

MCHS Trading has a department dedicated to understanding and defining how the organization will respond to the many regulations it is subject to, such as tax, import/export regulations, health and safety, privacy, vendor regulations, and many more. This department reports to the chief operating officer (COO).

### Benefits

- The organization develops a cost-effective response to the regulations it must comply with.

### Liabilities

- Reading and reviewing regulations takes time. It needs tools that can contain the regulations and link to the organization's interpretation and response. Often there are industry bodies that can provide guidance on how to implement the regulations within the industry. The cost of implementing a regulation may be greater than the cost of noncompliance.

### Usage

The responsibility for reviewing regulations and defining the response is usually centralized in a business controls operation. These people also drive the documentation and auditing of compliance within the organization.

Tools exist to manage and document regulations. A common name for them is the Inventory of Obligations. The regulations and responses associated with the regulation may be referenced in an Enterprise Content Management system, or captured and stored in a wiki (a commonly accessible and online reference site within the organization). Audit, Legal, and Risk Management functions within an organization are generally responsible for the review, response, and monitoring of these obligations.

### Search Keywords

- Patterns of Information Management
- Information Centric Organization
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Management Strategy

### Qualified Name

DesignPattern::Information Management Strategy

### Category

Information Centric Organization Patterns

### Description

Define an information strategy that lays out the why , what , and how the organization will manage information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to become an Information Centric Organization.

### Problem Statement

What are the aspects of an organization's information management that it should focus on to develop a strategy to become more information centric?

Many organizations recognize that trusted information is a key to their success. However, they have a lot of information and changing everything at once is neither feasible nor necessary because some types of information are more important than others. The organization needs to define a strategy that lays out its approach.

### Problem Example

How does MCHS Trading become an information centric organization? What type of information should it focus on? What solutions should it invest in? What else needs to change?

### Forces

- Business strategy—An organizations has a strategy that defines how it will produce/ acquire and sell goods or services in order to achieve a profit within constraints, options, or directions.
- Limited resources—An organization has limits in terms of money, physical resources, and human resources that it can apply to its information management strategy.
- Limited ability to absorb change—The resources in an organization have a finite ability to handle change at a given point or for a given period of time.
- Variety of information—An organization has many kinds of information—of varying value and quality.
- Duplicated information—The same information may be stored in many places in an organization's systems.
- Many formats for each type of information—Each copy of information tends to have its own unique format and there are differences in validation rules and the use of the information.
- Inconsistent information—The set of valid values for an information attribute may not be consistent throughout the organization.
- Information comes from many sources—An employee receiving new information may not be a direct user of any of the information processes within the information supply chain.
- People make mistakes—They may enter incorrect information into a user interface, either through lack of attention, lack of training, or because the values they have are not correct.
- Information quality varies—Information coming in from the outside of the organization can arrive through many channels, and have differing levels of quality.
- Storage costs money—Each copy of information costs money to store and maintain.

### Solution Description

Define an information strategy that lays out the why, what, and how the organization will manage information.

An information management strategy defines the goals and road map for developing and improving the collection, use, and management of information.

The why section covers the business imperatives that drive the need to be information centric. This helps focus the effort on activities that deliver value to the organization.

The what section covers the type of information that MCHS Trading must manage to deliver on its business imperatives. This includes the subject areas to cover, which attributes within the subject area need to be managed, the valid values for these attributes, and the management policies (such as protection and retention) that the organization wants to implement.

Finally, the how section is described using Information Management Principles that provide the general rules for how information is to be managed by the information systems and the people using them along with how information flows between them.

### Solution Example

MCHS Trading has the following business imperatives that are relevant to the information management strategy:

- Exemplary customer service, where an individual customer experiences a continuous and coherent "conversation" with the organization, no matter whom they talk to
- Accurate, complete, and reliable information about an interesting range of products sourced from responsible and efficient suppliers
- Privacy and security of all personal information retained by the organization
- Efficient delivery of orders through a transparent supply chain MCHS Trading identifies the following subject areas of information that it should focus on.

### Benefits

- Developing an information management strategy creates a set of objectives for the organization, which guides the investment in information management technology and related solution that support the business. Starting with the business imperatives ensures the information management strategy is aligned with the needs of the organization, making it easier to demonstrate its relevance and value.

### Liabilities

- An information management strategy needs sponsorship from the business—without it, the actions it recommends will not be implemented. The stakeholders in the organization need to support efforts to align projects with the strategy and ensure the information governance program is empowered to support it.

### Usage

An enterprise architecture team developing a shared approach to IT for the organization often creates the information management strategy, typically in the form of an IT strategy and an enterprise architecture. It helps them think through where they should invest to deliver the best value for the organization.

### Search Keywords

- Patterns of Information Management
- Information Centric Organization
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Management Principle

### Qualified Name

DesignPattern::Information Management Principle

### Category

Information Centric Organization Patterns

### Description

Agree the underlying general rules that define how information shall be used, maintained, and/or protected.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is defining its information management strategy.

### Problem Statement

An organization has not defined how information should be managed.

As a result, every IT project makes an independent decision on how they collect, manage, store, and use information. Over time, the variety of approaches leads to high maintenance costs and requires complex integration software to connect all of the systems together.

### Problem Example

MCHS Trading is looking to improve how its information nodes manage information and need to develop guidance on how the technical teams should develop this new capability.

### Forces

- Variety of technology—Many types of technology and vendors offering information management solutions. Which ones should be used, when, and in which combination?
- Variety of patterns for information management—Which style of information management should be used and under what circumstances?
- Rapid shifts in technology and skill requirements—Changes in technology and the skill sets to use the new technology require regular review to ensure they are addressed by the defined principles.
- Acquisition of new business and resources—Mergers, acquisitions, and initiation of new business lines bring together teams working from different core sets of principles. The differing principles must be merged, aligned, or resolved.
- Limited skill and resource—Many organizations have a fixed pool of IT staff, have limitations in training that staff, and have a limit as to how many different types of technology it can support.

### Solution Description

Agree on the underlying general rules that define how information shall be used, maintained, and/or protected.

These general rules are called information management principles and they are a core element of the Information Management Strategy of an organization:

They are used to capture the core beliefs and approaches defining how the organization will utilize and deploy both business and information technology assets and resources to support the information supply chains.

Each principle is defined with a short description, the reasons (purpose) for adopting the principle, and a list of implications for the organization:

- The purpose statements provide a basis for justifying all proposed decisions and related activities.
- The implication statements provide an outline of the key tasks, resources, and potential costs to the business of implementing the principle. They also provide valuable inputs to future transition initiative and planning activities. Once approved, information management principles are often refined into policies and rules that are specific to different parts of the organization. They are embedded in the operation of processes across the organization and measured through metrics defined by the information governance program.

### Solution Example

MCHS Trading defines the following set of information management principles to guide its information solutions. Here are some examples:

Information is an asset. It has value, and cost, to the organization and should be captured, managed, stored, used, and disposed of according to well-defined and cost-effective procedures that ensure it is available to the appropriate person at the right time and at a sufficient level of quality. Purpose:

- Raises awareness and motivates leaders to focus effort on the effective management of information—from creation to destruction.
- Prevents incorrect or inconsistent information from inhibiting decision making. Implications:
- Individuals who use the organization's information must be aware of their responsibilities toward the information that they handle.
- Consideration of the management of information is an important part of any IT project.
- The organization should create a model of the cost and value of its information to help steer investment in its information management capability. Information is shared. It should be captured, stored, and managed in a way that will allow appropriate sharing across the organization based on business need and security rules. It should be validated as it is captured and it should flow between applications along well-defined information supply chains. Purpose:
- Reduces the number of independent copies of information that must be kept synchronized. Implications:
- The organization should agree on what information is important to share and how it should be managed.
- The IT part of the organization should invest in skills and projects to enable it to actively manage the sharing of information between information collections. Information is identified. The core types of information that are of critical importance to the organization are defined in a subject area definition and preferred structures for managing this information are documented in information models. The management and distribution of this type of information is handled through an information supply chain. Purpose:
- Ensures consistent view and use of information throughout the organization
- Increases the consistency of how this type of information is stored in the information collections and transmitted between the information nodes Implications:
- One or more individuals must be given responsibility to maintain the descriptions and models of this type of information.
- The subject area definition and information models should be used in decision making and the development of new information solutions. Information is governed. An information governance program is responsible for governing how each type of information should be managed, protected, and used. This program defines the rules, communicates them to affected parts of the organization, reviews and grants exceptions to the rules where appropriate, audits compliance, and refines the rules to meet new business requirements. Purpose:
- Provides a focal point for defining and enforcing policies related to the management of information. Implications:
- The organization needs to appoint an Information Governor and provide him or her with the appropriate sponsorship to be able to make the necessary changes to the way people work, and to commission changes to the information nodes that manage the information. Information is protected. Information is protected from inappropriate use, only available to authorized users, and recoverable. Purpose:
- Ensures information is only used by authorized people and does not leak out of the organization.
- Ensures the privacy of any person's details stored by the organization.
- Protects the organization's information from theft or malicious attack.
- Ensures the organization's information is recoverable in the event of a disaster. Implications:
- Individuals within an organization need a unique identity (user account/password) so that all of the activity they perform using the information nodes is attributable.
- Individuals need well-defined roles that determine which information they have access to.
- Individuals need to understand their roles in protecting the information they do have access to.
- There must be good information management practices around the information nodes to ensure their information collections are properly maintained and backed up. Information is measured. The quality, volume, consistency, usage, and redundancy of information is measured on a regular basis, and continuous improvement is made to the management of information to ensure these measures are trending in a positive direction. Purpose:
- Enables fact-based decision making for information management.
- Ensures consistent view and use of information throughout the organization.
- Improves the coordination and integration between information nodes.
- Prevents incorrect or inconsistent information from inhibiting decision making. Implications:
- The IT infrastructure is instrumented with information probes to collect the measurements.
- Operational management takes the time to review the measurements and take action if the indicators are moving in the wrong direction.
- There is continuous investment in the IT infrastructure that supports the management of information.

### Benefits

- Information management principles provide an effective framework within which the business can start to make conscious decisions about the business, its management style and structure, and how its information infrastructure.

### Liabilities

- Information management principles are only effective if they are enforced across the organization. This requires buy-in at multiple levels of the organization.

### Usage

The notion of identifying "principles" is a common approach used by architects to define a framework of rules that will govern the projects within their domain. These principles comprise part of an enterprise architecture.

### Search Keywords

- Patterns of Information Management
- Information Centric Organization
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Governance Program

### Qualified Name

DesignPattern::Information Governance Program

### Category

Information Centric Organization Patterns

### Description

Appoint an Information Governor to set up and run an information governance program.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is concerned with the efficient and accurate use of information.

### Problem Statement

An organization is experiencing quality and management issues with its information.

They want to find a reliable and repeatable resolution to this issue.

### Problem Example

A customer calls the MCHS Trading call center to inform the company that he changed his address. Nothing is done about it and MCHS Trading continues to use the old address—much to the annoyance of the customer.

### Forces

- Variety of information—An organization has a lot of different types of information— of varying value and quality.
- No single version of the truth—Information is often duplicated and inconsistent when looking across the information nodes.
- Decentralized ownership of information—Different copies of information tend to be owned by different groups/teams within the organization.
- No common definitions for information—There are different perspectives on what is valid and relevant to different groups/teams within the organization.
- Unknown content—The knowledge of what type of information is held by an IT system may be lost.
- Poorly communicated or understood principles—The principles on which to act in regard to information are not provided or clarified for those who work with the information.

### Solution Description

Appoint an Information Governor to set up and run an information governance program.

Information governance requires a two-way exchange of information enabling the governance board to set policy, communicate requirements, and then receive requests for exceptions and amendments to the policies. Comprehensive monitoring and metrics to demonstrate both compliance and value delivered by the program must back this up.

The leader of the governance program is called the Information Governor. This role chairs a governance board that decides on the information subject areas that require special care and the Information Management Principles (policies, impact, and outcomes) by which this information will be governed.

Information Owners are identified for each of the key information nodes and/or processes that use this type of information and they appoint Information Stewards to monitor the quality of the information and remediate any issues. There are five main activities in an information governance program:

- Managed communication—Ensuring people understand their role in information governance
- Managed vitality—Keeping the governance program up to date and relevant to the organization
- Managed feedback—Measuring and reporting on the effectiveness of the governance program
- Managed exception—Enabling people to request an exemption from following the governance program for a particular circumstance
- Managed compliance—Particular procedures that enforce the requirements of the governance program These activities describe how the governance team interacts with the other teams in the organization that are responsible for the information being governed. They are supported by information management functions that support the measurement, reporting, enforcement, and remediation of issues with governed information.

### Solution Example

Whenever MCHS Trading receives a change of address for a customer, it must be captured, the address validated and standardized so all the relevant fields are completed, and then it must be distributed to the Customer Hub, E-Shop, and Stores applications. The customer address for inflight orders is unchanged.

Prior to the introduction of the Customer-Care application, this process was ad hoc and very error-prone. MCHS Trading recognized that its current systems make it very difficult to ensure that a change to a customer's details is made reliably and consistently to all copies of this information. Worse still, its employees had come to accept there is nothing that they can do about it. Therefore, a governance program is set up for customer details. The team assigned to this program first focuses on how customer details are managed by the information nodes. It discovers each system has its own copy of this information and there is no synchronization. The team commissions a number of projects to create an Information Supply Chain for customer details. This includes a new Customer-Care application where customer-facing employees can request changes to customer details. This includes changing contact details as well as issues, complaints, and special requests. The team also provides training to all employees who work with customer details for its responsibilities toward its quality. Finally, the team adds regular monitoring and reporting on how the quality of customer details is changing over time.

### Benefits

- An information governance program provides a focal point for coordinating the management of shared information.

### Liabilities

- The information governance program will cause additional work for some teams, who may not necessarily reap the benefit. The information governance program needs executive sponsorship and must routinely demonstrate that it is delivering value. As such, starting small, demonstrating success, and then growing scope is often an effective strategy. The information governance program has to listen for and adapt to the changing priorities of the organization to maintain its relevance. Finally, it has to have teeth; otherwise, once teams realize nothing happens when they are noncompliant, they tend to deprioritize their compliance work.

### Usage

Information governance programs (sometimes called data governance programs) are common in large organizations where the number of systems typically is more than an individual can oversee. Typically, an organization implements information governance in a staged manner, gradually increasing its level of information governance maturity (see http://www-935.ibm.com/ services/uk/cio/pdf/leverage_wp_data_gov_council_maturity_model.pdf).

### Search Keywords

- Patterns of Information Management
- Information Centric Organization
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information User

### Qualified Name

DesignPattern::Information User

### Category

Information User Patterns

### Description

Classify the people connected to the organization according to their information needs and skills. Provide common channels of communication and knowledge sharing about information. Then provide user interfaces and reports through which they can access the information as appropriate.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

There is an organization. It exists to fulfill a purpose and employs people to perform activities that contribute to that purpose.

### Problem Statement

Individuals need access to the organization's information in order to perform their work.

Each individual's information need is specific to the work he or she is performing. It must be delivered in the right context, and at the right time, to support his or her work. An individual may also have new information to contribute. The organization must make it easy for the individual to provide this information and also validate that it make sense.

### Problem Example

An MCHS Trading employee is talking to a customer on the order help line. The employee needs to retrieve information about the customer, answer queries about any orders the customer has, and make a record of the conversation. The employee may also need to update information about the customer, such as a change of address, phone number, or email account.

### Forces

- Information must be protected from inappropriate use—For example, information about individuals should be treated as private. Financial results, or information that gives an organization a competitive advantage, must only be revealed to employees who are privileged to receive it.
- The value and meaning of information depends on perspective—Individuals across the organization will need different types of information, with different levels of precision, accuracy, and currency.
- Information has multiple interpretations—Information about the same object, person, organization, activity, result, event, or concept exists in many forms and is not always consistent.
- Poorly communicated or understood principles—The principles on which to act in regard to information are not provided or clarified for those who work with the information.
- Knowledge is recorded locally—Individual users working with information do not consistently record details where other users can access and understand it.
- Rapid turnover of resources—Regular change in information users may disrupt the flow and understanding of information as well as the principles that govern it.
- Multiple points of user entry with differing roles—Systems, applications, processes, and information stores do not necessarily have consistent implementations of user roles. Consequently, users may have overlapping and potentially conflicting roles in their work.

### Solution Description

Classify the people connected to the organization according to their information needs and skills. Provide common channels of communication and knowledge sharing about information. Then provide user interfaces and reports through which they can access the information as appropriate.

The classification of individuals interacting with an organization's IT systems is typically expressed as user roles. A user role expresses a person's responsibilities and goals, his or her skills, the tasks he or she needs to perform, the information he or she is working with when performing tasks, and where he or she needs to get information to perform his or her role.

Information Processes provide IT support for the tasks a person performs. The information is displayed and accepted through user interfaces, such as web browsers, mobile devices, and the more traditional laptops or computer terminals. An information process drives sequences of interactions between the individual and the IT systems, enabling him or her to select the task he or she wants to perform and then stepping through screens that allow the individual to retrieve, change, and add information. The information process may support the work by performing calculations or bringing significant facts to the individual's attention.

Behind the scenes, the information process is interacting with the information supply chain through Information Services that are responsible for retrieving and updating the Information Collections as appropriate. The information collections persist the information in case of system failure. See Figure 3.6.

### Solution Example

The MCHS Trading employee talking to the customer on the telephone uses the Customer-Care application. This application incorporates information processes to retrieve customer details along with related orders and make changes as necessary. These information processes are designed to support the Customer Support Representative user role.

### Benefits

- Identifying the user roles of individuals using an organization's IT systems enables the organization to control what information is made available to whom and under which circumstances. This can be very helpful and reduce the effort to demonstrate that the organization is compliant with regulations related to information production and use. This type of analysis can simplify the work of many individuals because they only have to learn how to perform the tasks relevant to their role, rather than having to understand a much broader view of the organization's operation.

### Liabilities

- Hard-coding the tasks and type of information made available to groups of people in the information processes can create inflexibility in the operation of the organization. Each person using an organization's information must be aware of his or her responsibilities for appropriate management of this information.

### Usage

Documenting user roles is a common practice for user experience practitioners. These user roles can be described as text or more formally in models (see http://www.ibm.com/developerworks/ library/ar-usermod1/).

Most user interfaces are provided from applications that implement the majority of information processes. These are also flexible approaches to supporting user roles using Business Process Management technology that works from a model of how the process should operate. This model defines the tasks a user of a particular role will perform. For example, see the HumanActor element in the Open Group's SOA Ontology (http://www.opengroup.org/soa/source-book/ontology/human_task.htm).

User roles are often used to control access to systems. A user registry, such as the Lightweight Directory Access Protocol (LDAP), defines what operations are permissible on the information. Then individuals are assigned to the roles. When an individual logs on to an information system, his or her identity is checked to discover which roles, and as a consequence, which operations/information access are permitted. Individual applications and databases incorporate their own specific security, which may or may not utilize common user registries.

User roles form part of the broader strategy for information security.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Auditor

### Qualified Name

DesignPattern::Information Auditor

### Category

Information User Patterns

### Description

Appoint an individual or team of individuals to review key aspects of how the organization is actually operating and compare it with agreed processes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An organization needs to demonstrate it is operating legally, ethically, and effectively.

### Solution Description

Appoint an individual or team of individuals to review key aspects of how the organization is actually operating and compare it with agreed processes.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Governor

### Qualified Name

DesignPattern::Information Governor

### Category

Information User Patterns

### Description

Appoint an individual to coordinate the definition of policies related to information governance and their implementation.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

There is no obvious point of control in an organization to ensure people treat information as an asset.

### Solution Description

Appoint an individual to coordinate the definition of policies related to information governance and their implementation.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Owner

### Qualified Name

DesignPattern::Information Owner

### Category

Information User Patterns

### Description

Appoint an individual to be the owner of the information collection who is responsible and accountable for ensuring it is capable of supporting the organization's activities.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An information collection needs investment to ensure its contents are of acceptable quality to support the organization's activities.

### Solution Description

Appoint an individual to be the owner of the information collection who is responsible and accountable for ensuring it is capable of supporting the organization's activities.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Steward

### Qualified Name

DesignPattern::Information Steward

### Category

Information User Patterns

### Description

Appoint an individual to coordinate the manual activity necessary to monitor and verify that an information collection is meeting agreed quality levels. Create user interfaces and access rights to involve this individual in information quality processes such as the exception management process.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Not all activity that ensures information quality can be automated, nor does it fit neatly into the organization's information processes.

### Solution Description

Appoint an individual to coordinate the manual activity necessary to monitor and verify that an information collection is meeting agreed quality levels. Create user interfaces and access rights to involve this individual in information quality processes such as the exception management process.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Worker

### Qualified Name

DesignPattern::Information Worker

### Category

Information User Patterns

### Description

Appoint individuals who are responsible for the manual steps in the core business activity. Create user interfaces and access rights to provide these individuals access to the information supply chain through the information processes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

The organization needs people to organize, manage, and operate its core business activity.

### Solution Description

Appoint individuals who are responsible for the manual steps in the core business activity. Create user interfaces and access rights to provide these individuals access to the information supply chain through the information processes.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Business Analyst

### Qualified Name

DesignPattern::Business Analyst

### Category

Information User Patterns

### Description

Appoint an individual to analyze the way people are working, understand where the processes can be improved, and define new procedures, rules, and requirements for the IT systems.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An organization needs to improve how it operates.

### Solution Description

Appoint an individual to analyze the way people are working, understand where the processes can be improved, and define new procedures, rules, and requirements for the IT systems.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Data Quality Analyst

### Qualified Name

DesignPattern::Data Quality Analyst

### Category

Information User Patterns

### Description

Appoint an individual to monitor and analyze the state of the information flowing through the information supply chain.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

The actual information values that are flowing through the information supply chain needs to be monitored and assessed.

### Solution Description

Appoint an individual to monitor and analyze the state of the information flowing through the information supply chain.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Data Scientist

### Qualified Name

DesignPattern::Data Scientist

### Category

Information User Patterns

### Description

Appoint an individual to analyze the information that the organization is collecting in order to understand patterns of success.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An organization needs to understand how it can improve its operational efficiency and customer service.

### Solution Description

Appoint an individual to analyze the information that the organization is collecting in order to understand patterns of success.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Infrastructure Operator

### Qualified Name

DesignPattern::Infrastructure Operator

### Category

Information User Patterns

### Description

Appoint an individual responsible for starting, maintaining, and monitoring the systems that support the information supply chain.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 3, "People and Organizations".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

The systems that support the information processes of an organization need to be available and operating correctly.

### Solution Description

Appoint an individual responsible for starting, maintaining, and monitoring the systems that support the information supply chain.

### Search Keywords

- Patterns of Information Management
- Information User
- People and Organizations

### Version Identifier

1.0

### Status

ACTIVE

____

