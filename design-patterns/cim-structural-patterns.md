<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**Structural Patterns for the Common Information Model**

This Dr.Egeria workbook loads the five structural design patterns described in Chapter 3 of
*Common Information Models for an Open, Analytical, and Agile World* into the open metadata
ecosystem, along with the specialization and relationship links that the chapter describes.

In the source book the pattern identifiers are typeset in small caps.  These small-capital
names — `COMMON INFORMATION MODEL`, `CONCEPT BEADS`, `CONTINUOUS FABRIC`, `ENCAPSULATED VIEWS`
and `UNIFYING CONTEXT` — are used here as the display names of the design patterns, and as the
reference names in the linking commands.

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Common Information Model

### Qualified Name

DesignPattern::Common Information Model

### Category

Structural Patterns for the Common Information Model

### Description

The generic structural pattern for a common information model.  An organization develops a shared understanding of the terminology, meaning and structure of its information so that its IT systems and business operations can be integrated in an agile and effective way.

### Legal

Extracted from Chapter 3, "Structural Patterns for the Common Information Model", of *Common Information Models for an Open, Analytical, and Agile World* by Mandy Chessell, Gandhi Sivakumar, Dan Wolfson, Kerard Hogg and Ray Harishankar, IBM Press, 2015, ISBN-13: 978-0-13-336615-0.  © Copyright 2015 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is looking to improve the methods it uses to develop and integrate IT systems into its operations.

### Problem Statement

An organization is struggling to integrate its IT systems and business operations.  This integration may be required to increase its efficiency, embrace new technology, expand its business, and/or improve its customer service.

Organizations today have many IT systems that have been developed over time.  They are struggling to innovate while trying to maintain and manage existing IT systems.  Market forces are driving organizations to become more integrated, to support new channels (such as mobile), exploit new platforms (such as cloud and big data), and support a more social way of working both inside and with external parties such as customers and business partners.  What can they do to provide a stable foundation for maintaining a state-of-the-art IT capability?

### Problem Example

A fictitious travel agent, GKDMR Travel, has many systems that have been acquired over the years as the business has grown.  Its systems are getting old and it wants to make better use of modern approaches such as mobile, social media, cloud-based deployments, open source software, and analytics.  The company's budget is not large, but it anticipates having to change some of its systems to accommodate its vision.  However, many of the existing systems will remain and there is a need to interface them to the new systems.

### Forces

- Existing systems provide key capability to the organization.  They are expensive to replace and must continue to operate while any changes are made to them.
- An organization's information is distributed among its existing IT systems, in people's heads, in unmanaged files on employee laptops, in paper documents, and externally on the Internet, or in business partner systems.
- The information within an existing system is rarely as good a quality as the organization that owns it believes.
- An organization will use inconsistent terminology across its many departments, professional disciplines, and internal fiefdoms.  Sometimes the same term is reused for different purposes, or even when the meaning is consistent, assumptions about its timeliness, precision, and accuracy will differ among the different groups inside the organization.
- The database schema of an application does not document all the information available through the application interface.  Some key values are derived, and so an important piece of information about a customer that could be useful for analytics or another customer service application can be locked inside a single application's logic.

### Solution Description

The organization should develop a shared understanding of its information's terminology, meaning, and structure in order to facilitate agile and effective integrated operations.

Information is at the heart of an organization's ability to service its customers, deliver on its promises, and collect the expected rewards for its services.  The types of information that an organization holds are stable, although the scope of information available has been growing recently with the digitization of many aspects of our lives.

The organization can develop a set of common information definitions that captures the meanings of key concepts, facts, events, and activities used by the organization; the preferred structures that should be used to store and exchange this information; and the types of values that must be captured to describe them.

These common information definitions are implemented as a collection of models and definitions.  This collection covers the portion of the organization's information that needs to be shared and synchronized.  It must represent many perspectives on this information and be consumable in different programming environments.  Collectively, these models and related artifacts are called the common information model.

An organization can choose which types of models to create, and to which level of detail.  The focus will depend on where change happens most often and where the cost of change is high or notoriously error prone.  The different types of models may not be entirely consistent.  However, the closer they are, the less transformation is required as information flows around the enterprise.

### Solution Example

GKDMR Travel has three major projects that will be assisted through the creation of a common information model.  It is building smartphone and tablet applications for its customers and customer-facing staff that must integrate with its existing systems and remain consistent with printed documentation and the company website.  It wants to offer real-time alerts and actions to support its traveling customers, which needs information from existing systems integrated with external information.  And it wants to improve the management reporting on the state of the business and the trends it sees, in order to optimize its operations.

The plan is to create a common information model that includes a glossary of terms describing the meaning of the different types of information used by customers and staff; a model of the objects used in the mobile applications so that they display consistent structures with consistently named fields; a model of the service interfaces that define how information is exchanged between the existing systems and the new ones; and a persistence model that describes how data should be consolidated and linked together.

The consistency that occurs between these models will speed up the collaboration between the different teams by implementing new capability and extending and enhancing the existing systems, which will then enhance the quality of the resulting applications.

### Benefits

- If an organization can understand the information it uses, then it is better able to assess which systems are important, how best to manage the information it has, what types of information need to be made available to new applications, and where special care must be taken to protect valuable or sensitive information.
- A well-formed common information model creates an adaptable definition of how information should be represented and shared at key places where the organization needs to synchronize or control its operations.  Without it, information sharing can be ad hoc and developed as a number of inflexible point-to-point solutions.
- When a new project is started, the common information model is an invaluable planning tool for identifying what type of information is needed, where it is located, and how it should be structured in the new capability.
- When an existing application built to the guidelines of the common information model must be maintained, the development team has the common information to guide its understanding of the existing code.

### Liabilities

- For a common information model to deliver value it must be treated as an asset, with an owner who is responsible for its ongoing maintenance and executive support to ensure it is properly governed and to encourage use of the common information model content.
- The contents of a common information model must be easily consumable by the teams that are building and maintaining the IT systems.  Ideally, physical artifacts such as interfaces and schema would be generated from the common information model and included in the developers' working toolset, so that it becomes easier for the development team to use the common model rather than create its own.
- In some organizations, where data modeling is not widely understood, the generated physical artifacts are the only part of the common information model that many developers see.  In this case, these physical artifacts should include comments and annotations covering the semantic definitions of the model.

### Usage

Some of the key uses of a common information model within an organization are creating a consolidated repository of information from different sources, such as a data warehouse, operational data store, and master data management hub; defining canonical information services for exchanging information in a service-oriented architecture, or for consumption by a business process management (workflow) engine; and identifying the information that needs to be supplied to the corporate reporting platform.

### Search Keywords

- Common Information Model
- Information Integration
- Data Modeling
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Concept Beads

### Qualified Name

DesignPattern::Concept Beads

### Category

Structural Patterns for the Common Information Model

### Description

A common information model built as a set of discrete, independent concept definitions, each with a clear meaning and a simple structure for recording information about an instance of the concept.  Suitable for teams with a low investment in modeling skills, such as agile development teams.

### Legal

Extracted from Chapter 3, "Structural Patterns for the Common Information Model", of *Common Information Models for an Open, Analytical, and Agile World* by Mandy Chessell, Gandhi Sivakumar, Dan Wolfson, Kerard Hogg and Ray Harishankar, IBM Press, 2015, ISBN-13: 978-0-13-336615-0.  © Copyright 2015 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is looking to improve the methods it uses to develop and integrate IT systems into its operations.

### Problem Statement

An organization needs common definitions of the simple concepts that are used in many applications to improve the efficiency and consistency of the work of its developers.  However, it does not have a strong skill base in modeling.

Some organizations do not have a strong skill base in data modeling.  This is often true where developers are using agile development, because their focus is on rapid prototyping and delivering solutions incrementally.  Without constant refactoring, the code developed using this approach can become bloated and inconsistent.  As a result, mature agile development teams have a strong emphasis on standards and consistent approaches.  How is it possible to bring the benefits of a common information model to a team of agile developers who do not want to spend time creating, or learning, a large data model?

### Problem Example

The mobile development team at GKDMR Travel is working on three new applications: a customer application that runs on a smart phone or tablet and enables people to maintain their customer details, see their loyalty status and outstanding offers, browse the holiday destination catalog, view other customers' feedback, book holidays, comment on their experiences, and pay their balance; a tablet application for the staff working at the holiday destinations to receive guest lists and meeting point details, receive instructions, report incidents, and interact with guests by text message or email; and a tablet application for the staff in the travel agent's office to help with customer enquiries, book holidays, document issues, note stock levels of brochures, and review the current promotions.

These applications need to be generated quickly, with iterations to allow the potential users to provide feedback on the suitability and ease of use of the applications.  How does the team ensure consistency in the way these applications use the enterprise data around personal customer details, stores, products, orders, packages, and payments?

### Forces

- Employing a common information model takes time.  The team needs to learn about the existing content, develop new definitions, and correct errors.
- Agile development is often used where the requirements are evolving with the code.  This is particularly common when the project is exploring a new technology, capability, or approach.
- The iterative nature of agile development means there is not time to wait for new model content to be developed, reviewed, and approved before it is used in the code.

### Solution Description

Create a common information model that defines a clear meaning for each concept and a simple structure for how to record information about an instance of this concept.

The concept beads common information model is defined as a set of discrete concepts.  Each concept definition has a business language description and preferred structures, possibly shown as a logical model for design documentation and then physical artifacts for different programming environments.  These physical artifacts could be XML structures, JSON interfaces, Java object definitions, or any others that are commonly needed by developers.

The concept beads style of model is used like a Chinese menu.  Developers select the concepts they need for their code, link them together as appropriate, and include them in their code.  Developers will adopt the standards defined in the concept beads common information model rather than create their own if the standards are easier to use, so the common information model artifacts should be placed so they are easy to search and download into the developers' tools.

Changes to the definitions are developed and iterated on using an agile governance approach.  Because the common information model is very modular, changes are localized and can be developed, approved, and deployed in a short period of time.

### Solution Example

GKDMR Travel begins its definition of a common information model by defining a collection of common concepts that are used repeatedly by its developers — for example Date, Time, Country, Flight, Airline, Airport, Train Journey, Train Operator, Train Station, Person Name, Holidaymaker, Employee, Holiday Booking, Invoice, Hotel, Passport, Visa and Address.

Each concept is then expanded with a textual description, a logical model definition, and an optional number of physical implementation examples.  The Address concept, for example, has a short and long business language description, a preferred logical structure of six address lines, and preferred JSON and XML structures that match it.

The developers can download the standard formats directly into their workbench.  The back-end applications that they need to call to connect to the business applications use similar structures.  The developers who use the standard formats are far more productive than those who do not.

### Benefits

- The concept beads common information model can be developed incrementally as part of an agile development process.  New elements can be developed as required by the development team and integrated into the model within the sprint (iteration) that identifies a new concept is required.
- The concept beads model is easy to consume, particularly by developers, because only a small part of it must be understood for it to be used, and it can be simply translated into programming artifacts for direct consumption into code.
- The concept beads model is flexible because concepts can be linked and combined in whichever way the developer wants.

### Liabilities

- The concept beads common information model does not provide any guidance on how concepts that are frequently linked together should be related.  This means there will be inconsistency in the relationships that are coded, which can be particularly problematic when trying to aggregate information from across sources for analysis.
- There will be situations where the attributes of a single concept bead are not well matched to the needs of a particular project.  There needs to be rapid, responsive processes to discuss whether the common concept bead should be updated, or whether the project is given an exception.

### Usage

The AS 4590-2006 standard from Standards Australia is an example of a concept beads model that is a technical standard for addresses.  Systems of Engagement-based "born on the web" companies may benefit from this as their starting point.

### Search Keywords

- Common Information Model
- Concept Beads
- Agile Development
- Data Modeling

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Continuous Fabric

### Qualified Name

DesignPattern::Continuous Fabric

### Category

Structural Patterns for the Common Information Model

### Description

A common information model in which all the concepts are linked together into a continuous network structure, defining the meaning, structure and relationships among all the core concepts of the organization.

### Legal

Extracted from Chapter 3, "Structural Patterns for the Common Information Model", of *Common Information Models for an Open, Analytical, and Agile World* by Mandy Chessell, Gandhi Sivakumar, Dan Wolfson, Kerard Hogg and Ray Harishankar, IBM Press, 2015, ISBN-13: 978-0-13-336615-0.  © Copyright 2015 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is looking to improve the methods it uses to develop and integrate IT systems into its operations.

### Problem Statement

An organization needs to integrate related information from a wide range of information sources.

The operation of an organization is typically supported by multiple applications, each supporting a unique aspect of the business.  To understand how the organization is performing as an aggregate, pulling information from each of these applications and consolidating it in a single repository is necessary.  Often the information from different applications is related and needs to be linked together in a consistent manner.  However, each application supports different data structures, identifiers (keys), quality rules, terminology, precision, and currency (timeliness).  How should the aggregated view of this data be represented?  These definitions should cover the concepts of the business and the relationships between them.  It must include historical detail for analytical mining and up-to-date information for understanding the current state of the business.

### Problem Example

GKDMR Travel wants to offer real-time alerts and actions for customers when they are traveling and for the staff who are supporting them.  Some of these alerts will be triggered by situations that develop while the customers are traveling, and some actions come from predictive analytics models that use historical information to predict the next best action the company should take to improve the service to a particular customer.

The company will need to create a repository of information that has historical and current information linked together and combined with information from external sources such as weather and location websites, customer comments, and other feedback, along with products and services from business partners.

### Forces

- Many people find large data models intimidating and difficult to understand.
- The relationships between concepts can be as important to the business as the details of the concepts themselves.

### Solution Description

Create a common information model that defines the meaning, structure, and relationships between all the core concepts.

A continuous fabric common information model is one where all the concepts are linked together into a continuous network structure.  It is built by defining the concepts that need to be represented (in a similar way to the concept beads), and then relationships are added that link the concepts together in meaningful ways.

The result is a model that describes a broad landscape of information for the organization.  Subsets of a continuous fabric model are typically used in a project.  The developer selects the concepts and relationships that are of interest and just uses that portion of the model.

### Solution Example

The analysts at GKDMR Travel create a model that describes all the concepts that could affect a customer's trip, including the causes and impacts and how they relate to each of the aspects of the customer's travel plans, insurance, and other related products they have purchased.  These are linked together to create a single linked structure — Person, Person Role, Employee Role, Holidaymaker Role, Travel Booker Role, Passport Details, Visa Details, Payment Details, Invoice, Holiday Booking, Itinerary, Destination, Journey, Transport, Transport Type and the associated Destination, Transport and Weather Reports.

This structure is used as the basis for the company's analytical repository supporting proactive customer service.  The conceptual model uses the UML notation because this was easiest to use with the company's business users.  After the model is accepted, it can be translated into an Entity-Relationship (E-R) logical model as part of the design process for the analytical repository.

### Benefits

- The continuous fabric common information model creates consistency in how concepts are linked together.  This creates a deeper level of consistency in the use of information.  For many businesses, much of the value of information comes from these relationships — knowing which customers use and buy particular products is more valuable than just having a list of customers and a list of products.  The continuous fabric model defines where the valuable relationships are and how they should be represented.

### Liabilities

- This pattern takes a greater level of maturity in the organization's governance and willingness to share information across lines of business.
- The continuous fabric model is typically very rich in object relationships and will require significant rationalization and transformation before it can depict a physical artifact that can be incorporated in an application.  The process will involve careful consideration of which aspects of the model are in scope for the project.
- Continuous fabric models can take a long time to develop.  Skilled modelers who may not be members of a project team build them.  As a result there can be a knowledge disconnect between the team owning the model and the teams using it in projects.

### Usage

Continuous fabric models are often used to describe repositories that consolidate information from many sources.  Examples of this are data warehouses and master data management systems.

Continuous fabric models are also often used to describe the concepts in a specific industry.  The SID model as published by the TeleManagement Forum (tmForum) is a good example.  The Information Framework (SID) is a reference model and common vocabulary for the information required to implement the Business Process Framework (eTOM) processes — see http://www.tmforum.org/InformationFramework/1684/home.html for more information.

### Search Keywords

- Common Information Model
- Continuous Fabric
- Data Warehouse
- Master Data Management
- Analytics

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Encapsulated Views

### Qualified Name

DesignPattern::Encapsulated Views

### Category

Structural Patterns for the Common Information Model

### Description

A common information model that defines small, independent clusters of related concepts that can be used as the structures for exchanging information on information services and application programming interfaces.

### Legal

Extracted from Chapter 3, "Structural Patterns for the Common Information Model", of *Common Information Models for an Open, Analytical, and Agile World* by Mandy Chessell, Gandhi Sivakumar, Dan Wolfson, Kerard Hogg and Ray Harishankar, IBM Press, 2015, ISBN-13: 978-0-13-336615-0.  © Copyright 2015 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is looking to improve the methods it uses to develop and integrate IT systems into its operations.

### Problem Statement

An organization needs common definitions to exchange information for multiple purposes.

Mature organizations typically have many existing applications, each supporting a particular business function.  Within an application, valuable data and capability is often locked within an individual application's unique data structures and interface styles.  When the business wants to integrate these applications together so the information and functions they contain can be shared, it must reconcile the different data structures and naming conventions.

This information sharing is typically achieved through integration interfaces called information services or application programming interfaces (APIs).  Each interface describes a number of operations that enable the caller to perform functions and create, update, retrieve, and delete information.  Each operation typically has a set of parameters or structures to pass information to the operation and a structure to return the results.  What is the best way to structure a common information model to help developers create consistent interfaces?

### Problem Example

GKDMR Travel wants to provide a consistent set of business interfaces that enable mobile and web applications to call their business applications to request details of a customer and to exchange information about holiday packages, bookings, and payments.  Specifically, it wants the representation of common entities such as holidaymaker and booking to be consistent wherever they appear in the business interfaces.  The business interface implementations will then map these common structures to the actual structure used by the application being called.

### Forces

- Many concepts are related and decisions need to be made on how these relationships will be represented.
- In creating these common definitions, choices need to be made on terminology used in the business interface as well as data structure and the valid values for each field.
- Documenting how each of the actual application interfaces maps to the common model is necessary.
- The information needed to support a particular business interface operation may need to come from multiple applications.

### Solution Description

Create a common information model that defines small clusters of related concepts that can be used as structures for exchanging information.

Each of the clusters of concepts is independent of one another, with relationships to concepts in different clusters being defined as holding the identifier of the referenced concept rather than a link to the type.

A key characteristic of this pattern is that the encapsulation provides a means of restricting access by an interface to a partition of the model rather than the entire model, which is a valuable step toward defining service or message payload structures in a consistent manner.

### Solution Example

GKDMR Travel creates encapsulated view models for Holidaymaker, Customer, Holiday Package, Booking, Itinerary, Invoice and Payment.  Each of these views includes multiple variations of the model for each concept to cover references, summaries, and queries, as well as the complete definition of the concept.

For example, Person Profile Id just includes the identifier and is used for passing a reference to an object; Person Profile Locator defines the attributes used to query for a particular Person Profile; Person Profile Summary includes the core attributes of a Person Profile; and the full details are described in the Person Profile structure.  Defining these variations simplifies the use of the common definitions, and consequently increases the consistency in which they are used.

### Benefits

- This pattern provides a common information model that supports a service-oriented approach to integration.  The data is modeled in discrete units that can be used directly in interface definitions as request or response parameters.
- This pattern is particularly important when integrating existing components because it seeks to reconcile the inevitable difference between these components.

### Liabilities

- The same concept may need multiple definitions so it can appear in messages: a small number of attributes to identify an instance of a concept, used on find queries or to represent a link to the instance; a summary of the concept, for reports or to populate a menu or table; and a complete definition of the concept when all details are required.

### Usage

OMG's Common Object Request Broker Architecture (CORBA) standards defined a set of encapsulated views that heterogeneous systems can use to integrate their operations.  See http://en.wikipedia.org/wiki/Common_Object_Request_Broker_Architecture and http://www.corba.org.

For the travel industry, the OpenTravel Alliance provides standardized XML messages for exchanging information between organizations working in the travel industry, so this seemed a reasonable starting point.  See http://www.opentravel.org.

### Search Keywords

- Common Information Model
- Encapsulated Views
- Service-Oriented Architecture
- Information Services
- APIs

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Unifying Context

### Qualified Name

DesignPattern::Unifying Context

### Category

Structural Patterns for the Common Information Model

### Description

A common information model that maps existing terminology and definitions from independently developed sources to a set of definitions representing a canonical view of the subject area, acting as a lingua franca between them.

### Legal

Extracted from Chapter 3, "Structural Patterns for the Common Information Model", of *Common Information Models for an Open, Analytical, and Agile World* by Mandy Chessell, Gandhi Sivakumar, Dan Wolfson, Kerard Hogg and Ray Harishankar, IBM Press, 2015, ISBN-13: 978-0-13-336615-0.  © Copyright 2015 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is looking to improve the methods it uses to develop and integrate IT systems into its operations.

### Problem Statement

An organization needs to unify operations that have been independent in the past.

When two organizations integrate either by merger or partnership, they often discover there are at least two ways of doing anything and a confusing inconsistency in the terminology used by each of the formerly independent units.  If the integration is to reap its intended benefits, the teams need to quickly reconcile their terminology and integrate/rationalize their systems.  These common definitions include terminology, concepts, policies, and processes.

### Problem Example

GKDMR Travel recently created a partnership with another holiday company that wanted to advertise GKDMR Travel's holidays in its brochure.  This broadened the potential audience for GKDMR Travel's holidays but meant it needed to use the interfaces provided by its business partner.  Although both organizations are in the travel industry, there are considerable differences in the terminology that each used to describe its customers and services.

### Forces

- The most confusion caused when two different sources of models are brought together is when the same term is used in each, but it has a different meaning.
- Often the level of granularity and the style of modeling can be different when two models from different sources are compared.  This means mapping directly between the models is hard.

### Solution Description

Create a common information model that maps existing terminology and definitions to a set of definitions that represents a canonical view of the subject area.

Models created by different groups of people tend to use different terminology, levels of granularity, and patterns within the structures.  As such, mapping between them directly is often very difficult.  The unifying context common information model uses a semantic model to act as a lingua franca to show how the concepts in two models relate to one another.  Each of the linking model concepts from the semantic model has a dotted line relationship to each of the elements in the models being mapped that has the same meaning.  Some of the concepts in the semantic model may only be present in one model, or appear in multiple places in the models.  Not only does this modeling effort create understanding of how two models relate, but it also shows where there are gaps, duplication, and discrepancies in either model.

### Solution Example

GKDMR Travel and its business partner agreed to base the canonical definition on the terminology used by the OpenTravel Alliance.  This organization provides standardized XML messages for exchanging information between organizations working in the travel industry, so this seemed a reasonable starting point.  The team extracted all the key concepts from the OpenTravel standard message sets and modeled its key attributes and relationships.  These models were verified with the business partner.  Then each organization mapped its messages to the OpenTravel messages — for example the business partner's *Profile*, the OpenTravel Alliance's *Traveler* and GKDMR Travel's *Holiday Maker* are shown as the same concept.

The result was a clear definition of how the terminology and APIs defined by the business partner maps to GKDMR Travel's definitions.  With this initial mapping in place, it is then possible to verify that the valid values for the equivalent terms are compatible, and to reveal where there are missing concepts in GKDMR Travel's common information model.

### Benefits

- The unifying context common information model provides an important communication vehicle when two teams are trying to work together for the first time.
- It highlights areas where mapping and normalization would be required and where mediations and transformations will need to be implemented.

### Liabilities

- If either model is changing, then the mapping needs constant maintenance.
- The mapping model may need to include semantic relationships, such as when generalizations and specializations of a particular concept of the models being mapped are at different levels of granularity.
- Although this pattern helps in understanding, it does not in itself address the structural and value-based issues that may need to be resolved at the logical and physical models.

### Usage

In a service-oriented architecture implementation, this style of common information model can be used to show the relationship between a canonical message format and the application-specific message formats used by each of the service providers and service requestors.

For organizations involved in mergers and acquisitions, this style of common information model can be used to show the relationships between terminology, processes, and systems from each of the original organizations.

### Search Keywords

- Common Information Model
- Unifying Context
- Canonical Model
- Mergers and Acquisitions
- Semantic Mapping

### Version Identifier

1.0

### Status

ACTIVE

____

**Linking the Patterns**

Chapter 3 states that the four remaining patterns "are specializations of the common information
model pattern.  Each supports a different purpose and style of usage for the common information
model."  These are captured with `Link Specialized Design Patterns`.

The cross-references in each pattern's *Related Patterns* section are captured with
`Link Related Design Patterns`.

____

## Link Specialized Design Patterns
> Nest specialized design patterns.

### General Design Pattern

DesignPattern::Common Information Model

### Specialized Design Pattern

DesignPattern::Concept Beads

### Label

Specialization

### Description

Concept Beads supports simple, fine-grained models of core concepts.  Suitable for an organization that needs to quickly assemble simple applications that would benefit from consistency in implementation since they use many common concepts.

____

## Link Specialized Design Patterns
> Nest specialized design patterns.

### General Design Pattern

DesignPattern::Common Information Model

### Specialized Design Pattern

DesignPattern::Continuous Fabric

### Label

Specialization

### Description

Continuous Fabric supports an organization where there is high value in understanding the relationships between people, assets, events, and activities; this provides a blueprint for how the landscape of information links together.

____

## Link Specialized Design Patterns
> Nest specialized design patterns.

### General Design Pattern

DesignPattern::Common Information Model

### Specialized Design Pattern

DesignPattern::Encapsulated Views

### Label

Specialization

### Description

Encapsulated Views supports an organization that wants to develop common interfaces to information irrespective of how or where the information is stored.  This style is called information virtualization and is a common approach in service-oriented architectures.

____

## Link Specialized Design Patterns
> Nest specialized design patterns.

### General Design Pattern

DesignPattern::Common Information Model

### Specialized Design Pattern

DesignPattern::Unifying Context

### Label

Specialization

### Description

Unifying Context is for an organization that has historically operated as multiple independent units and wants to become more consistent and integrated in its use of information.

____

## Link Related Design Patterns
> Link related design patterns.

### Design Pattern 1

DesignPattern::Concept Beads

### Design Pattern 2

DesignPattern::Continuous Fabric

### Label

Starting Point

### Description

The concept beads pattern provides a starting point for creating a continuous fabric model because it contains the core entities that will make up the model.  Conversely, if the relationships between concepts are important, and benefit exists in having consistency in how they are represented, then consider the continuous fabric pattern in preference to concept beads.

____

## Link Related Design Patterns
> Link related design patterns.

### Design Pattern 1

DesignPattern::Concept Beads

### Design Pattern 2

DesignPattern::Encapsulated Views

### Label

Starting Point

### Description

The concept beads pattern provides an excellent starting point for encapsulated views.  Conversely, if the relationships between concepts are important, and benefit exists in having consistency in how they are represented, then consider the encapsulated views pattern in preference to concept beads.

____

## Link Related Design Patterns
> Link related design patterns.

### Design Pattern 1

DesignPattern::Continuous Fabric

### Design Pattern 2

DesignPattern::Encapsulated Views

### Label

Decomposition

### Description

A continuous fabric model can become large and requires considerable effort to learn.  The encapsulated views pattern is an approach that breaks up the model into smaller pieces, primarily for use as parameters (message structures) in information service definitions.  However, it can also be used to break up a large continuous fabric model into subject areas.

____

## Link Related Design Patterns
> Link related design patterns.

### Design Pattern 1

DesignPattern::Unifying Context

### Design Pattern 2

DesignPattern::Concept Beads

### Label

Canonical Basis

### Description

The concept beads pattern provides a good basis for the canonical form of a unifying context model.

____

## Link Related Design Patterns
> Link related design patterns.

### Design Pattern 1

DesignPattern::Unifying Context

### Design Pattern 2

DesignPattern::Continuous Fabric

### Label

Canonical Basis

### Description

The continuous fabric pattern provides a good basis for the canonical form of a unifying context model.

____
