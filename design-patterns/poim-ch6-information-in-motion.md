<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**Information in Motion**

Dr.Egeria commands for the design patterns in Chapter 6, "Information in Motion", of *Patterns of
Information Management* by Mandy Chessell and Harald C. Smith (IBM Press, 2013).
The book sets each pattern's identifier in small capitals; those small-capital names are used
here as the display names, and as the reference names in [poim-pattern-links.md](poim-pattern-links.md).

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Request

### Qualified Name

DesignPattern::Information Request

### Category

Information Request Patterns

### Description

Open a communication link with the remote information node and exchange the information and associated commands using an agreed-upon protocol.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization's information is distributed among its Information Nodes.

### Problem Statement

An information process needs to work with information located on a remote information node.

The information process will call a Remote Information Service to access the information collection. How is the remote information service implemented?

### Problem Example

MCHS Trading's Customer-Care application needs to work with customer details that are stored in the Customer Hub application.

### Forces

- Multiple information processes often work with the same stored information. This information may be located on a different information node.
- An information node is not always running.
- The structure in which information is stored is not always the most convenient structure for a consuming information process.
- If the structure of an information collection is changed, it may affect all information processes that use it.

### Solution Description

Open a communication link with the remote information node and exchange the information and associated commands using an agreed-upon protocol.

The full exchange is described below and it is illustrated in Figure 6.2 that follows:

1. The information process makes a request to the remote information service, passing parameters that described the request.
2. The remote information service formats the request and its parameters into an Information Payload and sends it to the information node where the information collection resides.
3. The information payload is received, unpacked, and the parameters are used to invoke a local information service.
4. The results of the local information service are formatted into another information payload and sent back to the originator to be returned to the information process.

### Solution Example

The Customer-Care application uses an information request to access the customer details stored in the Customer Hub.

### Benefits

- The information request pattern provides up-to-date information to information processes located in different information nodes and reduces the need to make copies of information.

### Liabilities

- The information node where the information collection is located must be operational whenever the information process needs information. In addition, the information service, or information process, may need to reformat the information to support the processing needs of the calling information process.

### Usage

The information request pattern is used for most types of remote procedure calls. These are available through the following types of technology:

- Web services technology
- Remote procedure calls (such as Enterprise Java Beans) supported by standards such as Java Enterprise Edition (JEE)
- REST
- ODBC and JDBC calls between an application and a database server

### Search Keywords

- Patterns of Information Management
- Information Request
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Flow

### Qualified Name

DesignPattern::Information Flow

### Category

Information Flow Patterns

### Description

Use an Information Trigger to start an Information Process to control the movement of information. This information process is responsible for extracting the required information from the appropriate sources, reengineering it, and delivering it to the destination information nodes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information needs to flow between information nodes with minimal impact to their current operation.

An organization is designing the implementation of a flow of information between information nodes. The source of the information is an existing information node. The destination may be a new information node, or an existing one, too. Neither information node currently has the capability to flow the information because it is not core to their operation.

This movement needs to be reliable, predictable, and asynchronous.

### Problem Example

Orders need to be transferred from the order-taking systems, such as E-Shop, to the Shipping system. Customers can order from E-Shop at all hours of the day. However, the order-processing component of the Shipping system is not continuously available—it is offline at certain times of the night to feed order information to the inventory system.

### Forces

- Availability differs—The availability of the source and destination information nodes may differ.
- Processing limitations—Processing capability may be limited in the source or destination information node whether due to system criticality, information volume, or platform limitations.
- Transformation required—Additional processing is required to transform the information before the destination can receive it.
- Complexity impacts design—As more information flows handling more information collections and more information processing are introduced, it becomes more difficult to design optimal information flows and reuse existing information flows.

### Solution Description

Use an Information Trigger to start an Information Process to control the movement of information. This information process is responsible for extracting the required information from the appropriate sources, reengineering it, and delivering it to the destination information nodes.

The information trigger that starts an information flow may be initiated from the source or destination information node, or from another information node such as an Information Broker. Refer to the information trigger patterns for more information on how each approach works.

The information process that is started is typically a provisioning information process. It may run in either the source or destination information nodes. However, it is more usual for it to run in an information broker. See Figure 6.4.

The provisioning information process often includes Information Reengineering Steps to transform the information into the required format for the destination. It may also include appropriate Information Guards and Information Probes to protect and monitor the flow of information, respectively.

The Information (RE)Deployment Process is the most commonly used information process for implementing information flows because it offers the most flexible capabilities for transforming the information as it flows between the source and destination.

### Solution Example

In the case of MCHS Trading's order information from E-Shop, a staging node is used to receive all incoming orders. The orders are collected until a specific information trigger starts a subsequent process to batch the information payloads in a standard format and deliver them to the Shipping system.

### Benefits

- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Information flows may require additional storage capacity for new staging nodes.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an Enterprise Service Bus (ESB). Usage includes the following:

- Synchronizing multiple applications that store the same type of information
- Acquiring and merging or consolidating information collections
- Distributing or broadcasting information to multiple destination information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Staged Routing

### Qualified Name

DesignPattern::Staged Routing

### Category

Information Flow Patterns

### Description

Insert a staging area in between the source and destination node to act as a temporary store for the information that is passing between them.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information needs to flow between two or more information nodes that are not always able to participate in the transfer at the same time; or an information node is unable to take responsibility for distributing information to a downstream node.

### Problem Example

MCHS Trading needs to provide its Customer-Care operations with faster access for order tracking to address customer complaints and missing orders.

### Forces

- Processing must be done external to the source or target—Information must be staged for additional processing from a source information node before it can be used in the destination information node.
- Timeliness varies—Where latency must be minimized, processing must occur immediately; where less critical, data may be batched for processing.

### Solution Description

Insert a staging area in between the source and destination node to act as a temporary store for the information that is passing between them.

Divide any processing required into the following:

1. An information process for extracting information from the source information node and storing it in the staging area
2. An information process for retrieving the information from the staging area and passing it to the destination Reengineering the information for the destination can be the responsibility for either of these information processes. It is shown in the second process in Figure 6.5.

### Solution Example

In the case of MCHS Trading's Customer-Care application, a new staging node is introduced after the order information processing queue, which serves the purpose of linking the order flow directly to the Customer-Care process. Customer-Care now has immediate access to all order information, reducing customer complaints and missing orders.

### Benefits

- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Information flows may require additional storage capacity for new staging nodes.

### Usage

Staged routing is most common in ETL engines or messaging engines. Where transformation of information is needed, the former is more likely. Where timely delivery on an ongoing basis is necessary, the latter is more likely.

Usage includes the following:

- Synchronizing multiple applications that store the same type of information in Application Nodes
- Acquiring and merging or consolidating information collections
- Distributing or broadcasting information to multiple destination information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Partitioned Routing

### Qualified Name

DesignPattern::Partitioned Routing

### Category

Information Flow Patterns

### Description

Identify which information needs the additional processing at the point it is sent. Route this information via an intermediate information collection, which feeds the additional processing, before forwarding it on to the downstream node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Some of the information that is flowing between two information nodes needs additional processing before the downstream information node can accept it.

### Problem Example

MCHS Trading needs different processing for customer name and address information than for order information coming from E-Shop that is simply passed through to the Shipping system.

### Forces

- Some data needs extra processing—Some information must be partitioned for additional processing from a source information node before it can be used in the destination information node.
- Computationally intensive processing—Some processing steps require dedicated information nodes to achieve the computations required in the necessary time frame.
- Timeliness is critical—The processing time must be minimized.

### Solution Description

Identify which information needs the additional processing at the point it is sent. Route this information via an intermediate information collection, which feeds the additional processing, before forwarding it on to the downstream node.

Partitioning allows multiple computational activities to occur simultaneously, reducing the overall processing time. It can be extended to include more than one partition depending on specific requirements. As long as sets of information can be segmented, multiple partitions may perform the same or different steps.

See Figure 6.6.

### Solution Example

MCHS Trading introduces a partitioned routing through a new information node to handle the additional processing needed for name and address information on E-Shop orders. This includes specialized Information Reengineering steps to Standardize Data, Enrich Data with demographics and geospatial information, and Link Entries to existing customer details in the Customer Hub. They add distinct partitions for North American and European customers as they expect minimal need to link data across sales regions. Within each region, because MCHS Trading needs to potentially link customers with nicknames or maiden names, they do not partition the customer name and address data further.

### Benefits

- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.
- Processing time for all information may be reduced.
- Only information requiring additional processing needs to be partitioned reducing the volume of information through that information node.

### Liabilities

- Information flows can increase latency between information nodes, particularly if some information must wait for the processing of partitioned information to complete.
- Information flows may require additional storage capacity for new staging nodes.
- Rules for partitioning must be maintained and may not readily respond to changing business conditions.

### Usage

Partitioned routing may be supported by an ETL engine, a messaging engine, or an ESB. Partitioning is used where information of different types is received and some require additional or different processing (such as account transactions over a specified monetary value). Partitioning may also be used to spread workload across multiple Information Brokers such as in parallel processing engines—in this case, partitioning may occur automatically as new information nodes are identified.

Usage includes the following:

- Synchronizing multiple applications that store the same type of information in Application Nodes
- Acquiring and merging or consolidating information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Buffered Routing

### Qualified Name

DesignPattern::Buffered Routing

### Category

Information Flow Patterns

### Description

Divide the problem into two parts: storing the information as it arrives into rolling timebased buffers and processing batches of information from each buffer when it is full.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Large quantities of information are arriving continuously that needs to be captured, filtered, and organized.

Sometimes there is a mismatch in the volume of information being produced by a source information node and the ability of the destination node to consume it. The information flow that links these information nodes together must balance the ability of the source information node to produce information against the ability of the destination to consume it.

### Problem Example

MCHS Trading started collecting social media data about the products its customers were interested in. The purpose was to understand and anticipate which products would sell well to different groups of people. There were two use cases for this data. The first was an immediate, operational use of the information to anticipate required stock levels and identify potential candidate products for promotions. This is covered in the Streaming Analytics Node pattern.

The second use was to create a historical record of the correlation of the social media content with the actual buying patterns of their customers. This second use of information requires summarized information from the social media data to be fed and correlated into their Historical System Of Record called the Reporting Hub. The issue they faced was how to organize the processing required to translate the insight from the social media data into the data warehouse structures at a fast enough rate to keep up with the incoming data.

### Forces

- Data is constantly arriving—Data generated from the real-world activity, such as social media data, or sensor data, continuously arrives. It is necessary to process it at the rate it is captured because otherwise you never get an opportunity to catch up.
- Data value degrades rapidly—This data contains a huge amount of detail about individual Information Events. The value of this level of detail tends to degrade fairly rapidly. To get the maximum value out of it, it is necessary to make use of the detail as soon as possible. Summarized versions of this data, when aggregated together, can provide interesting perspectives with longer-term value.

### Solution Description

Divide the problem into two parts: storing the information as it arrives into rolling time-based buffers and processing batches of information from each buffer when it is full. See Figure 6.7. The objective of this solution is twofold:

- To minimize the contention on the storage media by only having one information process accessing it at any one time
- To balance the processing power given to the computing intensive work of summarizing and collating information into the destination The information broker working with the source is focused on filling the staging areas with information. It fills one then moves on to the next. When it has filled them all, it starts again, filling the first one. In the meantime, one or more information brokers are unloading the filled staging areas. They must complete their processing before the source's information broker starts to reuse their staging area. They are responsible for summarizing and collating the raw information from the source and transferring the results to the destination.

### Solution Example

MCHS Trading use the buffered routing pattern to handle the summarization and collating of the insight from the social media data into its Reporting Hub.

### Benefits

- By separating the process of capturing the information into chunks and then processing each chunk, it is possible to scale out the computing intensive work of the destination information brokers. The result is a flexible implementation that can adapt to changes (usually increases) in data volume.

### Liabilities

- The trick when using this pattern is to have sufficient destination information brokers to handle the velocity of the incoming data. It is also important to have a contingency, or spare capacity, in the staging areas, for when the destination is not available—for example, during maintenance.

### Usage

This pattern is often used when loading large volumes of operational data into an Information Warehouse. Buffered routing may also be applied when handling widely varying volumes of messages to ensure that message queues are not filled up.

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Filtered Routing

### Qualified Name

DesignPattern::Filtered Routing

### Category

Information Flow Patterns

### Description

Filter the information collection to send only the information required in the downstream information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

A downstream information collection does not require or cannot consume all information from the upstream information collection.

### Problem Example

MCHS Trading cannot distinguish the types of customers used in its reporting processes.

### Forces

- Not all data is needed—Information must be filtered from a source information node before it can be used in the destination information node.
- Processing resources are limited—The cost to increase processing capability is not justified versus the work that must be done.

### Solution Description

Filter the information collection to send only the information required in the downstream information collection.

See Figure 6.8.

### Solution Example

In the case of MCHS Trading's reporting process, only certain customers should be reported so customer information flowing to the Reporting Hub is filtered to address this consideration.

### Benefits

- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Only required information needs to be filtered and passed to the destination information node, reducing the volume of delivered information.
- Timeliness of delivery is improved as processing volume is reduced.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Rules for filtering must be maintained and may not readily respond to changing business conditions.

### Usage

Filtered routing may be supported by an ETL engine, a messaging engine, or an ESB, particularly where the source system cannot segregate outgoing information. Usage includes the following:

- Acquiring and merging or consolidating information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, Application Node, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational applications
- Reporting on information stored in specific information collections

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Summarized Routing

### Qualified Name

DesignPattern::Summarized Routing

### Category

Information Flow Patterns

### Description

Summarize the information collection to send only the information required in the downstream information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

A downstream information collection cannot consume detailed information or requires summarized or aggregated information from the upstream information collection.

### Problem Example

MCHS Trading currently dumps all transactional information into the Reporting Hub. This has significant impact on the ability to generate reports pertaining to customer orders for key product lines as well as performing subsequent analysis.

### Forces

- Information must be summarized—Information must be summarized from a source information node before it can be used in the destination information node.

### Solution Description

Summarize the information collection to send only the information required in the downstream information collection.

See Figure 6.9.

### Solution Example

In the case of MCHS Trading's Reporting Hub, product details are now summarized in the routing process into broader product lines relevant to order summaries. The Reporting Hub can generate reports faster and subsequent analysis provides greater insight into customer buying patterns.

### Benefits

- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Only required information needs to be summarized and passed to the destination information node.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Rules for summarization must be maintained and may not readily respond to changing business conditions.
- Changes to summarization levels can dramatically impact downstream dependencies (e.g., reporting).

### Usage

Summarized routing is primarily supported by an ETL engine. Usage includes the following:

- Acquiring and merging or consolidating information collections
- Populating and maintaining summarized information collections stored in an Information Warehouse, Information Mart, Information Cube, or Information Asset Hub
- Supporting information reporting and analytics solutions

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Synchronized Consolidation

### Qualified Name

DesignPattern::Synchronized Consolidation

### Category

Information Flow Patterns

### Description

Use a provisioning information process to extract and assemble the information from the source information nodes and send it on to the downstream information node(s).

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Consistent values need to be consolidated from multiple information nodes.

### Problem Example

MCHS Trading's Customer-Care services requires consolidated information from both the Shipping system for orders and the Customer Hub for customer detail in order to effectively respond to customer service requests. The lack of consistent and timely information from the Shipping system has significantly impacted the quality of customer service.

### Forces

- Consumption of information must be synchronized—Information must be synchronized between multiple source information nodes before it can be consumed in the destination information node.
- When information is updated, the changes must be synchronized with all copies— Without this synchronization, the copies become inconsistent.
- Information must be consolidated from multiple sources—Information must be grouped or consolidated from multiple source information nodes before it can be used in the destination information node.
- Time delays must be minimized—Latency must be minimized or nonexistent between source and destination information nodes.
- Timing is different between information sources—Information must be processed from multiple source information nodes on differing schedules.

### Solution Description

Use a provisioning information process to extract and assemble the information from the source information nodes and send it on to the downstream information node(s).

With a synchronized consolidation, all the data that either system knows about specific information values is sent at the same time.

See Figure 6.10.

### Solution Example

In the case of MCHS Trading's customer data processing, the introduction of an Order Tracking process allows earlier capture of customer order information. However, it still requires a synchronized consolidation to ensure that the right customer information is available and connected to the order information in a timely manner for Customer-Care services to respond appropriately.

### Benefits

- Consolidation from all sources occurs at the same time, minimizing discrepancies to downstream destinations.
- Synchronization ensures that consistent information is available across the information flow.
- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Synchronization requires coordinated timing across the information flow.
- The synchronization process needs to understand the format of each of the sources and the destination system and the scope of information required.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new source is added to the information supply chain.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an ESB. Usage includes the following:

- Synchronizing information from multiple sources into an Application Node or an Operational Status Store
- Acquiring and merging or consolidating information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages, particularly those entered as multiple parts (e.g., a header, some number of line item details, and a trailer), from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Filtered Consolidation

### Qualified Name

DesignPattern::Filtered Consolidation

### Category

Information Flow Patterns

### Description

Use a provisioning information process to extract and filter the information from the source information nodes and send it on to the downstream information node(s).

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information from multiple information nodes must be consolidated through specific filters for use by one or more downstream nodes.

### Problem Example

MCHS Trading's Product Hub application generates and sends out all product catalog information. The Stores only care about product information for those products that they stock on shelves and receive a filtered collection. However, this approach has inhibited the Stores from keeping up with current buying trends, resulting in business shifts to the E-Shop, Mail-Shop, or other companies.

### Forces

- Not all data is needed—Information must be filtered from multiple source information nodes before it can be consumed in the destination information node.
- Some information is more valuable than others—It makes sense to focus on the most valuable and delete the information that has no value at all.
- Information is spread across multiple sources—Information must be grouped or consolidated from multiple source information nodes before it can be used in the destination information node.
- Timing may be distinct in different sources—Information must be processed from multiple source information nodes on differing schedules.

### Solution Description

Use a provisioning information process to extract and filter the information from the source information nodes and send it on to the downstream information node(s).

See Figure 6.11.

### Solution Example

In the case of MCHS Trading's Stores system, the application is enhanced to not only filter the product catalog from the Product Hub to the Stores system based on individual store stock requests, but also to receive an additional list of best-selling items from the Shipping system. This additional filtered consolidation of product information has allowed the Stores to change stocking patterns to become competitive.

### Benefits

- Only required information needs to be filtered and passed to the destination information node, reducing the volume of consolidated and delivered information.
- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new source is added to the information supply chain.
- Rules for filtering must be maintained and may not readily respond to changing business conditions.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an ESB. Usage includes the following:

- Filtering information from multiple sources into an Application Node
- Acquiring and merging or consolidating information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Filtering and delivering messages from multiple incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Ordered Consolidation

### Qualified Name

DesignPattern::Ordered Consolidation

### Category

Information Flow Patterns

### Description

Use a provisioning information process that is able to sequence and process the information from multiple nodes in a given order even in the event of a failure and restart.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information needs to be reliably obtained and consolidated from multiple information nodes in a predefined order.

### Problem Example

MCHS Trading's Reporting Hub receives unordered transaction information from the Shipping and Invoicing systems. However, this has created reporting issues as invoices and payments are not correctly linked to the associated orders.

### Forces

- Information must be ordered—Information must be ordered or sequenced before it can be consumed in the destination information node.
- Information must be brought from different sources—Information must be grouped or consolidated from multiple source information nodes before it can be used in the destination information node.
- Timing of delivery varies—Information must be delivered from multiple source information nodes on differing schedules.

### Solution Description

Use a provisioning information process that is able to sequence and process the information from multiple nodes in a given order even in the event of a failure and restart.

Ordering can be supported by specific sequencing in retrieving or triggering requests of information from the sources, or by processes that subsequently order the information within the information flow. Ordered consolidation is needed when the values from one system determine which values to pull from another. See Figure 6.12.

### Solution Example

MCHS Trading's Reporting Hub is modified to support an ordered consolidation where it receives and processes transactions in a specific sequence of order, invoice, and payment.

### Benefits

- Ordering ensures that information is appropriately sequenced and available across the information flow.
- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Ordered information flows increase latency between information nodes as information must wait for specific sequencing, particularly as the number of incoming components within the information flow grows more complex.
- Ordering requires coordinated timing across the information flow particularly in the source information nodes.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new source is added to the information supply chain.
- Rules for ordering must be maintained and may not readily respond to changing business conditions.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an ESB. Usage includes the following:

- Sequencing information from multiple sources into an Application Node or an Event Correlation Node
- Acquiring and merging or consolidating information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational applications particularly where sequence of messages must be understood and maintained (e.g., create order before update or cancel order)

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Independent Consolidation

### Qualified Name

DesignPattern::Independent Consolidation

### Category

Information Flow Patterns

### Description

Flow the information from each information node independently as soon as it is available. Consolidate their values within the receiving information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

An information node requires information from multiple information nodes as soon as it is available.

### Problem Example

MCHS Trading needs to fulfill orders from the E-Shop and Mail-Shop as soon as they are received in order to ensure timely entry of customer orders and to maintain accurate inventory levels.

### Forces

- Information consolidated from multiple sources—Information must be grouped or consolidated from multiple source information nodes before it can be used in the destination information node.
- Timing varies—Information must be processed from multiple source information nodes on differing schedules.
- Time delays must be minimized—Latency must be minimized or nonexistent between source and destination information nodes.

### Solution Description

Flow the information from each information node independently as soon as it is available. Consolidate their values within the receiving information node.

See Figure 6.13.

### Solution Example

In the case of MCHS Trading's Order Transaction system, all order transactions are delivered independently from the E-Shop and Mail-Shop as they are received. The Order Transaction system has processes to read these transactions from an information broker that queues all incoming requests.

### Benefits

- Independent consolidation removes synchronization and ordering requirements across the information flow.
- Independent information flows can minimize latency between information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Complexity may be increased in the source and destination information nodes to handle independent processing.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new source is added to the information supply chain.
- Rules for handling each information source must be maintained and may not readily respond to changing business conditions.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an ESB. Usage includes the following:

- Acquiring and merging or consolidating information collections into an Application Node
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from multiple incoming information nodes to specific operational applications or Application Nodes

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Synchronized Distribution

### Qualified Name

DesignPattern::Synchronized Distribution

### Category

Information Flow Patterns

### Description

Use a provisioning information process that is able to send the information to multiple nodes even in the event of a failure and restart.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information needs to be reliably distributed to multiple downstream information nodes.

### Problem Example

Customers of MCHS Trading find that the products available in the E-Shop and Mail-Shop are not consistently available. This creates customer confusion and frustration when trying to order goods.

### Forces

- Delivery must be synchronized—Information must reach multiple destination information nodes at the same time.
- When information is updated, the changes must be synchronized with all copies— Without this synchronization, the copies become inconsistent.
- Timing is critical—Latency must be minimized or nonexistent between source and destination information nodes.

### Solution Description

Use a provisioning information process that is able to send the information to multiple nodes even in the event of a failure and restart.

With synchronized distribution, all the data about specific information values is sent to and stored at all destinations simultaneously.

See Figure 6.14.

### Solution Example

In the case of MCHS Trading's Product Hub application, the distribution of product catalog details was not synchronized across the different customer shopping channels. By introducing a new integration process, MCHS Trading can now synchronize distribution to both the E-Shop and Mail-Shop applications.

The processes in the information flow control the distribution to all of the destinations in a consistent and simultaneous fashion. In the synchronized distribution pattern, the process needs to understand the formats of each system and which subset of the information is required.

### Benefits

- Distribution to all destinations occurs at the same time, minimizing discrepancies between downstream destinations.
- Synchronization ensures that consistent information is available across the information flow.
- Synchronization is handled outside the source or destination information collections, reducing processing complexity.
- Removal of information in all information nodes is supported when deliveries to one or more information nodes fail.
- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Synchronization requires coordinated timing across the information flow and must be able to remove previously delivered information if other information nodes fail to receive the same information.
- The synchronization process needs to understand the format of the source and each destination system and which subset of the information is required.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new destination is added to the information supply chain.

### Usage

Synchronizing information flows describe how information moves from one information collection to another and stay consistent with one another. The technology that supports them may be an ETL engine or an ESB. Usage includes the following:

- Synchronizing multiple applications that store the same type of information
- Distributing information to multiple destination information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Partitioned Distribution

### Qualified Name

DesignPattern::Partitioned Distribution

### Category

Information Flow Patterns

### Description

Extract and store the appropriate information into transient information collections, one per destination. Transform and deliver to each destination from the appropriate information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information from an information node must be distributed among multiple downstream information nodes according to a classification rule.

Partitioning allows multiple computational activities to occur simultaneously, reducing the overall processing time. It can be extended to include more than one partition depending on specific requirements. As long as sets of information can be segmented, multiple partitions may perform the same or different distribution steps.

### Problem Example

MCHS Trading's Product Hub application is used to create the approved descriptions of the products that the company sells. Once the product details are approved, they must be sent to the appropriate order-processing systems: E-Shop, Mail-Shop, Stores, Shipping, and Invoicing. Each order-processing system has its own format for storing product details. Because not all products are sold through every channel, each of the order-taking systems (E-Shop, Mail-Shop, and Stores) needs a different subset of the product details.

### Forces

- Information must be segmented—Information must be partitioned for delivery across multiple destination information nodes.
- Timeliness is critical—The processing time must be minimized.

### Solution Description

Extract and store the appropriate information into transient information collections, one per destination. Transform and deliver to each destination from the appropriate information collection.

Partitioning allows multiple computational activities to occur simultaneously, reducing the overall processing time. It can be extended to include more than one partition depending on specific requirements. As long as sets of information can be segmented, multiple partitions may perform the same or different distribution steps.

See Figure 6.15.

### Solution Example

MCHS Trading uses partitioned distribution to flow the product details from the Product Hub application to the order-processing application. Each application receives a subset of the product details to match its scope. See Figure 6.16.

### Benefits

- Only required information needs to be partitioned and passed to the destination information nodes, reducing the volume of distributed information.
- Processing time for all information may be reduced.
- Complexity is reduced in the source and destination information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new destination is added to the information supply chain.
- Rules for partitioning must be maintained and may not readily respond to changing business conditions.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an ESB. Usage includes the following:

- Distributing or broadcasting information to multiple destination information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational Application Nodes

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Ordered Distribution

### Qualified Name

DesignPattern::Ordered Distribution

### Category

Information Flow Patterns

### Description

Use a provisioning information process that is able to send the information to multiple nodes in a given order even in the event of a failure and restart.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information needs to be reliably distributed to multiple downstream information nodes in a predefined order.

### Problem Example

MCHS Trading's Stores system generates new loyalty cards and must ensure accuracy for customer accounts. However, the customer and loyalty card information are delivered directly to the Accounting system without correctly creating or updating the Customer Hub first. As a consequence, the Accounting system stores the loyalty card information but in many instances links to the wrong or no customer records. Customers are upset that they encounter issues trying to use their loyalty cards.

### Forces

- Sequencing is critical—Information must be delivered across multiple destination information nodes in a specific order or sequence.
- Availability may impact ordering—Information must be delivered to multiple destination information nodes on differing schedules.

### Solution Description

Use a provisioning information process that is able to send the information to multiple nodes in a given order even in the event of a failure and restart.

See Figure 6.17.

### Solution Example

In the case of MCHS Trading's Stores system, the distribution is modified to perform an ordered sequence of events: first, generating the customer information in the Customer Hub; then, generating the loyalty card information in the Accounting system. This resolves the issues in the Accounting system.

### Benefits

- Ordering ensures that information is appropriately sequenced and available across the information flow.
- Complexity is reduced in the source and destination information nodes.
- Removal of information in initial information nodes is supported when deliveries to subsequent information nodes fail.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Ordered information flows increase latency between information nodes as information must wait for specific sequencing, particularly as the number of outgoing destinations within the information flow grows more complex.
- Ordering requires coordinated timing across the information flow particularly in the destination information nodes and must be able to remove previously delivered information if other subsequent information nodes fail to receive the same information.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new destination is added to the information supply chain.
- Rules for ordering must be maintained and may not readily respond to changing business conditions.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an ESB. Usage includes the following:

- Distributing or broadcasting information to multiple destination information collections such as Application Nodes
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational Application Nodes

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Independent Distribution

### Qualified Name

DesignPattern::Independent Distribution

### Category

Information Flow Patterns

### Description

Use independent Information Requests , or Information Flows , to transmit the information from each of the nodes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

Information needs to be distributed to different downstream nodes on different schedules.

### Problem Example

MCHS Trading has encountered a high level of customer duplication between their E-Shop and Mail-Shop, and the lack of a Customer Hub means that customers often must reenter their information to place new orders, increasing customer frustration.

### Forces

- Delivery time is critical—Latency must be minimized or nonexistent between source and destination information nodes.
- Information must be delivered to multiple destination information nodes on differing schedules.

### Solution Description

Use independent Information Requests or Information Flows to transmit the information from each of the nodes.

See Figure 6.18.

### Solution Example

When MCHS Trading introduced its Customer Hub, one of its goals was to ensure that existing customers did not have to reenter their information to place new orders in either the E-Shop or Mail-Shop. By establishing an independent distribution from the Customer Hub, updated customer information is made available to the E-Shop and Mail-Shop at the points when those applications can apply it.

### Benefits

- Independent distribution removes synchronization and ordering requirements across the information flow.
- Independent information flows can minimize latency between information nodes.
- Information flows can be standardized and reused in multiple conditions.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Information flows can increase latency between information nodes, particularly as the components within the information flows grow more complex.
- Complexity may be increased in the source and destination information nodes to handle independent processing.
- Recoding of the processes in the flow may be required every time a change is introduced to the information collection or a new source is added to the information supply chain.
- Rules for handling each information destination must be maintained and may not readily respond to changing business conditions.

### Usage

Information flows describe how information moves from one information collection to another. The technology that supports them may be an ETL engine, a messaging engine, or an ESB. Usage includes the following:

- Distributing or broadcasting information to multiple destination information collections
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational Application Nodes

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Broadcast Distribution

### Qualified Name

DesignPattern::Broadcast Distribution

### Category

Information Flow Patterns

### Description

Use an Information Broadcast Process running in a Queue Manager to broadcast to destination adapters that can transform and deliver the information to the destination.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 6, "Information in Motion".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information should flow between information collections located in different information nodes.

### Problem Statement

An information node needs to distribute information to an arbitrary number of downstream information nodes.

### Problem Example

MCHS Trading is finding it difficult to ensure that product inventory levels are consistently updated from the Shipping system across their E-Shop and Mail-Shop applications (the Stores maintain their own product inventories) in a timely fashion impacting customer satisfaction.

### Forces

- Only interested parties want the information—Information is distributed only to destination information nodes with an interest in the information.
- Process as quickly as targets demand—Latency must be minimized or nonexistent from the source but may vary based on the destination information nodes.
- Targets operate independently—Information must be delivered to multiple destination information nodes on differing schedules.

### Solution Description

Use an Information Broadcast Process running in a Queue Manager to broadcast to destination adapters that can transform and deliver the information to the destination.

If a destination is able to consume the information from the source, then the destination adapter is not needed. Also, if the information broker is able to host the information broadcast process, the queue manager node would not be required. See Figure 6.19.

### Solution Example

In the case of MCHS Trading's product inventory, the Shipping system processes are modified to utilize a broadcast distribution flow instead of independent processes. Each of the receiving application nodes is also modified to subscribe to the broadcast.

### Benefits

- Broadcast distribution removes synchronization and ordering requirements across the information flow.
- Complexity is minimized in the source and destination information nodes, as all processing is independent and disconnected.
- Broadcast distribution flows can minimize latency to destination information nodes.
- Recoding of the processes in the flow is not required when new destinations are added to the information supply chain.
- Information flows can be standardized and reused in multiple conditions.
- New target information nodes can be easily added.
- Variability in access to information nodes can be accommodated.

### Liabilities

- Broadcast distribution flows can increase latency between information nodes, when destination information nodes cannot increase their speed of processing.
- There is a limited ability to ensure that target information nodes pick up the new information.
- Recoding of the processes in the destination information nodes may be required every time a change is introduced to the broadcast information collection.

### Usage

Information flows describe how information moves from one information collection to another. The technology that most commonly supports broadcast distribution is a messaging engine or an ESB. Usage includes the following:

- Broadcasting information to multiple destination information collections
- Populating and maintaining information collections stored in an Application Node, Information Content Node, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational Application Nodes

### Search Keywords

- Patterns of Information Management
- Information Flow
- Information in Motion

### Version Identifier

1.0

### Status

ACTIVE

____

