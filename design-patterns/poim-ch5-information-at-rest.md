<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**Information at Rest**

Dr.Egeria commands for the design patterns in Chapter 5, "Information at Rest", of *Patterns of
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

Information Service

### Qualified Name

DesignPattern::Information Service

### Category

Information Service Patterns

### Description

Define well-defined interfaces to the information that meet the needs of particular consuming information processes to enable them to create, retrieve, and maintain just the information they need.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities. This information process is using stored information.

### Problem Statement

Some information processes need the same information, but each requires it to be formatted differently.

The difference in the formatting may be structural—or formatted for a different vocabulary. For example, consider an information collection that contains entries for people that are linked to other collections containing details such as address and contract. This information could be consumed in the following ways:

- All people and the contracts they have with the organization
- Each sales area and the people who live within it
- All employees (these are people with an employment contract) The first two examples are structural changes; the last one takes a subset of the information and renames it from information about people to information about employees.

### Problem Example

MCHS Trading's E-Shop application is taking customer orders through the Internet. It has three main information processes:

- Login—To identify a customer. This needs access to the stored customer details to verify the customer's account details.
- Browse Catalog—To allow the customer to search and view the details of products offered for sale. This requires access to the stored product details.
- New Order—To make an order for products from MCHS Trading. This is using the stored payment details about the customer, order codes from the product details, and stored details of a new order. These processes are making use of three information collections: customer details, product details, and order details in a variety of ways. How should the information processes access these information collections?

### Forces

- Specialized information collections are the fastest—Information collections designed specifically for an information process, and stored locally in the same information node as the information process, typically provide the fastest access to the information for the information process.
- Information copies add cost—Every copy that is made of some information values costs money to store and maintain.
- Inline transformation is transient—If transformed information is not stored, then the transformation must be redone each time the information is needed in that format. This makes sense if the information values are changing rapidly, they must be current, or the transformations are minimal. However, when the information values are fairly static or the transformations necessary are complex, collating and reformatting the set of information values on the fly over and over again is inefficient.
- Inconsistent terminology for the same information—Different parts of an organization may use inconsistent terminology from each other. This terminology difference may derive from a different heritage, skill sets, or decentralized operation.

### Solution Description

Define well-defined interfaces to the information that meet the needs of particular consuming information processes to enable them to create, retrieve, and maintain just the information they need.

This interface includes actions (operations) with parameters where information is passed in and out. Each parameter is defined as a structure with one or more attributes that are named according to the requirements of the consuming information process. This structure is used on the programming interface of the Information Service. When the consuming information process interacts with the information service, the information is formatted as defined by the view.

An information service provides one or more operations on the interface. Each operation performs a well-defined function. Typically, the operations are related and focus on providing access to a particular type of information. The operations could include the following:

- Create—Add new information to the information collections.
- Retrieve one—Retrieve a discrete instance of information.
- Retrieve cursor—Retrieve a related set of information instances that can be stepped through one at a time.
- Retrieve collection—Retrieve a related set of information instances altogether.
- Update—Change specific information values.
- Delete—Either remove the information from the information collection or mark it as removed so the information processes can no longer use it. The implementation of an operation shown in Figure 5.3 makes use of the information protection pattern groups described in Chapter 8, "Information Protection." The Information Probes can record the request and the response or monitor for exceptional conditions. An Information Guard validates that the information process is allowed to access the information on the request, and another information guard may prune or mask the results on the response. Information Reengineering Steps transform the request before calling the information collection, and transform the result to create an appropriate form for the information process. The precise mechanism used by the information service to access the information collection is described by the information service implementation patterns:
- Local Information Service
- Remote Information Service
- Triggering Information Service

### Solution Example

MSCH Trading's E-Shop application provides six information services to support its three main information processes:

- Verify customer—Compares the customer's input with the stored account details from the customer details collection
- Get payment details—Retrieves details of the customer's preferred payment method
- Search catalog—Returns a list of products that matches a search criterion
- Get product details—Retrieves descriptive details of selected products from the product details information collection
- Get order code—Retrieves the product codes used in the warehouses
- Create order—Adds a new entry in the Order Details information collection This is illustrated in Figure 5.4.

### Benefits

- Software developers who are writing new information processes are more likely to use stored information appropriately because the information service formats it for their needs.
- The information processes are isolated from the provisioning mechanism used to supply the information through the information service. This creates opportunities to consolidate and improve the information "behind the scenes" without affecting the implementation of the information processes.
- Information collections can use a canonical form with a more complete scope and coverage than local programmers need. The information services expose useful subsets of this information, making them consumable to a broader set of information processes.

### Liabilities

- If information services are not properly defined, cataloged, and communicated, redundant and inconsistent information services can be created, making it difficult to understand which to use and when.
- Using this pattern may result in additional latency if the format of the information as it is stored is very different from the format that is used by the information services. This can become a significant and unnecessary overhead for a popular information service if the information values are relatively static and suggests the need for a Reference Usage copy of the information for these information collections.

### Usage

There are many technologies that provide interfaces to information. For example, databases offer SQL interfaces, such as Open Database Connectivity (ODBC) and Java Database Connectivity (JDBC). Application servers offer remotely callable interfaces such as web services and Representational State Transfer (REST) interfaces. Such an interface is an information service if the interface is a well-defined contract for working with information that is offered to consumers. This interface may very closely resemble the way the information is stored, or an abstraction of it.

### Search Keywords

- Patterns of Information Management
- Information Service
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Local Information Service

### Qualified Name

DesignPattern::Local Information Service

### Category

Information Service Patterns

### Description

Interact directly with the local information collection whenever the information process calls the information service.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information process is using an information service. How is this information service accessing the information from the information collections?

### Problem Statement

The information requested by an information process is located in an information collection hosted on the local information node.

How does the information service retrieve and maintain the information requested by the information processes?

### Problem Example

The MCHS Trading E-Shop application has a login information process that needs to access information about a customer's account in order to validate that customer's identity and operate according to the predefined preferences.

### Forces

- Different structures of information—The structure of the information that is stored may be different from the needs of the information process.
- Specialized information collections are the fastest—Information collections designed specifically for an information process, and stored locally in the same information node as the information process, typically provide the fasted access to the information for the information process.
- Information in motion needs protection—As information is requested within an information node, it needs protection to ensure it is not intercepted and either stolen or changed in an unauthorized way.
- Information copies add cost—Every copy that is made of some information values costs money to store and maintain.

### Solution Description

Interact directly with the local information collections whenever the information process calls the information service.

Every information collection provides a basic interface for retrieving and maintaining the information it retains. The information service uses this interface to access the stored information. See Figure 5.5.

### Solution Example

The login information process calls the verify customer information service that, in turn, calls the customer details information collection to retrieve the stored details about the customer. The login process then compares the results with the input from the customer and acts accordingly.

### Benefits

- With this pattern, the information collection and the information processes using it are located in the same information node. This is typically the fastest way to supply information and typically the information collections are styled to favor the needs of the local information processes.

### Liabilities

- If an organization only uses local information services, shared information must be copied into information collections located in each information node to ensure it is local to all of the information processes that need it. This results in high cost of moving, storing, and managing the copies.

### Usage

Local information services are interfaces that are private to the information processes within the local information node. An information node may be implemented with multiple server processes. For example, it could be implemented with an application server and a database where the processes may be making network requests to access the stored information. However, only the locally hosted information processes need to be changed when the information service changes.

### Search Keywords

- Patterns of Information Management
- Information Service
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Remote Information Service

### Qualified Name

DesignPattern::Remote Information Service

### Category

Information Service Patterns

### Description

Issue an information request to call an information service hosted in an information node that has access to the required information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information process is using an information service. How is this information service accessing the information from the information collections?

### Problem Statement

The information requested by an information process is stored in a different information node.

The information values are changing rapidly and there is a strong desire not to create a local copy of the information for the information process because of the cost of keeping it synchronized with the original information collection. How is this information supplied to the information process?

### Problem Example

MCHS Trading plans to add the ability for an E-Shop customer to cancel an order that has not yet been shipped. The Cancel Order information process in the Customer-Care information node will implement this capability using the process in Figure 5.7. How is information supplied to this information process?

### Forces

- Information nodes are not always available—The information collection hosted on a remote information node may not be available when the information process requires information.
- Redundant information nodes add cost—When the information process requires an information collection and the primary information node is unavailable, a redundant or mirror node may be required, resulting in additional storage costs.
- Communication costs—It takes time to transfer information from one information node to another.
- Information in motion needs protection—As information is transferred between information nodes, it needs protection to ensure it is not intercepted and either stolen or changed in an unauthorized way.
- Closed application information—Many applications have information collections that store information in proprietary formats that cannot be easily accessed outside of the application.

### Solution Description

Issue an information request to call an information service hosted in an information node that has access to the required information.

An Information Request is a pattern that describes how to package up a request for an information service and send it to another information node to execute. The information request then packages up the results and sends them back to the local information service. See Figure 5.8.

In most cases, the remote information service uses Information Configuration to determine the network location of the information service it must call. This configuration is typically static—either hard-coded in the remote information service or read from configuration at startup. In circumstances where this linkage needs to be more flexible, it is possible to have a dynamic registry of information services that the remote information service contacts to looks up the network information each time it issues an information request.

### Solution Example

The Cancel Order information process shown in Figure 5.9 uses information services to connect directly with the information it needs.

### Benefits

- Remote information services allow information processes to work with authoritative information located on remote information nodes. They can also be used to initiate work in other information nodes and/or to distribute workload among a cluster of similar information nodes.

### Liabilities

- The information node that hosts the information collection may be unavailable when the information process calls the information service. The information service should log that the information collection is not available and the information process should fail gracefully when this occurs. Or for critical information processes, there may be a requirement for an alternate information node to be available.

### Usage

Remote information services are available through many types of technology. Here are some examples:

- Remote procedure calls supported by standards such as Java Enterprise Edition (JEE)
- Web services technology
- RESTful interfaces
- Linked data interfaces such as Open Services for Lifecycle and Collaboration (OSLC)
- Remote interfaces to databases such as Open Database Connectivity (ODBC) and Java Database Connectivity (JDBC)

### Search Keywords

- Patterns of Information Management
- Information Service
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Triggering Information Service

### Qualified Name

DesignPattern::Triggering Information Service

### Category

Information Service Patterns

### Description

Partition the request into calls to other information services that between them have access to the requested information—then combine and return the results.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information process is using an information service. How is this information service accessing the information from the information collections?

### Problem Statement

The information requested by an information process is dispersed among multiple information collections.

### Problem Example

When a customer calls the MCHS Trading customer care center, the customer service representative needs to understand who the customer is, his or her history of interaction with the organization, and in-flight/recent orders.

### Forces

- Inline transformation is transient—If transformed information is not stored, then the transformation must be redone each time the information is needed in that format. This makes sense if the information values are changing rapidly, they must be current, or the transformations are minimal. However, when the information values are fairly static or the transformations necessary are complex, collating and reformatting the set of information values on the fly over and over again is inefficient.
- Dispersed information is inconsistent—Combining information from disparate information collections takes care to ensure proper correlation is made as the information is brought together. The effort required to do this may be too much to do on demand—particularly when it requires human judgment to handle the edge cases.

### Solution Description

Partition the request into calls to other information services that between them have access to the requested information—then combine and return the results.

The triggered information service calls an Information Service Trigger to start or invoke an Information Process. This information process is responsible for calling the multiple information services and combining the results. See Figure 5.10.

### Solution Example

The information process shown in Figure 5.11 calls a triggered information service to create the complete view of the customer. It uses an Information Federation Process to call the information service for customer details in the Customer Hub, and then using the customer's identifier from the customer details, it calls the Order-Tracking application to extract the recent orders for the customer. Then, from these order details, it calls the Product Hub to provide more information on the products ordered.

### Benefits

- The triggered information service can be used to correlate information from multiple sources together. It can also initiate work in another information node.

### Liabilities

- The information services may use different security models, requiring the information process to switch security credentials for each call. These security credentials need to be managed securely for the information process's exclusive use so others cannot acquire or make use of them.
- The triggered information service is only available if all of the sources it calls are available. For critical information services, alternate information collections may be required, resulting in additional storage cost.

### Usage

Triggering information services are used in federating technologies to pull together information from multiple sources.

### Search Keywords

- Patterns of Information Management
- Information Service
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Collection

### Qualified Name

DesignPattern::Information Collection

### Category

Information Collection Patterns

### Description

Group related information together into a logical collection and implement information services to access and maintain this information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization uses a wide variety of information to support its activities. This information must be easy to locate, manage, and protect.

### Problem Statement

Information must be organized so it can be located, accessed, protected, and maintained at a level that is consistent with its value to the organization.

Not all information has equal value to the organization. The type of information, how it is used, and the context in which it is used will affect the types of access and the level of availability, management, and protection required.

How should information be organized so that an information process can locate the right information and the appropriate mechanisms can be applied to the management and protection of the information behind the scenes?

### Problem Example

The MCHS Trading E-Shop application has to manage details of many different customers and the orders they are making. How should this information be organized?

### Forces

- Information is subject to obligations—Information collections must be aligned to information management obligations in the form of governmental regulations, legal requirements, or organizational governance.
- Information nodes are not always available—Information processes, hosted in information nodes, manage information for an organization. The hosting information nodes are not always available. They may be shut down for regular maintenance or may fail at unexpected times.
- Information collections may be accessed from remote information nodes—Information processes hosted on different information nodes may need access to the same information. As such, information must be accessible from a remote information node.
- Information users and processes have different needs for information—Information users and processes need similar, but often subtly different, information. These distinctions create variations through an information supply chain, or even produce new information supply chains.

### Solution Description

Group related information together into a logical collection and implement information services to access and maintain this information.

An information collection is a group of related information that is managed together. Often, an information collection supports information related to a single subject area, such as customer details; however, this is not essential. An information collection may contain information about a single event or information gathered from a single location.

An information collection must be accessible to an information supply chain. See Figure 5.12. Specifically, Information Processes use Information Services to locate and access the information collections. These information services provide operations to retrieve, create, update, and delete information in the information collection.

An information collection must be stored somewhere to make sure it is not lost when the information nodes are restarted. It can be stored in a single information node (Physical Information Collection) or partitioned across multiple information nodes (Virtual Information Collection).

Within an information supply chain, an information collection will be used in a particular way by the information processes. Understanding how the information collection is to be used, by which processes, and the location of these processes is necessary to decide on the appropriate style of Information Provisioning to use. The usage patterns for an information collection are described in the following patterns:

- Master Usage
- Reference Usage
- Hybrid Usage
- Sandbox Usage An information collection also has a scope that defines the proportion of unique instances it maintains with respect to the total number existing for the subject area. The choices are described in the following patterns:
- Local Scope
- Complete Scope
- Transient Scope Finally, it has a coverage pattern for the attributes it contains relative to the Subject Area Definition:
- Local Coverage
- Core Coverage
- Extended Coverage
- Complete Coverage In summary, an information collection describes stored information that is related in some way. Information processes use information services to access the information collection and the usage, scope, and coverage patterns classify their approach.

### Solution Example

Within the MCHS Trading E-Shop application, there are three information collections: one for customer details, one for orders made, and once for the products that are on sale through the website. Figure 5.13 summarizes the usage and scope of these. Also note that there are relationships from order details to both the customer details and product details.

### Benefits

- The information collection pattern describes a simple concept for thinking about the information stored within the information nodes of an information supply chain. In particular, it identifies the location of information about a particular subject area and its scope and usage. This knowledge is invaluable in the understanding and planning of effective information supply chains.

### Liabilities

- The volumetrics for the information collection (includes details such as the size of the information store, average number of entries, number of requests to either read or update the information, availability times, and reliability) will affect the sophistication of capability necessary to implement the information collection.
- The same type of information may be managed by more than one information node. There is no guarantee that each information node will implement its information collections in the same way. The attribute structures, valid values, level of quality, and supported operations may all be different. These differences will need to be uncovered and tackled when building an information process that implements the logic to synchronize the information between these information collections.

### Usage

The majority of IT systems, particularly applications, keep information in persistent storage such as files, databases, or content management systems. Here are some examples of information collection implementations:

- An information collection could be implemented in a file where each row stores an information entry and the values of the entry's attributes are delimited by a special character (e.g., a comma-separated value or .csv file).
- An information collection could be implemented in a file where each information entry is stored as a different XML document, or fragment.
- An information collection could be implemented in a database using one or more linked tables. The information entry would be stored in one or more rows of these tables.
- An information collection could be a directory of documents, images, and/or video stored on a file system.
- An information collection could be a collection of documents, images, and/or video stored in a content management system.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Physical Information Collection

### Qualified Name

DesignPattern::Physical Information Collection

### Category

Information Collection Patterns

### Description

Provide persistent storage to the information node where related information can be stored.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Collection is hosted on an Information Node. This means that the Information Node is responsible for managing and protecting the information within the collection.

### Problem Statement

The information hosted by an information node must be retained even if the information node is shut down and restarted.

### Problem Example

The MCHS Trading E-Shop application has to manage details of many different customers and the orders they are making. This information must be preserved even if the E-Shop fails or is restarted for maintenance.

### Forces

- Even the best-run information node fails from time to time—When the information node fails, the information that it was working with will be lost if it is not written to persistent storage. Even if the information node does not fail, it needs to be shut down from time to time for maintenance. How should the information node preserve the information it is responsible for over a shutdown and restart? How should this preserved information be organized so it can be retrieved and maintained?
- Increasing requirements produce a complex information collection—An information supply chain is much easier to manage if there is a single place where information about a particular subject area is created, updated, and deleted. However, different information processes need different subsets of information. The more information processes use an information collection, the more complex each information entry within the information collection becomes and the bigger the impact of any change to the information collection.

### Solution Description

Provide persistent storage to the information node where the entire information collection can be stored.

The information collection and persistent storage are located within the boundaries of an information node. See Figure 5.14. Information processes located within the same information node use a Local Information Service to access the information. Information processes located in other information nodes use a Remote Information Service to access the information collection.

### Solution Example

In the E-Shop application, the customer details, product details, and order details are persisted in a database as database tables. There is a root table for each of the collections and other tables holding supplementary information and relationships between the information collections, such as the relationship between an order and a customer.

### Benefits

- Persisting the information for a collection within the information node that hosts the information collection makes the responsibilities for managing the information very clear. Investments can be made that are in line with the value of the information and appropriate people in the organization can be made accountable for its proper management.

### Liabilities

- An organization will have many information nodes. With each information node persisting its own information collections, there will be inconsistencies in how the information is protected and managed, and potentially additional storage costs.

### Usage

The majority of information collections are stored in the same information node in which they are managed. Sometimes, a group of information nodes will share a persistent storage service (such as a shared file system or database server) to simplify some of the operations tasks, such as backup and archiving. However, if the information nodes share information in this persisted store, then the persistent store should be considered as an information node in its own right because it is effectively providing an information service to the consuming information nodes. Ownership of the information collection is also moved to the persistent store and the original consuming information nodes are using remote information services to access the information collection.

This is illustrated in Figure 5.15. If a database server is providing a shared database to multiple applications, it is an information node and owns the information collections it stores (1). If the applications had their own independent database, stored on the same database server, then each has its own information collection and the database server is just part of the supporting infrastructure (2).

The difference between the two scenarios is the point of control. In many organizations, the information node is the control point for ownership, investment, staffing, and change. Where information is shared, changes to the information must be coordinated between the consumers, but at the end of the day, it needs a single owner.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Virtual Information Collection

### Qualified Name

DesignPattern::Virtual Information Collection

### Category

Information Collection Patterns

### Description

Create an information service to represent the desired collection of information and use information processes to obtain and maintain the distributed information whenever requests are made to the information service.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization has many information nodes, each hosting information collections.

### Problem Statement

Some related information needed by an information process is dispersed among a number of information collections hosted on different information nodes.

This information needs to be gathered together, correlated, and presented to the information process in a usable form. Depending on the requirements for the information collection, there may be additional need for restructuring and standardization of the information from the different collections.

### Problem Example

The Shipping application is supporting three physical warehouses. The warehouses coordinate the distribution of goods and are located at strategic places to give MCHS Trading a fast and efficient distribution capability. Each warehouse runs its own stock management system that keeps track of local stock levels and coordinates orders and deliveries from its suppliers. The Shipping application is responsible for allocating the orders among the warehouses. It needs to know the stock levels in each warehouse to ensure it is making the best allocation. How does it know the stock levels of the items listed in an order when the stock levels are kept in the stock management systems located in each of the warehouses?

### Forces

- Information processes are dispersed—As with all distributed information situations, the question is, should the information be consolidated into a local information collection in advance of the information process's need, or should the information be pulled together on demand when the information process makes a request to an information service? This will depend on how much information is involved, how rapidly it is changing, how much transformation is needed, and the availability of the hosting information nodes.
- Information processes have different requirements—An information supply chain is much easier to manage if there is a single place where information about a particular subject area is created, updated, and deleted. However, different information processes need different subsets of information in different structures.
- Sharing can increase semantic complexity—As more information processes use a virtual information collection, there is greater need for clear semantic understanding of all information entries within the information collection and the relationships between those information entries.

### Solution Description

Create an information service to represent the desired collection of information and use information processes to obtain and maintain the distributed information whenever requests are made to the information service.

This pattern is also known as a federated view. The caller of the top-level information service is unaware that the information collection is dispersed. The mechanism that pulls the information together is hidden behind the top-level information service.

This mechanism is configured with details of where the information collections are located, how to access them, and the transformations and mappings required to stitch together the information from the different sources in response to the calls to the virtualized information service.

### Solution Example

The stock management system in each of the warehouses supports an information service that can return the stock levels and estimated time to deliver an order. The Shipping application has an information service that calls each of the stock management systems and returns the aggregated stock levels, best delivery time, and warehouse to use.

### Benefits

- This pattern avoids creating another copy of the information required to provision the information process.

### Liabilities

- This pattern creates operational dependencies between the information node where the virtual collection is logically hosted and the information nodes whose information services are called to satisfy requests to the virtual collection.
- This pattern assumes that the semantics and the level of quality of the information collections it is federating are equivalent and the effort to match information across them is suitable for real-time invocation.

### Usage

There are three basic types of technology used to provide a virtualized information collection illustrated in Figure 5.16. They are sometimes called information federation technologies.

Database-level federation (1) is typically implemented in a database server and provides an SQL interface to a set of virtual tables. When an SQL request is made, the request is broken up and pushed down to the databases that are actually storing the information.

Service-level federation (2) triggers an information process to call the services of the information collections that are storing the information and then collate the results to pass back to the caller.

Both database-level federation and service-level federation are well-established techniques for creating a virtual information collection. There is a third approach that is being explored by a number of organizations that is called semantic federation (3). The Semantic Integration solution pattern describes this approach in more detail.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Master Usage

### Qualified Name

DesignPattern::Master Usage

### Category

Information Collection Patterns

### Description

When these information processes run, they update the information in the appropriate information collection directly, as part of their processing logic. As a result, the values stored in the information collections represent the latest status known to these processes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information collections are storing information throughout the information supply chain. Some information collections will store the same type of information and need to be synchronized. You want to understand the best way to keep them synchronized. This is dependent on the behavior of the information processes using it.

### Problem Statement

A group of related information processes must maintain up-to-date information about a subject area.

This means they are creating, retrieving, updating, and deleting information entries in the information collection.

### Problem Example

MCHS Trading's E-Shop application needs to store details of the people who have registered accounts. This customer profile contains information about the individual's name, address, payment information, and other web preferences.

### Forces

- An information supply chain is much easier to manage if there is a single place where information about a particular subject area is created, updated, and deleted. However, different information processes need different subsets of information. The more information processes use an information collection, the more complex each information entry within the information collection becomes and the bigger the impact of any change to the information collection.

### Solution Description

When these information processes run, they update the information in the appropriate information collections directly, as part of their processing logic. As a result, the values stored in the information collections represent the latest status known to these processes.

An information collection used in this way is said to be playing the master usage in the information supply chain. Multiple information processes would use such an information collection as their primary source of information. The information services that these processes use to maintain the information collection would include create, retrieve, update, and delete operations.

Information collections playing the master usage are often used as a source of information to distribute to other information collections in the information supply chain.

Information collections playing the master usage typically reside in the same information node as the information processes that are using them. However, this is not essential because information collections can be accessed from a remote information collection via a Remote Information Service. See Figure 5.17.

### Solution Example

E-Shop has a master usage information collection to maintain customer details. See Figure 5.18.

### Benefits

- An information collection performing the master usage provides a complete set of services to the information processes that are using it. The fact that the information processes update the information inline with the work they are coordinating means these types of information processes represent the up-to-date status of the information processes.

### Liabilities

- New information needs to be validated before it is stored and/or distributed to ensure it does not contaminate other parts of the information supply chain.
- Any changes to the information in the information collection should be distributed to other copies of the information located throughout the information supply chain.

### Usage

There are three common uses of this pattern:

- It is typical for an Application Node to provide master information collections that are used exclusively by the information processes it hosts. In this situation, it is possible to open up these information collections to other information processes, but this must be done with care because the application may have internal assumptions coded that assume its information processes are the only ones updating the information collections. The result could be a loss of data integrity if changes are made to these information collections that violate these assumptions.
- An Information Asset Hub may provide master information collections for Information Assets. These master collections support many information processes hosted by other information nodes.
- An Information Activity Store provides information collections with a master usage for recording the status of one or more information processes that are processing a particular type of Information Activity.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Reference Usage

### Qualified Name

DesignPattern::Reference Usage

### Category

Information Collection Patterns

### Description

Create a read-only copy of the information from an appropriate information collection and locate it where it is accessible to the new information processes. Use information provisioning to keep this copy in synchronization with the original.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information collections are storing information throughout the information supply chain. Some information collections will store the same type of information and need to be synchronized. You want to understand the best way to keep them synchronized. This is dependent on the behavior of the information processes using it.

### Problem Statement

An organization wants to centralize the management of information, but information processes located on different information nodes still need their own local copy of the information.

Reasons for this include (1) the format of the information is not convenient, (2) the performance of the remote requests to retrieve information is not adequate, (3) the availability of the remote information node is not convenient, or (4) the information node hosting the information collection is not able to take on the additional workload to supply this information either because of cost or spare capacity.

### Problem Example

Each of MCHS Trading's order-processing applications needs up-to-date product information. MCHS wants to maintain product information in one place. It introduces a new application called Product Hub that provides the central place where product details can be maintained. The Product Hub has a master usage information collection for product details with information services that can be accessed by remote information processes. However, E-Shop, Mail-Shop, Stores, Shipping, and Invoicing are applications that need the product details in their own databases in their local format. It would take a huge investment to re-write them to support the Product Hub information services. The case for Reporting Hub is slightly different. It is maintaining a historical perspective about the products. Product Hub only contains the current product details. Reporting Hub needs regular feeds from Product Hub that contain the changes to the product catalog to add to its historical information collection.

### Forces

- Every copy of an information collection that is created and distributed adds to the cost of maintaining the information supply chain.
- Retrieving information from a remote information node takes more processing than retrieving information from the local information node.

### Solution Description

Create a read-only copy of the information from an appropriate information collection and locate it where it is accessible to the information process.

An information collection that is a read-only copy of another information collection is said to be playing the reference usage in the information supply chain. Specifically, only the information processes responsible for provisioning it should update such an information collection. All other information processes (that is, the ones that caused this copy of the information to be made) should only retrieve information from it. This is reflected in the reference usage information services because they will only include retrieve operations for the information collection. If these information processes do update the information with the reference information collection, it becomes a master information collection and such updates may have to be synchronized back to the original information collection.

Information collections playing a reference usage are typically located in the same information node as the information processes that are using it. Its contents will be refreshed from the original copy as appropriate. See Figure 5.19.

### Solution Example

Each order-processing application is sent a read-only copy of the product details. See Figure 5.20. These information collections are provisioned from the Product Hub application, which has the information processes that maintain the master information collection.

Any information processes implemented in the order-processing applications that would change the product details are either modified or disabled to ensure the product details remain consistent with the master copy in the Product Hub application. For example, Figure 5.21 shows E-Shop's Maintain Product Catalog information process is disabled.

### Benefits

- This pattern provides a read-only, purpose-built information collection to one or more information processes to directly support their needs.

### Liabilities

- This information collection needs to be continuously synchronized with the original information collection; otherwise, the information processes using it will be working with obsolete information. Any information processes that are capable of updating a reference usage information collection should be disabled.

### Usage

Reference information collections are used extensively throughout many IT systems particularly for lookup tables, which are constantly referred to by the information processes, but can be maintained elsewhere.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Hybrid Usage

### Qualified Name

DesignPattern::Hybrid Usage

### Category

Information Collection Patterns

### Description

Create an information collection that supports all of the attributes needed by the local information node. Maintain as many attributes as possible through local processing and supply the other attributes, as read-only copies, from other information collections.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information collections are storing information throughout the information supply chain. Some information collections will store the same type of information and need to be synchronized. You want to understand the best way to keep them synchronized. This is dependent on the behavior of the information processes using it.

### Problem Statement

A group of related information processes requires access to information about a subject area that is broader than the attributes it is able to manage locally.

The need for multiple information collections may be for performance, technical, or political reasons. Each information collection is located in a different information node. The information processes running on each information node are maintaining a different subset of values from the information processes on the other nodes.

### Problem Example

MCHS Trading plans to introduce an Information Asset Node called Customer Hub to provide a single view of its current customers. This single view resides in an information collection located in the Customer Hub. Values from E-Shop, Stores, and Mail-Shop will be synchronized with it. In addition, new applications, such as Customer-Care, will use it as their principle information collection for customer data. There will be analytical insight that classifies each customer added from the analytics team. All in all, many information nodes claim ownership to different parts of each entry in the information collection.

### Forces

- If each of these information collections plays a master usage, they will have to be synchronized using Peer Provisioning. This could allow information nodes to change values they do not officially own and have them distributed to the other information collections.

### Solution Description

Create an information collection that supports all of the attributes needed by the local information node. Maintain as many attributes as possible through local processing and synchronize the other attributes though the information supply chain.

This type of information collection is said to be playing the hybrid usage. In this type of collection, some of the attributes are directly changeable through the hybrid usage information services, and others are read-only. The read-only attributes are copies that are updated through a regular provisioning process. See Figure 5.22.

### Solution Example

The customer details information collection in the Customer Hub is maintained directly by some information processes and also fed to these collections through both Mirroring Provisioning and Peer Provisioning.

### Benefits

- The hybrid information collection is directly supporting a decentralized approach to managing shared data. For many organizations, this can help to break down the resistance to sharing information because the ability to update information and extend it with local attributes is retained.

### Liabilities

- The integration logic to synchronize the information with a hybrid collection can become complex. It is also necessary to maintain governance on how the information is changed, exchanged, and used across the different information collections that are synchronized with the hybrid collection.

### Usage

This type of information collection is typically found in Master Data Management (MDM) hubs that are operating in a decentralized organization.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Sandbox Usage

### Qualified Name

DesignPattern::Sandbox Usage

### Category

Information Collection Patterns

### Description

Commission and provision a set of information collections that are suited to support the needs of the project. During the project, the team is able to run the workloads and make the changes to the information as and when they need to. At the end of the project, these information collections are deleted.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information collections are storing information throughout the information supply chain. Some information collections will store the same type of information and need to be synchronized. You want to understand the best way to keep them synchronized. This is dependent on the behavior of the information processes using it.

### Problem Statement

A group of related information processes used for a project needs to make experimental changes to the organization's information.

### Problem Example

MCHS Trading would like to do some what-if analysis on the mix of products available through each channel. It wants a set of information collections that covers its customers, the products they buy, through which channel, and when. The Reporting Hub has this information but the structure of the data is not ideal for this type of analysis. In addition, MCHS Trading wants to make changes to some of this data to understand how changes in its product offerings could affect sales.

### Forces

- When information is shared among multiple information processes, each information process is affected by the work of the others. While an information process is partway through a set of related updates, the affected information entries are typically locked so the other information processes do not see the partially completed changes. This works well for changes that take a few seconds. Anything longer than that needs an alternative approach.

### Solution Description

Commission and provision a set of information collections that is suited to support the needs of the project. During the project, the team is able to run the workloads and make the changes to the information as and when they need to. At the end of the project, these information collections are deleted.

Information collections that are provisioned for a specific experimental project are playing the sandbox usage. These information collections help to isolate the project's information processes, which may be creating fluctuating workloads, from the regular production workloads. See Figure 5.23. It is not possible to detect sandbox usages from the information services that access the information collection. These information services may include create, update, and delete operations as well as retrieve and may not look any different from master usage information services. It is the management policy associated with the information collection that determines that it is an information collection populated for experimental purposes for a specific project.

### Solution Example

MCHS Trading uses Snapshot Provisioning to create linked information collections to support this analysis project. The team is able to change the channels that products are available through and understand how these changes could affect sales based on the knowledge of the channels that its customers work on.

### Benefits

- Creating dedicated information collections that are optimized to support a particular project will improve the efficiency of the project.

### Liabilities

- Every copy of an information collection that is created and distributed adds to the cost of maintaining the information supply chain. Ideally, the availability of the sandbox should be time boxed so the information can be properly disposed of and the storage freed up once the project is complete.

### Usage

Sandbox information collections are often used for analytics such as data mining. They are also test data sets when testing new information processes and services.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Complete Scope

### Qualified Name

DesignPattern::Complete Scope

### Category

Information Collection Patterns

### Description

Connect the information process to an information collection that stores a single information entry for each instance of the subject area that occurs within the information supply chain. Such an information collection is said to have a complete scope.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information collections are storing information throughout the information supply chain. The existence or absence of an information instance in a specific information collection will depend on the information processes that maintain it. How do we classify the scope of the information entries within an information collection?

### Problem Statement

An information process needs to perform an activity once for each instance of a particular subject area (such as customer, product, order, invoice, shipment, ...) that occurs within the information supply chain.

To do this, it needs a list of these instances.

### Problem Example

MCHS Trading wants to send a letter to every one of its customers to advertise some special offers it has.

### Forces

- In many organizations, it is common for information about the same subject area to be duplicated and distributed among multiple information collections. These information collections are used by different subsets of information processes and have become inconsistent over time. In these circumstances, without deliberate Information Provisioning, not all instances will appear in each of these information collections.

### Solution Description

Connect the information process to an information collection that stores a single information entry for each instance of the subject area that occurs within the information supply chain. Such an information collection is said to have a complete scope.

For example, for a collection of customers to have complete scope, it would include all customers for the organization.

Information collections with complete scope are very valuable in an information supply chain because they provide a place were information processes can work with a complete list of information entries for a subject area and they are an excellent place to distribute information from.

### Solution Example

Customer information in MCHS Trading's original set of applications is located in information collections hosted in the E-Shop and Stores applications. However, each of these information collections has local scope—covering only the customers who used the particular channel. Of course, some customers used both channels, and will appear in both information collections. Others may only use the Mail-Shop channels, which means their details are buried in the orders they have made in the past. The result is that there is no easy way to generate a list of people to send the letter to.

MCHS Trading adds a new information node called Customer Hub. This information node is an Information Asset Hub. Its responsibility is to maintain the authoritative source of customer details. As such, it hosts an information collection for customer details that has one entry for each of the individuals who has done at least one of the following:

- Registered on the E-Shop website
- Bought something through mail order or by calling the customer service number
- Registered for a store card This information collection has complete scope and is suitable to act as the list of customers to receive the letter.

### Benefits

- When an information collection has complete scope, it can be used to drive many information processes where the activity should be once and once only for each instance of a subject area.

### Liabilities

- Information collections with complete scope are typically provisioning from multiple information collections. There is an opportunity for duplicate entries to occur. These need to be regularly matched and consolidated to maintain the value of having the complete scope.

### Usage

You will see information collections with complete scope in either of the following situations:

- In an application that is exposed to every possible instance known to the organization as part of normal business
- Where Information Provisioning is used to explicitly introduce all known instances from the information supply chain to a specialized information node, such as an Information Asset Hub or Information Warehouse

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Local Scope

### Qualified Name

DesignPattern::Local Scope

### Category

Information Collection Patterns

### Description

Provide information collections within the information node for the sole use of its information processes. These information collections will then only have information entries that are created by the locally hosted information processes. These types of information collections are said to have a local scope.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information collections are storing information throughout the information supply chain. The existence or absence of an information instance in a specific information collection will depend on the information processes that update it. How do we classify the scope of the information entries within an information collection?

### Problem Statement

The implementations of the information processes hosted within an information node assume they are in complete control of changes to the information they use.

### Problem Example

The E-Shop application has information processes that need to store information about the people who have registered to use the E-Shop website. These details include their account identifier, password, default delivery address, and privacy preferences.

### Forces

- Many of the values used by these information processes are also required by other information processes, which may also be implemented as if they were the only activity updating the information.

### Solution Description

Provide information collections within the information node for the sole use of its information processes. These information collections will then only have information entries that are created by the locally hosted information processes. These types of information collections are said to have a local scope.

Periodically review and prune the information that is retained by the information node to keep it appropriately scoped.

### Solution Example

The E-Shop application has an information collection for customer details. Each entry in this information collection represents a customer who has registered to use the E-Shop website. Customers who only use the mail-order service are not listed in this information collection.

### Benefits

- The information collection only contains information that is relevant to the information processes that are using it.

### Liabilities

- The information collection will not reflect a complete picture from an organization's point of view.
- Information provisioning must be used with great care to synchronize new values stored in the local information collection with other parts of the information supply chain.

### Usage

Most applications host information collections with a local scope.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Transient Scope

### Qualified Name

DesignPattern::Transient Scope

### Category

Information Collection Patterns

### Description

Create an information collection to temporarily store the information entries in the information node. From time to time, the information entries stored in this information collection will change, and so we say this collection has transient scope.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information collections are storing information throughout the information supply chain. The existence or absence of an information instance in a specific information collection will depend on the information processes that update it. How do we classify the scope of the information entries within an information collection?

### Problem Statement

An information node needs to provide temporary storage for information entries that are being continuously added and removed by the information processes.

### Problem Example

New orders need to be passed from E-Shop, Mail-Shop, and Stores to Shipping. As part of the transfer process, the structure of the orders needs to be transformed to fit with the way Shipping expects to receive these orders.

### Forces

- Transferring data between two information nodes requires them to both be available at the same time.
- How do you ensure information added to temporary storage is on there temporarily?

### Solution Description

Create an information collection to store the information entries in the information node.

This information collection should implement an ordering mechanism for the information entries so that it is easy for the information processes to ensure complete handling of the transient information.

### Solution Example

A Queue Manager is used to pass orders from E-Shop, Mail-Shop, and Stores to Shipping. It uses transient scope information collections that contain the orders that are partway through the transfer process between the applications.

### Benefits

- With an information collection of transient scope, it easy to see how many information entries are yet to be processed.

### Liabilities

- Care must be taken to ensure information entries are added and removed with integrity to avoid losing or duplicating information entries. The information entries should also be processed in a timely manner.

### Usage

Information collections with transient scope typically occur as part of the implementation of Information Provisioning. These collections may be stored, for example, in memory, as a message, in a temporary spreadsheet, or in Staging Areas during the life of an extract, transform, load (ETL) process.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Complete Coverage

### Qualified Name

DesignPattern::Complete Coverage

### Category

Information Collection Patterns

### Description

Create an information collection that supports all of the attributes for the subject area.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An organization needs an information collection that can store all attributes that are known about a subject area.

### Solution Description

Create an information collection that supports all of the attributes for the subject area.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Core Coverage

### Qualified Name

DesignPattern::Core Coverage

### Category

Information Collection Patterns

### Description

Create an information collection that supports the minimal set of attributes necessary to understand the critical values that identify each unique instance within the subject area.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An organization needs an index of the instances of a particular subject area.

### Solution Description

Create an information collection that supports the minimal set of attributes necessary to understand the critical values that identify each unique instance within the subject area.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Extended Coverage

### Qualified Name

DesignPattern::Extended Coverage

### Category

Information Collection Patterns

### Description

Create an information collection that supports the minimal set of attributes necessary to understand the essence of each instance within the subject area plus any additional attributes needed by the consuming information processes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An organization needs an information collection that can store all of the attributes required by a diverse range of information processes.

### Solution Description

Create an information collection that supports the minimal set of attributes necessary to understand the essence of each instance within the subject area plus any additional attributes needed by the consuming information processes.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Local Coverage

### Qualified Name

DesignPattern::Local Coverage

### Category

Information Collection Patterns

### Description

Create an information collection that just has the attributes to support the consuming information processes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An information node needs to store the attributes used by its locally hosted information processes.

### Solution Description

Create an information collection that just has the attributes to support the consuming information processes.

### Search Keywords

- Patterns of Information Management
- Information Collection
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Entry

### Qualified Name

DesignPattern::Information Entry

### Category

Information Entry Patterns

### Description

Organize the information collection so each instance is stored as a distinct entry that can be retrieved and maintained independently through the information collection's information services.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information collection is a logical grouping of related information.

### Problem Statement

Distinct instances of a subject area need to be stored in an information collection.

Each instance of a subject area will have multiple information values associated with them. These values are characterized by attributes. The attributes define the types of the information values that are to be stored.

### Problem Example

The MCHS Trading E-Shop application stores information about its customers in its customer details information collection. How is information about each individual customer organized to ensure information about different people is not mixed together?

### Forces

- Unique instances of information must be distinct—Information about each individual instance of a subject area needs to be kept distinct while managed in a consistent manner with the other instances.
- Instances must be identifiable—An individual instance needs to be identifiable from other instances.
- Instances must have correct values—An individual instance needs to contain valid values.
- Same change may require propagation to all instances—Sometimes the same change needs to be made to all instances within a subject area.
- Distinct instances may need to be grouped or summed—Sometimes it is important to know how many distinct instances are known about so they may be either counted or categorized.
- Support may be necessary to meet service agreements—Large, complex, and highly valuable information requires special support to ensure it can be accessed within agreed service levels.
- Majority of information is unstructured—Most electronic information today is unstructured data such as documents, images, and video.
- Different processes may use the same information instance—The same instance of a subject area may be used by information processes on different information nodes. This can result in it being stored multiple times and the values becoming out of synchronization.

### Solution Description

Organize the information collection so each instance is stored as a distinct entry that can be retrieved and maintained independently through the information collection's information services.

There are a number of ways to structure an entry within an information collection. Some of them are covered by the Static Structure, Dynamic Structure, Entry-Level Structure, and Tagged Media Structure patterns. Whatever the approach, the structure provides some constraints on what can be stored in the entry. These constraints can be quite strict, forcing an information process that is creating or updating the values to conform to predefined standards.

The information collection then supports Local Information Services that provide the operations that can be performed on the information entries. Operations would typically include the following:

- Retrieving a subset of information entries that match a certain criteria
- Retrieving, creating, updating, or deleting a specific information entry
- Iterating over the whole collection, or a subset, to perform an operation When an information process is updating an information entry, it should lock it while the update is in progress. Approaches to locking an information entry are described by the Local Locking, Distributed Locking, and Optimistic Locking patterns. In addition, the other information entry patterns define some more specialized operations. These patterns are Lifecycle States, Unique Entries, Deferred Update, Soft Delete, Proxy, Provenance, Historical Values, and Relationships.

### Solution Example

The MCHS Trading E-Shop application requires that a given customer create an account name and password when ordering as well as a shipping address, phone number, email address, and credit card information. Each customer account name serves as a unique Information Key, and a given customer account name can only occur once—other customers attempting to create an account with the same account name are informed that they must create a different account name.

MCHS Trading realizes that a given customer may, in fact, use another family member's account name or create multiple account names (often because they forgot they already created one). They do not attempt to resolve this in the E-Shop application, but deliver all customer account names and information to the Customer Hub for resolution and consolidation, if appropriate.

### Benefits

- Well-defined structured information entries with strong enforcement of valid values within them simplify the work of an information process that is consuming the information because they can make assumptions about the meaning and quality of the information.

### Liabilities

- Over time, the requirements covering the types of information that should be stored will change, and as a result, the implementation of the information collection will have to be updated and the existing information migrated to the new structure.

### Usage

The information entry pattern describes how structured information stores are organized. For example,

- When a database table is being used to store an information collection, an entry is stored in a row in that table.
- When a file is used to store an information collection, a record (or row) is often used to represent an information entry.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Caller's Key

### Qualified Name

DesignPattern::Caller's Key

### Category

Information Entry Patterns

### Description

For each entry, store the appropriate key from the remote information collection along with the identifier of the remote information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

When the unique identifiers for a collection of information entries change because they are moved to a new information collection, how are the references to them (which use the original unique identifiers and are stored in related information collections) reconciled with the unique identifiers in the new source of information?

### Solution Description

For each entry, store the appropriate key from the remote information collection along with the identifier of the remote information collection.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Key

### Qualified Name

DesignPattern::Information Key

### Category

Information Entry Patterns

### Description

Either use one (or more) of the attributes of the information entry or add a new attribute and assign a unique value to it.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Entry typically represents something discrete—for example, a concept, person, thing, event, or activity—that is also documented in other information collections owned by the organization. Customers, suppliers, external publications, and other sources often refer to it outside of the organization, too.

### Problem Statement

An information entry needs a unique identifier.

Most pieces of information, though not necessarily all, have some form of identification. We recognize people by name; where names are the same, we look for additional identifications, such as date and place of birth, national or tax IDs, or place of residence. People can make this adjustment. IT systems are less flexible.

Ensuring each information entry has a unique identifier speeds up retrieval and ensures links between information entries are definitive.

### Problem Example

MCHS Trading must have a unique identifier for each order it takes so it can coordinate the processing of the order, and answer questions about it from the customer.

### Forces

- Multiple ways to identify a particular piece of information often exist in the real world—These are often not completely unique. For example, there are many people who have the same name—particularly those in the same family, possibly at the same address.
- Many information collections use their own scheme for identifying their information entries—These are rarely globally unique. This is particularly true of information collections implemented in applications where Local Provisioning is assumed.
- Incomplete or incorrect data may result in incorrect identification and labeling of information entries.

### Solution Description

Either use one (or more) of the attributes of the information entry or add a new attribute and assign a unique value to it.

The information key consists of one or more attributes in the information entry that together will uniquely identify the information entry. See Figure 5.25. collection.

### Solution Example

Each of the MCHS Trading order-taking systems (E-Shop, Mail-Shop, and Stores) will assign a locally unique identifier to an order when it is created. This identifier is only unique within the scope of the originating application. When the order is sent from the order-taking systems to Shipping, a code name of the source information node is added to the information keys to guarantee they are unique across the enterprise. In addition, Mail-Shop uses a recycled key and so its keys must be augmented with a time stamp before being sent to Shipping.

### Benefits

- Information keys provide a unique identifier for an information entry. Having a unique identifier is useful to be sure that people and systems are referring to the same instance, both for retrieving the right stored information or linking between information entries.

### Liabilities

- Unique keys are typically generated based on a local counter or using the system clock and as a result, most keys are only unique within the scope of a single information collection. This can create an interesting challenge when matching up information from different information collections.

### Usage

Unique identifiers are typically termed keys, which is where the name of this pattern comes from. For example, database systems use a particular nomenclature of primary, foreign, and natural keys. These terms refer to the style of key in use in an information entry:

- Primary key is the unique key that identifies an information entry.
- Foreign key is the unique identifier of another information entry that this information entry is linked to.
- Natural key refers to the use of existing attributes as the information key. This is described in the Natural Key pattern.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Local Key

### Qualified Name

DesignPattern::Local Key

### Category

Information Entry Patterns

### Description

Assign a unique identifier as an additional attribute in the information entry using a local counter or a time-based value.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Entry typically represents something discrete—for example, a concept, person, thing, event, or activity—that is also documented in other information collections owned by the organization. Customers, suppliers, external publications, and other sources often refer to it outside of the organization, too. Having a unique identifier for each information entry is useful to be sure that people and systems are referring to the same instance, both for retrieving the right stored information or linking between information entries.

### Problem Statement

An information node needs to uniquely identify each entry in an information collection for its own internal use.

### Problem Example

The E-Shop application needs to assign a unique identifier to an order when the order is created.

### Forces

- Multiple ways to identify a particular piece of information often exist in the real world—These are often not completely unique. For example, there are many people who have the same name—particularly those in the same family, possibly at the same address.
- Many information collections use their own scheme for identifying their information entries—This is particularly true of information collections implemented in applications where Local Provisioning is assumed.
- Incomplete or incorrect data may result in incorrect identification and labeling of information entries.
- Many applications are designed with only local scope in mind—This can cause issues in ensuring unique identifiers when information is distributed beyond its original scope.

### Solution Description

Assign a unique identifier as an additional attribute in the information entry using a local counter or a time-based value.

This is stored as an additional attribute in the information entry. It may simply be a counter, or something that includes a time stamp or local machine identifier. The information node assigns the local key when the information entry is created and it is always bound to that information entry. The value of the key bears no relationship to other values in the information entry. It will be unique within the information collection and meaningful only while the information entry exists. When the information entry is deleted, the key value is never reused. Because of this, it is possible to pass local keys across the information service interface and even store them on other information collections to show a relationship (or link) to the information entry. See Figure 5.26.

Every entry in the information collection must use the same attributes to represent its information key. If there is an Information Schema for the information entry structure, it often indicates which attributes are used for the key.

### Solution Example

E-Shop uses the next number in a sequence as a unique identifier for each new order.

### Benefits

- Local keys allow specific applications or processes to uniquely identify an information entry within the scope of an information collection.

### Liabilities

- Local keys are not unique outside the scope of the information collection.

### Usage

Local keys are the most common approach to creating unique identifiers for information entries. They may be stored in cross-reference files or tables and used in lookup functions by multiple applications, systems, or services.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Recycled Key

### Qualified Name

DesignPattern::Recycled Key

### Category

Information Entry Patterns

### Description

Reuse keys previously allocated to information entries that have since been deleted, starting with the oldest first.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Entry typically represents something discrete—for example, a concept, person, thing, event, or activity—that is also documented in other information collections owned by the organization. Customers, suppliers, external publications, and other sources often refer to it outside of the organization, too. Having a unique identifier for each information entry is useful to be sure that people and systems are referring to the same instance, both for retrieving the right stored information or linking between information entries.

### Problem Statement

An information node is running out of unique keys to assign to new information entries in an information collection.

This is particularly common in older systems where the data structure used to store the information key is of limited size.

### Problem Example

MCHS Trading's Mail-Shop application is its first application. It was developed in-house with a limited budget when the company was starting up. Each order it records is given the next order number in sequence. The order number is stored in a 3-byte field. When the next order number will overflow this 3-byte field, the sequence starts again at 1. As a result, every couple of months or so, the order numbers recycle.

### Forces

- Multiple ways to identify a particular piece of information often exist in the real world—These are often not completely unique. For example, there are many people who have the same name—particularly those in the same family, possibly at the same address.
- Many information collections use their own scheme for identifying their information entries—This is particularly true of information collections implemented in applications where Local Provisioning is assumed.
- Incomplete or incorrect data may result in incorrect identification and labeling of information entries.
- Many applications are designed with only local scope in mind—This can cause issues in ensuring unique identifiers when information is distributed beyond its original scope.

### Solution Description

Reuse keys previously allocated to information entries that have since been deleted, starting with the oldest first.

A recycled key is similar to a Local Key, except that it is reused. At any one time, each key uniquely identifies an information entry. However, a historical view shows multiple information entries mapping to the same recycled key value. See Figure 5.27.

### Solution Example

The Mail-Shop application is recycling its information keys for orders fairly rapidly. Its Infrastructure Operators ensure that older orders are archived out of its order details information collection on a regular basis so that the application does not run out of unused key values. Then the order is sent to the Shipping application for processing; it is prepended with the order date and time to ensure it is globally unique, even when the information key is recycled in the Mail-Shop application.

### Benefits

- The life of the application is extended because it does not run out of unique key values. The alternative is often an expensive redesign of the key management capability of the application to extend the range of the information key values.

### Liabilities

- This scheme is manageable in the local information node. However, when this key is distributed, it must be extended with a time stamp or similar counter so that an information entry can be distinguished from previous, and future, uses of the same key value.
- It is important to monitor how frequently the key recycles to ensure the information node does not run out of free keys. Obsolete information entries need to be removed frequently enough to maintain plenty of free slots.

### Usage

Recycled keys are used in older applications where the storage was at a premium and large key values would have been expensive to store and maintain. In the public domain, telephone numbers are recycled keys.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Natural Key

### Qualified Name

DesignPattern::Natural Key

### Category

Information Entry Patterns

### Description

It is safe to use this existing identifier to solely identify an information entry if it can be guaranteed to always be both stable and unique into the future.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Entry typically represents something discrete—for example, a concept, person, thing, event, or activity—that is also documented in other information collections owned by the organization. Customers, suppliers, external publications, and other sources often refer to it outside of the organization, too. Having a unique identifier for each information entry is useful to be sure that people and systems are referring to the same instance, both for retrieving the right stored information or linking between information entries.

### Problem Statement

An information entry being created by an information process represents an object that already has one or more unique identifiers by which it is known in the real world.

Is it possible to make use of one of these unique identifiers as the information key for an information collection? This would make it easy to locate the information entry when the request comes from an external party.

### Problem Example

MCHS Trading's E-Shop application needs to create an information entry to store the account details of a customer registered with its online shopping website. Each customer must have his or her own unique account name (as well as an email address) for confirming orders and other related communication.

### Forces

- Multiple ways to identify a particular piece of information often exist in the real world—These are often not completely unique. For example, there are many people who have the same name—particularly those in the same family, possibly at the same address.
- Many information collections use their own scheme for identifying their information entries—This is particularly true of information collections implemented in applications where Local Provisioning is assumed.
- Incomplete or incorrect data may result in incorrect identification and labeling of information entries.
- Information may be overloaded with local data—Organizations may reuse natural keys for specific local processing purposes, resulting in incorrect identification of information entries.
- Many applications are designed with only local scope in mind—This can cause issues in ensuring unique identifiers when information is distributed beyond its original scope.

### Solution Description

Use the existing unique identifier as the information key for entries in this collection.

This unique identifier may already be stored in the information entry as one or more attributes. See Figure 5.28.

### Solution Example

MCHS Trading decides to use the customers' email addresses as their login names. This has the advantage that it is unique and the customer should be able to remember it easily. The disadvantage is that many customers change email addresses frequently (as they change providers or use new services), and some customers use the same email address for multiple members of a household, reducing its uniqueness.

### Benefits

- The implementation of a natural key makes it easier to retrieve the right information entry based on information from an external system or person. For example, natural keys are useful when interacting with members of the public because it is easier for them to remember the number.

### Liabilities

- Natural keys are often outside the control of the organization and may be prone to change or incorrect usage leading to duplicate information entries for the same piece of information or incorrectly linked information entries for distinct pieces of information.

### Usage

Examples of natural keys are as follows:

- For people—Their name, email address, passport number, driver's license number, tax identification number, and (sometimes) physical address or mobile phone number (though these latter are recycled in the context of individuals so must be treated with caution as natural keys)
- For organizations—The DUNS number, the legal entity name
- For products—Universal Product Code (UPC), stock-keeping unit (SKU), International Standard Book Number (ISBN)
- For assets—Serial number, make + model + date purchased
- For locations—Physical address, geospatial coordinates (latitude/longitude)

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Mirror Key

### Qualified Name

DesignPattern::Mirror Key

### Category

Information Entry Patterns

### Description

Use the same keys as the source.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Entry typically represents something discrete—for example, a concept, person, thing, event, or activity—that is also documented in other information collections owned by the organization. Customers, suppliers, external publications, and other sources often refer to it outside of the organization, too. Having a unique identifier for each information entry is useful to be sure that people and systems are referring to the same instance, both for retrieving the right stored information or linking between information entries.

### Problem Statement

What is the appropriate scheme for identifying the information entries in a new information collection that is provisioned from an existing information collection?

### Problem Example

MCHS Trading's Shipping application is receiving orders from E-Shop, Mail-Shop, and Stores. What key value should it use for each product in an order?

### Forces

- Multiple ways to identify a particular piece of information often exist in the real world—These are often not completely unique. For example, there are many people who have the same name—particularly those in the same family, possibly at the same address.
- Many information collections use their own scheme for identifying their information entries—This is particularly true of information collections implemented in applications where Local Provisioning is assumed.
- Incomplete or incorrect data may result in incorrect identification and labeling of information entries.
- Many applications are designed with only local scope in mind—This can cause issues in ensuring unique identifiers when information is distributed beyond its original scope.

### Solution Description

Use the same keys as the source.

### Solution Example

Shipping uses the key value located in the "order-id" attribute of the order Information Payload it receives from the order-taking applications. This is based on the key value used when the order was created in the originating application. The initial key value is augmented in the Information Flow with a code value that indicated which order-taking application created the order. In addition, the Mail Shop's key value is also augmented with a time stamp because Mail-Shop uses a Recycled Key.

### Benefits

- The mirror key is a simple approach that avoids the need to store mappings between the source and destination information keys.

### Liabilities

- If the source information node supports multiple keys per information entry (because, for example, it is supporting Stable Key or Caller's Key), then the destination information node may need to do one of the following if the information keys from the destination are saved in other information collections:
- Support multiple keys per information entry.
- Duplicate information entries so that there is a copy for each key.
- Pick one of the keys to use.

### Usage

Mirror key is a common pattern used when information is being distributed.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Aggregate Key

### Qualified Name

DesignPattern::Aggregate Key

### Category

Information Entry Patterns

### Description

Assign a new unique key value to the aggregated record.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Entry typically represents something discrete—for example, a concept, person, thing, event, or activity—that is also documented in other information collections owned by the organization. Customers, suppliers, external publications, and other sources often refer to it outside of the organization, too. Having a unique identifier for each information entry is useful to be sure that people and systems are referring to the same instance, both for retrieving the right stored information or linking between information entries.

### Problem Statement

What should be the identity of an information entry that is derived by dynamically combining information values from multiple sources, all of which use different key values?

### Problem Example

MCHS Trading's Customer Hub is receiving customer details from a variety of systems. What should it use as an information key for the customer details information entries it stores?

### Forces

- Multiple ways to identify a particular piece of information often exist in the real world—These are often not completely unique. For example, there are many people who have the same name—particularly those in the same family, possibly at the same address.
- Many information collections use their own scheme for identifying their information entries—This is particularly true of information collections implemented in applications where Local Provisioning is assumed.
- Incomplete or incorrect data may result in incorrect identification and labeling of information entries.
- Many applications are designed with only local scope in mind—This can cause issues in ensuring unique identifiers when information is distributed beyond its original scope.

### Solution Description

Assign a new unique key value to the aggregated record.

This unique key has no relationship to the information keys used in the source information nodes. This is because the information keys from the sources are likely to be Local Keys and not unique beyond the scope of their information collection. See Figure 5.29.

### Solution Example

In addition to its locally assigned customer ID, the Customer Hub also stores the information keys from the E-Shop and Stores applications when it receives information about a customer from them. Figure 5.32 shows the consolidated information in information entry 25802823. This information entry can be accessed either using 25802823 or using either of the account numbers as long as the account type is also supplied.

### Benefits

- Caller's keys allow a remote information node to use its own unique key to access equivalent information in the local information collection.

### Liabilities

- Caller's keys require a mechanism to associate the keys from the calling systems with the keys from the local system. This should be done dynamically when each remote information node shares information.

### Usage

Master Data Management (MDM) hubs should support caller's keys to simplify the retrieval of the information it manages from remote information nodes. Information exchanges with external third parties typically need caller's keys.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Stable Key

### Qualified Name

DesignPattern::Stable Key

### Category

Information Entry Patterns

### Description

Ensure an information entry that has been formed from the merging of two other entries is still returned with either one of the keys from the merged records.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An Information Entry typically represents something discrete—for example, a concept, person, thing, event, or activity—that is also documented in other information collections owned by the organization. Customers, suppliers, external publications, and other sources often refer to it outside of the organization, too. Having a unique identifier for each information entry is useful to be sure that people and systems are referring to the same instance, both for retrieving the right stored information or linking between information entries

### Problem Statement

An information node is merging and restructuring information entries while remote information nodes are retrieving specific information entries.

What information key should a remote information process use to retrieve information after the information entry has been merged with another?

### Problem Example

MCHS Trading wants to have a single information entry in its Customer Hub for each individual customer. The customer information is supplied from E-Shop, Mail-Shop (in new orders), and Stores. Details about an individual customer may come in independently from each of these three applications and be stored in separate information entries. Subsequent processing in the Customer Hub may detect these duplicate entries and merge them together. What is the customer's identifier (CID) before and after the merge?

### Forces

- Multiple ways to identify a particular piece of information often exist in the real world—These are often not completely unique. For example, there are many people who have the same name—particularly those in the same family, possibly at the same address.
- Many information collections use their own scheme for identifying their information entries—This is particularly true of information collections implemented in applications where Local Provisioning is assumed.
- Incomplete or incorrect data may result in incorrect identification and labeling of information entries.
- Many applications are designed with only local scope in mind—This can cause issues in ensuring unique identifiers when information is distributed beyond its original scope.

### Solution Description

Ensure an information entry that has been formed from the merging of two other entries is still returned with either one of the keys from the merged records.

The consolidation (or subsequent splitting) of multiple information entries requires consistent access to any of the individual entries over time, as seen in Figure 5.33.

### Solution Example

When information entries in the Customer Hub are consolidated, the consolidated information entry is given a new unique information key and the keys from the original information entries are associated with the new information entry as stable keys. An information process can retrieve the new information entry using either the new key or the stable keys.

Figure 5.34 shows the merging of two customer records: 57293200 and 25802823. A new information entry called 75828499 is created, which can be accessed using any of these keys: 57293200, 25802823, or 75828499. Because the Customer Hub supports caller's key, it can also be accessed using the account identifiers as long as the account type is also supplied.

### Benefits

- Stable keys enable an information node that is accessing the information collection through its information services to save the key in another collection as a method of linking together related information entries in different information collections.

### Liabilities

- Because stable keys must be maintained over time in a consistent fashion, it can be expensive to change or introduce stable keys. Where stable keys cannot be introduced, other keys must be translated, mapped, and linked to simulate stable key support, usually in cross-reference files. Maintenance of such cross-references can be time consuming and prone to error.

### Usage

Stable keys are typically stored in Master Data Management (MDM) hubs that are merging and splitting information entries.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Dynamic Structure

### Qualified Name

DesignPattern::Dynamic Structure

### Category

Information Entry Patterns

### Description

Provide an interface on the information node to add new optional attributes to an information collection's data schema. Use self-describing data structures on external interfaces with the ability to query the schema.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

The structure of the information entries in an information collection must expand over time without requiring development effort.

### Solution Description

Provide an interface on the information node to add new optional attributes to an information collection's data schema. Use self-describing data structures on external interfaces with the ability to query the schema.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Entry-Level Structure

### Qualified Name

DesignPattern::Entry-Level Structure

### Category

Information Entry Patterns

### Description

Enable an Information Schema to be associated with one or a group of information entries within an information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Each entry in an information collection must be structured differently.

### Solution Description

Enable an Information Schema to be associated with one or a group of information entries within an information collection.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Static Structure

### Qualified Name

DesignPattern::Static Structure

### Category

Information Entry Patterns

### Description

Use a predefined static data schema that governs how the values in an information entry are formatted. Use the schema consistently for all entries. Embed the data schema in the information store and use it for all access to the information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

The values stored in an information entry need to be accessed with minimum processing.

### Solution Description

Use a predefined static data schema that governs how the values in an information entry are formatted. Use the schema consistently for all entries. Embed the data schema in the information store and use it for all access to the information collection.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Tagged Media Structure

### Qualified Name

DesignPattern::Tagged Media Structure

### Category

Information Entry Patterns

### Description

Create a set of structured "tags" that describe the characteristics of the unstructured data.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Each entry in an information collection contains what is called unstructured data, for example, text, documents, audio, or video. We call this information unstructured, but it does have some structure to it.

### Solution Description

Create a set of structured "tags" that describe the characteristics of the unstructured data.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Distributed Locking

### Qualified Name

DesignPattern::Distributed Locking

### Category

Information Entry Patterns

### Description

Provide a pessimistic locking scheme in each of the called information nodes that can be controlled by the calling information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An information node needs to coordinate changes to information in multiple information nodes.

### Solution Description

Provide a pessimistic locking scheme in each of the called information nodes that can be controlled by the calling information node.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Lifecycle States

### Qualified Name

DesignPattern::Lifecycle States

### Category

Information Entry Patterns

### Description

Use a state machine to model the life cycle of an archetypal information entry in the information collection. For each entry, record its current state. When an operation is issued against an entry, its state is checked to ensure the operation is allowed at this time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Not all operations on an information entry are valid all of the time.

### Solution Description

Use a state machine to model the life cycle of an archetypal information entry in the information collection. For each entry, record its current state. When an operation is issued against an entry, its state is checked to ensure the operation is allowed at this time.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Local Locking

### Qualified Name

DesignPattern::Local Locking

### Category

Information Entry Patterns

### Description

Provide the ability for an information process to lock information entries locally within the information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An information node needs to ensure each process it is performing in parallel works with consistent information during its lifetime.

### Solution Description

Provide the ability for an information process to lock information entries locally within the information collection.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Optimistic Locking

### Qualified Name

DesignPattern::Optimistic Locking

### Category

Information Entry Patterns

### Description

Use an optimistic locking scheme where the update() operation passes in the time stamp of the information entry when it retrieved it. If no changes have been made since then, the update() succeeds. Otherwise, it is rejected.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

When an occasional change is made to an information entry, it should have minimal performance impact on the frequently occurring read operations.

### Solution Description

Use an optimistic locking scheme where the update() operation passes in the time stamp of the information entry when it retrieved it. If no changes have been made since then, the update() succeeds. Otherwise, it is rejected.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Deferred Update

### Qualified Name

DesignPattern::Deferred Update

### Category

Information Entry Patterns

### Description

Prepare the changes in the information collection and program them to become active at the required date and time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Changes need to happen to an information entry at a certain point in time.

### Solution Description

Prepare the changes in the information collection and program them to become active at the required date and time.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Historical Values

### Qualified Name

DesignPattern::Historical Values

### Category

Information Entry Patterns

### Description

Keep all versions of the data and provide temporal queries to be able to access the values for any point in time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

What were the values of an information collection at a certain point in time in the past?

### Solution Description

Keep all versions of the data and provide temporal queries to be able to access the values for any point in time.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Provenance

### Qualified Name

DesignPattern::Provenance

### Category

Information Entry Patterns

### Description

Record details of the originating source, provisioning mechanism, and time of creation or update with the entry.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Where did the values from an information entry come from?

### Solution Description

Record details of the originating source, provisioning mechanism, and time of creation or update with the entry.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Proxy

### Qualified Name

DesignPattern::Proxy

### Category

Information Entry Patterns

### Description

Use an information service to retrieve the remote values whenever the entry is requested.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Some of the values for an information entry are located in a remote information node.

### Solution Description

Use an information service to retrieve the remote values whenever the entry is requested.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Relationships

### Qualified Name

DesignPattern::Relationships

### Category

Information Entry Patterns

### Description

Create relationship services and information collections to support different patterns of grouping and linking information entries together.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

How are the groups and relationships between individuals, organizations, things, and events represented in the information supply chain?

### Solution Description

Create relationship services and information collections to support different patterns of grouping and linking information entries together.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Soft Delete

### Qualified Name

DesignPattern::Soft Delete

### Category

Information Entry Patterns

### Description

Mark the entry as deleted so it no longer appears in normal operational queries. Keep the entry in the information collection, or move it to a separate information collection for the required retention period.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An entry is no longer needed operationally but must be kept for legal or reporting reasons.

### Solution Description

Mark the entry as deleted so it no longer appears in normal operational queries. Keep the entry in the information collection, or move it to a separate information collection for the required retention period.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Unique Entries

### Qualified Name

DesignPattern::Unique Entries

### Category

Information Entry Patterns

### Description

Add a search function to the add() and update() operations to determine if the entry already exists in the information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An organization does not want duplicate entries in an information collection.

### Solution Description

Add a search function to the add() and update() operations to determine if the entry already exists in the information collection.

### Search Keywords

- Patterns of Information Management
- Information Entry
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Node

### Qualified Name

DesignPattern::Information Node

### Category

Information Node Patterns

### Description

Related information processes and information collections should be hosted together in a server.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

You are designing an information supply chain and have a view on the information processes and information collections that are involved. The next question to consider is what type of IT infrastructure they should run on. This may be IT infrastructure that already exists or new.

This pattern language does not go into depth on how to design IT infrastructure for an information supply chain, but it does cover the basic notions of where information and the processes that operate on it are located because it affects the availability and efficiency of the information supply chains.

### Problem Statement

What is the appropriate IT infrastructure to host information collections and information processes?

### Problem Example

MCHS Trading is creating new customer care information processes that provide support for its customer-facing staff across all of the sales channels. Where should these new information processes run?

### Forces

- IT infrastructure takes resources—Needed resources include the power, space, and human effort to maintain the IT infrastructure.
- IT infrastructure is not always available—The IT infrastructure fails at inopportune moments and is also taken out of service from time-to-time for maintenance.
- Ownership of IT infrastructure is distributed—The IT infrastructure for an organization may be split up and managed by different groups, each providing different levels of service.
- IT infrastructure is specialized—The type of IT infrastructure required will depend on the type of workload the information processes are performing against the information collections.
- IT infrastructure needs specialists—Each type of IT infrastructure typically needs a specialist to maintain it.

### Solution Description

Related information processes and information collections should be hosted together in a server.

The server provides the execution environment for the information processes and collections. It also supports the Information Node Management Process to enable Infrastructure Operators to control the availability of the server (and, hence, the availability of the information processes and collections).

The server also provides the implementations of the Information Service capabilities that enable an information process to access the information collections that are either in the local information node or remote from it.

Figure 5.35 is a schematic of a typical information node. A specialized type of information node may contain a subset of these components, or specialize on a particular type of process or information. The numbers on the diagram refer to these notes:

1. An infrastructure operator has user interfaces and command-line capability to manage the information node (through the information node management process); to schedule information processes for later, or periodic, execution (through the Scheduling Process) and run any other locally hosted information processes they have permission to use.
2. Other types of information users are also interacting through user interfaces with information processes running on the information node.
3. The information processes are accessing information through information services.
4. The Local Information Services provide interfaces to the information collections hosted on the local information node.
5. The Remote Information Services call Information Requests to connect to information services on other information nodes.
6. When a local information collection is changed, it may be configured with an Information Change Trigger that initiates an information process locally. This new process may simply call a Remote Information Service to notify another information node that the change occurred. This could be part of an Information Supply Chain.
7. This shows an information process using an Information Trigger to start another information process on the information node.
8. The Scheduling Process uses the Scheduled Information Trigger when it is time to initiate an information process.
9. The Archiving Process is responsible for removing unwanted information values from the local information collections. The scheduling process initiates this process at regular intervals.
10. Whenever the information users want to start a new information process, they may type in a command or select an option from the user interface and this results in a Manual Information Trigger starting the desired information process.
11. An information process in another information node may use a remote information service to call a Triggered Information Service hosted locally.
12. The triggered information service will use the Information Service Trigger to start the requested information process.
13. A remote information service may alternatively call a local information service to access one of the local information collections. As you can see, most of the work of the information node is in triggering information processes and providing access to information. The distinguishing features of each of the variations of the information node patterns are the type of information processes that they support and the type of information they store in the information collections.

### Solution Example

Because the existing order-taking applications are only focused on a single channel, and their customer information collections only cover the customer using that channel, they are not suitable places for the new customer care information processes. MCHS Trading decides to install a new information node called Customer-Care to host these information processes. These information processes use Remote Information Services to access the customer information in the Customer Hub information node.

### Benefits

- Related information processes and information collections may be collocated, giving efficient operation. The server infrastructure around them enables their availability to be managed.

### Liabilities

- An information node takes effort to maintain, so there is often savings to be made by consolidating as many information processes and collections together into a single information node. However, this will increase the criticality of this node and so the cost of change can become high. Note: Multiple information nodes can be hosted on a single physical machine, or split across a cluster of networked machines.

### Usage

Examples of information nodes include application servers, bespoke applications, database servers, data warehouses, workflow engines, Master Data Management servers, ETL engines, enterprise service buses, search engines, and many more.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Application Node

### Qualified Name

DesignPattern::Application Node

### Category

Information Node Patterns

### Description

Host these information processes and information collections together in their own server. Ensure the server is available when the information users supporting this part of the business need it.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

A set of information processes, and their related information collections, provides support for a particular aspect of an organization's core business. These information processes must all be available when the information users need them and they need to be managed and maintained consistently.

### Problem Statement

What is the appropriate infrastructure to host information collections and information processes that collectively support a particular aspect of the business?

### Problem Example

MCHS Trading has an online shopping website that allows people to create an online account, browse and search the product catalog, and make orders. All of the information processes that support this website need to be available all of the time.

### Forces

- Information processes, and the information collections they depend on, must be available when their users need them—For example, if office workers in a single location are the only people to use a group of information processes, then these information processes may only be required during office hours. If, however, the information processes, or the information collections, are used by people all over the world, then they must be available 24 hours each day, and given the weekend varies from country to country, they may be needed 6–7 days a week as well.
- The logic inside an information process can be complex and require specialized knowledge to create—If this knowledge is outside of the core competency of an organization, the organization may choose to buy the implementation of these information processes as a software package. Such a software package will typically include the required information collections together with the information processes.

### Solution Description

Host the information processes and information collections together on their own server. Ensure the server is available when the information users supporting this part of the business need it.

Figure 5.36 shows the structure of an application node. You can see it follows the information node very closely. The numbers on the diagram in Figure 5.36 refer to these notes:

1. Application nodes are managed by the Infrastructure Operators using the Information Node Management Process.
2. The users of the majority of information processes running on the application node are used by Information Workers.
3. The information processes are focused on one function of the business.
4. Much of the information in use is locally hosted on the application node.
5. The information collections typically have Master Usage, Local Scope, and Local Coverage. Figure 5.37 shows the interaction of an application node with other information nodes. The numbers on the diagram in Figure 5.37 refer to these notes:
1. This is the application node itself.
2. There are other information nodes exchanging information with it using information services.
3. The application node may export or import information to/from an information store. Other information nodes could use this information store as an information-sharing mechanism.
4. The application node may pass messages to/from a Queue Manager information node. The queue manager may distribute these messages further. This is a useful approach to distribute updates and alerts as they happen.
5. Information may be passed in an out of the application node via an Information Broker that is implementing an Information Flow.

### Solution Example

The information processes and information collections that support the online shopping website are all hosted in an application node called E-Shop.

### Benefits

- A separate application node supporting a localized group of people, specialized for their needs, can be managed and made available to them with a high degree of reliability because the needs are well defined.

### Liabilities

- The people using an application node typically have a very localized view of the organization. The information collections managed by the application node typically require synchronization with other information collections to keep them in line with the rest of the organization.

### Usage

This pattern is a very common approach for grouping and managing related processes together. For example,

- A packaged application is an application node, running information processes that follow the Packaged Application Process pattern, with Local Provisioning of information collections that have a Master Usage.
- A homegrown application is very similar. It consists of an application node running information processes that follow the Bespoke Application Process pattern, with Local Provisioning of information collections that have a Master Usage.
- If you are using a workflow, or business process management software, then its runtime environment is an application node running information processes that support information processes following the Agile Business Process, State Driven Process, and/or Collaborative Editing Process patterns.
- If you are an information user who is using either the Information Monitoring Process or Operational Health Monitoring Process, then these processes will be hosted on an application node that has information collections containing the Information Events that describe what is going on in the information supply chains.
- If you are an information user who is browsing business reports, an Information Reporting Process running on an application node would have produced these reports.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Content Node

### Qualified Name

DesignPattern::Information Content Node

### Category

Information Node Patterns

### Description

Use a specialized information node that is able to maintain an index and related metadata around the documents and media files.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The fastest growing type of information is what is called unstructured. This includes documents, web pages, text files, video and audio files, and images. It requires different approaches to manage it because the information values within it are dispersed and hard to identify.

### Problem Statement

What is the appropriate infrastructure for managing large collections of documents and other types of media files?

### Problem Example

MCHS Trading needs to maintain documents relating to its contracts and other agreements plus images of products and services that are used in a variety of places. How does it catalog and manage these files?

### Forces

- Documents and media files are unstructured—Specific information values have to be discovered through parsing or inference.
- Documents and media files have limited useful lifetime—They need to be managed from creation to destruction.
- Documents and media files take up a lot of storage—Reducing the number of copies of the files and destroying them once they are no longer needed helps to minimize the amount of storage.
- Regulations define retention period—Some information must be retained for a defined period based on governmental or legal regulations. Keeping information longer than required is a liability.

### Solution Description

Use a specialized information node that is able to maintain an index and related metadata around the documents and media files.

This node is called the information content node. It stores the unstructured information and assigns classifications, such as tags and keywords, owners, descriptions, and a life cycle to each document/file to control how it is managed.

What makes this type of node special is that the information collections are structured following the Tagged Media Structure pattern and each stored document can support the Lifecycle States pattern. This enables the storage of the tags, the management of the life cycle of the document, and the proper assignment of ownership and responsibilities for the document throughout its life cycle.

Figure 5.38 shows the interaction of an information content node with other information nodes. As you can see, the integration of an information content node is very similar to an application node. The difference is in the types of Information Payloads that are transmitted. The content of the document or media file is rarely transformed as it flows through an information supply chain; however, the tagging and other descriptive information is structured information and may be transformed as it flows between information nodes. The numbers on the diagram in Figure 5.38 refer to these notes:

1. This is the information content node itself.
2. There are other information nodes exchanging information with it using information services.
3. The information content node may export or import information to/from an information store. Other information nodes could use this information store as an informationsharing mechanism.
4. The information content node may pass messages to/from a Queue Manager information node. The queue manager may distribute these messages further. This is a useful approach to distribute updates and alerts as they happen.
5. Information may be passed in an out of the information content node via an Information Broker that is implementing an Information Flow.

### Solution Example

MCHS Trading installs a new information content node to manage its documents and media files. This gives them a centralized place to manage and share these files. It is now clear which files are the latest approved copies of documents and images, thus saving time and avoiding mistakes caused by using the wrong version of a file.

### Benefits

- The information content node provides an organizing framework around documents and media files so they can be located when needed and destroyed once they are not needed.

### Liabilities

- The information content node typically holds valuable information for the organization, but it is often hard to make use of this information outside of this node. Partly this is due to the nature of the information it stores, but there is also limited access to the classification and descriptive metadata.

### Usage

A class of middleware called content management systems implements the information content node pattern. These systems not only manage the documents and media files, but also provide Agile Business Processes to provide case management capabilities along with search and text analytics capability.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Search Node

### Qualified Name

DesignPattern::Search Node

### Category

Information Node Patterns

### Description

Create a server to host the processes that crawl through the information sources creating a search index, and then provide access to the search index through a user interface.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to be able to locate information on an ad hoc basis.

### Problem Statement

What is the appropriate infrastructure to enable an organization to locate information on an ad hoc basis?

### Problem Example

Employees of MCHS Trading need to make ad hoc queries for information stored in documents and files.

### Forces

- Information is distributed across multiple information nodes.
- It is not possible to anticipate all of the types of information queries an organization will need.
- Information is not always consistent or perfectly correlated.

### Solution Description

Create a server to host the processes that crawl through the information sources creating a search index, and then provide access to the search index through a user interface.

The search node breaks the problem of locating information into the following parts:

- Locating and indexing information—This is a batch operation, run at least once a day to scan through the information, picking out the presence of keywords and tags.
- Matching the user's search request with the relevant content from the index— When a person requests information, the keywords from the request are matched against the index and a list of relevant documents that match the keyword are returned. Figure 5.39 shows the search node interacting with other information nodes that contain information worthy of searching.

### Solution Example

MCHS Trading deploys a search node to create and manage a search index that represents the content of these documents and files. This search node also has a web user interface, which is embedded into the company's home page so employees can access the search index and link to the required information.

### Benefits

- The search node provides an approach to locating information in the organization without requiring change to the existing information nodes.

### Liabilities

- The processing necessary to crawl through the information sources and create the search index can take a large amount of processing power. If the indexes are not refreshed regularly, the search locates missing, or incomplete, information.

### Usage

This type of information node is also known as a search engine.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Store

### Qualified Name

DesignPattern::Information Store

### Category

Information Node Patterns

### Description

Design a file/directory structure or database schema to act as a store for the information. Information processes running in different information nodes are responsible for consuming and maintaining this information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Some information does not seem to belong to any specific information node.

### Problem Statement

What is the appropriate infrastructure to store information that does not have a natural home with the information processes that make use of it?

This information may need to be kept independently from the information processes because:

- The information node where the information processes reside is not able to host this information.
- Information processes hosted on multiple information nodes share the information. None of the existing information nodes has the quality of service to support the needs of all of these information processes.
- The information is only required for a short period of time and an implementation that does not impact the existing information node is required.

### Problem Example

One of MCHS Trading's managers needs to create documents and presentation to support his or her role. He or she needs somewhere to store them with the related information that is supporting his or her work.

### Forces

- Ownerless information—Information that does not have an owner is rarely managed properly.
- Shared information needs broader availability—Information nodes may be available at different times of the day. An information node must be available whenever any of the information processes (local or remote) need it.

### Solution Description

Design a file/directory structure or database schema to act as a store for the information. Information processes running in different information nodes are responsible for consuming and maintaining this information.

The information store is a very flexible and simple information node that is not able to run information processes beyond those needed to manage the information node itself. Its schematic is shown in Figure 5.40. The numbers on the diagram in Figure 5.40 refer to these notes:

1. The infrastructure operation is able to start and stop the information store using the information node management process.
2. Remote information processes are able to access the information through remote information services.
3. The remote information services call the local information services of the information store. These information services reflect the structure in which they are stored in the information collections.
4. The information collections are responsible for the storage and retrieval of the information. Although the information store cannot run its own information processes to work with its information, the information services make the information available to a wide range of remote information processes—see Figure 5.41.

### Solution Example

The MCHS manager has a private information store to keep the draft documents. They are added to a shared repository when they are ready to be shared.

### Benefits

- An information store is simple to create and use.

### Liabilities

- Because an information store does not support information processes, it is reliant on information processes running in other information nodes to maintain the information collections it stores.
- There are many packages that create information stores. The result is that information workers can create private information stores that are unmanaged. This is fine for noncritical or information for personal use. But there is always a danger that parts of the organization may become dependent on this private information store that could be vulnerable to loss or theft. See the User Private Provisioning pattern for more details on this liability.

### Usage

Information stores are typically implemented using database servers or file systems.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Mart

### Qualified Name

DesignPattern::Information Mart

### Category

Information Node Patterns

### Description

Create a dimensional view of the historical information to suit the reporting and/or analytical needs of the group.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities. This information process is using information.

### Problem Statement

A group within an organization needs its own source of historical information to match its reporting needs.

### Problem Example

MCHS Trading's Reporting Hub maintains the relationships between customers and the products they buy. Some of the management reports need to see customers by segment and the products they buy. Others need to focus on product categories and the buying trends within these categories. Essentially, the information behind each of these reports is the same. However, the way the values are rolled up and structured is very different.

### Forces

- Specialized information collections are the fastest—Information collections designed specifically for an information process, and stored locally in the same information node as the information process, typically provide the fasted access to the information for the information process.
- Information copies add cost—Every copy that is made of some information values costs money to store and maintain.
- Inline transformation is transient—If transformed information is not stored, then the transformation must be redone each time the information is needed in that format. This makes sense if the information values are changing rapidly. However, when the information values are fairly static, collating and reformatting the set of information values on the fly over and over again is inefficient.
- Inconsistent terminology for the same information—Different parts of an organization may use inconsistent terminology from each other. This terminology difference may derive from a different heritage, skill sets, or decentralized operation.

### Solution Description

Create a dimensional view of the historical information to suit the reporting needs of the group.

A dimensional view is one particularly suited to reports. It stores the main facts of the report in the core database table and then links off to tables that provide supporting information.

For example, an information mart for reports about orders would have a core table where each row contained the essential information about an order. This row would include the customer identifier, number of items, value, date of the order, date it was fulfilled, identifier of warehouse that shipped the goods, and so on. Linking off of this core table would be customer details relating to each referenced customer identifier. Similarly, there would be a table of warehouse details for each warehouse identifier.

Figure 5.42 shows how the information mart interacts with other information nodes. The numbers on the diagram in Figure 5.42 refer to these notes:

1. This is the information mart.
2. An Information Broker provisions the information mart from other information nodes such as an Information Warehouse. The information broker will extract the appropriate subset of the information and transform it into the desired format for the consumers of the information.
3. One or more information nodes (running, for instance, the Information Reporting Process) use the information from the information mart.

### Solution Example

The Reporting Hub has information marts that store the information in the appropriate format for each of the reports.

### Benefits

- The information mart provides information to the information workers in the form they need it. It can also serve as a historical record for the organization if it does not have an Information Warehouse.

### Liabilities

- The information workers should not update the information mart. It should have reference usage by the business processes and only be updated via the information provisioning processes of the information supply chain.

### Usage

The information mart pattern is describing what is often referred to as a data mart, a structure related to an information (or data) warehouse. The dimensional structures are either called Star Schemas or Snowflake Schemas and are commonly described in books about data warehousing and business intelligence.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Cube

### Qualified Name

DesignPattern::Information Cube

### Category

Information Node Patterns

### Description

Create a snapshot of the desired information and store it in a cube structure where the information attributes can be referenced as a point or a series of related points.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Some activities require thought and ad hoc analysis. An individual needs to look at the evidence and come to a conclusion. Often information that is correlated in multiple dimensions is needed to fully understand the situation.

### Problem Statement

An information user needs to analyze multiple dimensions of correlated information.

### Problem Example

MCHS Trading would like to do some what-if analysis on the mix of products available through each channel. It wants a set of information collections that covers its customers, the products they buy, through which channel, and when. The Reporting Hub has this information, but the structure of the data is not ideal for this type of analysis. In addition, MCHS Trading wants to make changes to some of this data to understand how changes in its product offerings could affect sales.

### Forces

- Correlating information requires quality information—Particularly when it comes from multiple sources.
- Specialized information collections are the fastest—Information collections designed specifically for an information process, and stored locally in the same information node as the information process, typically provide the fasted access to the information for the information process.
- Information copies add cost—Every copy that is made of some information values costs money to store and maintain.

### Solution Description

Create a snapshot of the desired information and store it in a cube structure where the information attributes can be referenced as a point, or a series of related points.

An information cube node hosts the cube structure and also provides analytics capabilities to enable an information user to experiment with different views of the information.

Figure 5.43 shows the information cube interacting with other information nodes. The numbers on the diagram in Figure 5.43 refer to these notes:

1. This is the information cube.
2. An information broker provisions the information cube from information that typically comes from an Information Warehouse or an Information Mart.
3. The information user can access and experiment with the information once it is loaded.

### Solution Example

MCHS Trading uses Snapshot Provisioning to create linked information collections to support this analysis project. It is stored in an Information Cube. The team is able to change the channels that products are available though and understand how these changes could affect sales based on the knowledge of the channels that its customers work on.

### Benefits

- The user of the information cube is able to quickly extract information from different perspectives to understand a complex situation.

### Liabilities

- This is, of course, another copy of the information. Every copy of an information collection that is created and distributed adds to the cost of maintaining the information supply chain. Ideally, the availability of the information cube should be time boxed so the information can be properly disposed of and the storage freed up once the project is complete.
- Information cubes require complex information transformations to populate it.

### Usage

The pattern we have described here is a specialized type of data mart that is designed for ad hoc analysis by an individual. The generic term that is used for this technology is OLAP, which stands for Online Analytical Processing. It is used for navigating through information, understanding aggregates, and relationships. It is also used for planning and forecasting. Then there are specialized types of OLAP technology. Examples include the following:

- Molap—Another name for traditional multidimensional cube support—that typically loads information into memory to process.
- Rolap—This is an OLAP implementation based around a relational database. The multidimensional structures are represented directly in the database tables.
- Holap—This is hierarchical OLAP that used both the relational database and inmemory calculations. To understand more about this type of technology, refer to books about data warehousing and business intelligence.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Broker

### Qualified Name

DesignPattern::Information Broker

### Category

Information Node Patterns

### Description

Use a specialized information node called an information broker to host these information processes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The transfer of information between existing information nodes is implemented by Information Flows. Often, these information flows add additional information processes to the information supply chain to perform the transfer of information.

### Problem Statement

What is the appropriate infrastructure to support the information processes that proactively move information between different information nodes?

These information processes are typically added after the source and destination information nodes are in place and are designed to minimize the impact on them.

### Problem Example

Where should the processes that move MCHS Trading's product details from the Product Hub application to the downstream order-taking systems, such as E-Shop, Stores, and Mail-Shop, be located?

### Forces

- Varying formats—Information stored in different systems is not likely to be the same format—nor will the information values be consistent.
- Limited availability—It is possible that the source and destination information nodes are not always available at the same time.
- Expensive to change—Changing the source and/or destination information nodes may be expensive and disruptive on the existing business.
- Limited integration capability—Application nodes, particularly, are designed to support their business function and don't typically have specialized capability needed to transform and transport information.
- Dynamic environment—The provisioning support needs to be flexible to allow the organization to continuously improve the integration and synchronization or the organization's systems.
- Limited capacity—The source and/or destination nodes may be running at full capacity performing their primary role.

### Solution Description

Use a specialized information node called an information broker to host these information processes.

An information broker is designed to provide a server environment for hosting provisioning information processes (also known as integration jobs), such as the Information Deployment Process.

It supports the dynamic creation and maintenance of these types of information processes and maintains information collections of metadata described in the information identification patterns to help pinpoint the types of information located in each of the information nodes.

The provisioning information processes make extensive use of the Information Reengineering Step patterns to reconcile the differences between the information in the source(s) and the intended destination systems.

Figure 5.44 shows the information broker interacting with other information nodes and using a Look-Up Table Node and Staging Area to manage the transformation of information as it moves from the source to the destinations.

Information brokers do not provide any facilities in which to store an organization's business information. Its information collections are for its internal use. As such, information brokers typically use Information Stores, Look-Up Table Node, and other types of information nodes to acquire the information used by the provisioning information processes.

Figure 5.45 summarizes the structure of the information broker. The numbers on the diagram in Figure 5.45 refer to these notes:

1. The information broker is started and maintained by the Infrastructure Operator.
2. The information broker hosts information collections of metadata that are maintained and used by information management users such as the Information Steward and Data Quality Analyst.
3. The metadata management processes are supporting many of the information identification patterns, such as Subject Area Definition, Information Location, Valid Values Definition, Information Values Profile, Information Lineage, Semantic Tagging, and Semantic Mapping.
4. The metadata information stores support the information provisioning processes with knowledge of the information to be provisioned.
5. When the information provisioning processes run, they access the metadata to locate the information to process and reengineer in the information. They work with Remote Information Services to access the information in the sources and destinations.
6. The remote information services are responsible for the network communication to access the information in the sources and destinations.
7. Information provisioning processes can be started in the information broker by invoking Triggering Information Services.

### Solution Example

The information processes that move the product details are part of a Partitioned Distribution information flow. They are hosted together in an information broker. This solution is also using a Staging Area to hold the intermediate results and Look-Up Table Node for translating code values from the source code values to the destination code values. This is illustrated in Figure 5.46. The numbers on the diagram in Figure 5.46 refer to these notes:

1. The first information process receives details of a product in an Information Payload. It is responsible for deciding which of the downstream information nodes needs to receive details about a particular product.
2. There is a staging area for each of the destination information nodes. The first information process places a copy of the payload into each of the appropriate staging areas. This type of selection is required when the destination information nodes have different scopes. In effect, this information process must understand the differing scopes in the downstream information nodes in order to select which payloads to put in each staging area.
3. The payloads in the staging area have Complete Coverage and are in the source systems format (although they could have been converted to a canonical format). Information is taken out of each staging area by a dedicated information process that selects the appropriate attributes from each payload to match the coverage of the destination and transforms them to match the destination's format.
4. The transformed payload is passed to the destination information node and used to update the appropriate information details. To perform this information flow, the provisioning information processes needed to know the internal details of the information collections within the source and destinations. This logic will have to be modified any time the usage, scope, or coverage of the information collections within these information nodes changes. This maintenance effort is simplified by hosting the provisioning information processes in an information broker because it is designed to make it easy to change its information processes.

### Benefits

- The information broker makes it easy to update the provisioning information processes that support the movement of information along the information supply chain.

### Liabilities

- This is another server to manage and ensure it is available.

### Usage

There are many middleware products that implement this pattern—from messaging engines, enterprise service buses, ETL (extract, transform, load) engines, data replication engines, and workflow engines. Each product will support a limited set of information processes and be tuned for particular nonfunctional requirements.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Queue Manager

### Qualified Name

DesignPattern::Queue Manager

### Category

Information Node Patterns

### Description

Use an intermediary information node that is able to reliably store and forward information payloads from one application and deliver them to the intended recipients when they are available.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information is changing all of the time. How do we keep the information collections synchronized across multiple information nodes?

### Problem Statement

An organization wants operational independence between its information nodes, allowing information to flow reliably between them even though they may not always be available at the same time.

### Problem Example

MCHS Trading's order-taking information nodes—E-Shop, Mail-Shop, and Stores—need to pass new orders to the Shipping information node, which is responsible for order fulfillment. Shipping needs a daily maintenance cycle where it is not available to receive new orders. What happens to the new orders that are received when Shipping is not available?

### Forces

- Information nodes fail unexpectedly—Even the best-run infrastructure may fail from time to time. It is necessary to have some contingency to minimize the impact of a component failing.
- Polling is inefficient—Polling is when an activity connects to a resource to look for a change of status, or a piece of work to do. This is wasteful of resources, particularly when there is often nothing to do.
- Diversity of formats—Each information node typically uses its own private format for the information it works with. When information is moved between information nodes, it must be transformed from the source's format to the destination's format.

### Solution Description

Use an intermediary information node that is able to reliably store information payloads from a source information node and deliver them to the intended recipients when they are available.

We call this information node a queue manager as it uses a queuing paradigm to manage the sequence of information payloads that need to be transmitted. Figure 5.47 shows its logical structure. The numbers on the diagram in Figure 5.47 refer to these notes:

1. The queue manager is started and stopped through the Information Node Management Process.
2. Either an Information Queuing Process or an Information Broadcasting Process receives an information payload that must be safely delivered.
3. The information payload is passed to a local information service that represents a queue.
4. The information service stores the information payload.
5. The result of storing the information payload triggers an attempt to deliver it to the intended recipient(s).
6. The intended recipient could be registered with the queue manager, providing the queue manager with an information service to call to deliver the information payload.
7. If the queue manager successfully delivers the information payload, then it is deleted from the information collection. If not, it remains in the information collection until (1) the recipient registers, in which case the stored payloads are passed to it and removed from the information collection, or (2) an information node requests an information payload explicitly. The queue manager is able to support the delivery of information payloads between many different information nodes. This is illustrated in Figure 5.48.

### Solution Example

As seen in Figure 5.49, a queue manager is installed "in front" of the Shipping information node. Orders are passed in information payloads from the order-taking information nodes to an information broker that is responsible for transforming the information payloads to the format understood by Shipping. The information broker then passes the transformed information payload to the queue manager. The queue manager delivers the order information payload to Shipping when it is next available.

The queue manager is able to buffer new orders whether Shipping is unavailable due to a planned outage or an unexpected failure. It can also throttle back the delivery of new orders during peak demand so Shipping does not get overloaded.

### Benefits

- The queue manager increases the resiliency of an information flow by ensuring information is delivered even if one of the destinations is not available when the information payload is sent. The queue manager logic can be implemented in the source, destination, or information broker nodes. However, the simplicity of the queue manager's behavior makes it easier to keep it running at high availability.

### Liabilities

- The queue manager must be configured for as close to continuous availability as possible. This is typically achieved by having a cluster of queue managers supporting the information supply chain so the service continues even if one of the queue managers is unavailable.
- Neither the information queuing process nor the information broadcasting process can perform transformation on the information payloads that pass through the queue manager. Because most information nodes implement their own private information format, the queue manager often needs to be used in conjunction with an Information Broker.

### Usage

The queue manager is a common component of message-oriented middleware. It is capable of supporting many more patterns than we have described here. However, we have focused on its use in the distribution of information. Its function is covered in greater detail in works on information integration technologies.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Staging Area

### Qualified Name

DesignPattern::Staging Area

### Category

Information Node Patterns

### Description

Create a dedicated information store to hold one or more information collections that have Transient Usage by the provisioning information processes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information needs to flow between information nodes.

### Problem Statement

An information node needs a temporary store to hold information that is in the process of being provisioned into a different information collection.

### Problem Example

Product details need to be distributed from MCHS Trading's Product Hub to the order-taking applications.

### Forces

- Different formats—There are differences in the way information is stored in each information node.
- Insufficient quality—Information from one information node may be of such poor quality that it needs a lot of work to bring it up to standards before it can be distributed to other information nodes. As such, it may be necessary to introduce information collections with transient scope to store intermediate results.
- Different processing needs—The processing required on some Information Payloads might be different from others. As such, they may need to take a different route in an Information Flow.

### Solution Description

Create a dedicated information store to hold one or more information collections that have Transient Usage by the provisioning information processes.

The information store is an information node dedicated to hosting temporary information collections that are needed to store the intermediate results while moving and transforming information.

Figure 5.50 shows the workings of a staging area. The numbers on the diagram in Figure 5.50 refer to these notes:

1. As with any information node, the staging area must be running for the information collections it hosts to be available.
2. The provisioning information processes read and write Information Payloads to staging areas using information services.
3. The information services provide access to the information collections.
4. The information collections have Transient Usage, for information payloads are typically being added and deleted, but rarely updated.

### Solution Example

The staging area provides information collections that are used as post boxes for the information processes running in the information broker. The numbers on the diagram in Figure 5.51 refer to these notes:

1. The staging area has an information collection for each destination information node. The information payloads are written to these information collections as required.
2. When an information payload is retrieved and processed, it is deleted from the information collection in the staging area.

### Benefits

- Provisioning information processes need to store intermediate results and use temporary files and database tables. Having a well-defined place to store these intermediate results ensures the content of these temporary files can be protected and, if there is an error in the logic of a provisioning information process, abandoning information payloads in one of these temporary stores, the condition can be checked for and rectified.

### Liabilities

- The staging area needs naming conventions for the information collections to be able to trace back and discover which information process created it.

### Usage

The staging area is a common approach used to provide temporary storage for integration logic. Sometimes files are used, or database tables. If database tables are used, the database features, such as triggers, can be used to implement Information Probes that monitor the flow of information.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Look-Up Table Node

### Qualified Name

DesignPattern::Look-Up Table Node

### Category

Information Node Patterns

### Description

Provide a lookup table that translates between the descriptive information values and the code values.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Many systems use code values to represent a fixed set of values that can be stored in an attribute within an information collection. (This is known as an enumeration.) The information processes that use the information collection need to understand the code values used.

### Problem Statement

An information process needs to look up the code value to classify or describe some information.

There are four basic use cases:

- An information process needs to interpret the code values to make a decision in its logic.
- An information process needs to convert a string supplied to it, typically from an information user, into a code value.
- An information process needs to convert the code value into a string of the right natural language to display to an information user.
- An information process needs to transform an information structure that includes code values from one format to another as part of an information flow or information service.

### Problem Example

When a MCHS Trading customer submits an order, he or she has three delivery options:

- To have it delivered to his or her home address
- To have it delivered to a store
- To have it delivered to an alternative address The attribute in the order details that stores the delivery option uses a code value. There is one code value for each option. The E-Shop application can operate in English or French. Also, the code values used for the delivery option are different in the Shipping application.

### Forces

- No standards for code values—The code values used by each information collection are typically different. When information is distributed to other information collections, the code values from the source must be transcoded to the code values for the destination. The information process that is choreographing the distribution must understand the mapping between the two code value sets. Errors in code value mapping are the largest source of errors in information supply chains.
- Sets of code values need to be maintained—New code values will need to be added to the list—and very occasionally, values need to be deleted.

### Solution Description

Provide a lookup table that translates between the descriptive information values and the code values.

This may be a simple lookup table supporting a single information collection, or one that supports the transcoding of code values from one information collection to another.

### Solution Example

In this example, there are two lookup tables:

- Within E-Shop, there is a code table that maps the three code values to their French and English strings.
- For the information broker that transforms orders from E-Shop, Mail-Shop, and Stores, there is a lookup table that maps between the code values used in E-Shop, Mail-Shop, and Stores to the code values from Shipping, as seen in Table 5.22. Notice that the mappings are not 1-1 as there are different options offered by each of the order-taking applications. Meaning Code Values Code Values Code Values Code Values from E-Shop from Mail-Shop from Stores from Shipping Home 0 H CA A Store 1 - SA B Alternate 2 A - C Unknown - U - C If a new delivery option is added, both code tables must be updated.

### Benefits

- Using code values for enumerations makes it easier to validate that a new value is acceptable; it saves storage and makes it easier to support text representations in different languages for display in messages and on user interfaces.
- Using lookup tables that can be shared with many information processes reduces the cost of maintaining the sets of code values.

### Liabilities

- Lookup tables are passive stores and need external information processes to maintain the values.

### Usage

Lookup tables are used within the implementation of applications and as standalone database tables for use by Information Brokers. They can be simple database tables, or a most sophisticated solution that offers authoring of code tables; mapping between them; information services for import, export, and transcoding; along with provisioning information flows to maintain consistent values in all of the copies. This type of solution is called a Reference Data Management (RDM).

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Event Correlation Node

### Qualified Name

DesignPattern::Event Correlation Node

### Category

Information Node Patterns

### Description

Consolidate the events into a single information node in real time and perform complex event processing on them.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The activity within an organization is complex, with many things happening at once. As an individual person, or information process, it is hard to recognize that a series of seemingly disparate events that have recently occurred indicate something significant has happened.

### Problem Statement

What is an appropriate infrastructure to host a complete picture of the enterprise with a historical perspective?

### Problem Example

MCHS Trading knows that the sales of certain products can be affected by a variety of events, such as weather, marketing offers, an item in the news, fashion, and public opinion. They do historical analysis of buying patterns, which gives them the overall trends in demand, but does not warn them of unexpected spikes in demand. How should they tackle this issue?

### Forces

- The events can come from multiple sources—They need to be brought together in real time.
- The timing of events affects their significance—For example, if an individual's address has changed 5 times in the last 10 minutes, then that suggests the individual might have been the victim of identity theft—but if an address changes 5 times in 20 years, then that is not so significant.

### Solution Description

Consolidate the events into a single information node in real time and perform complex event processing on them.

This information node is called the event correlation node. It is a specialized piece of software comprising state machines, timers, mapping, and correlation processing. Each event is processed as it arrives. This processing classifies it and groups it with related events. Each group is being monitored to see if it matches a pattern. When/if the pattern is confirmed, a new event is published, recording that a significant complex event has occurred. This new event is passed to other information nodes to handle the situation.

### Solution Example

MCHS Trading adds an event correlation node to detect weather and media events and correlate them with unusual levels of sales through its channels. If it looks like a product has a spike in popularity, it contacts its suppliers to acquire more stock.

### Benefits

- The event correlation node detects when events from multiple sources together indicate that something significant has occurred.

### Liabilities

- The complex event processing logic is difficult to write and needs constant evaluation and tuning to ensure it continues to be accurate.

### Usage

Event correlation nodes are used to detect unusual demand from customers, potential fraudulent activity, and potential opportunities to sell something to a client.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Mirror Store

### Qualified Name

DesignPattern::Information Mirror Store

### Category

Information Node Patterns

### Description

Provide a replica set of information collections that are hosted together on a different information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization has many information nodes supporting its day-to-day business.

### Problem Statement

An organization needs to support queries against information located in either a closed or overloaded information node.

An existing information node contains valuable information required by other parts of the information supply chain. However, this information node is not able to support remote queries of its information collections from other information nodes.

### Problem Example

The MCHS Trading application called Stores is responsible for providing order management support for the physical stores (shops) located in various cities. It is a mainframe application that uses application files to manage information about each store's capability, where they are located, employees, stock, and the customer store card. The stock information covers both the orders they are making either for the shelves, or for individual customers, and the deliveries they receive.

The developers of the Stores application have been totally focused on the needs of the stores themselves. When the stores are open for business, this application is running at full capacity and is not able to handle additional workload. However, head office needs information about the operation of the stores.

### Forces

- Applications are valuable—An application represents a significant investment and its usefulness makes it hard to change.
- Overloaded information node—Calls to an information node's services create a processing load on the information node.
- Information formatted for original use—One of the reasons the original source information may be hard to query is that it is formatted to suit its primary local use cases and this is not compatible with the remote queries.
- Information is constantly changing—If a copy of some operational information is taken, the copy must be kept synchronized with the original or it will become increasingly worthless.

### Solution Description

Provide a replica set of information collections that are hosted together on a different information node.

The information mirror node is an information store that hosts the replica information collections as seen in Figure 5.52. These information collections can be populated as follows:

- Regular Snapshot Provisioning that takes a fresh copy of the information from the original information node and completely replaces the replica information collections.
- After an initial load of the original information, the replica is kept up to date with delta updates using Mirroring Provisioning. This approach can only be used if it is easy to detect which values have changed since the last time the information mirror node was refreshed. The approach used will depend on how frequently each of the values in the information is changing. In either case, however, the information collections in the mirror information store have Reference Usage.

### Solution Example

MCHS Trading creates an information mirror store for a replica of the Stores information. It is replicated once a day once the processing is completed for the physical store's daily trading. The frequency that it is updated is a compromise between the capacity of the Stores application and the information needs of the rest of the organization.

### Benefits

- The information mirror store is able to support information services that provide access to the information without impacting the original information node. The information can be reformatted as it is synchronized into the information mirror store to better support the queries.

### Liabilities

- The information mirror store takes additional storage and needs to be kept synchronized with the original information node.

### Usage

This is a simple operational data store. You would use this to off-load the query traffic from the application either because the application does not have a query interface, or it is overloaded, or it is not always available.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Event Store

### Qualified Name

DesignPattern::Information Event Store

### Category

Information Node Patterns

### Description

Create an information node where information event records can be consolidated.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization has many information nodes supporting its day-to-day business.

### Problem Statement

An organization needs an audit trail of who did what, why, where, and when.

### Problem Example

MCHS Trading needs to monitor the information flow along its information supply chains.

### Forces

- Auditors require proof—It is not enough for an organization to comply with a regulation—it needs to be able to demonstrate that it is compliant.
- Events happen in many places—It is necessary to capture the event type, time, location, and the context in which it occurred.

### Solution Description

Create an information node where information event records can be consolidated.

This information node is called an information event store—see Figure 5.53. It is a specialized information store that is designed for inserting new records. It hosts a number of local information collections that each store a particular type of information event as an information entry. The information event record provides information services to receive new information events. These services are used most of the time. There are also information services for retrieving sets of information events for reports and audit, which are called occasionally. There are no facilities for changing the events that are recorded.

### Solution Example

MCHS Trading uses Information Probes throughout its information supply chains to monitor particular aspects of its operation. These probes use information event stores to record their readings. The information events are consolidated through a consolidating information supply chain to a central operations console where unexpected events are reviewed and action taken.

See the Information Monitoring solution pattern for more information about this use case.

### Benefits

- The information event store provides a reliable store for information events. It can be used as a local store for an information probe and it can be used to store information events in a centralized monitoring node and console.

### Liabilities

- The information event store takes additional storage and needs to be kept with the latest activity from the original information nodes.

### Usage

This type of store is used for diagnostic logs and audit trails.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Operational Status Store

### Qualified Name

DesignPattern::Operational Status Store

### Category

Information Node Patterns

### Description

Create a set of linked information collections that can store the required information and host them together on an information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization has many information nodes supporting its day-to-day business.

### Problem Statement

An organization needs a consolidated view of the operational state of an aspect of its day-to-day business.

This requires consolidating and linking the most recent values from the information activity records and information assets spread throughout the information supply chains.

### Problem Example

MCHS Trading has three main physical warehouses that goods are shipped from. When they run out of stock, the Shipping application must order more from the supplier. Meanwhile, customer orders are not being fulfilled. How does MCHS Trading coordinate the ordering of new supplies with the management of the customers with waiting orders?

### Forces

- Applications have limited scope and coverage—An application contains information that represents the interests of a business function within an internal organizational unit.
- Inconsistent distributed information—Information assets are distributed across multiple information nodes, duplicated, and inconsistent.

### Solution Description

Create a set of linked information collections that can store the required information and host them together on an information node.

This information node is implemented as an information store (typically a database) that provides a place to marshal and correlate information from different information nodes to support complex queries.

Information processes hosted in an information broker maintain the information within the operational status store. Information is accessed through its information services (typically as SQL queries). See Figure 5.54. information node(s).

### Solution Example

MCHS Trading introduces a Re-Stocking operational status store. This information node maintains information about the orders to suppliers being handled by the Supplier-net application and the customer orders being handled by the Shipping application.

Re-Stocking is used by the Customer-Care application that is managing queries from customers. It also feeds the Reporting Hub on the impact of out-of-stock conditions on customer orders and which product lines these occur in.

### Benefits

- The operational status store may be used to provide a consolidated view of the organization's activity and/or to provide a consolidated information collection that can be used as a source for distributing this information to other information nodes.

### Liabilities

- The operational status store takes additional storage and needs to be kept up to date with the latest activity from the original information nodes.

### Usage

This is a type of operational data store that has normalized and correlated operational data. It is used to support use cases where information needs to be correlated from multiple systems. It could also be a feed for a data warehouse (Information Warehouse) or data mart (Information Mart).

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Asset Hub

### Qualified Name

DesignPattern::Information Asset Hub

### Category

Information Node Patterns

### Description

Create a specialized information node where the information assets can be consolidated and managed, plus providing a base from which to synchronize the values in other information nodes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information Assets such as customer and product details are central to an organization's operations. As a result, this information tends to be replicated in many information nodes.

### Problem Statement

An organization needs a consolidated and consistent view of the information assets that are central to its operation.

This consolidated view can be used to enable new capabilities and can act as a hub from which to distribute updates.

### Problem Example

MCHS Trading needs a consolidated view of its customers' details for operational use. At the moment, customer details are stored in E-Shop (for customers who use the Internet shopping service), Stores (for customers who have a store card), and they are entered into each order in Mail-Shop. There is a consolidated list of customers in the Reporting Hub, but that information node is not suitable for an operational load.

### Forces

- Slowly changing—Information assets do change, but it tends to be updates each week/ month rather than every few minutes.
- Widely used—Information assets contain information that is core to the organization's work and, as a result, they are needed in many of the business information nodes.
- Difficult to identify—Information assets often represent people, concepts, objects, and organizations in the real world. They do not come with a unique identifier and so many information nodes assign an identifier. In fact, each node assigns a different identifier when it stores information about the asset. Information nodes are often not good at ensuring they haven't already stored information about the asset, and so may store it twice, resulting in it having two identifiers in one information node. The result is that an information asset has many identifiers.
- Disconnected information—An information node receives new information about an asset, for example, through its user interface. It stores the update locally. Because there is no linkage to the other information entries about this asset that are stored in various information collections dotted among the organization's information nodes, there is no easy way to propagate this update to the other copies. The result is that, over time, the copies become inconsistent.

### Solution Description

Create a specialized information node where the information assets can be consolidated and managed, plus providing a base from which to synchronize the values in other information nodes.

This information node is called an information asset hub. It becomes the authoritative source of these information assets.

Figure 5.55 shows the internals of the information asset hub. The numbers on the diagram in Figure 5.55 refer to these notes:

1. Most information collections contain information assets, although there may be references and summaries of relevant Information Events and Information Activities.
2. The information collections are accessed through Information Services. The hub may offer different views over the same information asset to service different consumers.
3. The information stored in the information asset hub can be retrieved directly through the information services.
4. When a change is to be made to information in the hub (create, update, delete), the request goes through a Triggered Information Service where a variety of validation rules can be checked.
5. For create and update requests, an Information Matching Process is run to make sure the new information is not going to create duplicate entries.
6. If a match is found that is fairly close, a Clerical Review Process may be triggered to involve an Information Steward in the decision.
7. The information steward may use its domain knowledge, additional information, or persona inquiry to make the decision.
8. Once the status of the new information is resolved, alerts in the form of Information Events may be sent out if an unexpected or suspicious condition has been detected. Information Payloads containing the new information may also be sent to synchronize the new information with downstream information nodes.
9. The scheduling process inside the hub is periodically running the ever-greening process to scan the information looking for decaying information and unexpected values.
10. If the ever-greening process discovers errors, an Information Quality Remediation Process is used to correct them.
11. Many information asset hubs use a Soft Delete approach when a request is received to delete an information asset. The Archiving Process runs to remove information assets that have been flagged as deleted for some time. The interaction of the information asset hub with other information nodes is critical to keep it up to date:
- Business information nodes call its information services directly to exchange information.
- Information brokers call the information services to synchronize information in and out of the hub as part of an information supply chain.
- The information processes within the information asset hub call remote information services to send out alerts and data synchronization requests.

### Solution Example

MCHS Trading deploys an information asset hub called Customer Hub, as seen in Figure 5.56. This information node provides a central location to manage its customer details.

### Benefits

- The information asset hub is a central place to manage, protect, and apply quality standards and governance to information. The canonical form of the information often can be used to provision new information processes—saving time and money by avoiding supporting another set of information collections.

### Liabilities

- This is another information node to manage containing another copy of the information for a subject area.
- The hub is merging information entries that the information matching process has flagged as duplicates. Information nodes downstream of the information asset hub in an information supply chain may need to merge their copies of these information entries as well. If at a later time, the merge is found to be invalid, all merged information entries need to be split apart again, and any decisions made using the merged versions may need to be revisited.

### Usage

The information asset hub is a description of a Master Data Management (MDM) hub that manages information assets such as customer details, product details, asset details, and account/contract details.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Activity Hub

### Qualified Name

DesignPattern::Information Activity Hub

### Category

Information Node Patterns

### Description

Create an information node where consolidated information activity records can be stored and then accessed in real time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization has many information nodes supporting its day-to-day business.

### Problem Statement

An organization needs a consolidated real-time view of the activity relating to a business transaction that is dispersed among multiple information nodes.

Multiple information processes are performing a particular type of activity. These information processes are distributed across different information nodes. Each of these information nodes has a local information collection to document the progress of the work occurring locally. This information needs to be consolidated in some way so it can be located and retrieved in real time, often in the context of an information asset.

### Problem Example

MCHS Trading's order-processing capability is dispersed among its E-Shop, Mail-Shop, Stores, Shipping, and Invoicing applications. How does MCHS Trading discover the status of a customer's order?

### Forces

- Applications have limited scope and coverage—An application contains information that represents the interests of a business function within an internal organizational unit.
- Real-time information sharing—Information about an activity piece of work needs to be shared in real time.
- Real-time decisions—Predictive analytics needs consolidated real-time information to provide recommendations as part of a business transaction.

### Solution Description

Create an information node where consolidated information activity records can be stored and then accessed in real time.

This type of information node is called an information activity hub. Within it are two types of information collections:

- An event information collection where each information entry is an Information Event that describes a change or action performed on behalf of an activity
- An activity information collection where each information entry is an Information Activity The information activity hub has information services that enable information events to be received. The arrival of an information event causes a State Driven Process to start. It is responsible for storing the information event in a local information collection and updating the status of the related information activity. Together, the information collections and state driven process provide the current status and an audit trail of the activity. Figure 5.57 shows the internals of the information activity hub. The numbers on the diagram in Figure 5.57 refer to these notes:
1. The information collections in the information activity hub operate in pairs. One of the information collections contains information activities.
2. The second information collection in the pair contains information events.
3. The information collections are accessed by information services.
4. The information services offer the ability to retrieve the activity status of collections of events.
5. When a new event is received, it is processed by a triggering information service that initiates the correct state driven process for the corresponding activity.
6. The state driven process retrieves the appropriate information activity and determines the new state based on the event. It updates and stores the information activity and inserts the event into the information event collection.
7. For some state changes, the state driven process may trigger an additional information process.
8. This triggered information process may invoke information services to send alerts, or initiate some related processing.
9. The scheduler will periodically kick off an Information Ever-Greening Process.
10. The information ever-greening process is looking for information activities that have stalled, or are in unlikely states, or have missing information.
11. When activities have been completed for a while, they are archived.

### Solution Example

MCHS Trading deploys an information activity hub called Order-Tracking that is responsible for maintaining the state of the customers' orders as seen in Figure 5.58. It receives events from E-Shop, Mail-Shop, Stores, Shipping, Invoicing, and Re-Stocking. It is used by the CustomerCare system for discovering the status of orders. It also feeds the Reporting Hub.

### Benefits

- The information activity hub may be used to provide a consolidated view of the organization's activity. It supports information processes that understand the significance of events occurring across multiple information nodes.
- It provides information services that support the current status of related activity that is occurring in distributed information nodes.
- It can detect when an event has not occurred—suggesting a silent failure.
- It can provide additional situational information relating to an information asset.
- It can be used as a source for distributing this information to other information nodes.

### Liabilities

- The information activity hub takes additional storage and needs to be kept up to date with the latest activity from the original information nodes.
- When changes occur in the information nodes that are performing the business transaction, the information activity node may be affected because it may start to receive different events.

### Usage

This type of information node is a useful supplementary store to a Master Data Management (MDM) hub (Information Asset Hub) because it keeps volatile information that is related to the information asset in a form that can be accessed in real time. The information activity hub may be hosted on the same physical server as the information asset hub, if the performance load allows—otherwise, they may be deployed separately.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Warehouse

### Qualified Name

DesignPattern::Information Warehouse

### Category

Information Node Patterns

### Description

Create a set of linked information collections that supports the full scope of the information that is required by the organization to know the full scope of its operations.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to understand what the state of its business is and how it is changing over time. This is necessary to improve the performance of the business, understand the history and context of specific events, and meet regulatory requirements.

### Problem Statement

What is an appropriate infrastructure to host a complete picture of the enterprise with a historical perspective?

### Problem Example

MCHS Trading needs a historical record of its customers and the products they are buying. This is to enable it to understand the trends in its business. For example, which products are selling well and which are in decline? This helps MCHS Trading plan new product offerings.

### Forces

- Change is inevitable—Any historical record needs to take into account that structures change. This could be a reorganization of the organization, acquisition, or expansion of the scope of the business; changing priorities; and markets affecting what data are collected. Individual facts must be considered within the structure, or context, in which they were gathered.
- Information decays at different rates—Over time, the value of keeping information about individual events may diminish.
- Foresight—When selecting the information to preserve, how do you know what information you will need in the future?
- Volume—Organizations create a lot of data. Keeping it all for indefinite periods of time takes a lot of storage.
- Seeing the wood for the trees—Too much information can be overwhelming, causing you to miss the critical facts.
- Regulators need proof—It is not enough to comply with a regulation; an organization must prove it is doing so.

### Solution Description

Create a set of linked information collections that supports the full scope of the information that is required by the organization to know the full scope of its operations.

These information collections will store not only the current state of the organization's information, but also the values that were used in the past. They are hosted together in a specialized server called an information warehouse. The information processes within this node are focused solely on the accumulation, management, and delivery of this information.

An information warehouse has to accommodate change, both in terms of how the information is structured and the relationships between the information entries and values within them. It must also represent the notion of time and the state of the business at a particular moment in time.

The information warehouse is a highly connected system that is fed from the majority of the organization's information supply chain. This keeps the information warehouse current, while being able to provide a historical perspective on the organization's performance.

### Solution Example

MCHS Trading creates an information warehouse that is part of the Reporting Hub. The information warehouse hosts the historical record of its business. It includes the following:

- Details of all of its customers, the channels they use, the orders they make, how they pay, what offers they were given, and which were accepted
- Details of all of its products, the suppliers, how well it is selling, through which channels it is selling, the effectiveness of delivery, levels of profit from the products, levels of customer satisfaction, issues, and returns

### Benefits

- The information warehouse creates an information repository that contains the facts about how your organization is running—This information is necessary for demonstrating compliance with regulation, understanding what is working well and what needs changing, and detecting trends and changes in the market.
- The art and science of building information warehouses is well understood—There are many books, best practices, and skilled technical professionals who understand how to construct these systems so they deliver value over many years.

### Liabilities

- The temptation is to store everything, just in case—An information warehouse needs to be carefully planned, with a good understanding of where the information is coming from and how it will be consumed. If people do not have confidence in the quality and usefulness of the information, then it will fall into disuse—and become an expense rather than an asset.
- The information warehouse is designed for structured information—Increasingly, an organization's information is unstructured and information warehouses need to be coupled with Map-Reduce Nodes and Information Content Nodes to manage the full breadth of information.

### Usage

Powerful database systems called data warehouses have been developed to cope with the volume of data—and the complex structures and operations—that are necessary for historical information. These systems support both relational and dimensional structures, along with the capability called extract, load, transform (ELT) to transform and move data between internal storage areas.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Streaming Analytics Node

### Qualified Name

DesignPattern::Streaming Analytics Node

### Category

Information Node Patterns

### Description

Use streaming technology to collect and collate data from various monitoring devices and publish summaries of this data into the information supply chain.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Sensor-based data represents a growing sector of information typically of high volume. It contains useful information for the information supply chain, but its format and content can be challenging to use directly in an information supply chain.

### Problem Statement

How do you introduce data from real-time monitors and sensor devices into the information supply chain?

Data received from real-time monitors and sensor devices may be unpredictable in terms of its arrival rates, of mixed quality, and of very high volume. From a nonfunctional point of view, this data is very different from the other types of data in the supply chain. As such, there needs to be some sort of analysis and consolidation of the data before it is introduced into the information supply chain.

### Problem Example

MCHS Trading has three large physical warehouses from where its goods are shipped. Many of the goods in its product line are valuable, or require a special license to purchase. There have been some incidents of theft which MCHS Trading has been ordered to stop by its regulator.

### Forces

- If an information process needs to react to events as they are happening, the information gathering and processing must be as close to real time as possible.

### Solution Description

Use streaming technology to collect and collate data from various monitoring devices and publish summaries of this data into the information supply chain.

Streaming technology is able to perform real-time data collection, analysis, and transformation of device information as the device is producing it. On its own, it could be used to pump summarized information directly into the information supply chain. However, this would introduce values into the information supply chain that are difficult to audit and it could be difficult to repair the effects of a rogue device.

The information streaming process consolidated the results of the streaming processing into one or more information collections. Information can then be passed into the information supply chain from these information collections. Figure 5.59 shows streaming technology in action. The numbers on the diagram in Figure 5.59 refer to these notes:

1. Data from sensors is being received at a tremendous velocity. The information within these readings has a very short lifetime where it is useful.
2. The readings are fed into the streaming processor. It runs many parallel threads, trying to process each reading on its own as much as possible, and then starting to classify, group, and consolidate the information that has been extracted.
3. Some facts that are discovered must be acted on immediately and these are turned into an information event and passed to another information node for processing using a remote information service.
4. All of the information that is extracted is stored. It is shown here as being written to a staging area, but it could be passed to a queue manager, information broker, or information store.

### Solution Example

MCHS Trading installs RFID tags on its stock and sensors on every doorway. These sensors detect the movement of goods. If a restricted item is moved through a gate, an alert is raised to the security team. This helps them restrict the movement of these goods through a single gate where the manifests can be checked manually. The streaming analytics is responsible for tracking and recording the movement of goods plus detecting when restricted goods move out of their designated area through an unauthorized exit.

### Benefits

- Sensors allow organizations to capture new information that may be related or correlated with other standard information sources. This pattern supports the processing of huge quantities of incoming data, which is extremely vital for managing information from real-world sensors and networks.

### Liabilities

- Care must be taken to save all of the information necessary for downstream information processes. In addition, some thought should be given to being able to demonstrate that the processing within the streaming provisioning is working correctly.
- The information from a streaming node is often time critical. Ensure that the downstream processing that works with this information is mindful of its time-critical nature.
- Storage of stream-based information may represent an additional resource cost.

### Usage

Information streaming processes are beginning to appear in larger organizations that need to constantly monitor input from specific sensors. Examples of this type of processing include traffic analysis, electronic device input, and automatic maintenance checks. For more examples, see recent works on "Big Data."1

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Map-Reduce Node

### Qualified Name

DesignPattern::Map-Reduce Node

### Category

Information Node Patterns

### Description

Use an information node that supports distributed map-reduce processing on a file system.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The fastest-growing type of information is unstructured information, particularly documents, web pages, social media, images, and video.

1. Paul Zikopoulos, Chris Eaton, et al., Understanding Big Data: Analytics for Enterprise Class Hadoop and Streaming Data (New York: McGraw-Hill Osborne Media, 2011).

### Problem Statement

An organization wants to perform analytics over a large collection of unstructured files.

How is this type of information assembled and processed?

### Problem Example

MCHS Trading wants to understand the sentiment around a product line that it is considering adding to its product catalog.

### Forces

- The processing must come to the information—When a collection of information gets very large, it is no longer viable to copy it around.
- Unstructured information does not fit well in a database—Databases are better at handling structured information.

### Solution Description

Use an information node that supports distributed map-reduce processing on a file system.

Map-reduce processing breaks down the processing of the files into a mapping process that looks for patterns in the information, and a reduce process where the results detected are combined and consolidated. The map processing in particular is highly parallelized, enabling this technology to scan vast quantities of information to perform an analysis as seen in Figure 5.60.

This technology is new and the best practices around its use are still evolving, so the pattern details are light at this stage, but there are increasing numbers of successful deployments that suggest it should be included in the pattern language.

### Solution Example

MCHS Trading takes daily downloads from the social media sites and uses map-reduce processing to detect and extract comments about products in its product line. These are fed through to the Marketing Department.

Figure 5.61 summarizes the processing. The numbers on the diagram in Figure 5.61 refer to these notes:

1. Downloads from social media are taken regulary and stored in files.
2. The map-reduce process runs, looking for discussons about products that MCHS Trading sells. When a reference is dicovered, the text around it is analyzed to discover the sentiment.
3. References to dangerous or illegal attributes of a product are sent as a high-priority alert to the marketing team to investigate and potentially withdraw the product.
4. All of the references to the products, with the surrounding text and sentiment classification are stored to files. These are picked up by an information broker and stored as additional attributes about the product in the Product Hub. The analysis could be extended to look for positive references to products that MCHS Trading does not sell but are similar to MCHS Trading's product line. This could provide suggestions for new products to add to the catalog.

### Benefits

- This type of processing is very powerful at performing the same operation on information spread across multiple distributed file systems.

### Liabilities

- The tools and programming languages for this type of processing are still evolving and so you need to expect some churn and rework around the use of this technology. There is also a shortage of people skilled at using the technology.

### Usage

The most well-known distributed map-reduce engine is Apache™ Hadoop™.2 It is a new technology and there are many experimental systems being built with it. Some are operating on unstructured data as the pattern suggests, whereas others are working on a mixture of structured and unstructured information. Two popular usage patterns are exploratory analytics, where new information sources are analyzed to discover interesting facts, and a queryable archive, where information is archived to the distributed map-reduce engine (which will run on commodity hardware) and can then be searched and analyzed at a later date. For more examples, see recent works on "Big Data."3

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Analysis Node

### Qualified Name

DesignPattern::Information Analysis Node

### Category

Information Node Patterns

### Description

Provide a dedicated information node to manage the demanding workloads created by information pattern discovery.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to use information-based decisions for particular aspects of its business. Information-based decisions use analytics and business rules that use the information stored in their information nodes to make a decision. This decision is embedded in an information process and affects the subsequent steps that the information process takes.

### Problem Statement

What is the appropriate infrastructure to support the development of analytics models and decision models?

Analytics models and decision models are created using the Information Pattern Discovery Process and the Information Decision Definition Process, respectively. These processes need access to the organization's information to operate. They perform large information manipulation and computational operations and need to visualize subsets of information in a variety of ways.

### Problem Example

MCHS Trading wants to implement a Next Best Action solution. This uses analytics to offer its customers relevant offers, information, and services depending on their individual interests. MCHS Trading needs to analyze information about its customers' interests, buying patterns, and channel usage along with the pipeline of new and existing products. This information is dispersed among MCHS Trading's production systems. Which information node should MCHS Trading use to develop the models that will drive the next best action analytics?

### Forces

- High performance requirement—The Information Pattern Discovery Process searches for patterns of values in one or more information collections. This processing can take considerable computing resources (memory, CPU, and disk IO) to perform this activity.
- Disparate sources of information—The information to be analyzed often originates from a variety of sources.
- Specialized tools—Specialized information users called data scientists and business analysts build these models. They need specialized tools that examine, analyze, and visualize the information to allow them to experiment with different algorithms.

### Solution Description

Provide a dedicated information node to host the specialized analytics tools, and information users, that build analytics models and decision models.

Because existing information nodes are unlikely to support the processing load of the analytical processes, nor have the information stored in an efficient structure for their operation, it is typical to set up a new information node that is dedicated to the analytics processing. This information node is called the information analytics node.

The information analytics node supports two primary information users: the data scientist and the business analyst. Figure 5.62 shows its operation. The numbers on the diagram in Figure 5.62 refer to these notes:

1. This is the information analysis node.
2. It is supplied information through a Single View Information Supply Chain. Typically, the frontline information nodes are information mining stores that are fed from a big data information node such as an Information Warehouse.
3. The data scientist uses the Information Pattern Discovery Process to extract, sample, visualize, and experiment with different algorithms to build an analytics model. This can be used as is in an Information Pattern Detection Process. It may also be passed to a business analyst to incorporate in a decision model.
4. The business analyst builds a decision model using the Information Decision Definition Process by combining analysis models with business rules and policies to create a piece of logic that is based on the evidence of the organization's information but tempered with its policies and rules. The completed decision model may also be executed in an information pattern detection process.

### Solution Example

MCHS Trading buys a high-quality analytics package that supports both the information pattern discovery process and the information decision definition process. This is run as an information analytics node. It is fed using an Information Mining Store that is the root node of a single view information supply chain.

### Benefits

- The information analytics node keeps the specialized tools with their high workload cost in a segregated environment where the ad hoc nature of the workload will not impact other users.

### Liabilities

- This information node relies on its information supply chain to ensure it has good information to work with.

### Usage

The information analysis node represents an analytics package that is bought and installed as a separate system. Such a package can offer sophisticated capabilities for understanding and manipulating information in pursuit of the perfect model. It is called out as a special type of information node in the pattern language because it uses information supplied to it to develop logic that will drive the organization's business. As such, it needs to be supplied with information through a well-defined information supply chain; otherwise, the models created by the package will probably be incorrect.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Mining Store

### Qualified Name

DesignPattern::Information Mining Store

### Category

Information Node Patterns

### Description

Create an information store that has flat structures in its information collections to allow the pattern discovery process to work most effectively.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 5, "Information at Rest".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Analytics processing, such as the Information Pattern Discovery Process, requires huge quantities of correlated, but highly denormalized information, both current and historical, to allow the analytics software to explore and discover the patterns in the information values that can be used to report on past events and predict future events.

### Problem Statement

An organization needs to create an effective source of information for information pattern discovery (data mining).

### Problem Example

MCHS Trading wants to implement a next best action solution. This uses analytics to offer its customers relevant offers, information, and services depending on their individual interests. MCHS Trading needs to analyze information about its customers' interests, buying patterns, and channel usage along with the pipeline of new and existing products. This information is dispersed among MCHS Trading's production systems.

How should this information be made available to the analysis processes?

### Forces

- High processing requirement—The Information Pattern Discovery Process searches for patterns of values in one or more information collections. This processing can take considerable computing resources (memory, CPU, and disk I/O) to perform this activity.
- Disparate sources of information—The information to be analyzed often originates from a variety of sources.

### Solution Description

Create an information store that has flat structures in its information collections to allow the information pattern discovery process to work most effectively.

This information store is called an information mining store. Figure 5.63 shows how it is used. The numbers on the diagram in Figure 5.63 refer to these notes:

1. This is the information mining node.
2. It is provisioned using an information broker.
3. The information collections in this new node are provisioned as required from other information nodes. Typically, the source of information would be one of the big data nodes such as the Information Warehouse. However, it may be provisioned from Information Marts or operational information nodes such as the Operational Status Store or Information Asset Hub.
4. Once provisioned, the information analysis node uses the information mining store as a source of information to analyze. It makes direct Information Service calls on the information mining store to retrieve the information. The information mining store can be used in two modes:
- The analytics may be part of an ongoing solution where the analytics models are in production, driving an aspect of the business. In this case, the information mining store must be kept up to date with the latest information to ensure the analysis is working on good information. The information broker should provision the information mining store using Mirroring Provisioning and the analytics processing should access the information using Reference Usage only.
- The analytics may be part of an ad hoc project with a short lifetime. In this case, the information broker uses Snapshot Provisioning to populate the information mining store. If the analytics processing makes changes to the information, for example, to understand the effect of particular changes to the information, the information broker can repopulate the affected information collections by rerunning the snapshot provisioning.

### Solution Example

MCHS Trading creates two information mining stores for the analysis of its customer, order, and product information as seen in Figure 5.64.

For the next best action solution, MCHS Trading creates an information mining store called Next Best Action Analysis Store. It is refreshed regularly from the Reporting Hub using Mirroring Provisioning to ensure the analysis continues to use the latest information.

From time to time, MCHS Trading also has an information mining store called Marketing Analysis Store that is used for ad hoc analysis of product sales to plan marketing campaigns. This node is provisioned from the Reporting Hub using Snapshot Provisioning whenever it is needed.

### Benefits

- The analysis processing is not affecting the performance of the production systems.
- The data scientists do not need to be given access to the production systems.
- The analysis can start with a small subset of the information and grow the sample size as confidence in the analytics model increases.

### Liabilities

- The information mining store may be provisioned with sensitive or valuable information. This must be properly safeguarded.
- The information stored in an information mining store gradually decays and needs refreshing at regular intervals for the results to remain relevant.

### Usage

Using an information mining store to work on a local copy of an organization's information is a common approach for analysis. Often, it is implemented as a directory of files, or a database or data mart. This is also known as a type 4 operational data store (ODS) that is supporting data mining or related processes.

### Search Keywords

- Patterns of Information Management
- Information Node
- Information at Rest

### Version Identifier

1.0

### Status

ACTIVE

____

