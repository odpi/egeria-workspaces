<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**Solutions for Information Management**

Dr.Egeria commands for the design patterns in Chapter 9, "Solutions for Information Management", of *Patterns of
Information Management* by Mandy Chessell and Harald C. Smith (IBM Press, 2013).
The book sets each pattern's identifier in small capitals; those small-capital names are used
here as the display names, and as the reference names in [poim-pattern-links.md](poim-pattern-links.md).

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Solution

### Qualified Name

DesignPattern::Information Solution

### Category

Information Solution Patterns

### Description

Create a project, or series of projects, to transform the way the information is managed by the organization's people and information systems.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

An organization recognizes there is a missing capability, or a major issue with the way it manages an aspect of its information.

The organization wants to invest in a solution to find a reliable and repeatable resolution to this issue.

### Problem Example

In MCHS Trading, order records are created in the order-taking applications (E-Shop, MailShop, and Stores) and passed to the Shipping application. The Shipping application controls the dispatch of goods. When all of the goods on the order are sent to the customer, a copy of the order record is sent to the Invoicing application. The Invoicing application maintains the accounts and controls the process for invoicing the customer and collecting the payment. This is shown in Figure 9.2.

Although this arrangement works—customers and the stores can order goods, they are delivered, and payment is received, MCHS Trading realizes its existing order-processing systems are not delivering the customer-centric service it wants to offer. It requires a consolidated view of its customers, the channels they use, the types of products they buy, and the results of the purchases (both good and bad).

### Forces

- The effects of changes are often widespread—Changes to information systems tend to affect the procedures that people use around them.
- Information is duplicated and inconsistent—Information that is duplicated across multiple systems is often stored in different formats with different validation rules and currency.
- Ownership without responsibility—It is not uncommon to find that parts of an organization feel they own a particular type of information but they are unwilling to invest in an organizationwide solution.

### Solution Description

Create a project, or series of projects, to transform the way the information is managed by the organization's people and information systems.

Information solutions typically go through the three high-level phases shown in Figure 9.3. First is the Solution Outline phase. This may involve protracted discussions internally, and with software and services vendors. Often prototypes or proof of concept projects are run to understand any new technology or change in information-processing approach.

When the go-ahead is given, the organization moves into the Solution Release phase. Development teams use a variety of methods during this phase. However, they need to accomplish five major activities:

- Analysis of affected systems and the information they use. This analysis feeds the design process and is a key activity to ensure the new solution will integrate successfully with the existing systems.
- Design of the information solution.
- Configuration, coding, and testing of the new capability.
- Deployment of the new capability into the production environment.
- Operations handover. These activities are, of course, coordinated using project management techniques. Once the new capability is developed and tested, it moves to the Solution Operation phase. An information solution will have changed the way information is managed going forward. Often, as the organization is using the information, there is an ability to monitor and improve the information it is using through information governance and stewardship processes. The success of the information solution will hopefully lead to further investment in additional information solutions. This is summarized in Figure 9.4. The specialized information solution patterns cover more detail of the types of capability that are often created by an information solution.

### Solution Example

MCHS Trading implements a series of information solutions to improve its management of information. This includes the following:

- Centralized Master for product details
- Synchronized Masters for customer details
- Managed Archive for completed order details
- Performance Reporting for monitoring the performance of the organization Refer to these patterns to understand the work that MCHS Trading needed to do for each of these solutions.

### Benefits

- Implementing information solutions will change the IT infrastructure to improve the management of information.

### Liabilities

- In general, the information needs of an organization are relatively stable and this investment can deliver value for many years. However, recent developments are opening up new sources of information through social media and real-world sensors. An organization should continually look for new opportunities to augment this information with new insight.

### Usage

The enterprise architecture team initiates most information solutions because they describe holistic solutions to information management issues that affect multiple parts of the organization.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

New Information Node

### Qualified Name

DesignPattern::New Information Node

### Category

Information Solution Patterns

### Description

Initialize, protect, and synchronize the new information node's information collections.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to deploy a new information node.

### Problem Statement

What are the information implications of deploying a new information node and how should the organization handle them?

The new information node may be supporting a new business, or improving an existing business, or be required to comply with a new regulation, or be part of an information supply chain's mechanism that keeps the organization's information synchronized. Whatever the reason, once it is up and running, the information node becomes important to the success of the organization. How should it be set up to become an integrated part of the business?

### Problem Example

MCHS Trading wants to replace its old Mail-Shop application with a new application called M-Shop. How should M-Shop be provisioned with information?

### Forces

- Operational criticality—For new information nodes supporting critical operational processes, the new information node and other existing information nodes may require parallel operation to ensure the new information node performs as expected.
- Initial load—A new information node has empty information collections. Unless this is a brand-new business, the organization needs to load the new information node with details of the relevant information assets.
- Ongoing synchronization—The information collections within the new information node will need to be synchronized with the other information collections used by the organization.
- Ensuring quality—New information nodes need to be evaluated for information quality from the point when they are initially loaded and on an ongoing basis to ensure they meet the expectations of all consumers of the information.
- Tracking performance—The new information node must be monitored to ensure adequate performance against data volumes, delivery times, and other key measurements.
- Limiting access—The new information node needs to be secured and only provide access to authorized people and information processes.
- Surviving disaster—An information node (even a new one) can fail. This could be caused by a hardware failure, software bug, operator error, or malicious attack. The result might be a failure of a single operation, the loss of a business transaction, the loss of the information node for a period of time, or the permanent loss of the system and/ or location where it was sited. How does the organization continue after this has happened?

### Solution Description

Initialize, evaluate, protect, and synchronize the new information node's information collections.

When the information collections are located in the same information node as the information processes that are using them, it is called Local Provisioning. These information collections may need to be initialized with existing information. This is called the initial load.

Once the initial load is completed and evaluated for appropriate quality, the information node is ready for new work (though in operational systems, it may operate in parallel to other existing information nodes for a period of time to ensure it functions as expected). However, if it remains disconnected from the rest of the organization, its local information will become inconsistent with other information nodes. It needs to be connected to the organization's Information Supply Chains.

Many of the other types of provisioning around an information node that connect it to the information supply chains are shown in Figure 9.5. The numbers on the diagram refer to these notes:

1. New information can be fed into the information node using Mirroring Provisioning, Peer Provisioning, or Snapshot Provisioning (not shown above, though commonly used when a new information node will run in parallel with an existing information node for an initial period of time).
2. When new information is passed into the information node, peer provisioning replicates it to other connected information nodes.
3. Information can be supplied or retrieved using Service Oriented Provisioning.
4. New information can be distributed to other information nodes using mirroring provisioning.
5. Alerts for unusual situations can be distributed using Event-Based Provisioning.
6. Recovery Provisioning should be provided for every information collection that cannot be re-created from other methods.

### Solution Example

The M-Shop application uses Agile Business Processes to support the creation of new orders. It needs customer details and product details to create the order and the order needs to be stored somewhere. The team decides that M-Shop should:

- Call the information services of Customer Hub to retrieve customer details.
- Have a read-only local version of the product details.
- Have a local information collection for storing orders. M-Shop needs to join two information supply chains: It needs to receive changes to product details from the product information supply chain and to feed new orders into the order details information supply chain. M-Shop needs Recovery Provisioning of its user registry and configuration. If the M-Shop information node was completely destroyed, it would be reinstalled on new hardware and the information collections reloaded as if it were newly commissioned. Any partial orders not published from M-Shop would be lost but that is a risk that MCHS Trading is prepared to take. They plan to advise customers to use E-Shop while M-Shop is unavailable, or to try again later.

### Benefits

- A new information node becomes an integrated part of the organization's operation with information that is consistent with the other information nodes.

### Liabilities

- A number of additional teams may need to be involved in the commissioning of the new information node to coordinate the integration of it into the information supply chains. There may need to be changes to the information processes that implement the information supply changes to accommodate the new information node.

### Usage

New information nodes are commissioned all of the time in a vibrant organization. In many cases, the team will use information from an existing information node for the initial load. If the new information node is critical to the organization's operation, it will be backed up and have some disaster recover contingency. If the organization is focused on synchronizing the type of information that the new information node has stored locally, then it will connect it to its information supply chains.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Node Upgrade

### Qualified Name

DesignPattern::Information Node Upgrade

### Category

Information Solution Patterns

### Description

Migrate, refresh, and reconnect the information from the existing information node to the new one.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is upgrading or consolidating one or more information nodes.

### Problem Statement

When an information node is upgraded, how will the new information node reflect the processing that has occurred in the past when the existing information node is decommissioned?

Most information nodes host information collections. When an information node is decommissioned, the information in its local information collections is lost. Does this matter or should the organization do something to preserve the information?

### Problem Example

When MCHS Trading launched its new loyalty card, it needed to migrate all of the existing Stores cardholders to the new loyalty program.

### Forces

- Existing dependencies—There may be information processes in other information nodes that are dependent on the existing information node's information services and the information collections behind them.
- Limited capacity to support parallel information nodes—There may be limits on whether the organization can run two parallel environments simultaneously.
- New user interfaces and terminology—The new version of the information node will have new capability and some of the existing capability will have changed. This will be reflected in the user interfaces and user messages that are produced.
- New information structures and relationships—The new version of the information node will probably have new implementations of the information collections that have the information formatted differently from the existing information collections. These new collections may have different relationships or dependencies across information elements.
- Private information collections—Information processes may have many of the integrity rules and interpretation logic for their information collections hard-coded in their logic so it is difficult for new information processes to interpret the contents of the information collections through its information services.
- Legal or other obligations—Obligations to maintain information for a specified period of time may require that the information collection from the old information node be saved and available in a specific state.
- Obsolete information—If an information node is no longer used for everyday business, its information becomes out of date or stale.

### Solution Description

Migrate, refresh, and reconnect the information from the existing information node to the new one.

To prepare the new version for operation, extract a copy of the information from the existing information node, reengineer it to the requirements of the new information node, and store it in the upgraded information node. Repeat the process with any changes made to the information in the existing information node until the new information node starts processing work.

If the new information node is to be run in parallel with the old information node, both should be set up to process the same work and the information in their information collections should remain logically consistent. Checks should be made to ensure it is the case.

When it is time for the old information node to discontinue operation, the provisioning of downstream information supply chains will be swapped over to the upgraded information node.

Note: If the existing information node has failed and there are no plans to put it into production, use Recovery Provisioning to load the latest information it processed and transfer it to the new information node.

### Solution Example

The existing store card scheme is managed by the Stores application. The information around the loyalty card scheme will be maintained in the Customer Hub. The first step in migrating over is to use Mirroring Provisioning from Stores to the Customer Hub to ensure information about all customers with a store card are represented in the Customer Hub and are allocated a new loyalty card. The new loyalty cards are sent out to the store card customers. There is a period of a couple of months where they may use either card. Any usage of the store cards—or updates to them—is mirrored to the Customer Hub. Usage of the loyalty cards is fed directly to the Customer Hub. When the store cards become obsolete, the information processes in Stores are decommissioned and the mirroring stops.

### Benefits

- Migrating information from an obsolete information node to one that will be actively involved in the organization's operations enables the complete shutdown and decommissioning of the obsolete information node. Using this approach enables the new information node to be prepared in advance of the shutdown of the old information node so the cutover time is as short as possible.

### Liabilities

- All information users of the obsolete information node will need to be trained on how to use the new information processes supported by the new information node.

### Usage

This pattern is implemented in three circumstances:

- Application migration—When the capability of one application is replaced by a new application. This may be a later version of the application or a completely different application.
- Application consolidation—When multiple deployments of an application are consolidated into one instance of the application.
- Middleware upgrade—When middleware software, such as an Information Broker or Information Asset Hub, is upgraded to a newer version.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Distributed Activity Status

### Qualified Name

DesignPattern::Distributed Activity Status

### Category

Information Solution Patterns

### Description

Create an information collection to manage the status that is fed by each of the information processes involved in the business activity.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

An organization needs to understand the status of a business activity that spans multiple information processes distributed among a variety of information nodes.

### Problem Example

MCHS Trading needs to store information about the state of the orders it has taken from its customers in order to resolve queries about them and to monitor efficiency.

### Forces

- No fixed order of execution—The order that events occur may vary when processing is distributed, particularly when different parts of an activity can run in parallel.
- An information process may fail—An information process that is part of a distributed activity may fail partway through before it has initiated other parts of the activity. The effect is that the distributed activity stalls until someone notices and restarts the appropriate information process.

### Solution Description

Create an information collection to manage the status that is fed by each of the information processes involved in the business activity.

Managing distributed activity status requires each information process that is involved in the business activity to generate and send events to a common information node. This information node uses the information events to piece together the current status of the activity.

There are three possible types of information node that could be used to determine the distributed status:

- An Information Activity Hub would use a state machine to track the status of the activity.
- If the event relationships are complex, it may be necessary to use an Event Correlation Node rather than an Information Activity Hub.
- If the events are arriving very rapidly, it may be necessary to use a Streaming Analytics Node in place of the information activity hub.

### Solution Example

MCHS Trading creates a new information node called Order-Tracking, which is an Information Activity Hub. This has an information collection that records the order status. The order-processing information processes use the information services provided by Order-Tracking to record the work they are doing to process an order.

Figure 9.6 shows the calls into Order-Tracking as orders are processed. New orders from E-Shop, Stores, and Mail-Shop are passed to Order-Tracking. It synchronizes the customer details with the Customer Hub before passing the request on to the Shipping application. Shipping sends the goods on to the customer and, once the order is complete, sends the request on to Invoicing. When the status of the order changes in either Shipping or Invoicing, these applications call Order-Tracking to record the latest status.

Once the Order-Tracking information node is in place, it is possible to support new information processes such as Cancel Order, which is located in the Customer-Care information node. See Figure 9.7.

### Benefits

- This solution enables an organization to track the status of a distributed activity to understand the current status, determine how long each step has taken, and detect that an activity has stalled, has failed partway through, is behaving in an unexpected way, or is just taking too long.

### Liabilities

- The definition of the state machine needs to be changed in line with changes in the participating information nodes because it may need to handle different events or a different sequence of events.

### Usage

Status tracking using state machines is a common approach to understand a distributed activity that is being coordinated with messages—for example, in an Enterprise Application Integration (EAI) approach.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Semantic Integration

### Qualified Name

DesignPattern::Semantic Integration

### Category

Information Solution Patterns

### Description

Create an ontology model to describe the question subject area and map it to the information collections using information services. Use the ontology to identify the information required to answer the questions.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

An organization needs to ask questions at multiple levels of abstraction about information located in a variety of information collections.

They need the ability to make ad hoc queries using keywords from the problem domain and have them translated into queries on the distributed information.

### Problem Example

MCHS Trading has many physical sites. These are the physical stores, warehouses, and distribution centers. Table 9.4 summarizes the United Kingdom operation. Headquarters Warehouses Distribution Centers Stores Milton Keynes Birmingham Aberdeen Aberdeen Edinburgh Bristol Bath Reading Glasgow Cambridge

The sites vary in size and each site will have appropriate types of facilities depending on their use. Most sites operate reasonably autonomously with local IT systems supporting their work. There is a small team at headquarters that is responsible for the management of these sites. How does this team manage the information it needs about these physical sites? Examples of their information requirements include questions such as which sites are close to one another, or could share facilities, or provide back up if something fails?

### Forces

- Information is stored for a particular purpose—This purpose provides a specialized context for the information that is typically reflected in the information services that surround it.
- Information about the same subject area may be distributed—The information services around each specific information collection may not be consistent with one another because they are probably targeted for different groups of information processes.
- Distributed information may be inconsistent—This makes it hard to match values from different information collections.

### Solution Description

Create an ontology model to describe the question subject area and map it to the information collections using information services. Use the ontology to identify the information required to answer the questions.

An ontology model is a description of the concepts in a subject area, the relationships between these concepts, and links to instances of the concepts. The ontology includes "composed-of" relationships and "is-a" relationships, plus concepts can have attributes associated with them.

At the leaf nodes of the ontology model are the instances—the actual information. These can be

- Literal values, enabling the ontology to include information not stored elsewhere.
- Information values copied from existing Information Collections. These need to be kept synchronized with the changing information values in the original information collections.
- Information Links to individual Information Entries in existing information collections. The information values are extracted in real time when the ontology instance is accessed. The links must be kept up to date as information entries are added and removed.
- A query to dynamically retrieve the information values from the existing information collections when the ontology instance is accessed. The information values are needed in the ontology model to enable inferencing to take place. That is, the navigation of the ontology model to locate instances that match a complex query. The approach on how these values are supplied depends on the volume and volatility of the information values in the organization's other information collections. Figure 9.8 illustrates this solution.

### Solution Example

MCHS Trading creates an ontology model that describes the physical sites, where they are located, the facilities they contain, and the different government agencies and business partners engaged for different regions and aspects of their operation.

With this ontology, MCHS Trading is able to ask questions such as:

- Which of our physical sites do the South East England Health and Safety Authority regulate and what type of site are they?
- Which of our Scottish sites have a backup generator? The ontology locates the instances of interest and then queries are made on the other information collections to drill into more detail.

### Benefits

- This approach provides a rich and flexible query interface to distributed information. It is effectively adding relationships between disparate information collections based in knowledge of the subject area.

### Liabilities

- This solution does not fix incorrect and incomplete information values. It is just linking them together.
- Ontology models can quickly become incomprehensible. The successful ones are very targeted to a single subject area.
- The semantic layer must be kept synchronized with the information collections it is federating together. This task grows as more information values are copied into the ontology to enrich the query capability.

### Usage

This approach to integration is experimental. There are a small number of implementations in progress that are showing good results over small ontology models. The w3 standards, Web Ontology Language (OWL)1 and Resource Description Framework (RDF),2 are the most common languages used for specifying the ontology model. Queries are expressed in the Sparql query language.3 Open Services for Lifecycle and Collaboration (OSLC)4 links are often used to implement information links in the ontology instance when OWL/RDF are in use because OSLC provides a URL reference for the information entry it refers to, plus operations to extract the values from the information entry.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Partner Collaboration

### Qualified Name

DesignPattern::Partner Collaboration

### Category

Information Solution Patterns

### Description

Set up a managed gateway between the two organizations where information can be exchanged in a controlled manner.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

1. http://www.w3.org/TR/owl-features/
2. http://www.w3.org/TR/rdf-primer/
3. http://www.w3.org/TR/rdf-sparql-query/
4. http://open-services.net/resources/tutorials/oslc-primer/what-is-oslc/

### Problem Statement

An organization wants to collaborate electronically with a business partner.

### Problem Example

MCHS Trading wants to be able to improve the exchange of product details and orders with its suppliers. Simply introducing electronic Information Flows between MCHS Trading and its suppliers does little to improve its existing manual solution—mostly a reduction in transportation cost—as the Information Flows retain the same point-to-point characteristic.

### Forces

- Different organizations are often independent legal entities—They have a duty to protect their own organization's assets and to report on their activities.
- Competition law—In many countries, competition law requires large organizations that are dominant in their sector to ensure that they deal fairly with business partners.

### Solution Description

Set up a managed gateway between the two organizations where information can be exchanged in a controlled manner.

This type of gateway is a specialized type of Information Broker that supports Electronic Data Interchange (EDI).

### Solution Example

MCHS Trading sets up a gateway information node called Supplier-net that is responsible for managing orders with the suppliers and introducing product details into the product information supply chain. The first focal area for MCHS Trading is collaboration in Order Management, Invoice Reconciliation, and Payment Processing, where each specific set of information is delivered as an Information Payload. The sets of information in each payload are defined by Information Codes.

See the "Connecting MCHS Trading into a B2B Trading Partnership" section in Chapter 2 for more discussion of this solution.

### Benefits

- Business partners can collaborate as effectively as internal parts of a single organization.

### Liabilities

- The organizations that are collaborating must maintain clear definitions of the information that is to be exchanged, under which conditions and with what security, and the level of service each guarantees to the other.

### Usage

This type of solution is used in many manufacturing and distribution companies where delivering good customer service in a cost-effective manner requires all organizations in the physical supply chain to coordinate their activities. Partner collaboration can incorporate many aspects of interaction, including purchase orders, invoices, inventory levels, shipment tracking, and payments.

Interaction with such Electronic Data Interchange (EDI) systems is often handled by enterprise resource planning (ERP) software, an example of a Packaged Application Process. The EDI information broker most commonly sends and delivers messages that define the type of content.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Shared Master

### Qualified Name

DesignPattern::Shared Master

### Category

Information Solution Patterns

### Description

Create a single master collection of the information and use information services in each information node to connect to this information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information. It is focused on the management of shared information—in particular, its Information Assets. It believes it needs Master Data Management (MDM) but are not sure how to use it.

### Problem Statement

Information processes distributed across a number of information nodes need access to the same up-to-date information.

### Problem Example

MCHS Trading needs a consolidated view of its customers' details for operational use. At the moment, customer details are stored in E-Shop (for customers who use the Internet shopping service), Stores (for customers who have a Store card), and they are entered into each order in Mail-Shop. There is a consolidated list of customers in the Reporting Hub, but that information node is not suitable for an operational load.

MCHS Trading decides to introduce an Information Asset Hub called Customer Hub to host the consolidated customer details information collection. How should the Customer Hub integrate with the other information nodes?

### Forces

- Repetitive work—Even with the best will in the world, people are not good at making the same edits to multiple copies of information.
- Remote access to information adds latency to an information service—An information request takes a finite amount of time to execute.
- Copied data needs to be synchronized—Mirroring information that is changing rapidly can create a lot of network traffic and it may be that the copies never truly reflect the most up-to-date values.
- Many information nodes are implemented with local information collections— Changing this to enable the information node to use remote information services would require extensive alteration to the information node and could be very expensive.
- Information is duplicated and inconsistent—Information assets are central to the organization's business, which means they appear in many information nodes. Each information node typically uses it own Information Key scheme and there is little attempt to keep the information about the information assets. The result is duplicated and inconsistent information that is hard to correlate.

### Solution Description

Create a single master collection of the information and use information services in each information node to connect to this information collection.

Create a Master Usage information collection and use information services in each information node to connect to this information collection.

Provide information services for the information collection to enable information processes to access it, irrespective of the information node they are located in. This is shown in Figure 9.9.

The shared master information node hosts an information collection with Master Usage, Complete Coverage, and Complete Scope. As a result, it supports all of the information needed by the information process for a particular subject area. The information services that provide access to this information collection present appropriate views of the information to the consuming information processes.

### Solution Example

If MCHS Trading used this approach to support its customer details, each of the order-taking information nodes would have to be changed so that they extracted their customer information from Customer Hub, rather than having their customer details stored locally. This would affect the majority of the information processes on these information nodes, which is why this would be an expensive solution to implement.

### Benefits

- This approach results in a single copy of the information—which is efficient in terms of storage and effort to maintain.
- With a single copy, it is simple to expand the attributes stored and hence expand the information processes that can be supported.

### Liabilities

- A shared master can easily become a single point of failure that affects many parts of the organization's operations if it is unavailable.
- Often this solution is not possible because existing information nodes hold this information already and it would be too expensive to change them to use the shared master.
- When the shared master is introduced, it often needs to be loaded with an initial set of values. The source of these initial values and the work that will be needed to clean and transform these values needs to be included in the project plan.

### Usage

This approach is used when an organization is adding support for a new type of information or is focused only on a small subset of the organization's information processes.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Centralized Master

### Qualified Name

DesignPattern::Centralized Master

### Category

Information Solution Patterns

### Description

Centralize all updates to a single master copy of the information. Distribute these information values to other information nodes to use as local reference (read-only) copies.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information. It is focused on the management of shared information—in particular, its Information Assets. It believes it needs Master Data Management (MDM) but are not sure how to use it.

### Problem Statement

The same updates need to be manually entered into multiple information processes to maintain consistency between the multiple copies of the same information.

### Problem Example

MCHS Trading needs a consolidated view of its customers' details for operational use. At the moment, customer details are stored in E-Shop (for customers who use the Internet shopping service), Stores (for customers who have a Store card), and they are entered into each order in Mail-Shop. There is a consolidated list of customers in the Reporting Hub, but that information node is not suitable for an operational load.

MCHS Trading decides to introduce an Information Asset Hub called Customer Hub to host the consolidated customer details information collection. How should the Customer Hub integrate with the other information nodes?

### Forces

- Repetitive work—Even with the best will in the world, people are not good at making the same edits to multiple copies of information.
- Storage costs money—Every copy that is made of information costs money to store and maintain. An information collection may be too large to make it cost effective to make copies of it.
- Inconsistent copies—Different copies of the same information located in different information nodes are typically inconsistent unless they are actively synchronized.
- Copied data needs to be synchronized—Mirroring information that is changing rapidly can create a lot of network traffic and it may be that the copies never truly reflect the most up-to-date values.
- Remote access to information adds latency to an information service—An information request takes a finite amount of time to execute. Collating and reformatting the same piece of information on the fly, over and over again, is inefficient.
- Many information nodes are implemented with local information collections— Changing this to enable the information node to use remote information services would require extensive alteration to the information node and could be very expensive.
- Information is duplicated and inconsistent—Information assets are central to the organization's business, which means they appear in many information nodes. Each information node typically uses it own Information Key scheme and there is little attempt to keep the information about the information assets. The result is duplicated and inconsistent information that is hard to correlate.

### Solution Description

Centralize all updates to a single master copy of the information. Distribute these information values to other information nodes to use as local reference (read-only) copies.

This is shown in Figure 9.10. The numbers on the diagram refer to these notes:

1. Nominate or create an information node to host the information collection that will be used to assemble, maintain, and coordinate the synchronization of the values for this type of information. This information collection will have Master Usage, Complete Scope, and Complete Coverage to be sure to support all destination systems.
2. When updated information is ready, distribute it to other information nodes using Mirroring Provisioning. These destination information nodes store this information and use it as local reference (read-only) copies.
3. The centralized master can be made available for update to other information processes through Service Oriented Provisioning.

### Solution Example

This approach would enable the order-taking information nodes to retain their local information collections for customer details where the information process only needed read access to the information. Information processes that created or updated customer information (such as the New Order process) would need to be modified to call the information services on the Customer Hub.

This pattern is the approach used for product details. Product Hub is their centralized master.

### Benefits

- People are only involved in the maintenance of one copy of the information, which is then automatically duplicated to the other information collection copies. This reduces cost and opportunities for human error.

### Liabilities

- The master information collection must have Complete Scope and Complete Coverage if it is to serve all of the other information collections.

### Usage

The centralized master approach is often used for product information management and maintaining employee details. It is often difficult to use this approach for customer details because updates come in through many channels, resulting in multiple information collections with master usage.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Registry

### Qualified Name

DesignPattern::Information Registry

### Category

Information Solution Patterns

### Description

Create a centralized information registry to combine the best of the core values from all of the information collections on demand.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information. It is focused on the management of shared information—in particular, its Information Assets. It believes it needs Master Data Management (MDM) but are not sure how to use it.

### Problem Statement

An organization needs a consolidated list of the unique information instances for a subject area, despite the fact that this information is distributed and duplicated across many information collections.

### Problem Example

MCHS Trading needs a consolidated view of its customers' details for operational use. At the moment, customer details are stored in E-Shop (for customers who use the Internet shopping service), Stores (for customers who have a Store card), and they are entered into each order in Mail-Shop. There is a consolidated list of customers in the Reporting Hub, but that information node is not suitable for an operational load.

MCHS Trading decides to introduce an Information Asset Hub called Customer Hub to host the consolidated customer details information collection. How should the Customer Hub integrate with the other information nodes?

### Forces

- Storage costs money—Every copy that is made of information costs money to store and maintain. An information collection may be too large to make it cost effective to make copies of it.
- Inconsistent copies—Different copies of the same information located in different information nodes are typically inconsistent unless they are actively synchronized.
- Copied data needs to be synchronized—Mirroring information that is changing rapidly can create a lot of network traffic and it may be that the copies never truly reflect the most up-to-date values.
- Remote access to information adds latency to an information service—An information request takes a finite amount of time to execute. Collating and reformatting the same piece of information on the fly, over and over again, is inefficient.
- Many information nodes are implemented with local information collections— Changing this to enable the information node to use remote information services would require extensive alteration to the information node and could be very expensive.
- Information is duplicated and inconsistent—Information assets are central to the organization's business, which means they appear in many information nodes. Each information node typically uses it own Information Key scheme and there is little attempt to keep the information about the information assets. The result is duplicated and inconsistent information that is hard to correlate.

### Solution Description

Create a centralized information registry to combine the best of the core values from all of the information collections on demand.

When the information service for the registry is called, it dynamically matches the values from the different sources to return the unique instances. Figure 9.11 illustrates how the information registry works. The numbers on the diagram refer to these notes:

1. A supply of information about the subject area it is covering. This comes from selected information nodes that host information collections for the subject area. For each relevant information collection, the hosting information node sends the Core Coverage attributes for all of the information entries it stores using Mirroring Provisioning.
2. An Information Asset Hub to host the information registry. This has one or more information collections to host the information coming from the source information nodes.
3. An Information Matching Process to combine the values from related information entries that originate from the different source information collections.
4. Information Services enable information processes to request the results of the information matching process. To the calling information processes, the information registry appears to be hosting an Information Collection for the subject area with Complete Scope and Core Coverage that supports the Reference Usage role.

### Solution Example

MCHS Trading implements an information registry for its customer details as a first step to having a consolidated master copy of its customer details. This information registry was used to identify how many individual customers it has and the channels each uses.

However, ultimately MCHS Trading wants to be able to manage customer details in a centralized manner and so it moves to the Synchronized Master solution.

### Benefits

- The information registry is able to create a read-only information collection with complete scope and core coverage, with very little disruption to the original source systems.

### Liabilities

- The information registry creates the combined view of an information entry on demand. If an information entry is requested many times, it may be more efficient to use the Golden Reference pattern, which creates the combined view once and stores it. The information registry typically stores only the Core Coverage attributes because they are all that is necessary to do the matching. It is possible to extend the coverage of the attributes that the information registry holds. This creates a richer set of information that can be returned on the registry's information services, but may increase the synchronization traffic between the source systems and in the information registry.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Golden Reference

### Qualified Name

DesignPattern::Golden Reference

### Category

Information Solution Patterns

### Description

Create an information collection for this information that has Complete Scope and Complete Coverage. Distribute and combine relevant information from the existing information collections into this new information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information. It is focused on the management of shared information—in particular, its Information Assets. It believes it needs Master Data Management (MDM) but are not sure how to use it.

### Problem Statement

An organization needs a complete, read-only view of the information it stores about a subject area.

Unfortunately, this information is distributed and duplicated across a number of disconnected information nodes.

### Problem Example

MCHS Trading needs a consolidated view of its customers' details for operational use. At the moment, customer details are stored in E-Shop (for customers who use the Internet shopping service), Stores (for customers who have a Store card), and they are entered into each order in Mail-Shop. There is a consolidated list of customers in the Reporting Hub, but that information node is not suitable for an operational load.

MCHS Trading decides to introduce an Information Asset Hub called Customer Hub to host the consolidated customer details information collection. How should the Customer Hub integrate with the other information nodes?

### Forces

- Storage costs money—Every copy that is made of information costs money to store and maintain. An information collection may be too large to make it cost effective to make copies of it.
- Inconsistent copies—Different copies of the same information located in different information nodes are typically inconsistent unless they are actively synchronized.
- Copied data needs to be synchronized—Mirroring information that is changing rapidly can create a lot of network traffic and it may be that the copies never truly reflect the most up-to-date values.
- Remote access to information adds latency to an information service—An information request takes a finite amount of time to execute. Collating and reformatting the same piece of information on the fly, over and over again, is inefficient.
- Many information nodes are implemented with local information collections— Changing this to enable the information node to use remote information services would require extensive alteration to the information node and could be very expensive.
- Information is duplicated and inconsistent—Information assets are central to the organization's business, which means they appear in many information nodes. Each information node typically uses it own Information Key scheme and there is little attempt to keep the information about the information assets. The result is duplicated and inconsistent information that is hard to correlate.

### Solution Description

Create an information collection for this information that has Complete Scope and Complete Coverage. Distribute and combine relevant information from the existing information collections into this new information collection.

The resulting Golden Reference is primarily for Reference Usage; however, it may be Hybrid Usage enabling additional, new attributes to be stored in the golden reference and distributed to downstream information nodes. This is shown in Figure 9.12. Service Oriented Provisioning Mirroring Provisioning The numbers on the diagram refer to these notes:

1. All changes to the information collections in the source systems are sent to the golden reference.
2. The golden reference has an Information Matching Process that compares the incoming information with that information already stored.
3. If the matching is close but not good enough to automatically combine, it is sent with the close matches to a Clerical Review Process to enable an Information Steward to decide where to store the new information.
4. The golden reference offers information services to allow other information processes to read the consolidated information collection.
5. Attributes from the golden reference can be distributed to other information nodes for reference usage.

### Solution Example

MCHS Trading considers the following solution for its customer details. The information asset hub (called Customer Hub) has a reference information collection for customer details with complete scope and complete coverage. It is provisioned from E-Shop, Mail-Shop, and Stores, and it is used, in turn, to provision the Reporting Hub. The Customer Hub is also supporting Service Oriented Provisioning for another new application called Customer-Care. This application is reading customer details through web services. See Figure 9.13.

### Benefits

- This solution provides a single authoritative source of information that can be used as a reference and as a distribution point.

### Liabilities

- The golden reference introduces another copy of the information that takes storage and needs to be maintained. If changes are happening to the information at a faster rate than it is used through the services, then the Information Registry may be a better solution.

### Usage

This style of solution is often used to consolidate information for distribution.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Synchronized Masters

### Qualified Name

DesignPattern::Synchronized Masters

### Category

Information Solution Patterns

### Description

Monitor for changes in any of the master information collections and distribute to the other copies, taking particular care to handle incompatible simultaneous changes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information. It is focused on the management of shared information—in particular, its Information Assets. It believes it needs Master Data Management (MDM) but are not sure how to use it.

### Problem Statement

An organization needs to provide a remotely accessible complete master information collection for a subject area that is synchronized with other existing information collections that also have master usage.

An organization needs multiple master information collections for a subject area where any attribute may change at any time, in any copy.

### Problem Example

MCHS Trading needs a consolidated view of its customers' details for operational use. At the moment, customer details are stored in E-Shop (for customers who use the Internet shopping service), Stores (for customers who have a Store card), and they are entered into each order in Mail-Shop. There is a consolidated list of customers in the Reporting Hub, but that information node is not suitable for an operational load.

MCHS Trading decides to introduce an Information Asset Hub called Customer Hub to host the consolidated customer details information collection. How should the Customer Hub integrate with the other information nodes?

### Forces

- Inconsistent copies—Different copies of the same information located in different information nodes are typically inconsistent unless they are actively synchronized.
- Copied data needs to be synchronized—Mirroring information that is changing rapidly can create a lot of network traffic and it may be that the copies never truly reflect the most up-to-date values.
- Remote access to information adds latency to an information service—An information request takes a finite amount of time to execute. Collating and reformatting the same piece of information on the fly, over and over again, is inefficient.
- Many information nodes are implemented with local information collections— Changing this to enable the information node to use remote information services would require extensive alteration to the information node and could be very expensive.
- Information is duplicated and inconsistent—Information assets are central to the organization's business, which means they appear in many information nodes. Each information node typically uses it own Information Key scheme and there is little attempt to keep the information about the information assets. The result is duplicated and inconsistent information that is hard to correlate.

### Solution Description

Monitor for changes in any of the master information collections and distribute to the other copies, taking particular care to handle incompatible simultaneous changes.

This is shown in Figure 9.14. The numbers on the diagram refer to these notes:

1. Information from master usages information collections is exchanged with the synchronized master using peer provisioning.
2. New information entries, or updates to existing information entries, cause an Information Matching Process to run that checks for duplicate entries.
3. If duplicate entries are found, they may require a Clerical Review Process where an Information Steward can review and collapse similar information entries together.
4. The synchronized master may be queried and updated using Information Services.
5. Information from the synchronized master may be distributed to information nodes that are downstream in the information supply chain.

### Solution Example

This is the solution that MCHS Trading chose for its customer details. At the same time, it moved the store card to a loyalty card that covered all of its sales channels. Support for the loyalty card was implemented across Customer-Care and the Customer Hub. This meant that the Stores application no longer needed to store information about the customers. The resulting flow of information between the information nodes is shown in Figure 9.15.

### Benefits

- The synchronized master solution provides a consolidated master usage information collection with centralized maintenance. The other information nodes with a master usage information collection only need to synchronize with the hub, which can be configured to manage the matching, enriching, and correcting of the information.

### Liabilities

- The synchronization logic for this pattern is complex and may be different for creates, updates, and deletes due to the different scopes of each of the master usage information collections.
- The synchronized master may merge information entries if it detects duplicate information entries. This can be disruptive to other information nodes that may be storing information keys from the synchronized master. Because of this, the synchronized master should support the Stable Key pattern for information processes using its information services and Caller's Key for source information nodes. Destination information nodes typically use the Mirror Key pattern based of off the synchronized master's stable key. However, if the merging of information entries in the destination causes problems, multiple copies of the merged information entry should be sent, one for each of the resulting stable keys associated with the merged information entry.

### Usage

This is a common approach to implementing a transactional style MDM hub, where there are still other information nodes that must maintain their own master usage information collection.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Historical System of Record

### Qualified Name

DesignPattern::Historical System of Record

### Category

Information Solution Patterns

### Description

Extract information from the operational systems; consolidate it into information collections that maintain a history of how the values are changing over time. Reformat and distribute this information to decision makers.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information. It is focused on understanding how the organization is performing holistically.

### Problem Statement

An organization needs a complete view of its operations, both past and present.

Operational systems focus on the current state of the day-to-day detail. An overseer (manager, executive, auditor) needs to understand the aggregated results compared against different criteria (cost, profitability, popularity, and many more).

### Problem Example

MCHS Trading cares about how well its business is performing and how it is changing over time so it can plan changes and improvements. The key driver for the business is the orders made by customers. The operational systems focus on the detailed and effective management of these orders.

Once an order is complete, it is no longer of interest to the operational systems. However, it contains valuable information for running the business—but not in the same form that the operational systems need it.

For example, by the time the order is complete, it contains details of who the customer was, what the customer ordered, how the customer paid, which warehouse the goods came from, how many packages were shipped, how long it took to complete the order, which employees worked on the order, how long the goods were in the warehouse before the goods were shipped, any issues that occurred and how they were resolved, who the suppliers were, what the profitability of the order was, ... and much more.

Each element of information listed above is an indicator of how well the business is performing—but it needs to be aggregated with similar information from other orders. For example,

- The warehouse team needs to know, on average, how long goods are stored in the warehouse and how long it takes to fulfill the order. The team also needs to know what factors impact the team's effectiveness—is it time of year, weather, public holidays, suppliers, location of customer, location of warehouse, type of product, or mix of products in an order?
- The merchandising team needs to understand which products are selling well, which suppliers are reliable, and where the most profitable product lines are for each season.
- The managers of employees need to know who is performing the best.
- The accountants need to know where the revenue and costs originate. It is the same information but is it separated out and regrouped to satisfy the needs of each part of the business.

### Forces

- Usefulness of detailed information changes over time—Detailed information that is collected and used in the short term has decreasing value as time passes.
- Averages matter—Aggregated information gives a clear impression of the overall effectiveness of a part of the business.
- Outliers matter—Unusual events, the behavior of the few highly profitable customers, or an unusual transaction may well indicate a risk, opportunity, or start of a new trend. These outliers can be missed if you only use aggregated information.
- Information needs change over time—The world is constantly changing—in many ways, it is becoming more complex and sophisticated. The information used by the organization must evolve with the times.
- Organizations are complex—They have many different systems, activities, departments, and information collections. The detail is too much for any one person to comprehend.
- Trends matter—To understand how well you are doing, it is necessary to understand the current situation and how that compares with past performance.
- Operational systems maintain the current state of the business—How is the past represented?

### Solution Description

Extract information from the operational systems; consolidate it into information collections that maintain a history of how the values are changing over time. Reformat and distribute this information to decision makers.

The historical system of record solution consists of a number of specialized information nodes that are responsible for storing, managing, and transforming information. At the core is an information warehouse. This holds most of the information.

The historical system of record solution is fed using Staging Areas and Queue Managers. It begins by collecting together the detailed operational information. This includes Information Activity information elements that need to be correlated with Information Asset information elements. For example, details of an order need to be correlated with details of the customer who made the order and the products selected in the order. This correlation links together the information activities that relate to a particular information asset— because, typically, it is information assets that represent the areas of interest to the management team.

Once correlated, it is possible to generate detailed reports about the activity related to key information assets. These reports have great value in the short term but are too detailed for longer-term views of trends and averages. Information processes create Information Summary and Information Metric information elements from the detailed information and also link them to the appropriate information assets—or to information summaries of groups of related information assets. These information elements are used for the longer-term analysis.

An information warehouse feeds Information Marts and Information Cubes. These information nodes provide different consumers with different views of the information. Some will need the fine-grained detail and others will need summaries.

As time passes, the detailed information elements are deleted, or more typically archived, to clear space for new information.

Figure 9.16 shows some of the typical connections you would see with other types of information nodes. The numbers on the diagram refer to these notes:

1. This is the information warehouse.
2. It is fed from operational systems.
3. Information from the operational systems is transformed, consolidated, and correlated by an Information Broker.
4. Some of the transformations are complex and the information may use a Staging Area for intermediate results.
5. Updates may be extracted directly from the operational systems by the information broker, or they may be fed to it through a Queue Manager.
6. Any information node may query information in the information warehouse.
7. However, it is more likely that subsets of the information are extracts by an information broker and passed to a variety of consuming information nodes, where the consolidated information can be used by the organization for reporting and other types of decision making.
8. Analytics processes may run against the information in the information warehouse and the results stored directly in its information collections.

### Solution Example

The historical system of record solution is implemented in MCHS Trading's Reporting Hub, which is a subsystem made up of a Staging Area, an Information Warehouse, and a number of Information Marts. This is illustrated in Figure 9.17. The numbers on Figure 9.17 refer to these notes:

1. The operational systems regularly send information to the Reporting Hub.
2. This information is initially added to a staging area ready for processing.
3. The information is retrieved from the staging area, correlated, transformed, and consolidated into the main system of record information collections.
4. Over time, the order records become less useful and they are summarized. They retain information about the customer, the products that were ordered, how much was spent, the supplier, and the delivery data. Information such as the delivery route, product batch, and driver are eliminated at this point.
5. Both the full record and the summaries are used to populate the information marts that serve the reporting in the Decision-Center.

### Benefits

- This solution delivers high-quality aggregated information to the key control points of the organization.
- It attempts to make efficient use of storage by slimming down the amount of detail that is kept over time.

### Liabilities

- The organization needs to make decisions on the type of information it needs for management purposes.
- There is a lot of implementation effort required to deliver this information. The information needs of the organization are continuously changing and if the implementation of the historical system of record solution is not continuously evolving, the information it creates will fall into disuse.
- This type of solution may miss the important outliers as a result of the aggregation process. There are experiments in progress to augment the information warehouse with a Map-Reduce Node to manage the accumulation of the original detailed operational information, augmented with information gathered from the Internet, to provide alternative forms of analysis.
- This type of information supply chain relies on the ability to correlate the information activities with the information activities. This can be tricky if the information activities come from multiple sources that use different Information Key values to identify the information assets. It often calls for an Information Asset Hub supporting the Caller's Key pattern.

### Usage

This type of information solution is often implemented as an enterprise data warehouse that is supporting business intelligence.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Workload Offload

### Qualified Name

DesignPattern::Workload Offload

### Category

Information Solution Patterns

### Description

Provision a new information collection on an information node that has sufficient spare capacity to support the new information process.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

An organization needs to enable a new information process but the information node where the required information collections are located is overloaded and the new information process needs to work with locally provisioned information.

### Problem Example

As part of its Next Best Action solution, MCHS Trading needs to analyze information about its customers' interests, buying patterns, and channel usage along with the pipeline of new and existing products. The analysis places a heavy strain on the information node that hosts either the Information Collections and/or Information Processes. The information is consolidated into the Reporting Hub.

### Forces

- Usefulness of the form—Information is not always captured in the form that is useful for processing.
- Impacts on other processing—Analytical processes require resources that may be needed for other processing.
- Additional resource costs—Adding copies of information collections and more information nodes costs money.

### Solution Description

Provision a new information collection on an information node that has sufficient spare capacity to support the new information process.

Typically, this uses Snapshot Provisioning if this information process is only needed for a short period of time or Mirroring Provisioning if it will run for an extended period of time and needs up-to-date information.

### Solution Example

MCHS Trading creates two information mining stores for the analysis of its customer, order, and product information. This is shown in Figure 9.18.

For the next best action solution, they create an information mining store called Next Best Action Analysis Store. It is refreshed regularly from the Reporting Hub using Mirroring Provisioning to ensure the analysis continues to use the latest information.

From time to time, they also have an information mining store called Marketing Analysis Store that is used for ad hoc analysis of product sales to plan marketing campaigns. This node is provisioning from the Reporting Hub using Snapshot Provisioning whenever it is needed.

### Benefits

- A processing-hungry information process can be isolated so it does not impact the operation of other information processes.

### Liabilities

- This solution requires investment in additional infrastructure to support the off-loaded information process and the information collections it uses.

### Usage

This solution is often used to offload analytics modeling, which can invoke large queries as it searches out patterns in the information collections.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Performance Reporting

### Qualified Name

DesignPattern::Performance Reporting

### Category

Information Solution Patterns

### Description

Provide decision makers with consolidated and summarized information about their organization's activity that covers the current state and how this state has been achieved over time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

An organization needs to understand how well its business is operating.

### Problem Example

MCHS Trading needs to know the characteristics of its high-valued customers to plan its investments and sale campaigns going forward.

### Forces

- Organizations are complex—They have many different systems, activities, departments, and information collections. The detail is too much for any one person to comprehend.
- Different views provide insight—A decision maker often needs to see the same information summarized and visualized in different ways to fully understand a complex situation.
- Trends matter—To understand how well you are doing, it is necessary to understand the current situation and how that compares with past performance.
- Operational systems maintain the current state of the business—How is the past represented?

### Solution Description

Provide decision makers with consolidated and summarized information about their organization's activity that covers the current state and how this state has been achieved over time.

This information can be extracted and visualized in multiple ways, allowing the decision maker to explore and understand the current state of the business and how it is changing over time. This capability is provided to the decision maker using an Information Reporting Process running in an Application Node. Typically, the information that the information reporting process is using is provisioned through an Information Mart.

### Solution Example

MCHS Trading introduces a new information node called Decision-Center to provide management reports. This includes the high-value customer report. Because this report is used many times, there is a monthly Information Movement process that extracts the relevant information from the Reporting Hub and builds a new entry in an information collection for the high-value customer report. The MCHS Trading employees can retrieve the high-value customer report for the current month or preceding months through the Reporting Hub's user interface, which is responsible for ensuring that the requesting person is authorized to access it.

### Benefits

- Performance reporting provides a view on how the organization is operating today with a historical perspective that shows whether particular aspects of the business are trending up or down.

### Liabilities

- The performance reporting solution is dependent on the information that is supplied to it. If this is inaccurate, out of date, or incomplete, then the results will be misleading.

### Usage

Performance reporting solutions are typically provided through business intelligence packages.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Operational Analytics

### Qualified Name

DesignPattern::Operational Analytics

### Category

Information Solution Patterns

### Description

Using historical data, determine the patterns of events and actions that preceded either a good or bad outcome. Add monitors to the information processes to detect these patterns and take the appropriate actions.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

An organization wants to classify and react in real time to patterns of use that suggest an opportunity or a threat to the organization.

### Problem Example

MCHS Trading wants to detect when its stock of each type of product should be replenished. The time interval and order size is different for every product and demand fluctuates based on season, weather, and fashion. Currently, MCHS Trading relies on the skill of its buyers to determine when to reorder more stock before it runs out.

### Forces

- Outcomes are caused by many events intersecting events—Often. it takes information about the events and likely causes and effect to be collected over time to be able to detect the key predictive indicators.

### Solution Description

Using historical data, determine the patterns of events and actions that preceded either a good or bad outcome. Add monitors to the information processes to detect these patterns and take the appropriate actions.

### Solution Example

MCHS Trading uses the data from the Reporting Hub to work out which factors affect the demand for each of its products. They then set a reorder threshold for each product in the Shipping application. It generates a request to purchase more stock when this threshold is reached when fulfilling an existing order. The threshold is a combination of how often the product is ordered and how long it takes to restock.

### Benefits

- Operational analytics can handle a volume of decisions far beyond the capacity of an organization's employees. This means they can be far more granular in their treatment of each business transaction.

### Liabilities

- The hardest part of operational analytics is building an effective analytics model. This requires the right information to be collected, for long enough for the patterns to emerge, plus a skilled Data Scientist to tease these patterns out.

### Usage

Operational analytics is sometimes called real-time analytics, or predictive analytics. The results or insights may be incorporated into user dashboards or reports to support operational business processes.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Next Best Action

### Qualified Name

DesignPattern::Next Best Action

### Category

Information Solution Patterns

### Description

The advice is derived from predictive analytics. It must be delivered in real time to the information user. Some part of the analytics can run inline. However, behind it is an information supply chain that is assembling information and running analytics ahead of time. The results are stored and used to augment the inline analytics.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information. In particular, it wants to provide exemplary service to its customers.

### Problem Statement

An information user needs immediate and reliable advice on the next best action to take.

Typically, an information user is in a situation where he or she has to make a decision in a very short period of time and the information needed to investigate the alternatives is diverse and voluminous, making it impractical to perform detailed research manually.

### Problem Example

When a customer contacts the MCHS Trading call center, the customer service representative needs to quickly establish why the customer is calling, what has happened recently in the customer's dealings with the organization, and, as a consequence, the next best action to take to increase the customer's satisfaction and loyalty in MCHS Trading—and ultimately increase the amount this person is spending with the company.

### Forces

- Satisfaction and loyalty are affected by many factors—The factors that affect customer satisfaction and loyalty are complex and changing.
- Multiple contact points within an organization—An individual may interact with an organization through multiple contact points and on different levels. From an IT point of view, details of customer interactions are dispersed in multiple systems (information nodes).

### Solution Description

The advice is derived from predictive analytics. It must be delivered in real time to the information user. Some part of the analytics can run inline. However, behind it is an information supply chain that is assembling information and running analytics ahead of time. The results are stored and used to augment the inline analytics.

Figure 9.19 is the logical view of the predictive analytics decision loop that is executed in real time. It is passed the context of the request (such as who the customer is and why he or she is calling). This context is augmented with stored information to drive the decision model. The results of the decision model are fed back to the caller. Once the suggested actions have either been used or rejected, feedback on the actual outcome is stored and fed back into the information used to configure and tune the decision model.

Figure 9.20 shows the information supply chains that support this process. There are two high-level flows: first, the supply of information to the model to configure and tune it for use; second, the flow of information into the operational systems that are needed to augment the context when the decision model is run.

Many organizations when they adopt predictive analytics will already have some of these information supply chains in place.

### Solution Example

Prescriptive analytics models are deployed into the Customer-Care application to support the customer service representative. The customer information supply chain supports these models both in terms of tuning the models and providing real-time information required to execute the model for a particular customer.

### Benefits

- Analytics and the appropriate information are brought together to influence the day-today operations of the organization. Without this automation, decisions would be made with incomplete or out-of-date information.

### Liabilities

- This type of solution requires a transformation of the day-to-day operations of the business to ensure the advice from the analytics is used and feedback on its effectiveness are collected to tune the analytical models.

### Usage

Prescriptive analytics is growing in importance for organizations that want to offer exemplary customer service or diagnostic capability.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Managed Archive

### Qualified Name

DesignPattern::Managed Archive

### Category

Information Solution Patterns

### Description

Create an archiving service that manages and acts on retention policies defined for each of the effected information collections.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with governing information throughout its lifetime.

### Problem Statement

An organization is not meeting its information retention obligations.

In many industries, it is necessary to retain certain records for a long period of time in case there are investigations that are necessary in the future. Keeping these records in the operational systems can slow them down and be expensive in terms of online storage.

### Problem Example

MCHS Trading needs to keep records of who bought some of the more sensitive products that it sells. There is a small chance that they will need to retrieve this information if a problem occurs.

### Forces

- Bloated information collections—Access to an information collection that has a lot of information that is no longer needed may be slowed down due to excessive size of the collection.
- Obsolete technology—The corollary of the rapid advancement of technology is that it also rapidly becomes obsolete. Often information has value well beyond the life of the technology on which it resides.
- Expensive or unavailable skills—Obsolete technology also requires skills that become increasingly expensive or hard to find to keep functioning.
- Decommissioning applications—An organization is often unable to decommission an application even though it is not being used because it may need the information it contains.

### Solution Description

Create an archiving service that manages and acts on retention policies defined for each of the effected information collections.

The managed archive solution has the following parts to it:

- A metadata description of the subject areas that need archiving, which information collections hold the information, how frequently archiving should run, how it identifies the information entries that are ready to be archived, and how long the information should be retained.
- An archiving agent that is scheduled to run and move the appropriate information entries from the information collections into the archive. This archiving agent needs access to an information service that allows it to locate, read, and delete these information entries. It must create a record of what was archived and where it was located. This record is added to the archive catalog that is used by the organization to locate and retrieve information when it needs to.
- An archive housekeeping process that removes information entries from the archive once their retention period has been reached.

### Solution Example

MCHS Trading implements a managed archive process in its Reporting Hub. All of the orders received by MCHS Trading are copied into the Reporting Hub, so the information is complete. The open format used by the Reporting Hub makes it easy to recover and interpret the information in the archive.

### Benefits

- The managed archive moves obsolete information to cheaper storage while keeping a record of what has been archived and when.

### Liabilities

- For long retention periods, the managed archive solution needs to ensure there is a system available that can still read the information that has been archived. There are two parts to this:
- Can the device used to store the archived information still be read?
- Can the contents be understood from a business point of view—particularly if the application that created the information has subsequently been decommissioned?

### Usage

Managed archiving is used in industries where there are regulations that require the organization to retain certain types of information for long periods of time, for example, policy records in the insurance industry. It is sometimes referred to as records retention or it is part of information lifecycle management (ILM).

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Access Audit

### Qualified Name

DesignPattern::Information Access Audit

### Category

Information Solution Patterns

### Description

Monitor and record every access to an information collection and validate that the use is approved.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with governing information throughout its lifetime.

### Problem Statement

An organization needs to know who is accessing its information.

This is particularly important for personal information and information that is competitively sensitive.

### Problem Example

MCHS Trading wants to be sure that its Customer Hub is only being used for legitimate purposes.

### Forces

- Access security defines maximum access rights—The traditional access security mechanisms define all of the resources that an individual should have access to. Once the access is given, the individual can access the information for any purpose.
- Inappropriate use—An individual may be given access rights to some data for a very specific task. That individual then may use this information for other purposes—including copying it to portable storage.
- Copying or replicating information adds risk—Sensitive information is often useful or critical for many functions. Wherever it resides, it is at risk and controls must exist in all places, not just central storage locations.
- The inclusion of access controls is not sufficient—It is not enough to just monitor for access violations after the fact.
- Monitoring access controls is time sensitive—Its value diminishes over time, and it must be processed as soon as possible.
- Access control monitoring can generate a huge volume of information—There must be capabilities available to find critical events and circumstances.

### Solution Description

Monitor every access to an information collection and validate that the use is approved.

In this solution, the monitoring is correlating the data access with the task being performed and the time (occasion) it is being performed. The purpose is to uncover unexpected uses of information.

### Solution Example

MCHS Trading adds a monitoring solution that records every access to the Customer Hub database that is not authorized, or is requesting particularly sensitive information.

### Benefits

- This type of monitoring provides additional proof that only authorized people are using the critical information collections. The level of monitoring can be adapted to meet the changing needs and threats to the organization over time.

### Liabilities

- The monitoring adds additional processing load to the information supply chain. Also, it must be someone's role to review, investigate, and action any alerts raised; otherwise, the monitoring is a waste of time and resources.

### Usage

Data privacy laws and regulations, particularly around Personally Identifiable Information (PII) and Payment Card Industry (PCI) information, describe specific information elements that must be protected, secured, and guarded.

This type of monitoring can be implemented by simple database triggers or user-defined functions. However, that tends to add a large additional load on the database. There are specialized network monitoring solutions that are able to monitor information requests as they flow into the network.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Monitoring

### Qualified Name

DesignPattern::Information Monitoring

### Category

Information Solution Patterns

### Description

Add information probes at key points in the information supply chain and analyze the measurements they bring back to detect gaps, abnormal patterns, or deteriorating quality in the information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 9, "Solutions for Information Management".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

Is the information supply chain working?

For example,

- Is the correct information being transferred between the information nodes in a timely manner? Is the information passed to the destination semantically equivalent to the information in the source?
- Is the information stored in each information collection complete, up to date, and protected?
- Are invalid values being detected and corrected—both within the information collections and during information provisioning?
- Is information being used appropriately?

### Problem Example

MCHS Trading wants to be sure that its information supply chains are working properly. For example, it wants to know that orders are being fulfilled on time, that its product descriptions are correct, and that its customer information is up to date. How does it achieve this?

### Forces

- Failures can occur at any time, any place for many reasons.
- The absence of activity may indicate a problem—It is not sufficient just to monitor for errors.
- Where an application does not completely meet the needs of an organization, the people using it find ways to work around it—This can involve putting information into attributes designed for different purposes, or changing values in files/databases after the application has finished processing.
- Network and system failures may interfere with the transfer of information—These disruptions must be recovered from once the failing components have been recovered to ensure that correct information content has been transferred with the correct relationships to other information.
- If a failure in an information supply chain is not detected, and resolved in time, further failures can occur downstream as a consequence—For example, if information about monthly sales figures from one region is not loaded in time, the report that aggregates the sales figures for the whole organization will be wrong.
- It takes local knowledge to understand how a particular information process should be operating.
- It takes holistic knowledge of the information supply chain to understand the impact of any incident.
- Monitoring information is context sensitive—Its meaning is lost if the location and circumstances under which the monitoring information was gathered is lost.
- Monitoring information is time sensitive—Its value diminishes over time, and it must be processed as soon as possible.
- Monitoring can generate a huge volume of information, causing resource shortages for other activity running within an information node.

### Solution Description

Add information probes at key points in the information supply chain and analyze the measurements they bring back to detect gaps, abnormal patterns, or deteriorating quality in the information.

The processing of this information is time critical. Its aim is to gather information from a wide range of sources and consolidate them into a central location where the values can be monitored in near real time, while also allowing historical analysis of the information.

The leaf nodes of this information solution are typically Information Probes that are continuously pumping out events. These events are stored either in an information collection that is hosted in the same information node as the information probe, or in an Information Event Store. Whichever approach is used, the events are periodically extracted and sent, either directly, or via intermediary nodes, to a central information node for analysis.

This is shown in Figure 9.21.

Information events in the original source information nodes need to be purged as part of the information supply chain's function. This may be as part of the information flow that sends the events toward the centralized information node, or via a regularly scheduled Information Archiving Process. Using an information archiving process leaves the events in place for a short period of time to enable a local Infrastructure Operator to monitor what is occurring in the local information node while still enabling the centralized monitoring.

Each information probe writes the events they detect to a local Information Event Store to provide a historical view of the events. This store can be accessed through a Remote Information Service to enable a Cascading Information Supply Chain to consolidate the interesting events into information event stores in a central monitoring information node. This node hosts information processes that review and action the events that are received.

### Solution Example

MCHS Trading sets up Information Probes at each of its information nodes to monitor the information processes that contribute to its information supply chains:

- Each information node is monitored for availability.
- Each information node monitors that its information processes complete successfully.
- Every information flow contains an information probe that counts the information payloads it has processed.
- The Order-Tracking information node monitors that orders are being processed in a timely manner. Each information probe writes the events it detects to a local Information Event Store. These are consolidated into event stores in the main operator console for MCHS Trading's systems. The availability of the information nodes, and any unexpected event any of them detect is sent to the operator console for review and action. The operator console is an Event Correlation Node and is able to filter events and detect common patterns, reducing the load on the infrastructure operator.

### Benefits

- Monitoring the consistency, reliability, and quality of information improves the information used by an organization for key decision making, resulting in cost savings, mitigated risk, or potential revenue opportunity. Such monitoring action becomes an aspect of a broader Information Governance Program.
- This approach enables detailed information to be collected from a wide range of sources.

### Liabilities

- An information node that is experiencing failures, or a shortage of resources, may not be able to forward on the information it has gathered at a fast enough rate to avoid being swamped by incoming information.
- There is a time delay between capturing information and processing it. This may be significant for time-sensitive events, in which case it will be better to query the event information directly from the source rather than use information flows to move them into a consolidated information collection.
- Monitoring processes must be kept in sync with changes to business processes and rules, potentially adding time and cost to implement such changes.

### Usage

Information monitoring is normally implemented by organizations that have a strong business need (such as regulatory requirements or customer service) to be sure particular types of information are correct. In these environments, it is not sufficient to just monitor for errors. The monitoring must positively demonstrate that all of the right information has been included, from authoritative sources, and it is not contaminated with inappropriate values.

### Search Keywords

- Patterns of Information Management
- Information Solution
- Solutions for Information Management

### Version Identifier

1.0

### Status

ACTIVE

____

