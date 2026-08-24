<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**Information Architecture**

Dr.Egeria commands for the design patterns in Chapter 4, "Information Architecture", of *Patterns of
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

Information Element

### Qualified Name

DesignPattern::Information Element

### Category

Information Element Patterns

### Description

Group together related information attributes that follow the same life cycle and manage them appropriately.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Managing the information needs of an organization can seem overwhelming. There are many types of information, located in different places, and managed using different technologies. Where do you start?

### Problem Statement

An organization is looking for the best approach to manage the many kinds of information it has.

The organization wants to focus on the most important kinds of information and manage that efficiently and effectively. It knows there are different types of information management technology (such as master data management hubs, information quality tools, data warehouses, information integration tools) that can help, but it is not obvious how to map them to the information nodes (systems) and subject areas (topics) the organization has and show how they deliver value to the business.

### Problem Example

The purpose of the MCHS Trading organization is to sell goods to its customers. This activity needs information about its customers, products, the orders taken, and the money received, among other things. How should this information be managed?

### Forces

- Information management must handle the variety of information and its needs change:
- An organization's information needs are complex—The information held by an organization is complex with many competing requirements.
- The world is constantly changing—Information needs to be kept up to date.
- Information is duplicated—Information about the same object, person, organization, activity, result, event, or concept exists in many forms and is not always consistent.
- When information is updated, the changes must be synchronized with all copies— Without this synchronization, the copies become inconsistent.
- Some information is more valuable than others—It makes sense to focus on the most valuable and delete the information that has no value at all.
- The value of information changes over time—How do you know when it is no longer required?
- The value and meaning of information depends on perspective—Individuals across the organization will need different kinds of information, with different levels of precision, accuracy, and currency.
- Some information is mandatory—Information that must be produced for legal regulations often also requires a proof that it is correct.

### Solution Description

Group together related information attributes that follow the same life cycle and manage them appropriately.

In information management, we think about the organization's information as a set of linked information elements. An information element is a collection of attributes that relates to a specific object, person, organization, activity, event, result, or concept.

An information element can be any size—from a few bytes representing a reading from a sensor, to details about a person, to a document describing how to fix an engine, to a multigigabyte result of a scientific simulation.

No matter what the size of an information element, its important characteristic is that the information within it follows the same life cycle—so we can manage the content of an information element in a consistent way.

The specifics of an information element's life cycle will depend on the Information Processes that are manipulating it, but, in general, the information element will follow one of the following patterns:

- Information Asset—The record of a core component or asset of the business, such as an organization, person, real-world concept, object, product, or physical assets. The lifetime of an information asset is typically of long duration and its values change slowly. Many information processes throughout the organization use this information so there are many copies that need to be synchronized.
- Information Activity—The record of an activity that the organization is performing or monitoring. The information activity element is created when the activity starts. As the activity progresses, more information is added to it to reflect the current state of the work. When the activity completes, the information activity element is no longer updated, but can be kept for reference. Eventually, it is deleted. Key attributes within an information activity may be Information Links to information assets and information events.
- Information Event—The record of an event that has occurred. This would include when, where, and in what context the event occurs. Information event elements typically do not change in their core values once they are created, although other information elements may be linked to it to describe the context in which the event occurred and any action taken as a result.
- Information Processing Variables—Private information values used by an information process as it executes. These values describe the context in which the process was started and in which information is being gathered from the information users of the information process. Some values are implicit in the code that drives the information process. Often the initial values of these information processing variables come from an information event that triggered the process to start. It is augmented with information from the information users and it, in turn, populates an information activity, which is the persisted information about the work that the information process is supporting.
- Information Payload—Information values packaged up for sending over the network. Information payloads have a short lifetime. At the start, they reflect the originator's view of the information. As it flows through the network, it may be transformed and enriched to match the needs of the destination(s).
- Information Link—Attributes that provide the information necessary to identify and retrieve values from a specific information entry stored in a different information collection. The information link is typically stored as an attribute in another information element and the information processes managing the hosting information element control its lifetime. So the life cycle of an information link is different from the information entry it represents—creating some interesting challenges.
- Information Metric—Information values that have been derived from other values to illustrate how well the organization is performing in a particular aspect of its operation. Information metrics are constantly refreshed, but maintain a historical record of their values to allow point-in-time queries.
- Information Code—A representation of an information value. Sets of related information codes are grouped together into code tables and are used to govern the values used in an information attribute.
- Information Summary—Summarized information kept for historical analysis. It is updated periodically as time passes because more values become available for summarization. Information about a subject area (topic) is not restricted to a single kind of information element. For example, consider the customer details subject area. When information is being collected to register a new customer, customer details are collected in information process variables and then possibly stored in an information activity if this is an auditable process. When the customer is established, his or her details will be managed as an information asset. When information about a customer is sent between information nodes, it is stored in an information payload. An order may link to customer details using an information link and, finally, customer details may appear in information summaries and information metrics for reporting purposes. This example illustrates the importance of identifying and classifying the information elements because these are the strongest indicators of how each piece of information should be managed. Also notice that information elements reference one another and some elements are created from others. As a result, errors should be removed from information as early as possible because they can rapidly become proliferated to multiple information collections, which in turn impacts multiple information processes. In addition, we must consider the following:
- How we manage different information elements that may nominally carry the same information but are located in different places and hosted by different technology
- How we maintain relationships between different kinds of information elements when each has its own independent life cycle Some answers to these questions can be found in the pattern descriptions for the specialized information elements and their related patterns.

### Solution Example

In order to sell goods to its customers, MCHS Trading manages information elements relating to its customers, the products it sells, and the orders that have been placed. MCHS Trading also needs to create invoices, packing lists, and process payments.

Figure 4.2 shows where this information is located and the type of life cycle it belongs to. Notice that even for this fairly simple use case, there is a lot of information required and it is duplicated across many of the Information Nodes (systems). Each copy is likely to be structured differently.

### Benefits

- Understanding the information elements associated with the information processes of an organization helps to ensure the information is properly managed throughout its life cycle.

### Liabilities

- Organizations typically have limited budgets for information management. The temptation is to categorize all of the information it manages—taking time and resources and yielding limited value. It is important to focus on the information that supports the most critical information processes for the organization. Once this is properly categorized and managed, the next focus should be on removing the information that either has no value, or represents a liability because it is inaccurate or obsolete.

### Usage

The generic concept of an information element is defined during the logical modeling of information structures. Groups of related attributes—for an object, for example, or an entity or a table— are referred to as model elements.

Aspects of an organization's information are classified into different kinds of information elements whenever an investment is being considered. This could be during the formation of the Information Strategy, when an Information Governance Program is being set up or extended, or at the start of an Information Solution. Further information elements are identified as these projects progress.

Practitioners recognize the different kinds of information elements, identifying and cataloging their occurrences whenever they are found, and using specialized technology to manage them. Associated practices on how to manage each kind of information element have also been developed. These are documented in the pattern descriptions for each kind of information element. However, to illustrate the point here, consider the Information Asset pattern. This type of information element is often referred to as master data. Master data is managed using the Master Data Management (MDM) practices and there are specialized MDM technologies to manage this information. Now consider the Information Link pattern. There are standards developed around this type of data such as the World Wide Web Consortium (W3C)'s uniform resource locator (URL) and Open Services for Lifecycle and Collaboration (OSLC). These standards have best practices and specialized technology to manage them. Finally, consider the Information Payload. To Enterprise Application Integration (EAI) practitioners, this is called a message, and it is supported using message-oriented technologies such as queues and publish-subscribe services.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Asset

### Qualified Name

DesignPattern::Information Asset

### Category

Information Element Patterns

### Description

Centrally manage this information and synchronize changes with other copies.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

An organization needs to retain information it knows about the goods and services it offers, the assets it has, and the relationships it maintains with other parties (people and organizations).

This type of information describes the physical world. It provides the background information for many of the activities in the organization. It enables the organization to document the complex interaction it has with the physical world. What are the information management approaches required to manage this type of information?

### Problem Example

MCHS Trading needs to maintain a product catalog and details of customers who have registered with the E-Shop or have a store card.

### Forces

- Widely distributed information—This type of information is needed in many of the information processes used by the organization because it describes the key concerns of the organization.
- Slowly changing—This type of information changes in a slow and continuous manner.
- Inconsistent validation—The set of valid values for an information element may not be consistent throughout the organization.
- Varying coverage—Not all parts of the organization use the same subset of attributes about the type of information.

### Solution Description

Purposefully maintain as little information as possible about the physical world and actively coordinate how this information is updated and distributed.

This type of information is called an information asset because it has enduring value across many activities of the organization and needs to be managed and maintained to preserve its value.

Within an information collection that contains information assets, there would be:

- An identifier, typically assigned by the organization
- Some basic attributes that the asset is known by outside the organization
- Information values that are shared by many of the other copies of this information
- Information values that are unique to this copy The state of the physical world is outside of the control of the organization. Even when it describes physical assets that the organization owns, it cannot be sure when it will break, or be needed by someone. This means it takes a proactive approach to keep this information up to date. Such updates need to be distributed among all of the copies. The principles for managing information assets are as follows:
- Maintain only the information that has value to the organization. This requires coordination between each part of the organization using this information to define what is really required. There will be differences in scope, precision, and vocabulary so these negotiations can take time and, inevitably, flexibility is required.
- Pay special attention to how individual instances are uniquely identified and mapped to the physical world.
- Be realistic about the rate of decay of this information and take steps to refresh the values when appropriate.
- Look for mechanisms that will allow you to automatically refresh the information from external sources.
- Minimize the places where this information is maintained.
- Coordinate the synchronization to other, reference copies.

### Solution Example

MCHS Trading maintains its product catalog in a single application called Product Hub. Once updates are made, read-only copies of the product descriptions are distributed to the other applications that need the product details using Mirroring Provisioning.

The story for customer details is more complex because both the Stores and the E-Shop maintain their own customer details. The Mail-Shop applications only take a customer's details as part of an order. MCHS Trading installed a Customer Hub (Information Asset Hub pattern) to act as the consolidated master for customer details that synchronizes updates between itself, E-Shop, and Stores using Peer Provisioning.

### Benefits

- Consistently managing your information assets creates an organization that is acting in a consistent manner with respect to the physical world objects, people, and assets they represent. It is also able to react to change because information remains stable even though the information processes will change.

### Liabilities

- Consistently managing information assets needs a mature organization that is willing to collaborate and agree how this information should be managed and paid for. We call this an Information Centric Organization.

### Usage

Information assets are often referred to as master data in operational systems and dimensional data in data warehouse and business intelligence systems. The approach used to manage this type of information is called Master Data Management (MDM).

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Activity

### Qualified Name

DesignPattern::Information Activity

### Category

Information Element Patterns

### Description

Manage this information close to the information processes that are supporting the activity and distribute read-only copies once the activity is complete.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

An organization needs to keep track of its activities to ensure it keeps its promises to deliver value and receives appropriate recognition.

This information is sometimes referred to as the transaction record of the activity and is used to record the decisions and actions of the information processes that are supporting the activity. Once the activity is complete, the organization may need to understand why a decision was made—or why an activity resulted in a particular outcome. Typically, this analysis happens some time after the event and the values of related information assets may have changed since the work was carried out.

### Problem Example

MCHS Trading must keep track of the orders it has accepted to make sure it delivers the goods as promised and collects appropriate payment. Once the order is shipped, MCHS Trading needs to know the actual name and address of the customer that was associated with a particular order in case there is an issue with the delivery. This is particularly important when a customer changes his or her address—was the order associated with the old address or the new one?

### Forces

- Activity is distributed—Not all of the activity to fulfill a business commitment occurs at the same time, place, or through a single information process.
- Intermittent failures occur—One or more information nodes may fail while an activity is partially complete. The information supply chain needs to recover and continue with the activity.
- Historical information is required—Not all information nodes are able to support temporal queries and so this historical information must be stored away from the originating information collection.

### Solution Description

Create a record of each activity with information about the environment in which the activity took place.

An information activity is a stored record of a business activity. While the activity is in progress, one or more information processes that are supporting the business activity maintain it.

The information held within an information activity typically includes the following:

- Links to the information assets that are involved in the activity
- Links to the information events that are relevant to the activity
- Details of the steps that have been processed so far and the current state of the activity The information activity is typically persisted as an information entry in an information collection. When the information process is complete, the information activity is marked as complete and this final update is persisted to the information collection. The information activity is not updated again. It may be retrieved at a later time to understand how the activity was processed. When the information activity is no longer needed for reference, it can be either deleted or archived to free up operational storage.

### Solution Example

When one of the MCHS Trading order-taking applications—E-Shop, Mail-Shop, or Stores— takes an order, it creates an information activity to represent the order.

Order information stored by MCHS Trading's applications always includes details of the customer's name, address, and customer number. It also includes the date and time the order was taken and the channel used. This means that there is a permanent record of where the goods were sent, even if the customer changes address at a later date.

This order information is sent to the Shipping application, which packages up the ordered goods and sends them to the customer. The order information is updated with the package information and the date it was sent. Then the order information activity is sent to the Invoicing application, where an invoice is sent and the payment is received. Again, the Invoicing application records the progress of collecting the payment in the order information activity.

When the order information activity is passed to the Shipping application, the order-taking applications do not update their copy of the activity again. Similarly, when the Shipping application sends the order information activity to the Invoicing application, it no longer updates its copy. The result is that you have to query the right application to find the latest state of the order, and there are three copies of the order information activity to delete/archive when they are no longer needed.

### Benefits

- The information activity pattern provides an elegant solution for storing the values associated with an information process along with its current state.

### Liabilities

- When an information process spans multiple information nodes, the out-of-date information activities are left on the information nodes that have completed their processing. Knowledge of the structure of the information process is needed to chase down the most up-to-date copy of the information activity.
- At some point in time after the information process instance has completed, the information supply chain must either archive or delete the information activity because the number of information activities grows over time.
- Storing the information activities once the information process is complete results in lot of additional information being kept for the rare occasion when it is necessary to investigate the processing or a particular piece of work. So the ability to understand a complete picture in these circumstances needs to be weighed against the increase in information being stored.

### Usage

An information process will use an information activity to store information about the business transaction it is processing.

In data warehouse applications, information activities are sometimes called transaction records, which are stored in fact tables in the data warehouse. These information activities may be consolidated from the various operational systems running the organization's business.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Event

### Qualified Name

DesignPattern::Information Event

### Category

Information Element Patterns

### Description

Store the event for audit purposes and send a read-only copy to the parties that must react to the new situation.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

Something significant has occurred and the organization needs to react to it.

Such an event can have consequences, either immediately, or sometime later.

### Problem Example

An MCHS Trading customer phones the customer support center to notify the organization that he has changed his address.

### Forces

- Auditors require proof—It is not enough for an organization to comply with a regulation—they need to be able to demonstrate that they are compliant.
- Events happen in many places—It is necessary to capture the event type, time, location, and context in which it occurred.
- Events happen in awkward places—The information process or individual who detects a significant event may not be the place where it can be processed.

### Solution Description

Record the event and send it to the parties who must react to the new situation.

The record of an event is called an information event. The type of information in an information event information element includes the following:

- The type of event
- The date/time it occurred
- Who or what detected it
- The information process that was executing, plus some of its context
- Links to other related information elements
- Other relevant information values The life cycle of an event is simple. The record of the event is created and stored. It may be retrieved, read, and copied to different locations. However, the content should never be changed from the time it is created to the time it is deleted. This means it is a true record of the event as it was detected at a particular moment in time. When the event is processed, it is linked to the information activity relevant to this processing.

### Solution Example

The customer service representative creates a customer address change event information element. This causes the new customer address information process to run, which looks up the customer in the Customer Hub to discover the list of accounts that the customer has. It then updates the address first in the Customer Hub, and then in any other system that holds the customer details.

### Benefits

- Understanding and managing the important events that occur in an organization helps it plan for how it should react when certain events happen.

### Liabilities

- Events are happening all of the time. It is important to focus on those that are significant to the organization.

### Usage

Information events are sometimes referred to as notifications. They are often saved to an audit log as a record of what is happening.

The Common Base Event standard provides a comprehensive view of the type of information that should be included in an information event: http://www.eclipse.org/tptp/platform/documents/resources/cbe101spec/CommonBaseEvent_ SituationData_V1.0.1.pdf

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Processing Variables

### Qualified Name

DesignPattern::Information Processing Variables

### Category

Information Element Patterns

### Description

The information process maintains this information in memory while it is running. This includes links to relevant entries in the information collections. It stores any new values into the appropriate information collections before it completes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

An information process operates in a context that defines why it was started and the existing information elements that it should be working with.

It needs easy access to the information for every step of its processing.

### Problem Example

What is the context of the New Order information process running in E-Shop?

### Forces

- Private information—The context is an integral part of the implementation of an information process.
- Limited lifetime—Some of the context may only be relevant to the information process and not needed once the information process has completed.

### Solution Description

Information values that describe the context are made available to the information process while it is running.

The information processing variables refer to the in-memory variables of an information process. It is created then the information process is initialized using values from the Information Event that triggered the information process.

The values in the information processing variables are displayed to Information Users through user interfaces. As the information process progresses, its knowledge of the context in which it is running grows as it is fed new information through these user interfaces. Additional values are acquired through the Information Services that access information stored in the Information Collections.

The information process persists relevant parts of its information processing variable to an Information Activity, or other relevant information elements such as information events and Information Assets.

### Solution Example

When the New Order information process is started, it has very little knowledge of its context beyond the implicit knowledge that a potential customer wants to order something from MCHS Trading's product catalog.

The customer may be logged in to E-Shop, in which case, New Order can retrieve the logon details and map them to an information entry in the customer details information collection. The Information Key of that entry is stored in New Order's information-processing variables.

Through its user interface, New Order guides the customer through the process of selecting the products he or she wants to order. These order items are stored in the information-processing variables.

Once the customer has selected the products he or she wants to order, New Order retrieves the address and payment details about the customer from the customer details information collection if he or she is a known customer, or invites the customer to enter the details directly. A new information entry in customer details is created if this is a new customer.

New Order creates a new information entry in the order details information collection and puts the information key of this new entry into its information-processing variables. This is the order number that will be displayed to the customer once the order is successfully completed.

This Order Details information entry is the information activity for the customer's order. The information key of the customer's details, the items ordered, and any payment details are added to this information element.

Once the order completes successfully, the New Order information process terminates and the information-processing variables are deleted.

### Benefits

- The information processing variables pattern clarifies the information that is being used by an information process. It provides a definition of the information dependencies that an information process has.

### Liabilities

- The information processing variables are lost when the information process ends— regardless of whether it succeeded or failed. Any of the information processing variables needed beyond the end of the life of the information process should be persisted into other information elements before this happens.

### Usage

In BPMN 2.0,1 the information-processing variables are specified using data objects.

The information-processing variables typically implemented as a set of local variables within an information-process implementation. They live mainly in memory, but may be stored in an information collection to enable the information process to be restarted or recovered partway through if the information node is capable to restarting processes partway through.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Summary

### Qualified Name

DesignPattern::Information Summary

### Category

Information Element Patterns

### Description

Combine the detailed operational data into summaries that retain enough detail for historical analysis, without recording the fine-grained detail of every activity.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

Detailed information that is collected and used in the short term has decreasing value as time passes.

An organization needs to retain historical information to enable it to compare current operations against those in the past. However, this takes up a lot of storage.

The information recorded in the operational systems is designed to enable the organization to know exactly where they are in an activity so they can manage both the expected and unexpected events that occur in any organization.

### Problem Example

In MCHS Trading when a package is shipped, details of the packaging style, truck, batch, drivers, route, intermediary depots, weather, and a full set of timings for each stage of the journey are recorded. This is to make it possible to locate a lost shipment or prove the goods were delivered, or similar types of incidents. MCHS Trading also uses this summary to monitor the effectiveness of the delivery companies it uses.

### Forces

- It is hard to know what information you might need in the future—The temptation is to keep it all just in case.
- The value of information can diminish over time—As such, it may not be cost effective to keep it forever.
- Information must be viewed in context for it to be understood correctly—Not everyone in an organization will use the same terminology, precision, validation rules, or have the same expectations for information quality and timeliness.
- Storing information that is never going to be used is wasteful—Storage costs money to buy and power to operate.

### Solution Description

Combine the detailed operational data into summaries that retain enough detail for historical analysis, without recording the fine-grained detail of every activity.

The design of these summaries, called Information Summary information elements, must reflect both the key pieces of information, plus the context in which the information was created.

### Solution Example

The detailed shipping information is summarized into two information elements as follows:

- A summary of the package shipment, including the following:
1. Order number
2. Package number
3. Shipment date/time
4. Delivery date/time
5. Shipping company
- A summary of each shipping incident, including the following:
1. Incident number
2. Order number
3. Package number
4. Incident raise date/time
5. Incident type
6. Incident description
7. Incident resolution type
8. Incident completion date/time These two types of summaries cover the minimal information about a shipment for most packages that are delivered without incident. When issues occur, additional information is kept about the shipping incident.

### Benefits

- Using summary information elements will reduce the storage necessary for keeping historical information. More important, designing summary information elements for this purpose means the information kept includes the context in which it was created.

### Liabilities

- It is possible that information needed in the future was not anticipated and is discarded in the summary process. Also, the summarizing logic requires an additional information process to be maintained and run.

### Usage

Rolling up information into summaries is common practice in data warehousing systems, less so in operational systems, which typically focus on creating the detailed information elements, such as information assets, information activities, and information events.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Payload

### Qualified Name

DesignPattern::Information Payload

### Category

Information Element Patterns

### Description

Package up the information into a well-defined schema that includes the context and action required in addition to the information values.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

An organization needs to verify that the information being passed between information nodes is being processed appropriately.

The information transmitted may be misleading or incomplete because it was created under different assumption to the information processes that will consume it at the destination. The information may be of a sensitive nature and need special protection. How does the organization ensure the appropriate information is sent between the information nodes?

### Problem Example

Orders are sent from MCHS Trading's order-taking systems—E-Shop, Mail-Shop, and Stores— for processing first by the Shipping application and then by the Invoicing application. How does MCHS Trading ensure the right information is flowing to make this processing successful?

### Forces

- Information must be processed in context—When information is received from a remote information node, it is necessary to understand the context under which it is sent in order to process it successfully.

### Solution Description

Package up the information into a well-defined schema that includes the context and action required in addition to the information values.

The software that manages the transfer of information between information nodes must be passed the information to send in a flattened structure called an information payload. The information payload is then inserted into a message structure for transmission.

The content of the information payload is of no interest to the networking software. However, it is of interest to the sending and receiving information nodes and its format should be explicitly defined to ensure there is clear understanding of what is being sent, and for what purpose; otherwise, it is very difficult to maintain governance over the Information Supply Chain.

There are three sections that are needed within the information payload:

- The information source—Such as where the payload is coming from, the activity that originated the information, and the information assets that are associated with this request.
- The action required—What should the destination information node do with this information?
- The information values that are being sent—These are the parameters to the action required.

### Solution Example

The information payload that represents an unfulfilled order includes the following:

- Order ID
- Order-taking system
- Order date/time
- Customer identifier
- Customer name
- Billing address
- Delivery address
- List of items ordered with price
- Total order cost
- Amount paid

### Benefits

- The information payload defines exactly what type of information is being exchanged between information nodes.

### Liabilities

- Many information payloads are defined based on the needs of the consuming information processes. These requirements may change as the operations of the organization evolve.
- The format of the information payload may need to change as it flows between the source and the destination information nodes. There are different approaches for which part of the processing is responsible for the transformation. Three suggestions are shown in Table 4.4. Icon Pattern Name Problem Solution SOURCEAn information process that The source information process sends Specific needs to send information into the data payload in its local format. Payload an information supply chain is The downstream information processes TARGETAn information process that The source information process, or an Specific needs to receive information intermediate information process, needs Payload from the information supply to transform the data payload into the CANONICALAn information supply chain Use a canonical data format for as many Based has many information prodata payloads as possible. The informaPAYLOAD cesses that each understands its tion processes then only need to be able

### Usage

Information payload definitions are referred to as message structures or message schemas by message-oriented middleware and request/response operation signatures, or schemas that define the parameter list by service-oriented middleware.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Canonical-Based Payload

### Qualified Name

DesignPattern::Canonical-Based Payload

### Category

Information Element Patterns

### Description

Use a canonical data format for as many data payloads as possible. The information processes then only need to be able to transform data between their local format and the canonical format.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An information supply chain has many information processes that each understands its own data format. How can the process of transforming data be simplified?

### Solution Description

Use a canonical data format for as many data payloads as possible. The information processes then only need to be able to transform data between their local format and the canonical format.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Source-Specific Payload

### Qualified Name

DesignPattern::Source-Specific Payload

### Category

Information Element Patterns

### Description

The source information process sends the data payload in its local format. The downstream information processes transform the data as required.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An information process that needs to send information into an information supply chain is not able to transform data.

### Solution Description

The source information process sends the data payload in its local format. The downstream information processes transform the data as required.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Target-Specific Payload

### Qualified Name

DesignPattern::Target-Specific Payload

### Category

Information Element Patterns

### Description

The source information process, or an intermediate information process, needs to transform the data payload into the required format before it reaches the destination information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

An information process that needs to receive information from the information supply chain is not able to transform incoming data.

### Solution Description

The source information process, or an intermediate information process, needs to transform the data payload into the required format before it reaches the destination information node.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Link

### Qualified Name

DesignPattern::Information Link

### Category

Information Element Patterns

### Description

Store information values that identify the information node, information collection, and information entry within the collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

An organization needs to be able to link together information entries from different information collections.

The information collections may be together hosted on the same information node, or distributed across different information nodes.

### Problem Example

MCHS Trading has an Order-Tracking information node that stores an information collection of in-flight orders. Each information entry in this information collection represents details of an order. The information entry needs to link to details of the customer (stored in the Customer Hub) and the products ordered (stored in the Product Hub).

### Forces

- Independent life cycles—The maintenance of information entries in different information collections is independent of one another.
- Broken links—If an information entry is deleted, all of the other information entries that have links to it now point to missing information.
- Link-based queries—An information service is required to retrieve the information values from the information entry that is referred to in the information link.

### Solution Description

Create a reference for the information entry and an information service that is able to return the values from the information entry on request.

An information link is an attribute in an information entry. It contains enough information about the linked to information entry to enable an information process to retrieve the information from a well-known service. Either the original information process that requested information from the information collection, or a new information process triggered by access to the information collection is responsible for retrieving the information values from the information entry.

### Solution Example

The information keys for the appropriate customer and the product details are used to implement the information links.

### Benefits

- Information links enable the latest information to be linked together and hence reduce the need to copy information into multiple information collections.

### Liabilities

- Information links can be broken when information entries are moved or deleted.
- An information link implies there is an information service that can retrieve the information values for an information entry based on the values stored in the information link. The values are only available if the information node hosting the information service is running.

### Usage

Information links are typically implemented using information keys. An information link typically contains the information key of the information entry being linked to and the code of the information processes that use the information link know which information service to call in order to get further details.

There is a semantic web standard called Open Services for Lifecycle and Collaboration (OSLC) that provides explicit mechanisms for supporting distributed information links. Each information entry is represented as a uniform resource locator (URL) that points to a service provider that can serve up the information values for that entry. The information link simply calls the URL to get the information. This has the advantage that the information service logic is not hardcoded into each information process that uses the link. However, it does require stable URLs and so server names and IP addresses should not be used in the URLs. The URLs should have logical names that are resolved by a directory service.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Metric

### Qualified Name

DesignPattern::Information Metric

### Category

Information Element Patterns

### Description

Maintain the results of calculations that indicate how well the organization is performing.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

An organization needs information to understand how well it is performing.

Many organizations are judged on the profit they make and the confidence that they will continue to make that profit going forward. The way this confidence is measured is not an exact science, but investors and managers look for indicators that suggest whether the organization is growing or shrinking; has unmanaged risks; is operating legally and ethically; is in a stable, growing, or diminishing market; and more intangible aspects such a public perception.

The information systems need to produce the right information to enable people to assess these indicators.

### Problem Example

MCHS Trading is unsure how well it is performing in terms of customer growth and existing customer satisfaction.

### Forces

- Some information is mandatory—Many regulations stipulate what type of information must be produced to demonstrate compliance.
- Information may be combined from multiple sources—Some metrics require calculations based on information gathered from multiple sources.

### Solution Description

Maintain the results of calculations that indicate how well the organization is performing.

These results are recorded in information indicators. These information elements record the time the calculation was made, the parameters used, the calculation used (such as the model or formula), and the results. Sometimes the parameters are complex and include a large volume of information, in which case the indicator may just contain a reference to the parameter information.

### Solution Example

MCHS Trading has decided to maintain the following information indicators to understand how well it is serving its customers:

- A count of the number of new customers who have registered with either their loyalty card or their Internet shop, E-Shop
- The average number of orders each customer is making
- A segmentation of how many customers have not made an order in the last month, in the last 6 months, in the last year
- The percentage of packages delivered without incident
- The level of satisfaction recorded by customers on receipt of their orders
- The ratio of ordered goods to returned goods These indicators, and how they trend over time, will help MCHS Trading to access how well its business is performing.

### Benefits

- Defining indicators and then recording and tracking these values creates a focus on the performance of the organization.

### Liabilities

- When people realize they are being measured on particular criteria, they change their behavior—which can have both positive and negative consequences.

### Usage

Information metrics provide key information for business intelligence applications such as management reporting. They are also known as Key Performance Indicators or Key Predictive Indicators—both shortened to KPI.

Analytical processes often generate information metrics called scores.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Code

### Qualified Name

DesignPattern::Information Code

### Category

Information Element Patterns

### Description

Use a code value for each of the valid values. The code value is stored and translated into a string format when it is displayed to a person.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

The way an information element is managed depends on what it represents and how it is used.

### Problem Statement

An information attribute has a fixed set of valid values that need to be efficiently stored and verified.

### Problem Example

A customer's name includes a courtesy title, such as Mr, Mrs, Miss, or Dr. How is the value for courtesy title stored in Mail-Shop's order details information collection?

### Forces

- The set of valid values changes over time.
- The valid values need to be displayed in drop-down menus for information users to select.
- The valid values may need to be displayed in different languages for different audiences.
- Each information node may implement a different set of valid values for an attribute in its information collections.

### Solution Description

Use a code value for each of the valid values. The code value is stored and translated into a string format when it is displayed to a person.

An information code is defined as a small number of attributes. The first attribute is the code value and the other values are various string representations of that code value. The information code definitions are stored in their own information collection with the code value as the primary key.

The code value is stored in information collections that are using the information code for one of its attributes.

The information processes that consume an attribute containing the code value are written in a generic fashion to access the information code definition and use the values it contains. This avoids hard-coding the values in the information process logic.

### Solution Example

Mail-Shop uses information codes to represent the list of valid values for the courtesy title. This is illustrated in Figure 4.3.

### Benefits

- Using an information code definition simplifies the maintenance of the valid values because they can be maintained by updating the information collection rather than having to change the display and validation code.

### Liabilities

- When information flows between information collections that are using information codes, the code values need to be translated from the set used in the source to the set used in the destination. This process is called transcoding.

### Usage

Information codes are used in applications to define the valid values for an attribute. They appear in UML models as enumerations.

An information code is defined in a database as a row in a table where the information code value is the primary key and the other columns are the different string values.

Information codes are sometimes called reference data and the centralized management of code values and the mappings between code values in different information nodes is called Reference Data Management (RDM). Note there is a confusion of terminology here between the term reference data and the Reference Usage of an information collection. Reference usage is for information collections that have read-only usage by its information processes, so it has applicability beyond information codes.

### Search Keywords

- Patterns of Information Management
- Information Element
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Identification

### Qualified Name

DesignPattern::Information Identification

### Category

Information Identification Patterns

### Description

Investigate and document the information requirements and existing support available to the organization.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is documenting its information architecture as part of a program to improve its information management.

### Problem Statement

An organization does not know what types of information it has, where it is located, how it is managed, and who is responsible for it.

This affects the organization's ability to manage its information because it has no basis against which to assess success, detect issues, or drive improvement.

### Problem Example

MCHS Trading is committed to high customer service. To achieve this, MCHS Trading knows it needs to keep information about its customers and the activities that concern them. There have been some recent incidents where a customer has not received good service and this has been attributed to incorrect information about the customer or a product he or she has ordered.

To fix this, MCHS Trading must first understand the types of information it needs to keep, where it is located, and its level of quality. Then it can put measures in place to resolve any issues.

### Forces

- Different definitions—The terminology and conventions around information may vary between different parts of the organization and IT systems.
- People move on—Changes in personnel over time reduce the available knowledge about an information collection.
- Unknown content—The contents of some information collections are not understood or clearly documented. The organization does not know whether it needs the information collection or, if it does—what levels of information management are appropriate.
- Technical limitations—Most IT systems are not able to supply semantic definitions of their information.

### Solution Description

Investigate and document the information requirements and existing support available to the organization.

Information identification is an iterative process that is integrated into the organization's operational and project practices. It creates a set of information identification resources, where each resource defines an aspect of the organization's information requirements or provision. These resources are linked together and stored in a common repository so other teams can use them in future work.

There are a number of parts to information identification that are described in the following sections:

- Defining Which Information to Manage and How—First, it is necessary to establish the scope of the information to manage. This is in terms of its meaning, the values that are valid for this information, and the way it should be managed. This is part of establishing requirements for the project or standing team.
- Defining How Information Is Structured—Next, it is necessary to define how information is to be structured so it can be efficiently stored and accessed by the information processes. This is part of the design work for a project or standing team.
- Locating the Right Information to Use—To make use of existing information, it is necessary to know where it is so there are information identification resources that define where the different types of information are located. A team creates these resources when it creates a new information collection or investigates an existing information collection that has not been documented yet.
- Different Reports About Information—Finally, a project or standing team often needs to understand the characteristics of the information values that the organization has. This section defines reports on the information values for a particular type of information. Each project or standing team is responsible for reviewing, developing, and using the information identification resources that are relevant to its work. Over time, as more teams perform information identification, these information resources expand to cover all the key information used by the organization.

### Solution Example

MCHS Trading begins to build up a picture of the information it needs to support its customercentric activities by creating the following information identification resources:

- A Subject Area Definition documents the semantics of customer information, including name, address, and tax ID.
- Information Location resources are used to document the location of customer information in the information collections.
- Definition of the content, structure, and quality of the customer information is achieved through the Information Model and Information Values Profile pattern.
- The Semantic Tagging pattern is used to ensure that the sources and content of the customer information are appropriately connected to the Subject Area Definition.
- During design and development of a new Information Supply Chain, the Information Flows that send customer information are appropriately validated through the Semantic Mapping pattern. As new information solutions are implemented, they use the previously established Information Identification resources and continue to extend it to cover more of the organization's information.

### Benefits

- Information identification creates a comprehensive and consistent definition of the information requirements and provision within an organization. This enables the organization to assess the state of its information management and drive improvements. The sharing of information identification resources reduces duplicated effort and increases the consistency of information management across the organization.

### Liabilities

- Information identification is only documentation. It must be maintained and used effectively to deliver value to the organization. Identifying, establishing, and maintaining the information identification resources takes time and requires commitment from both the business and IT parts of the organization to ensure this information is accurate and used where appropriate.

### Usage

Information identification is used in the requirements gathering phases of many IT projects. It is sometimes referred to as metadata management. An example of an implementation of metadata management is described in:

- Metadata Management Using IBM Information Server, IBM Redbook, http://www.redbooks.ibm.com/abstracts/sg247939.html?Open

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Subject Area Definition

### Qualified Name

DesignPattern::Subject Area Definition

### Category

Information Identification Patterns

### Description

Describe the types of information values associated with the topic, and link them to definitions of how they are structured and where they are used.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is documenting its information architecture as part of a program to improve its information management.

### Problem Statement

An organization wants to document details of the information it keeps about a particular topic.

This definition is focused on the semantics (meaning) of this information, rather than the implementation. The aim is to create something that the information users will understand and can agree that this is the type of information they need.

### Problem Example

MCHS Trading is focusing on the management of its customer information. The first question it asks is: What type of customer information does it need?

### Forces

- Information requirements are unclear—The organization does not have a clear definition of the information needs of each group within the organization.
- Inconsistent definitions—Typically, each group has a slightly different set of requirements and/or terminology to describe its information needs and usage.
- Local coverage of information—Applications typically only store the subset of attributes that they need to perform their specific processing.
- Semantic drift and quality erosion—The meaning of terms, attributes, and information values gradually change over time. This change can occur at different rates in different parts of the organization.

### Solution Description

Describe the types of information values associated with the topic, and link them to definitions of how they are structured and where they are used.

This description of a topic area is called a subject area definition. It consists of terms with a textual definition describing what it means and where is it used. The terms may be classified into related groups and linked together to show related concepts, synonyms, and antonyms.

This subject area definition becomes the authoritative source of documentation for the terminology in use in the organization and a nontechnical view of the information needs of the organization.

### Solution Example

MCHS Trading creates subject area definitions for Customer Details, Product Details, and Order Details.

### Benefits

- The subject area definition clarifies the meaning of information required by the organization.

### Liabilities

- Establishing and maintaining a subject area definition can be time consuming and requires commitment by the organization across and including business and technical teams.
- For a large organization, it may not be practical to create subject area definitions to cover all aspects of the organization's information needs. In this case, they can be created gradually, focusing on the high-value information first and then adding to it as projects and the organization's focus requires.

### Usage

There are a number of approaches to implementing a subject area definition in use today. The approach used by an organization depends on how formal a definition they need.

- Glossaries—A glossary is an alphabetically organized set of terms and their definitions. It can be used to create standard semantic definitions of the different types of attributes used by the organization. The attribute names used are based on the vocabulary used by people in the organization.
- Taxonomies—A taxonomy extends a glossary in that it provides a classification scheme around the terms and their definitions. With a taxonomy, it is possible to see how the attributes are related to the subject areas. It is consumable by both business and IT professionals.
- Data dictionaries—A data dictionary defines the meaning of the data fields implemented in databases, files, and messages. IT professionals use it to understand what values are stored in a particular repository.
- Ontologies—An ontology is a formal definition of the concepts and attributes in a subject area showing how they relate together. The ontology provides the most comprehensive view of the types of information that an organization wants to store. It must be created by ontology modeling experts and can become quite complex if its scope is large. The most useful ontologies typically only cover a small number of subject areas because this is about as much complexity that a person can comprehend.

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Valid Values Definition

### Qualified Name

DesignPattern::Valid Values Definition

### Category

Information Identification Patterns

### Description

Define a rule or set to characterize the valid values allowed for the attribute in an implementation independent format. Use this definition as a requirement for all projects that implement an information collection that includes this attribute.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is documenting its information architecture as part of a program to improve its information management.

### Problem Statement

An organization wants to maintain consistency in the values that are allowed in a particular attribute across multiple information collections.

This will broaden the number of people and information processes that will be able to interpret the information correctly.

### Problem Example

MCHS Trading wants to establish a set of valid values to support marketing by understanding how a customer learned about the products.

### Forces

- Information processes are implemented independently—Each information process may hard-code different information validation rules and standards. When a change is required, it can take a lot of recoding.
- Inconsistent definitions—Typically, each unit has a slightly different set of requirements and/or terminology to describe its information needs and usage, which means different sets of valid values may exist for the same type of information.
- Active information maintenance—For the valid value definitions to remain an authoritative source of information needs, they must be regularly maintained and reviewed.
- Semantic drift and quality erosion—Over time, employees may come to assign certain existing valid values to new conditions, even if not truly accurate. Also, there may be default values that are used to represent unknown states or values that are used to quickly process information and avoid specific conditions. All of these can change the quality of the information.

### Solution Description

Define a rule or set to characterize the valid values allowed for the attribute in an implementation-independent format. Use this definition as a requirement for all projects that implement an information collection that includes this attribute.

The rules or sets of valid values are called valid values definitions. They define whether the value assigned to one or more attributes is an allowable value—although not that it is necessarily the correct value.

There are a number of approaches to specifying a valid values definition. For example,

- Defining a list of valid values.
- Defining a range of values.
- Ensuring a selection of related attributes are consistent.
- Defining an authoritative source that lists the valid values. This may, for example, be a set of Information Codes, or a collection or Information Assets, that are known to be the complete set of valid values.

### Solution Example

MCHS Trading creates a set of valid values for Marketing Channel:

- "C" = other customer
- "E" = email
- "M" = mail (e.g., flyers)
- "S" = social media
- "W" = website

### Benefits

- Creating and maintaining a set of valid values provides the definition of key information requirements for an organization. This can be used to facilitate an information governance program. It may also drive initiatives to optimize and simplify the IT system provision for the organization by identifying what information is considered valid by the organization.

### Liabilities

- In an ideal world, there is a consistent definition of the valid values for a particular piece of information that is checked when information is received/created and honored in each system. In reality, there will be many approaches to implementing the piece of information requiring different mechanisms to validate it. In addition, not all information processes will enforce the valid values either through age, bugs, or priority.

### Usage

Valid values definitions are typically documented either in text, pseudocode, or using a rules package. A rules package allows rules to be defined in a human-consumable format, but with enough rigor that the rules can be executed in the IT systems.

There are many commercial rules packages available. The Object Management Group (OMG) has a rules standard called Semantics of Business Vocabulary and Business Rules (SBVR).2

2. http://www.omg.org/cgi-bin/doc?formal/08-01-02.pdf

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Configuration

### Qualified Name

DesignPattern::Information Configuration

### Category

Information Identification Patterns

### Description

Deploy configuration at each of the key points of variability in the information processes that control how the information is managed. Provide the ability for appropriate information users to change and redeploy this configuration to modify how the information is managed.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is documenting its information architecture as part of a program to improve its information management.

### Problem Statement

An organization wants to be able to modify the way that information is managed on an ongoing basis.

The organization needs to set, control, and adjust processing thresholds, timing intervals, and similar parameter values.

### Problem Example

MCHS Trading wants to periodically tune the parameters of its automated matching of customer information from different information nodes to control the number of Clerical Review Processes generated for its Information Stewards by the Information Matching Process.

### Forces

- Hard-coded behavior—Many information processes have hard-coded implementations that require a code change to alter their behavior.
- Validation of behavior—No matter how it is specified, the behavior of an information process needs to be verified to ensure it is meeting the needs of an organization.

### Solution Description

Deploy configuration at each of the key points of variability in the information processes that control how the information is managed. Provide the ability for appropriate information users to change and redeploy this configuration to modify how the information is managed.

A place in an information process where externally defined values are used to control its behavior is called a point of variability. The externally defined values are called the information configuration.

The information configuration values are set through the configuration user interfaces of an information node or information process, or through external rules packages that are called during the execution of the information processes.

When the information process reaches a point of variability, it retrieves and interprets the information configuration to determine the next step to take.

### Solution Example

MCHS Trading utilizes an Information Matching Process within its Customer Hub to match customer records from different information nodes together. This matching process has an information configuration that controls the matching process—including determining the thresholds where an information steward is required to verify the match. As its confidence with the effectiveness of matching configuration grows, MCHS Trading tunes the matching thresholds to specific levels to maximize high-quality matches and minimize manual review of common exceptions.

### Benefits

- Using information configurations rather than hard-coded logic in its information processes provides an organization with more control over the behavior of its information processes on an ongoing basis.

### Liabilities

- Retrieving and interpreting information configuration can slow down the execution of an information process. If the information configuration values are changing slowly, they could be cached in memory and only refreshed when either the information process starts or the information node hosting the information process is restarted.

### Usage

Information configuration is often used to allocate processing resources to an information process—such as a pointer to a persistence store, or memory or storage space. It is also used to set thresholds for when something happens—such as how long since it was last accessed should an information entry in an information collection be archived.

This configuration can also determine the way information is classified, which in turn determines which logic path it is processed on by the information process. For example, the configuration may determine the characteristics of a high-value customer, which may affect the way one of the orders is processed.

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Model

### Qualified Name

DesignPattern::Information Model

### Category

Information Identification Patterns

### Description

Use a modeling language to create a welldefined logical model of the information elements, the attributes they contain, and the relationships between these elements.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is documenting its information architecture as part of a program to improve its information management.

### Problem Statement

Individuals in an organization need to discuss and document how information for a particular purpose is or will be structured.

This helps identify that attributes are stored, the kinds of information elements involved, and the way pieces of information are related to one another.

### Problem Example

MCHS Trading wants to create a Reporting Hub that supports a range of management decisions based on orders, sales, and stock inventory.

### Forces

- Inconsistent definitions—Typically, each unit has a slightly different set of requirements and/or terminology to describe its information needs and usage, which means different sets of information elements must be reconciled for an effective information model.
- Active information maintenance—For the information model to remain an authoritative foundation of information needs, it must be regularly reviewed, maintained, and utilized. The most effective way to achieve this is to make the use and maintenance of the information model a part of selected employees everyday jobs.
- Semantic drift and quality erosion—Over time, employees may come to utilize certain information elements for purposes other than what was intended in the information model. Such use changes the context and quality of these elements in processing across the information supply chain and creates risk in effective use of the information model for subsequent applications.
- Information volume—The number of information elements to model, or the number of information models to maintain, may overwhelm the people performing the tasks.

### Solution Description

Use a modeling language to create a well-defined logical model of the information elements, the attributes they contain, and the relationships between these elements.

### Solution Example

MCHS Trading reviews the information elements from the information collections in the Customer Hub, Shipping, Invoicing, Purchasing, and Accounts Payable applications. It uses a modeling tool to establish an initial information model focused on sales of products to customers that includes sales details (as well as summaries by week, month, quarter, and year) and product cost per unit.

This information model is connected to the Subject Area Definition to ensure that the information elements used in the model are clearly understood and is used to generate the Information Schema for the Reporting Hub used by the report developers.

### Benefits

- The modeling process helps the team to think through the type of information it needs to capture.

### Liabilities

- The model needs to be kept up to date with the changes to the systems or it becomes useless. This takes governance in the software development life cycle.
- An information model only covers the static structure of information. It does not cover the dynamic aspects, such as when the information is available, or the level of quality and precision that is needed. This must be specified elsewhere in Valid Values Definitions and state machine models.

### Usage

Information modeling is a well-established practice for relational database construction, and is a primary activity in designing and developing information processing to store information collections. Usage includes the following:

- Integrating multiple applications that contain pieces of information collections
- Acquiring and merging (or consolidating) new data sources into existing information models
- Designing, developing, and integrating into a data warehouse, data mart, or Master Data Management system There are many types of information models, such as the following:
- Entity-relationship data models are used to describe how information is persisted in a database or file.
- UML class diagrams are used to describe how information is structured in applications, information processes, and information services.
- An ontology model is used to describe the concepts and the relationships between them in a subject area.

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Schema

### Qualified Name

DesignPattern::Information Schema

### Category

Information Identification Patterns

### Description

Define a description of the structure of the information element that is both machine readable and human readable.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is documenting its information architecture as part of a program to improve its information management.

### Problem Statement

An information process needs to understand how the attributes within an information element are structured in order to process it correctly.

### Problem Example

MCHS Trading wants to create a Reporting Hub that supports a range of management decisions based on orders, sales, and stock inventory.

Once the Information Model for the Reporting Hub is defined, it needs to be translated into a technical form usable by the information processes that will store information in the Reporting Hub and those that will report on the contents.

### Forces

- Information requirements are unclear—The organization does not have a clear definition of the information needs of each unit within the organization.
- Inconsistent definitions—Typically, each unit has a slightly different set of requirements and/or terminology to describe its information needs and usage, which means different sets of information elements must be reconciled for an effective information model and its associated information schema.
- Active information maintenance—For the information schema to remain usable by the information processes, it must be regularly reviewed, maintained, and utilized. The most effective way to achieve this is to make the use and maintenance of the information schema a part of selected employees everyday jobs.
- Ad hoc change—For information schemas to remain effective, they need to remain aligned with their associated information models. Ad hoc changes to the information schemas to quickly address problems result in schemas that are no longer aligned to their information models.
- Semantic drift and quality erosion—Over time, employees may come to utilize certain information elements for purposes other than what was intended in the information model and its associated information schemas. Such use changes the context and quality of these elements in processing across the information supply chain and creates risk in effective use of the information schema for information processing.
- Information volume—The number of information models to maintain and translate into schemas, or the number of ad hoc changes needed to schemas, may overwhelm the employees performing the tasks.

### Solution Description

Define a description of the structure of the information element that is both machine readable and human readable.

### Solution Example

MCHS Trading uses a standard database management software (DBMS) product for its Reporting Hub. Its information modeling tool can automatically generate the scripts in the form needed by the DBMS to create an information schema.

This information schema is connected to the Subject Area Definition based on the information model to ensure that the information elements incorporated are clearly understood by application and report developers.

### Benefits

- The structure of the information is in a form that is both machine and human readable.

### Liabilities

- The schema must be updated when the information needs changes. Some teams are tempted to store information in available attributes that were designed for different values rather than update the schema.

### Usage

Information schema generation is a well-established practice for relational database construction, and is a primary activity in designing and developing information processing to store information collections. Usage includes the following:

- Integrating multiple applications that contain pieces of information collections
- Acquiring and merging (or consolidating) new data sources into common information schemas
- Designing, developing, and integrating into a data warehouse, data mart, or Master Data Management system

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Location

### Qualified Name

DesignPattern::Information Location

### Category

Information Identification Patterns

### Description

Create a description of the information collections hosted by the organization's information nodes and who is responsible for them. Link this definition to the appropriate subject area definitions.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information must flow along an information supply chain.

### Problem Statement

An organization does not know where its information is located, how well it is managed, and who owns it.

### Problem Example

Certain customer demographic information falls under specific data privacy and reporting policies, such as date of birth, gender, and credit rating. Where is this information located?

### Forces

- Unknown data contents—The location, content, format, ownership, and quality of the data in each system are not well understood.
- Information governance—Information governance is a priority for the organization.
- Rapid organizational change—New business and information initiatives need to rapidly identify how to obtain the required information.

### Solution Description

Create a description of the information collections hosted by the organization's information nodes and who is responsible for them. Link this definition to the appropriate subject area definitions.

This definition should detail the name of the information node, who owns it, and the information collections it hosts. It should also detail the types of usage patterns that the information processes use and an estimate of the number of Information Entries each information collection contains.

### Solution Example

Review the information collection in each information node and in the case of MCHS Trading's Stores Account customer demographic information, the contents of the information collection must be identified, appropriately tagged, and then designated for use in a provisioning inventory:

- Create the inventory of the Stores application, including the Account and Account Reference tables.
- Create an Information Values Profile to discover and analyze the data fields in the Stores application that are not clearly understood or documented.
- Establish business terms for Date of Birth, Gender, and Credit Rating through the Subject Area Definition.
- Connect the Information Location entry for fields Acbdt, Acgcd, and Arcrt to the core business concepts through Semantic Tagging to ensure that the sources and content of the customer information are appropriately connected to the Subject Area Definition.
- Identify the same or associated data for Information Provisioning through Information Lineage.

### Benefits

- Once the provisioning inventory is complete, it needs to be maintained as systems are updated over time.
- This provisioning inventory may be used as a resource to understand where data is located during the development of an information supply chain.

### Liabilities

- Establishing and maintaining an inventory for information provisioning can be time consuming and requires commitment by the organization across and including business and technical units.

### Usage

Information identification is a primary activity in managing information collections and moving data from one information collection to another. Usage includes the following:

- Integrating multiple applications, which contain pieces of information collections
- Acquiring and merging (or consolidating) new data sources
- Populating and maintaining information collections stored in a data warehouse, data mart, or Master Data Management hub
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Semantic Tagging

### Qualified Name

DesignPattern::Semantic Tagging

### Category

Information Identification Patterns

### Description

Use a subject matter expert to analyze and identify the meanings of the attributes. Document the meanings with their associated subject area. Link the meanings to the attribute definitions.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information must flow along an information supply chain.

### Problem Statement

An organization does not understand the meaning of the attributes within a data payload.

The business or semantic context of the data elements is not well understood or does not align with expected content.

### Problem Example

MCHS Trading maintains an information collection for Account data as part of the Stores system with associated customer information where there may be multiple accounts based on unique store location for any given customer. The system is an older application and while different individuals have understood the use of certain fields over time, the field names are quite cryptic and many individuals familiar with the system have left the organization. Aside from sporadic emails, there is nothing to connect the fields with their actual purpose. Even information found through data profiling may quickly be lost, such as the following:

- The Acxdt field in the Account table does contain dates, but only contains dates when the associated Account status field equals ‘Canceled' indicating this is the Account Cancellation date.
- The Acmnm field in the Account table contains a mixture of names, cryptic 8-character alphanumeric values, and questions. This information not only needs to be segregated, but likely falls under new governance and data privacy requirements.
- The Actid field in the Account table does contain tax identifiers though in a mixture of formats as well as many default values and other duplicated values, which must be accounted for in subsequent usage.

### Forces

- Information governance—Information governance is a priority for the organization.
- High cost/risk—Incorrectly applied data in an information supply chain has a cost or risk to the business in the design, development, delivery, or management of that supply chain.
- Unknown data contents—The content, validity, and reasonableness of the data in each system is not well understood in its business context.

### Solution Description

Use a subject matter expert to analyze and identify the meanings of the attributes. Document the meanings with their associated subject area. Link the meanings to the attribute definitions.

Apply automated data classification to identify potential semantics of each data element. Discover underlying sensitive and critical data elements. Assess data content, metadata definitions, and data lineage to link (or tag) data elements with their associated business terms to assign business context. Add additional links or tags as new systems are inventoried and additional data is profiled.

### Solution Example

In the case of MCHS Trading's account information, data stewards take advantage of a business glossary storing Subject Area Definitions where they can assign relationships and semantically tag the assets stored in a metadata collection:

- Information Values Profile software that includes automated data classification tags the fields in the metadata collection with rough detail: The Acxdt field in the Account table is a Date; the Acmnm field in the Account table contains mixed Text; the Actid field in the Account table contains a high percentage of tax identifiers, specifically Social Security numbers.
- Data analysts use the metadata collection, including the detailed analysis from an information values profile, to conduct a data-driven tagging and annotation to ensure greater accuracy in semantic tagging.
- Data stewards add labels to both the business glossary and known assets to facilitate further semantic tagging, and assign assets to glossary terms: The Acxdt field is assigned to the Account Cancellation Date term; the Acmnm is assigned to the Account Maiden Name term as well as the Account Password Reset term given the additional data present; and the Actid field is assigned to the Account Tax Identification term.

### Benefits

- Once the semantic tags are created, they should be regularly reviewed for updates as systems, data, and semantics change over time.
- The semantic tags may be used as a resource to understand data structure, content, and quality during the development of an information supply chain.

### Liabilities

- If there are many different terms and information nodes within the information supply chain, the burden of creating and managing semantic tagging can be high.
- Establishing and maintaining a metadata collection of information terms for use in semantic tagging can be time consuming and requires commitment by the organization across and including business and technical units.

### Usage

Information identification is a primary activity in managing information collections and moving data from one information collection to another. Usage includes the following:

- Integrating multiple applications that contain pieces of information collections
- Acquiring and merging (or consolidating) new data sources
- Populating and maintaining information collections stored in a data warehouse, data mart, or Master Data Management system
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Semantic Mapping

### Qualified Name

DesignPattern::Semantic Mapping

### Category

Information Identification Patterns

### Description

Use semantic tagging to guide the mapping process.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information must flow along an information supply chain.

### Problem Statement

An organization does not understand the relationship between attributes in two different data payloads.

The relationship of business or semantic terms to data elements is not well understood or does not provide sufficient insight in identifying and mapping information along the information supply chain.

### Problem Example

MCHS Trading is integrating account, demographic, and customer information from the Stores systems into its Customer Hub for downstream reporting. There are inconsistencies in data content and format across the systems and the developers of the Customer Hub do not understand which fields relate to which other fields. Without clear semantic relationships across data, prior projects have seen the following:

- The Acmnm field in the Account table was interpreted as a middle name field when it actually contains maiden name, resulting in incorrect customer names and failed attempts to correctly match customer data.
- The Acxdt field in the Account table was interpreted and used as the account creation date when it is actually the account cancellation date.
- The Actid field in the Account table was interpreted as a customer ID when it is actually the tax identifier and incorrectly mapped to the customer ID in downstream systems.

### Forces

- Information governance—Information governance is a priority for the organization.
- High cost/risk—Incorrectly mapped data because of semantic mismatches in an information supply chain has a cost or risk to the business in the design, development, delivery, or management of that supply chain.
- Information requirements are unclear—The relationship or mapping of the business semantics is not well understood in its relationship to the information supply chain.

### Solution Description

Use semantic tagging to guide the mapping process.

Discover semantic mappings based on similarity of related terms, lexically similar metadata, data element relationships, and data lineage relationships. Apply additional semantic mappings across the discovered relationships.

### Solution Example

In the case of MCHS Trading's integration of account, demographic, and customer information from the Stores systems into its Customer Hub for downstream reporting, MCHS data analysts have utilized the Subject Area Definitions and associated assets tagged with the terms in a metadata collection to enhance their mapping process:

- Data analysts and data stewards have tagged the Acmnm field in the Account table as maiden name in their metadata collection.
- The Acxdt field in the Account table is tagged as the account cancellation date.
- The Actid field in the Account table is linked to the tax identifier with annotations to indicate it is not for use as a customer identifier.
- Data analysts use Semantic Mapping as part of their mapping specification process to discover similar fields with the same semantic tag in the new Customer Hub and the Reporting Hub.
- Where fields are not yet semantically tagged, the data analysts use the results from an Information Values Profile to review data contents and formats, explore overlaps across data sources, and suggest or recommend additional semantics in the Subject Area Definitions of the metadata collection.
- Where fields are linked in the mapping specification but only one of the fields contains the Semantic Tagging, the data analysts push the linkage into the metadata collection as new Semantic Mapping.
- The mappings created and captured in the metadata collection establish Information Lineage patterns, which enable more semantic mapping in the future.

### Benefits

- The semantic mappings may be used as a resource in establishing the connections between information and data elements in the design and development of the information supply chain.
- Once the semantic mappings are created, they should be regularly reviewed for updates as systems, data, and semantics change over time.

### Liabilities

- If there are many different terms and information nodes within the information supply chain, the burden of creating and managing semantic tagging necessary for semantic mapping can be high.
- Establishing and maintaining a metadata collection of information terms for use in semantic mapping can be time consuming and requires commitment by the organization across and including business and technical units.

### Usage

Information identification is a primary activity in managing information collections and moving data from one information collection to another. Usage includes the following:

- Integrating multiple applications that contain pieces of information collections
- Acquiring and merging (or consolidating) new data sources
- Populating and maintaining information collections stored in a data warehouse, data mart, or Master Data Management system
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Values Report

### Qualified Name

DesignPattern::Information Values Report

### Category

Information Identification Patterns

### Description

Create a report that shows the information values of interest, typically with related summaries and metrics.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is using the information it is managing and wants to assess its content.

### Problem Statement

An organization wants to review the values of some of its information.

The organization needs this information collated and summarized to help it understand the relevance and significance of the values it is reviewing in order to understand a particular situation.

### Problem Example

As part of its annual sales review, MCHS Trading needs reports by product type and brand that indicate how well such items have sold over the past year.

### Forces

- Relevant information is dispersed—Often the information that an information user needs to make a decision is dispersed among different information collections.
- Processing overhead—Collating and summarizing information from multiple sources can require a fair amount of processing power. If a report is required frequently, it requires special provision to reduce the overhead.
- What does it mean?—Information from different parts of the organization may be collected with different assumptions that may create misleading results when they are consolidated together.
- The effect of failures—A failure in the information supply chain that provisions an information values report can cause misleading values in the report.

### Solution Description

Create a report that shows the information values of interest, typically with related summaries and metrics.

An information values report provides summaries of some related information values. Information users use them to assess the state of the organization, the behavior of the teams and IT systems, along with the health of the business.

Information values reports are created by Information Reporting Processes. These processes pull information together from multiple information collections to assemble the report contents.

Reports that are produced frequently typically have their own information collections that have been provisioned solely to support the needs of the report.

### Solution Example

For MCHS Trading's sales review, several ad hoc information values reports are created against the new Reporting Hub. One report shows the values for product type; one report shows the values for brand. In each case, the reports summarize total number of items sold, total gross sales, and total net sales by month, quarter, and year for the respective values.

The MCHS Trading buyers will note product types and brands with no sales or declining sales for discontinuation.

### Benefits

- Consistent representation of information collections ensures that the information values reports have consistent meaning and can be effectively utilized to drive key business decisions and performance indicators.

### Liabilities

- In identifying information and information values, there is the possibility that information may be lost, incorrectly identified, or misapplied in the information nodes resulting in incorrect or invalid reports.
- If there are many different information nodes and data flows within the information supply chain, the burden of choosing the right information node for correct communication can be high. Decisions based on the wrong information can have significant negative consequences for the organization.

### Usage

Information values reporting is supported by most applications to show the operational state of the aspect of the business. Business intelligence and specialized reporting packages provide more sophisticated information values reports that have been created from consolidated information collections such as data warehouses and data marts.

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Values Profile

### Qualified Name

DesignPattern::Information Values Profile

### Category

Information Identification Patterns

### Description

Use a data-profiling tool to understand the types of data stored and range of values these types are set to.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is using the information it is managing and wants to assess its content.

### Problem Statement

An organization does not know what type and level of quality of data is located in a particular information store.

### Problem Example

MCHS Trading maintains an information collection for Account data as part of the Stores system with associated customer information where there may be multiple accounts based on unique store location for any given customer. The system is an older application and due to system limitations certain fields have been reused for different purposes or contain multiple contents. Further, the field names are quite cryptic and many individuals familiar with the system have left the organization:

- It is believed that a field in the Account table called Acxdt contains the Account Activation date, but documentation has been lost.
- A field in the Account table called Acmnm is thought to store the customer's middle name for purposes of data consolidation to the Customer Hub but has caused errors during testing.
- The field in the Account table called Actid is thought to store the tax identifier but seems to have inconsistent usage.

### Forces

- Rigid information processes—The data structures used with each information node cannot be easily changed (this is particularly true when the information originates from or is flowing to third parties, such as government agencies or existing or packaged applications).
- Unknown data contents—The location, content, format, ownership, and quality of the data in each system are not well understood, preventing applicable rules and policies from being applied appropriately.
- Information governance—Information governance is a priority for the organization.
- Rapid organizational change—New business and information initiatives need to rapidly identify how to utilize the available information.

### Solution Description

Use a data-profiling tool to understand the types of data stored and range of values these types are set to.

Data profiling typically occurs as a key step of information identification within an information supply chain initiative to provide data-driven understanding of the format, content, and quality of the actual data.

### Solution Example

In the case of MCHS Trading's Stores application information, data profiling reveals key data considerations for each field that is captured, analyzed, and reported:

- The Acxdt field in the Account table does contain dates, but only contains dates when the associated Account status field equals ‘Cancelled' indicating this is the Account Cancellation date.
- The Acmnm field in the Account table contains a mixture of names (that in some cases matches last name where the gender is female, suggesting it was originally a maiden name field), cryptic 8-character alphanumeric values (suggesting it stores some customer passwords), and questions (such as "What is the name of your first pet?" indicating it is used to hold password prompts). This information not only needs to be segregated, but likely falls under new governance and data privacy requirements.
- The Actid field in the Account table does contain tax identifiers though in a mixture of formats (some with hyphens, some without) as well as many default values (‘999999999') and other duplicated values that must be accounted for in subsequent usage.

### Benefits

- Consistent representation of information collections is achieved in the target information node without requiring modification of the source information node.
- Information collections are enriched with associated and relevant information.
- Reengineering data dynamically whenever it is moved along the information supply chain means the information nodes are free to structure their information collections to suit their internal needs.

### Liabilities

- In identifying information, there is the possibility that information may be lost, incorrectly identified, or misapplied in the information nodes.
- If there are many different information nodes and data flows within the information supply chain, the burden of information identification can be high.

### Usage

Information identification is a primary activity in managing information collections and moving data from one information collection to another. Usage includes the following:

- Integrating multiple applications that contain pieces of information collections
- Acquiring and merging (or consolidating) new data sources
- Populating and maintaining information collections stored in a data warehouse, data mart, or Master Data Management system
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Lineage

### Qualified Name

DesignPattern::Information Lineage

### Category

Information Identification Patterns

### Description

Review design documentation, metadata, and existing system configuration and behavior to build up a picture of the information supply chain to the information store.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is using the information it is managing and wants to assess its content.

### Problem Statement

An organization does not know where data located in an information store could have come from.

Existing data flows and relationships are not well understood or do not align with expected flows.

### Problem Example

MCHS Trading is attempting to understand the flow of data from the Stores systems as it builds its Customer Hub for downstream reporting. However, the lineage into the Order, Inventory, and Shipping systems is not recorded. Therefore, they cannot readily establish the following:

- Which fields are used to drive order fulfillment?
- Which customer data has precedence in the order?
- What is the origin of data on business reports?
- Which fields are critical to the upcoming Customer Hub and reporting initiatives?

### Forces

- Information governance—Information governance is a priority for the organization.
- High cost/risk—Incorrectly applied data in an information supply chain has a cost or risk to the business in the design, development, delivery, or management of that supply chain.
- Poorly understand information flows—The flow and relationship of the data in and across each system in the information supply chain is not well understood or is no longer correctly described.

### Solution Description

Review design documentation, metadata, and existing system configuration and behavior to build up a picture of the information supply chain to the information store.

Incorporate existing information supply chains into a metadata collection and review the associated data lineage. Discover underlying information flows and relationships, including information store and data mapping. Identify those data domains and elements that should be profiled and monitored.

### Solution Example

In the case of MCHS Trading's movement of Stores Account information into the Customer Hub, the bulleted activities are implemented as part of an information pathway:

- Data sources are captured in the metadata collection as part of the Subject Area Definition.
- Process flows are added into the metadata collection linking one data source to another, either automatically as processes or jobs are implemented or manually when capturing older, existing processes or jobs.
- Ongoing executions of process flows add operational metadata to the Information Lineage.
- Semantic Tagging allows users to build different views of the Information Lineage in order to identify data usage in reports, as well as identify impacts of potential changes to the information supply chain.

### Benefits

- Once the metadata collection is complete, or new information supply chains are built, it should be periodically updated as systems change over time.
- The data lineage may be used as a resource to understand data flows and relationships during the development of an information supply chain.

### Liabilities

- If there are many different processes and information nodes within the information supply chain, the burden of creating, managing, and understanding the data lineage can be high.
- Establishing and maintaining a metadata collection of information assets for use in data lineage can be time consuming and requires commitment by the organization across and including business and technical units.

### Usage

Information identification is a primary activity in managing information collections and moving data from one information collection to another. Usage includes the following:

- Integrating multiple applications that contain pieces of information collections
- Acquiring and merging (or consolidating) new data sources
- Populating and maintaining information collections stored in a data warehouse, data mart, or Master Data Management hub
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Identification
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Provisioning

### Qualified Name

DesignPattern::Information Provisioning

### Category

Information Provisioning Patterns

### Description

Information is supplied to an information process when it starts, through its user interfaces, and through stored information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities, and information must be provided to the process.

### Problem Statement

An information process needs information to perform its work.

An information process operates in a context. This context is the information that describes how and why it was started, whom it is working for, the resources available to it, and how it relates to past events and activities. How is this information process provisioned with the contextual information it needs?

### Problem Example

The Mail-Shop application is responsible for recording new orders. Where does the new order information come from? How is the order processed?

### Forces

- The same information is needed multiple times—Individuals do not want to repeatedly type in the same information.
- Valid values vary—The definition of which are valid values for an attribute in a subject area may not be consistent throughout the organization.
- Information costs money to store and maintain—Multiple copies multiply the cost.
- Information needs to be shared between processes—Although each process is probably using different subsets of the information and may want it formatted differently.
- Reformatting takes processing effort—Collating and reformatting the same piece of information on the fly, over and over again, is inefficient.

### Solution Description

Information is supplied to an information process when it starts, through its user interfaces, and through stored information.

See Figure 4.4.

An Information Trigger starts an information process. This trigger may have an Information Event associated with it, which is passed to the information process when it starts. This is the first piece of information that the information process receives and typically describes the context in which it was invoked.

Once running, the information process may have one or more user interfaces that are used to interact with its information users. A user interface represents a key opportunity to receive new information—and to deliver valuable information to the organization. It is also a place where incoming information needs rigorous validation, while outgoing information must only be delivered to the right information users.

Finally, an information process may work with stored information. This is made available to it through Information Services. An information service will produce information for an information process on request. It will allow the information process to create, update, and delete information as well. Typically, an information service supports information from a particular subject area and so it is common for an information process to work with multiple information services.

The information service is responsible for locating the stored information and hiding the details of this mechanism from the information process. Ultimately, the information is stored in one or more information collections. However, the precise location and format of the information is hidden from the information process.

The mechanisms required to support the work of the information services are where the complexity of information management lies. These different mechanisms are explained in detail by the specialized information provisioning patterns that follow. The choice of provisioning pattern is typically a compromise between providing local information structured exactly to the needs of the information process and reducing the number of copies of the same information kept in the organization's information nodes.

### Solution Example

When a customer phones the mail order help line, the customer service representative triggers a new order information process in the Mail-Shop application. This takes the customer service representative through a series of screens requesting information about the customers, the goods they want to order, their payment details, and the delivery address. These values are stored in an information collection when the process is complete and the customer confirms the order.

### Benefits

- Information provisioning provides a well-defined approach to supplying information to the organization's information processes.

### Liabilities

- In an ideal world, there would only be one copy of each type of information stored by the organization. However, this is rarely feasible because information processes can have slightly different information needs to one another. As a result, information provisioning has to become more sophisticated, creating multiple copies of the information and potentially synchronizing these copies through multiple stages of processing in order to meet all of the needs of the organization.

### Usage

Information provisioning is a continuous and active part of every IT system.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

User Private Provisioning

### Qualified Name

DesignPattern::User Private Provisioning

### Category

Information Provisioning Patterns

### Description

Provide the ability to run an information process and store the results in the information user's private workspace.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

An information user needs to perform an ad hoc piece of work using the information he or she have in his or her private workspace.

Not all work in an organization is planned. Sometimes ad hoc requests are made to an information user. They need IT facilities that are flexible enough to allow them to process ad hoc data and retain the results.

### Problem Example

An information user has a new idea for a customer offering and wants to develop it further before sharing it with others.

### Forces

- Ad hoc activity needs ad hoc provisioning—It is impossible to anticipate exactly what the information is required for an ad hoc activity.
- Keeping early drafts private—Often information users want to keep information private to them, particularly in the early stages of a project when various aspects are still fluid.
- Centralized provisioning—The IT-provided systems tend to automate the commonly occurring, business-critical, and consistently defined activities as information processes.

### Solution Description

Provide the ability to run an information process and store the results in the information user's private workspace.

This information process may be running on the information user's personal computer, smart device, or a centrally managed information node.

### Solution Example

A buyer in the Merchandising Department at MCHS uses a process in the Product Hub to download (copy) a set of products and its details to a local file and populates the information in her spreadsheet. She adds additional information out of several supplier catalogs to the spreadsheet and performs analysis on the information there.

### Benefits

- This type of provisioning creates a flexible environment where information users can support ad hoc requests.

### Liabilities

- This type of provisioning results in information that could be important to the organization being stored in an ungoverned manner. It relies on the judgment of the information user to know how to protect the information and when to share it. Often, when sharing occurs, it is also in an ungoverned manner via emails and shared storage.

### Usage

This pattern is in operation when people use desktop applications such as word processing and spreadsheets. It is good for locally optimizing the work of an individual but has negative consequences on governing and sharing the information people use and create.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Application Private Provisioning

### Qualified Name

DesignPattern::Application Private Provisioning

### Category

Information Provisioning Patterns

### Description

Locate the information collections in the same information node as the information processes. The local information processes are responsible for maintaining these information collections on a day-to day basis.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

The information processes within an information node need independent control of the information collections that they are using.

This may be because it is to be deployed into many different environments and cannot depend on other sources of information for its ongoing operation.

### Problem Example

The E-Shop application is a packaged application for providing web-based catalogs and ordering. The application is sold by a vendor to many organizations and needs to be able to operate independently of other systems because there is no knowledge of what will be available in each deployment.

### Forces

- An information process is dependent on all of the information collections it uses— These information collections are only available if the information nodes that host them are operational.
- No application is truly an island—It needs to receive up-to-date information about other activities in the organization. Also, other information nodes need the information that it possesses.

### Solution Description

Locate the information collections in the same information node as the information processes. The local information processes are responsible for maintaining these information collections on a day-to day basis.

See Figure 4.6. An information node where the information processes are locally provisioning with their own private information collections is often referred to as an application.

### Solution Example

When first installed, the E-Shop application had its own information collections for storing customer accounts, the product catalog, and orders from customers. All of its locally hosted information processes use these local collections.

### Benefits

- An information node with this type of provisioning can be deployed into many environments.

### Liabilities

- An information node using only this style of provisioning does not share information with other information nodes. The information sharing happens between people, through conversations, printouts, memory keys, and emailing snapshots of data between groups of people. The result is that the sharing of information is not governed and teams can become dependent on an extracted snapshot of data that has an unknown provenance; it is not backed up nor protected in any way.
- Organizations running many applications invest in synchronizing and distributing information between them. The better application packages recognize this requirement and provide interfaces to facilitate additional information provisioning.

### Usage

Most applications and commercial software packages are written to use their own private information collections.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Daisy Chain Provisioning

### Qualified Name

DesignPattern::Daisy Chain Provisioning

### Category

Information Provisioning Patterns

### Description

Pass control of the work for the business transaction between the information processes in a similar way that a baton is passed between runners in a relay.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

A single business transaction is supported end-to-end by information processes from multiple information nodes. How is this work coordinated?

This often occurs when the organization has many specialized applications. Each application implements part of the required processing and then needs to initiate another information process to continue the work.

### Problem Example

When the E-Shop application creates a new order, it must be passed to the Shipping application to fulfill the order.

### Forces

- Applications are typically implemented in an independent fashion—Particularly packaged applications because they are to be sold into many organizations and need to operate independently.
- Organizations operate in silos—As organizations grow, they need to be split into independent operating units to make the work manageable. Applications are often implemented to support just one part of an operating unit. The people working within the operating unit are specialists and are unaware how the rest of the organization operates.
- Information processes are implemented with assumptions on how their information is managed—For example, E-Shop may assume a person with an entry in its customer details information collection is registered to use the E-Shop application. These assumptions limit how much information can be consolidated and changed.
- Applications may not be easy to integrate with other systems—For example, they may not have externally callable interfaces to provide access to the information processes and information collections. As such, integration middleware is needed to connect them to the organization's information supply chains.

### Solution Description

Pass control of the work for the business transaction between the information processes in a similar way that a baton is passed between runners in a relay.

The original information process should raise an information event to trigger the new information process. This event is raised through a Triggering Information Service.

Figure 4.8 shows how this works. The numbers on the diagram of Figure 4.8 refer to these notes:

1. When a new business transaction is detected, an Information Event is raised.
2. The Information Trigger detects this information event.
3. The information trigger starts the first information process.
4. The information process runs to completion.
5. It calls a Triggering Information Service for the subsequent processing.
6. The information service raises another information event for the next step to begin.
7. This, in turn, creates another information trigger to initiate the next information process.
8. The triggering of the sequence of information processes continues until the business transaction is complete. Often, the information processes supporting the business transaction are hosted in different information nodes. This case is shown in Figure 4.9. The sequence is very similar. The numbers on the diagram in Figure 4.9 refer to these notes:
1. When a new business transaction is detected, an Information Event is raised.
2. The Information Trigger detects this information event.
3. The information trigger starts the first information process.
4. The information process runs to completion.
5. It calls a Remote Information Service to initiate the next step.
6. The remote information service uses an Information Payload to send the request to the next information node.
7. Receipt of the information payload invokes a Triggering Information Service.
8. The triggering information service converts the information payload into an information event.
9. This, in turn, creates another information trigger to initiate the next information process.
10. The triggering of the sequence of information processes continues until the business transaction is complete. In both cases, important context information must be passed to the information processes. This is the role of the information event and the information payload structures. While the information process is running, the context is stored in Information Processing Variables. The context typically contains details of the business transaction, intermediate results, and references to stored information. The information processes may be referring to the same information collections, but it is most common that each has its own private information collection and the information passed between them is just enough information to locate the appropriate locally stored information.

### Solution Example

The E-Shop application was not designed with integration in mind. The implementation of the New Order information process does not include a trigger to kick off any order-fulfillment process. It has its own information processes that require an information user to repeatedly query for new orders. MCHS Trading's operations are too extensive to make that approach practical and it needs to automate the fulfillment of orders as much as possible. This includes automatically triggering the Shipping application to ship the goods. This triggering is driven when E-Shop writes the new order in its order details information collection.

Each new order results in a new Information Entry in the order details information collection. When the information entry is written, it creates an event that results in an Information Change Trigger. This information change trigger issues a Remote Information Service to copy details of the order to an Information Payload and send it to an Information Broker. The information broker transforms the information payload into a format suitable for Shipping and passes it to a Queue Manager. The queue manager's role is to safeguard the information payloads for the periods when the Shipping application is not available. It will pass the information payload to the Shipping application as soon as possible. When Shipping receives the information payload, it starts to fulfill the order.

### Benefits

- Using daisy chain provisioning is a very cost-effective approach to passing work between existing applications and allows work to be parallelized. The integration is very loosely coupled and the people working with each of the applications are not affected by the operation of the other applications.

### Liabilities

- It may be hard to trace where a piece of work has got to—or to correct the information about it once it has left the first application. Typically, an investigator has to query each application in turn to understand what processing has occurred.
- This style of provisioning is often used between information nodes whose information processes were designed to use Application Private Provisioning. This means that each step in fulfilling the business transaction is executed using different information collections. These information collections must be kept synchronized to ensure consistent behavior throughout the business transaction.
- If an information process is unavailable, the passing of work will fail and part of the business transaction will not run.

### Usage

Daisy chain provisioning is often referred to as Enterprise Application Integration (EAI). EAI uses distributed messaging to pass work between applications.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

User Shared Provisioning

### Qualified Name

DesignPattern::User Shared Provisioning

### Category

Information Provisioning Patterns

### Description

Provide an information node that can store a variety of information under the control of the team members.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

A team of information users is working together to perform an ad hoc project.

As a result, the information they are using and creating will need to be shared among them. The team needs to control how this information is organized, which information is available to people outside of the team and when this happens.

### Problem Example

MCHS Trading decides to acquire another company to expand its distribution capability. It needs to perform analysis of how this will affect its existing offerings, how this will be financed, how the organization will be structured, and create communications for various audiences—all before the acquisition goes ahead.

### Forces

- It is impossible to anticipate exactly what information is required for an ad hoc activity.
- Often, information users want to keep information private to them, particularly in the early stages of a project when various aspects are still fluid.
- The IT-provided systems tend to automate the commonly occurring, business-critical, and consistently defined activities as information processes.

### Solution Description

Provide an information node that can store a variety of information under the control of the team members.

Typically, the information being generated is in the form of documents and spreadsheets. It needs to be organized so it can be reviewed and commented upon. Multiple versions of this information will be created as the team's thoughts mature.

### Solution Example

The financial analysts at MCHS Trading create reports from the Reporting Hub and store them in a shared information node. They obtain reports from the other company as part of their due diligence and bring the information together in a set of shared spreadsheets in which they perform their financial analysis. From their results, they build documents and presentations that are also stored in the shared information node.

### Benefits

- This approach allows a level of sharing, management, and protection of the information being produced by the team, without restricting the type of information it can produce.

### Liabilities

- The structure and organization of the information is left to the team's discretion, which can make it hard to harvest the information for future projects.

### Usage

This pattern describes the use of collaboration technology, such as network file systems, wikis, blogs, and document repositories.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Service Oriented Provisioning

### Qualified Name

DesignPattern::Service Oriented Provisioning

### Category

Information Provisioning Patterns

### Description

Provide information services for the information collection to enable information process to access it, irrespective of the information node they are located in.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

An information collection is too big, too sensitive, too valuable, and/or changing too rapidly to be copied to other information nodes.

### Problem Example

MCHS Trading's E-Shop application is responsible for capturing customer orders through the Internet. However, in order for a customer to place an order, the application must obtain the stored payment details about the customer and the order codes from the product details. This information is not stored in the E-Shop application.

### Forces

- Independent implementations—Packaged applications in particular have distinct implementations because they are to be sold into many organizations and need to operate independently, and, therefore, have distinct and different information services from those built within an organization.
- Inconsistent information definitions—Lack of clear understanding of information across the information supply chain can impact effective service definition or the selection of the right information collection to use.
- Assumptions on how information is requested and delivered—The assumptions/ models incorporated when services are introduced may limit how much information can be integrated, consolidated, utilized, and changed within an information process.
- Difficulty integrating with other systems—For example, a set of information services may not have externally callable interfaces to provide access to the information processes and information collections with which they work. As such, specialized integration middleware is needed to connect them to the organization's information supply chains.

### Solution Description

Provide information services for the information collection to enable information processes to access it, irrespective of the information node they are located in.

See Figure 4.10.

### Solution Example

MCHS Trading's E-Shop application incorporates Information Services that work with local Information Collections and those that can invoke remote Information Services to obtain information from remote Information Collections.

### Benefits

- This approach allows a level of sharing, management, and protection of the information being utilized by different information processes, without requiring the movement of all information to a specific information node and ensuring that the information used is the most current information.

### Liabilities

- The structure and organization of the information is based on the requirements of the local information nodes, which can make it hard to integrate the information. The information services must be standardized, cataloged, and managed to ensure consistency of use across the different information nodes and processes that call them, and to reduce the cost of maintaining them.

### Usage

This pattern describes the use of information services as commonly incorporated within service oriented architectures (SOA) and applications built using such architectures.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Linked Information Provisioning

### Qualified Name

DesignPattern::Linked Information Provisioning

### Category

Information Provisioning Patterns

### Description

Store a reference to the entry, which includes the location for its information collection and the identifier of the entry within it.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

Data from distributed sensors and probes is required to support an information process.

An entry in a specialized information node needs to pass its information to another (possibly remote) information collection.

### Problem Example

The MCHS Trading warehouses receive product stock from various suppliers. The warehouses have implemented bar-code scanners to record the shipments received and reduce manual error. The bar-code scanners have limited memory and storage and cannot serve as Information Nodes that house Information Collections, though they link to an Information Node that does log all transactions. MCHS Trading needs to connect this information to other applications.

### Forces

- Minimal information storage—Sensors, probes, and related devices receive and transmit information in high frequency, but may not support storage of significant amounts of information.
- Difficulty integrating with other systems—Sensors and similar devices have unique operating systems and may not readily connect with other systems or applications.
- High information volume and/or frequency—The information process and information collection into which the information is delivered must be able to meet the volume/ frequency of the incoming information.

### Solution Description

Deliver and store a reference to the entry, which includes the location for its information collection and the identifier of the entry within it.

Receive the data from the source and store it, including references to the source Information Node. Perform a first pass on the data as close to its source as possible with an aim to cleanse and add context to it. Then pass the data to a centralized information collection where information processes can build up the big picture.

### Solution Example

MCHS Trading establishes an Information Node containing an Information Collection to record the shipment's bar-code information. The node is directly linked to the bar-code scanner application, which sends the information entries into the collection. Other applications such as the Shipping and Purchasing applications can now connect to this Information Collection through other regular provisioning patterns.

### Benefits

- High volume and high frequency information can be recorded, forwarded, and collected where it can be utilized by other applications.

### Liabilities

- Information will be limited by what the sensor or other device can record. Certain types of devices are susceptible to "noise," in which case such noise will be forwarded and stored as well as legitimate information. This may have significant consequences when other applications attempt to use the information.

### Usage

Initial receipt of information coming from devices such as sensors, probes, and scanners utilize this pattern.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Cache Provisioning

### Qualified Name

DesignPattern::Cache Provisioning

### Category

Information Provisioning Patterns

### Description

Keep a relevant subset of information for the consuming information processes in memory and refresh it as appropriate.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

A critical information collection may occasionally be offline or not able to provide information fast enough for the consuming information processes.

How does a consuming information process continue to operate?

### Problem Example

MCHS Trading's E-Shop application is responsible for capturing customer orders through the Internet. The E-Shop is expected to be available twenty-four hours per day, seven days a week (24/7) for customers to place their orders, but the applications handling the customer and product details required for the orders are offline at scheduled intervals to address daily processing requirements.

### Forces

- Information collections are not always available—The information collections from which the information is obtained are not accessible.
- Information values change over time—Any copies of information need to be kept synchronized with the master usage information collection.

### Solution Description

Keep a relevant subset of information for the consuming information processes in memory and refresh it as appropriate.

The area where the information is held in memory is called a cache. There are two approaches for provisioning the cache:

1. An additional information provisioning process pre-populates the cache with all of the information from the information collection and copies the latest values from the critical information collection into the cache as they become available. The consuming information processes accesses the cache whenever it wants some information.
2. The consuming information process calls an information service. The information service checks to see if the requested information is in the cache. If it is (and has not been in the cache too long and become stale), this value is used; otherwise, the requested values are retrieved from the information collection. They are then placed in the cache and returned to the requester.

### Solution Example

The E-Shop application incorporates specific services that poll the customer and product Information Collections at periodic intervals and stores the results in a local cache. When the E-Shop application fails to directly connect to its targeted Information Collection, it triggers an alternate information process that provisions the calling information process from the cache.

### Benefits

- Continuous operational processing can be maintained.

### Liabilities

- Information processes may not have current information available, if there is delay updating the cache.

### Usage

Cache provisioning is often used to speed up the access of slowly changing information, such as images for web pages or user profile attributes. The first time the information is requested, it is read from the information collection and added to the cache. It stays in the The cache may be located in the web server, or further out in an edge-of-network server.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Snapshot Provisioning

### Qualified Name

DesignPattern::Snapshot Provisioning

### Category

Information Provisioning Patterns

### Description

Schedule an information flow from each of the source information collections to transfer the information to an information collection that will contain the snapshot of information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

A team needs its own copy of some information for analyzing or for experimenting with.

Often, this is for a specific project where the team wants to make experimental changes to aspects of the information to understand the effects. By using a copy, the team can perform the experiments without disrupting the existing business.

### Problem Example

MCHS Trading decides to acquire another company to expand its distribution capability. It needs to experiment with the way that the stores and sales teams will be organized after the acquisition.

### Forces

- Each application typically has its own unique data formats that must be supported by the provisioning process.
- Information is not always captured in the form that is useful for processing.
- When information is shared among multiple information processes, each information process is affected by the work of the others. While an information process is partway through a set of related updates, the affected information entries are typically locked so the other information processes do not see the partially completed changes. This works well for changes that take a few seconds. Anything longer than that needs an alternative approach.

### Solution Description

Schedule an information flow from each of the source information collections to transfer the information to an information collection that will contain the snapshot of information.

When the team has finished with this copy of the information collection, it can be deleted. Alternatively, its contents can be replaced periodically to refresh the values. See Figure 4.11.

### Solution Example

The acquisition team is given a snapshot of the sales and stores information so that the team can try different organizations to determine the best one.

### Benefits

- This style of provisioning allows experimentation without disrupting the existing business.

### Liabilities

- This style of provisioning creates a copy of information that must be protected as if it were the original version. Particularly, when the team has finished with it, it must be destroyed appropriately.

### Usage

This style of provisioning is used to support projects that need information for a finite period of time or to seed the information collections of a new application. Sometimes the provisioning is into a spreadsheet, stored in an information user's private workspace. Alternatively, the snapshot could be located on a managed information node.

Note that snapshot provisioning is also common when replacing an operational system where the old and new systems are to run in parallel for a period of time. The snapshot is generally run once to populate the new system, and then both systems are supported by Information Flows with the same style of provisioning until Information Users are satisfied with the results in the new system. At that point, the old system is disconnected from the Information Supply Chain, and the new system takes its place in the Information Supply Chain.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Mirroring Provisioning

### Qualified Name

DesignPattern::Mirroring Provisioning

### Category

Information Provisioning Patterns

### Description

Create new information collections for the information process and regularly provision them from other sources of information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

When a new information process is introduced, or updated, the stored information it requires is not always available at a suitable class of service.

Typically, this may be because the changes are being made to an information collection with Master Usage and they are being distributed to a related information collection with the Reference Usage.

If the information is not synchronized, some, or all, of the information processes will be working with out-of-date information.

### Problem Example

MCHS Trading has product information in the following systems: E-Shop, Mail-Shop, Stores, Shipping, Invoicing, and Reporting Hub. This product information needs to be synchronized with the master copy of the product catalog that is maintained in the Product Hub application.

### Forces

- Unique data requirements—Each application typically has its own unique data formats that must be supported by the provisioning process.
- Offline working—An information process needs occasionally to work offline from one of its reference information collections and needs to keep a relevant subset of information for the information process in memory and refresh it as appropriate.
- Need for rapid data access—Local information collections, designed specifically for an information process, typically provide the fastest access to the information for that information process.

### Solution Description

Create new information collections for the information process and provision them from other sources of information.

The mirroring provisioning pattern copies information between Information Collections in order to simplify the work of one or more information processes. For example, the information provisioning mechanism may copy information so it is local to a consuming information process for faster access, to consolidate and correlate the information from multiple places so a complete view is available, or reformat the information to match the queries used by the information process. Whenever a change is made to the source information collections, trigger an information flow to transmit the changes to each of the destination information collections. This is shown in Figure 4.12. The numbers on the diagram in Figure 4.12 refer to these notes:

1. An information process changes information in the source information collection.
2. This change triggers an information flow.
3. The information flow transforms and transports the information to one or more destinations. Mirroring provisioning is usually designed in three phases:
1. The initial load of the new information collection(s). This copies all of the existing values into the new information collections. Often, specialized techniques for bulk-loading data into the persistent storage are required to complete the initial load in a reasonable time.
2. The synchronization of subsequent changes to the source information collections with the copies. This processing is sometimes called the delta load if it is batch or "tricklefeed" if it is real time. It is necessary if the copy is to reflect the current state of the information over a sustained period of time. Typically, the implementation of this synchronization is different from the initial load—the triggering process must be more selective, ensuring the appropriate information is sent at the right time. The transport mechanism is often different—optimized for smaller, frequent transfers of a variety of information payloads.
3. The decommissioning of the copies when they are no longer needed. A phase that is often forgotten about in the rush to create the new copy. This copy will have information processes dependent on it—but for how long? When does the organization know it can remove the copy? How will it be done? Information Flows are used to implement the initial load and the subsequent trickle-feed. They are either passed the information, or they extract it from the original information collections. They then may perform a number of Information Reengineering activities on it, before delivering it to the destination information collections. The choice of information flows required will depend on the type of information provisioning. These are described in the information patterns that follow. Decommissioning is essentially a delete process, although many organizations move the contents to an archive in case the information collections need to be restored.

### Solution Example

An Information Process Trigger fires whenever there are new product details to distribute and that action triggers a Partitioning Distribution information flow. See Figure 4.13.

### Benefits

- Mirroring provisioning (1) enables new information processes to be introduced by the organization that have slightly different information needs to the existing information processes; (2) can move information to more cost-efficient information nodes for certain types of processing.

### Liabilities

- Mirroring provisioning can create copies of information that need to be stored and maintained. It is important to ensure these copies are properly secured and deleted once no longer needed.
- Ideally, the information collections that are being provisioned using mirroring provisioning will have Reference Usage or Hybrid Usage by the information processes that use them. Any updates made to the copy may be lost as a result of new information being received through the trickle-feed. Also, understanding which collection has the best set of values becomes problematic if there are multiple information collections for the same subject area that have Master Usage.
- Care must be taken to ensure the meaning of the information at the originating information node matches the intended use in each of the destinations.

### Usage

Mirroring provisioning is used extensively in data warehouse and analytical applications. It often is a mechanism that is used to keep operational systems synchronized or to migrate information between versions of the same application.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Peer Provisioning

### Qualified Name

DesignPattern::Peer Provisioning

### Category

Information Provisioning Patterns

### Description

Each time an information entry in any of the information collections changes, the updated information values are sent to the other collections.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

An information supply chain needs to keep the information in multiple master information collections synchronized.

This situation arises when the same kind of information must be collected from multiple sources and this information is stored close to where it is collected.

### Problem Example

MCHS Trading has multiple sources of input for customer data: the Stores, the Mail-Shop, the E-Shop, and the new Customer-Care application. The customer details have been consolidated into a Customer Hub, but because the E-Shop application is a primary entry point for customers, it receives updates through its own Customer Master, distinct from the Customer Hub. For effective customer service, MCHS Trading must ensure that updates to the Customer Hub reach the E-Shop and those from the E-Shop are applied into the Customer Hub.

### Forces

- Multiple points of origination—Where multiple applications originate change, these must be synchronized across all the applications to ensure that the most recent information is available everywhere and not repeatedly overlaid by out-of-date information.
- Unique data requirements—Each application typically has its own unique data formats that must be supported by the provisioning process.
- Need for rapid data access—Local information collections, designed specifically for an information process, typically provide the fastest access to the information for that information process.
- Impact of latency—In some industries, there is no or little tolerance for latency in distributing the changes to the data.

### Solution Description

Each time an information entry in any of the information collections changes, the updated information values are sent to the other collections.

If there are only two Information Collections to synchronize, then Mirroring Provisioning can be used flow updates made to one of the information collection on to the other so the information is flowing in both directions.

As the number of information collections involved increases, this approach leads to multiple point-to-point solutions with increasing risk of inconsistent change and delivery. A second approach is for each to push the new information into a Queue Manager running an Information Broadcasting Process that distributes the updates to the other information nodes.

### Solution Example

MCHS Trading only needs to keep its Customer Hub and E-Shop application synchronized, but it also wants to leave room for possible changes (such as acquisitions of new business lines) in managing its customer details. Each information node is allocated a queue on a Queue Manager. When a change is made to customer information on either information node, it triggers an Event Information Request to copy details of the change into the appropriate queue.

An Information Broker picks up the resulting Information Payload from the queue. Customer Hub has Complete Scope so all information payloads from E-Shop are transformed and passed to Customer Hub. E-Shop has Local Scope so only information payloads that are related to existing Information Entries in E-Shop's customer information collection are transformed and passed to E-Shop. Otherwise details of customers using other channel would find their way into E-Shop's customer data, which would cause errors in the E-Shop information processes.

### Benefits

- The most current information is available in all applications, although such information comes from many distinct points of entry.

### Liabilities

- Changes that are propagated to a peer should not cause a return flow back to the originator—causing a continuous loop of updates. As a result, the trigger for the synchronization typically cannot be driven from the detecting changes in the information collections (see Information Change Trigger).
- There may be race conditions where the same attribute is updated in two places with different values—which one is kept?
- Peer provisioning may be synchronizing information collections that have different scopes and coverage. The provisioning process should only introduce new information entries into a destination information collection if it makes sense with respect to the scope of this information collection. The provisioning process may have to retrieve attributes from an additional information collection if the coverage of a destination information collection is broader than the coverage of the source information collection.

### Usage

Peer provisioning is used extensively in applications handling master data or where operational systems must be synchronized.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Event-Based Provisioning

### Qualified Name

DesignPattern::Event-Based Provisioning

### Category

Information Provisioning Patterns

### Description

Collect together the events into a wellknown information collection that the information process can access.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

An information process needs to keep track of when particular events occur, either locally or in other parts of the organization.

### Problem Example

MCHS Trading wants to monitor the comments that people are making about its products on social media so that it can react to them in a timely manner whenever appropriate.

### Forces

- Minimal reaction time to events is required—If an information process needs to react to events as they are happening, the information gathering and processing must be as close to real time as possible.

### Solution Description

Collect together the events into a well-known information collection that the information process can access.

As these facts and events are discovered, details of them are sent using Event Information Requests to a common information collection that is available to the information process.

### Solution Example

MCHS Trading has set up a feed from a number of social media sites and uses an Information Streaming Process to parse the text and detect when people are commenting on either the company or selected products. When these entries are detected, events are sent to the customer call center detailing the source.

### Benefits

- This pattern supports the processing of huge quantities of incoming data, which is extremely vital for managing information from real-world sensors and networks.

### Liabilities

- Care must be taken to save all of the information necessary for downstream information processes. In addition, some thought should be given to being able to demonstrate that the processing within the streaming provisioning is working correctly.

### Usage

Monitoring of information utilizes event-based processing and occurs in situations such as social media feeds, operational health monitoring, or information quality remediation processes.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Recovery Provisioning

### Qualified Name

DesignPattern::Recovery Provisioning

### Category

Information Provisioning Patterns

### Description

Maintain an ongoing backup copy that is physically separate and secure. Ensure there is an alternative infrastructure to host the restored collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

How is information supplied to an information process?

### Problem Statement

The infrastructure supporting an information collection may fail. How do we restore the information to the information supply chain?

### Problem Example

One stormy night, there is a power outage and the E-Shop application suffers a disk head crash. How does the MCHS Trading team recover the situation?

### Forces

- Failures may happen at any time—An unusual incident can create a cascading series of failures.
- Constant change of information—Information that is critical to an organization's operation is often changing all of the time.

### Solution Description

Maintain an ongoing backup copy that is physically separate and secure. Ensure there is an alternative infrastructure to host the restored collection.

Recovery provisioning is enabled through backup/restore routines. It takes planning to work though all of the permutations of possible failures from a simple accidental delete of information, to hardware failure, or an incident at the physical location of the information nodes, which prevents their use. The plans should consider how to act if the situation is either temporary or permanent. Finally, an organization must practice its responses to different types of incidents to ensure all recent changes to teams, systems, and working practices are covered in the plans.

### Solution Example

MCHS Trading replaces the failed drive and restores E-Shop's information collections from its backup that fortunately finished about an hour before the storm started.

### Benefits

- Having backup collections and processes helps to ensure successful recovery from unanticipated disasters or from planned maintenance.

### Liabilities

- Backups need to be regular and managed in order to be successful, particularly as part of a disaster recovery plan, a common managed activity. Backups require storage, which adds cost, whether onsite or offsite. Disaster recovery plans and backups also require periodic review and tests to ensure effectiveness.

### Usage

Recovery provisioning is used after an incident that takes away the information normally available to an information process.

### Search Keywords

- Patterns of Information Management
- Information Provisioning
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Supply Chain

### Qualified Name

DesignPattern::Information Supply Chain

### Category

Information Supply Chain Patterns

### Description

Design and manage well-defined flows of information that start from the points where information is collected for the organization and links them to the places where key consumers receive the information they need.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is a complex mix of people and assets, cooperating and interacting with the world around it to fulfill its purpose.

### Problem Statement

An organization needs to process information in order to fulfill its purpose. How is the flow of information coordinated throughout the organization's people and systems?

The volume and quantity of information needed to operate even a small organization is much more than any one individual can comprehend. So work and information is divided up into manageable chunks. These chunks need to coordinate and share information. The interactions are complex with many opportunities for error.

How do we coordinate the sharing of information in a reliable, timely, and cost-effective way?

### Problem Example

MCHS Trading owns a number of applications, each supporting different parts of the business. Information must flow between its order-taking, Shipping, and Invoicing applications to receive and fulfill customers' orders.

Any failures in this flow of information could affect the organization's ability to serve its customers or collect money for goods sent out.

### Forces

- Duplicated information—The same information may be stored in many places in an organization's systems.
- Variety of information formats—Each copy of information tends to have its own unique format and there are differences in validation rules and the use of the information.
- Inconsistent definition—The set of valid values for an information attribute may not be consistent throughout the organization.
- Disconnected information supply—An employee receiving new information may not be a direct user of any of the information processes within the information supply chain that manages this type of information.
- People make mistakes—Someone may enter incorrect information into a user interface, either through lack of attention, lack of training, or because the values he or she has are not correct.
- Multiple channels—Information coming in from the outside of the organization can arrive through many channels and have differing levels of quality.
- Storage and maintenance costs—Each copy of information costs money to store and maintain.
- Synchronization latency—There is always some latency in synchronizing new information between the various copies.
- Different perspectives and needs—People in different parts of the organization have different specialized skills, resulting in different perspectives on what is important and the information they need.

### Solution Description

Design and manage well-defined flows of information that start from the points where information is collected for the organization and links them to the places where key consumers receive the information they need.

An information supply chain is a flow of information between information collections in order to convert information received from outside the information supply chain into the form that is needed by its information users. The movement, transformation, and storing of information in the information collections is the responsibility of the information processes.

The type of information within an information supply chain is typically information from a particular subject area (topic) or information for a particular process. This information is transformed between the different kinds of Information Elements as it flows along the information supply chain.

Consider Figure 4.15. The start of an information supply chain is where the organization receives new information either from people or external systems that is needed for it to fulfill its goal. It combines this "information supply" with the built-in capability/knowledge of the organization to produce the information products.

Information Processes inside the information supply chain are responsible for processing information to build the information products. There are many types of information processes in the information supply chain, each with their own responsibilities to receive, transform, and move information around.

Information Nodes are the systems that host the information processes. They also host the storage of information in what are called Information Collections.

Information processes may need to access information stored in information collections that are hosted on different information nodes. Information Provisioning provides the mechanisms to connect the information processes to the information they need.

The information within the information supply chain must be protected from carelessness, theft, accident, and improper use. It is protected using three groups of patterns:

- Information Reengineering—Defines the types of processing that improves the quality of the information
- Information Guard—Defines ways to ensure information is only used for its intended purpose
- Information Probe—Measures that information is what it should be, where it should be, and when it should be These capabilities are applied within the information provisioning part of the information supply chain. The descriptions for these patterns explain how they are used. Information supply is one of the key points of vulnerability of the information supply chain. It provides the opportunity to receive bad information. It also runs the risk of missing information that is vital to the correct working of the organization. Managing the information supply is hard because information is supplied to the organization through many different routes. For each route, it is important to understand the context under which the data is captured because this will affect the assumptions that can be made about the values and where it is appropriate to use it in the information supply chain. In broad outline, the information supply chain has the following parts:
- Capture the information preferably at the point information enters the organization. This is typically (a) through an externally facing employee, (b) through an external user interface, (c) from another system outside of the information supply chain, or (d) from a sensor monitoring the environment.
- Reengineer the information to ensure it meets the needs of the information supply chain. Any errors need to be detected and returned to the supplier as soon as possible.
- Store the information in an information collection—in case of system failures.
- Distribute the information through information provisioning to the various copies of the information that needs updating throughout the information supply chain.
- Export the information as information products for consumption by external parties. These steps should be present and executed in a consistent manner for each of the routes that a particular type of information enters the information supply chain. When an information supply chain produces information for a consumer, it goes through the following steps:
- The recipient connects to the information supply chain at the appropriate point.
- Information guards ensure the recipient is allowed to receive the information.
- The information is gathered from the information collections and an information product is created.
- The information product is exported from the information supply chain to the recipient. A record of the export may be stored. Some information products require information to be gathered from multiple remote information collections. Then it must be restructured, aggregated, and analyzed before the information product can be created. Information collections store the values for the information product where the processes needed to create it are involved, or the product is used repeatedly. When the information product is requested, it can be quickly generated from this information collection alone. This not only saves work, it also provides useful information for auditors to understand who knew what information at any one time. Within the information supply chain, updates to the stored information are received from the information processes and information is moved between the information collections. The usage of these information collections along the information supply chain should ensure the Master Usage information collections are at the start, then the Hybrid Usage information collection and the Reference Usage in the middle and Sandbox Usage collections in the leaf nodes. This is described in Figure 4.16. The numbers on the diagram for Figure 4.16 refer to these notes:
1. All information collections in the information supply chain with master usage should be synchronized, typically with Peer Provisioning.
2. A master usage information collection can be used to provision hybrid and reference usage information supply chains, typically with Mirroring Provisioning, and sandbox usage information collections, typically with either mirroring provisioning or Snapshot Provisioning.
3. A hybrid usage information collection can feed another hybrid usage information collection. All of the attributes sent should be reference values in the downstream information collection that have been enriched with additional master usage attributes.
4. A hybrid usage information collection may feed a master usage information collection as long as the master usage information collection only stores attributes that are mastered by the hybrid information collection.
5. A hybrid information collection can also feed a reference usage and a sandbox usage information collection.
6. A reference information collection can feed a reference usage and a sandbox usage information collection.
7. The sandbox usage information collections are always in the leaf nodes of the information supply chain. If you see different patterns of usage, it is a sign that there are inconsistencies in the information supply chain.

### Solution Example

MCHS Trading has five information supply chains that are critical to its business, as shown in Figure 4.17:

- Customer—Synchronizing and collating information about their customers
- Product—Maintaining and distributing information about the products they are selling
- Order—Sending details of the orders to process between the order-processing information nodes
- Stock—Requesting new stock from suppliers
- Summaries—Collating and summarizing the state of the business Each was designed and improved independently. However, you can see that they share components such as information nodes and information collections. Looking at the customer information supply chain in more detail, you can see that it originates from a new application called Customer-Care. An MCHS Trading employee is able to enter new details for a customer through Customer-Care's user interface and validate that the details are complete and correct. If the customer is present, he or she can also perform a validation of the other contact details, request a loyalty card, and answer questions about the status of orders or other inquiries. All changes are sent to the Customer Hub to update the master customer record. The Customer Hub would also receive updates from the E-Shop application when the customer changes his or her contact details directly through the E-Shop website. New customer details received through the Mail-Shop application are more problematic because they are captured in the context of making an order, rather than the customer explicitly informing MCHS Trading that his or her details have changed. MCHS Trading needed to make a policy decision as to how it wanted to handle this case:
1. The safest approach is to ask the customer explicitly at the time of ordering if the address given is a permanent residence. This changes the implicit change of address into an explicit request. It would require changes to the mail order forms and the Mail-Shop application would have to retrieve customer details from the Customer Hub so that the customer service employee can verify the address information on the order while the customer is on the line. This approach is using the Unique Entries pattern.
2. The second approach is to ignore all customer details entered through the Mail-Shop application. This would mean the Customer Hub only maintains details of customers that have either established a relationship with MCHS Trading either through a Stores card or an E-Shop account. This is the cheapest solution but may have knock-on effects for the Reporting Hub.
3. Third, MCHS Trading could assume the card address received in an order is the customer's permanent address and have the Customer Hub either:
- Update the new value directly.
- Create a new customer record with the new address that is linked to the original one as a potential duplicate. When the customer next makes contact with MCHS Trading, either the E-Shop or Customer-Care application asks the customer to validate his or her address so that the address question is resolved. This discussion illustrates how important it is to understand the context in which information is collected and where they are mismatches with the context in which it is to be used, there is an Information Management Principle set out describing how it should be handled. This information principle would have to apply consistently across the information supply chain. Once the customer master is updated, the Customer Hub distributes the changes to the Reporting Hub and, if necessary, to the E-Shop application. The flow of information along the customer information supply chain is maintained using Mirroring Provisioning.

### Benefits

- Analyzing the end-to-end flow of information as an information supply chain highlights how information is created and used within an organization. It identifies the information processes that create the information products, the information collections they use, and how information is provisioning between them. This focus can demonstrate that the organization is working effectively because the information flow is timely and appropriate. This understanding also ensures that the inevitable failures in systems or processes can be dealt with effectively because the consequences of the failure can be traced and corrected.

### Liabilities

- An organization gets the information it deserves. Good design of the information supply chain provides the basic mechanisms, but if there is no governance around information, meaning an individual is not incented to treat information quality as an important part of his or her role, much of the value is lost. There is more detail on the information governance in the Information Governance Program pattern.
- Most information supply chains need to include applications because these systems act as key sources of the latest information. However, these systems are not always built with information provisioning in mind and they must be connected into the information supply chain with care so this additional processing does not detract from their main mission.
- Connecting an existing system to the information supply chain means that the downstream systems become dependent on it, which may make it harder to upgrade and enhance it in the future.
- The validation rules for information located in an information node within the information supply chain must be compatible with the rules in force downstream of it or information values will not be able to flow all of the way along the information supply chain.

### Usage

An information supply chain is created whenever systems are integrated so information is flowing between them. Each information supply chain is focused on achieving a particular goal:

- Synchronizing information of a particular subject area, such as Customer Details
- Consolidating information that supports a particular information product, such as a regulatory report
- Supplying an information process, such as analytics
- Supplying information to a group of people with specialist skills, either for a project, or an ongoing basis Often these information supply chains are implemented by a single project and may not take a holistic view of the organization's information as suggested by this pattern.

### Search Keywords

- Patterns of Information Management
- Information Supply Chain
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Cascading Information Supply Chain

### Qualified Name

DesignPattern::Cascading Information Supply Chain

### Category

Information Supply Chain Patterns

### Description

Distribute read-only copies of the information to other information nodes and synchronize these copies whenever values change in the centrally controlled information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to process information in order to fulfill its purpose. How is the flow of information coordinated throughout the organization's people and systems?

### Problem Statement

Information that is centrally maintained must be distributed to other parts of the organization.

More specifically, there are other information nodes that host read-only information collections of the same subject area and these information collections need to be kept synchronized with the centrally maintained information.

### Problem Example

MCHS Trading has introduced a Product Hub application for creating the definition of the goods and services it offers to its customers. These product definitions need to be distributed to the order-taking systems: E-Shop, Mail-Shop, and Stores, plus the Shipping and the Invoicing applications.

### Forces

- Different information formats—Each information collection will probably store information from the same subject area in its own private format.
- Different subsets of information—Each information collection will have its own scope of information entries and coverage of attributes.
- Different availability—The information nodes may be available at different times.
- Different keys—The information collection may use different approaches to identifying their information entries.

### Solution Description

Distribute read-only copies of the information to other information nodes and synchronize these copies whenever values change in the centrally controlled information.

This information supply chain assumes there is a single place in the organization where information values from a subject area are maintained (created, updated, deleted). This information collection, called the centralized master, can be maintained by:

- Information processes hosted on the same information node
- Information processes hosted on another information node, but accessing through remote information collections Other information nodes may host these values, but they are read-only reference copies of the centralized master that are synchronized using collection-level Information Provisioning. The simplest form of this information supply chain is where all of the attributes for the subject area are maintained and then distributed from a single information collection. However, the information supply chain may be multilevel where downstream information nodes may add additional attributes before cascading the information further. Figure 4.18 illustrates the cascading information supply chain. The numbers on the diagram in Figure 4.18 refer to these notes:
1. At the head of the information supply chain, information is collected together and stored in an information collection.
2. The information is distributed to one or more downstream information nodes, where it is stored in local information collections.
3. The information received is read-only, but an information node may add attributes to each information entry.
4. These additional attributes may be distributed with the original information.
5. No matter how many times the information is distributed, no received values can be changes—only new attributes added.

### Solution Example

See Figure 4.19. The numbers on the diagram in Figure 4.19 refer to these notes:

1. Product details from the suppliers are supplied to MCHS Trading via the Supplier-net gateway and are sent to Product Hub.
2. The Product Hub is used to define additional information about the product to make it suitable for the MCHS Channels. The Customer-Care application uses an information service to query the product details in the Product Hub whenever they are needed.
3. MCHS Trading use Mirroring Provisioning to synchronize the product details from Product Hub to E-Shop, Mail-Shop, Stores, Shipping, Invoicing, and Reporting Hub. Notice that each of these applications has a different scope and coverage so the provisioning must filter and transform the information differently for each of the destinations.
4. The Reporting Hub sends summaries of the product details to different information marts in the Decision-Center. The E-Shop and Mail-Shop applications both have information processes that allow an information user to maintain their product details information collection. These information processes are disabled once the product details information supply chain is in place. See Figure 4.20. operational.

### Benefits

- This information supply chain is the easiest to coordinate because all updates are happening in one copy of the information—in the single source. Therefore, there is only one place where the quality of the information needs to be assured and because all copies are derived from a common base, there is good consistency between them.

### Liabilities

- The systems on the receiving end of this information supply chain must not make changes to the information they receive because:
- It breaks the consistency of the information supply chain because there is no mechanism to distribute these changes back to the other systems.
- These changes are likely to be overwritten at some point when updates from the upstream systems are received. As a result, any information processes in these downstream systems that make changes to the information collections must be disabled.

### Usage

This pattern is used whenever it is possible to centralize information and publish read-only copies to other systems that need the information stored locally.

It is also used to populate an Information Warehouse and related Information Marts and Information Cubes.

### Search Keywords

- Patterns of Information Management
- Information Supply Chain
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Hub Interchange Information Supply Chain

### Qualified Name

DesignPattern::Hub Interchange Information Supply Chain

### Category

Information Supply Chain Patterns

### Description

Consolidate the information into new information collections (often hosted in a new information node) and then distribute the consolidated information from there.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to process information in order to fulfill its purpose. How is the flow of information coordinated throughout the organization's people and systems?

### Problem Statement

Information that has distributed ownership among peer organizations must be managed and shared.

This means that information from the same subject area is located in a variety of information nodes owned by different parts of the organization. This information must be collated and distributed as a consistent view of information among these information nodes.

### Problem Example

Loyal and satisfied customers are a key reason MCHS Trading has been so successful over the years. However, the rising number of channels that provide service to their customers has led to a fragmentation of the information about their customers. How do they enable the different channels to continue to operate independently while sharing a consistent view of their customers?

### Forces

- Unsuitable formats—The format of the same information in different information nodes is typically different.
- Different scopes and coverage—The scope and coverage of the information collections in each information node is probably different. Note: Scope and coverage are concepts covered in the Information Collection patterns.
- Inadequate availability—The availability of the different information node will vary because the operating times of different parts of the organization are different.
- Uncorrelated information—Information about the same instance is rarely correlated between the different sources of information. For example, information about a particular person may appear in more than one information node and the information keys used to identify the person are likely to be different in each source.
- Inconsistent information—Information about the same instance is rarely consistent between the different sources of information. For example, information about a particular person may appear in more than one information node and the information values stored could vary between each source.

### Solution Description

Consolidate the information into new information collections (often hosted in a new information node) and then distribute the consolidated information from there.

The new information collections form a hub that is used to synchronize the information. They are often hosted in a new information node because it must be available whenever any of the existing information nodes need it and this is easier to achieve if the hosting node is only managing information. See Figure 4.21. The numbers of the diagram in Figure 4.21 refer to these notes:

1. Some information collections are feeds to the hub. These are master usage information collections and receive no updates to that information from the hub. The hub may treat these values as reference values, or it must be reconciled between any new values that come from these sources and those stored in the hub.
2. Some information collections are synchronized with the hub. New values are exchanged in either direction.
3. Some information collections receive updates from the hub. These values should be treated as reference values in order to have a synchronized information supply chain. Before the hub can be used, it must be loaded with the information that is to be shared between the existing information nodes. This loading process will cleanse, correlate, and consolidate the information together so there is a single consolidated view of the information. Once the single consolidated view of the information is available, the organization may choose to synchronize these values back to the original information nodes. This can potentially create a lot of churn in the original information nodes if the quality of their information is poor. However, the benefit is that all of the information nodes begin with consistent information. Once the hub is operational and any initial information synchronization is complete, a variety of Information Provisioning approaches are used to keep all of the information collections synchronized among the participating information nodes as information is created, retrieved, updated, and deleted. For example,
- Information Services are used to supply information from the hub to information processes on demand. These information processes may be business information processes supporting the organization's work directly or provisioning information processes that are synchronizing information with other information collections.
- Mirroring Provisioning is used to pass new information to the hub from information collections that are just acting as a source of information for the hub.
- Mirroring provisioning is also used to distribute new information to information collections that are only destinations for the hub.
- Peer Provisioning is used to synchronize information both to and from the hub and another information collection. The synchronizing of information between the hub and the other information nodes can be done immediately when a change occurs, or batched up and delivered periodically.

### Solution Example

MCHS Trading introduces an Information Asset Hub called Customer Hub to manage its customer details. See Figure 4.22. This is kept synchronized through Peer Provisioning with the E-Shop application (1). At the same time, the loyalty card for the physical stores is upgraded to cover all channels and support for it is transferred to a new information node called Customer-Care (2). Customer-Care uses the Information Services of the Customer Hub directly to get access to customer details because it needs to access information about all customers irrespective of the channel they use. Any changes to customer details are sent from the Customer Hub to the Reporting Hub (3).

### Benefits

- The hub provides a place to consolidate and correlated distributed information into a canonical form before it is distributed. It provides the means to decouple the sources from the destinations. It also provides a point to run analytics and other monitoring against the information.

### Liabilities

- You have introduced another copy of the information that needs to be managed. As such, it needs an owner who will sponsor ongoing development and maintenance of the hub so that it continues to meet the needs of the destinations.
- As information is distributed from the hub, care must be taken to respect the scope and coverage of the destination information nodes to ensure they are not affected by the availability of more information than they were designed to handle.

### Usage

This pattern is used to synchronize information with a Master Data Management (MDM) hub or operational data store.

### Search Keywords

- Patterns of Information Management
- Information Supply Chain
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Single View Information Supply Chain

### Qualified Name

DesignPattern::Single View Information Supply Chain

### Category

Information Supply Chain Patterns

### Description

Consolidate information into coherent information collections that provide appropriate information services to collectively meet the information requirements.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to process information in order to fulfill its purpose. How is the flow of information coordinated throughout the organization's people and systems?

### Problem Statement

An organization requires a real-time consolidated view of information that is managed through distributed operation and ownership.

A new information process can introduce requirements for a new information collection. The information that belongs in this information collection exists, but is currently located in a multitude of information nodes. How can this information be accessed and correlated to answer real-time information service queries from the information process?

### Problem Example

When a customer calls the MCHS Trading customer care center, the customer service representative needs to understand who the customer is, his or her history of interaction with the organization, and in-flight/recent orders. This information is located in multiple information nodes, including E-Shop, Mail-Shop, Stores, Shipping, and Invoicing.

### Forces

- Real-time access—The information process needs up-to-date information in real time but this information is dispersed among a variety of information collections.
- Information does not meet requirements—The format and consistency of the information in the sources is not necessarily consistent with the requirements of the information process.
- Multiple element types—A consolidated view typically includes multiple types of information elements. The core is often an Information Asset that is linked to multiple types and instances of Information Activities and Information Events, which in turn may link to other types of information assets. Each type of element may be located in a different information collection and they must be retrieved and linked together to support the single view.
- Incompatible availability—The availability of the information sources is not necessarily compatible with the needs of the single view consumers.

### Solution Description

Consolidate information into coherent information collections that provide appropriate information services to collectively meet the information requirements.

The on-demand information supply chain is based around an Information Collection that meets the needs of the consuming information processes. This information collection is implemented with an Information Federation Process that calls information services of a set of information collections that provide the information for the virtual information collection. Some of these information collections are located in existing information nodes and others are created especially to support this information supply chain. These new information collections are synchronized with other existing information nodes using either Mirroring Provisioning or Peer Provisioning. The single view information supply chain is illustrated in Figure 4.23.

The virtual information collection at the root of the information supply chain is labeled (1) and supports the federated views of the information. Behind it are the frontline information nodes (2) that host the information services that collectively support the virtual information collection. They are called each time the top-level information service is called.

These types of information supply chains often need a consolidated view of key Information Assets among the frontline information nodes, which is why you see an Information Asset Hub at position (3).

Downstream information nodes (5) may feed the frontline nodes using Information Flows (4).

Both the frontline and downstream information nodes are still accessed directly (6). The information they see is a partial view of the same information exposed through the single view information supply chain.

### Solution Example

The Customer-Care application creates the complete view of the customer using an information service call to the Customer Hub for the customer's details. See Figure 4.24. Then using the customer's identifier from the customer details, it calls the Order-Tracking application to extract the recent orders for the customer. Then from these order details, it calls the Product Hub to provide more information on the products ordered.

### Benefits

- The information processes using the virtual information collection are reusing information stored in existing information collections.

### Liabilities

- All of the frontline information nodes must be available for the virtual information collection to be available.

### Usage

This approach is used to create consolidated views of customer details for websites and predictive analytics scoring.

### Search Keywords

- Patterns of Information Management
- Information Supply Chain
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Consolidating Information Supply Chain

### Qualified Name

DesignPattern::Consolidating Information Supply Chain

### Category

Information Supply Chain Patterns

### Description

Perform a first pass on the information as close to its source as possible with an aim to cleanse and add context to it. Then pass the results to centralized information collections where information processes can build up the big picture.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to process information in order to fulfill its purpose. How is the flow of information coordinated throughout the organization's people and systems?

### Problem Statement

Information must be provided for centralized control of distributed activity.

### Problem Example

MCHS Trading wants to centrally monitor that its information supply chains are working properly. For example, it wants to know that orders are being fulfilled on time, that product descriptions are correct, and that customer information is up to date. How does MCHS Trading achieve this?

### Forces

- Information has a context—This must be captured and preserved if the information is moved to a new location.

### Solution Description

Perform a first pass on the information as close to its source as possible with an aim to cleanse and add context to it. Then pass the results to centralized information collections where information processes can build up the big picture.

The effect is that the scope of the information collections increases as the information moves further down the information supply chain. See Figure 4.25.

### Solution Example

MCHS Trading set up Information Probes at each of its information nodes to monitor the information processes that contribute to its information supply chains. Each information probe writes the events it detects to a local Information Event Store. Periodically, new events are extracted from the information event store and sent to their central operations console. Events more than 3 days old are removed from the event stores.

This use of a consolidating information supply chain is often time critical. Its aim is to gather information from a wide range of sources and consolidate them into a central location where the values can be processed in near-real-time, while also allowing historical analysis of the information. See Figure 4.26.

### Benefits

- This type of information supply chain efficiently collates and consolidates information from information collections that are distributed throughout an organization's information nodes.

### Liabilities

- The process of collating and consolidating the information may introduce a delay before the information is analyzed. Where events need to be evaluated within minutes, it may be better to use a Single View Information Supply Chain.

### Usage

Consolidating information supply chains are used to support centralized monitoring solutions where information is captured in highly dispersed locations and then consolidated into a central monitoring point. It is sometimes referred to as a fan-in style of integration. The way that events are moved through the information supply chain is sometimes referred to as store and forward.

### Search Keywords

- Patterns of Information Management
- Information Supply Chain
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Hierarchical Information Supply Chain

### Qualified Name

DesignPattern::Hierarchical Information Supply Chain

### Category

Information Supply Chain Patterns

### Description

Design a multiway synchronization where each information node flows changes to the values it masters to the other information nodes that maintain a reference copy.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to process information in order to fulfill its purpose. How is the flow of information coordinated throughout the organization's people and systems?

### Problem Statement

Information must be exchanged between centralized and decentralized parts of an organization.

### Problem Example

MCHS Trading has a Shipping application for controlling the delivery of orders to customers and stores. Goods are distributed from three physical warehouses. Each warehouse runs a stock control system. How is information about product details and stock coordinated between these four systems?

### Forces

- Shared ownership—The ownership of information is shared between the information nodes, although each maintains its own copy.

### Solution Description

Design a multiway synchronization where each information node flows changes to the values it masters to the other information nodes that maintain a reference copy.

The hierarchical information supply chain uses information collections with Hybrid Usage. The strategy is that for each value, there is only one information node that is responsible for updating it (Master Usage), while the others read it (Reference Usage).

Figure 4.27 illustrates the pattern.

The numbers on the diagram in Figure 4.27 refer to these notes:

1. The hierarchical information supply chain is split into two levels: the top-level node and then subordinate nodes.
2. When information changes in one level, it is made available to the other level. In the diagram, this is shown using mirroring provisioning, which will copy the information from one level to another. An alternative is to use Virtual Information Collections that use Information Services to exchange information as it is requested. This pattern can repeat through additional levels, but it can get increasingly hard to apportion ownership of the information values, as the tree gets deeper.

### Solution Example

The Shipping and stock management systems each have a stock information collection that has Hybrid Usage. The Shipping application is the owner of the product attributes within these collections, and the stock management systems own the stock level. This is shown in Figure 4.28. The numbers on the diagram Figure 4.28 refer to these notes:

1. When product details change, they are updated in the Shipping collection and then the new values are copied into the stock management system's information collection where they have reference usage.
2. When one of the warehouses ships a package to a customer, its local stock level is reduced. This change is not relevant to any of the other stock management systems, but it does need to be reflected in Shipping. MCHS Trading had two choices to do this: either to use Mirroring Provisioning to sent the new value from the stock management system to Shipping, or to use a Remote Information Service call from Shipping to retrieve the latest values whenever they are needed. MCHS Trading opted to use the information service call approach because the stock values were changing much more frequently than the Shipping application queried the values.

### Benefits

- This pattern establishes clear ownership rules that lead to a simple synchronization approach.

### Liabilities

- There is no synchronization between the leaf nodes.

### Usage

This type of information supply chain is useful for providing a headquarters view of decentralized operations. Here is an example for customer details. The company chooses which level that they will introduce all new customers at and how the ownership of attributes is distributed. See Figure 4.29. The numbers on the diagram Figure 4.29 refer to these notes:

1. Introducing customers at the headquarters level ensures a single consistent view of the customer across the organization, and simplifies the centralized coordination when details of a new customer must be checked to ensure they meet any regulatory criteria. For example, under anti-money laundering (AML) legislation banks must validate the identity of a person opening a new account.
2. Introducing customers in the decentralized parts of the organization means that only the headquarters view sees the consolidated view of the customer (they would need to use a Hub Interchange Information Supply Chain to achieve that).

### Search Keywords

- Patterns of Information Management
- Information Supply Chain
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Peer Exchange Information Supply Chain

### Qualified Name

DesignPattern::Peer Exchange Information Supply Chain

### Category

Information Supply Chain Patterns

### Description

Each organization is responsible for broadcasting all changes to its peers, who are then responsible for incorporating these changes in their information collections.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 4, "Information Architecture".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization needs to process information in order to fulfill its purpose. How is the flow of information coordinated throughout the organization's people and systems?

### Problem Statement

Independently operating organizations need to share information among one another.

In this scenario, there is no centralized group to support a hub to coordinate the synchronization of information (compare this with the Hub Interchange Information Supply Chain). Each organization needs to be able to update the information and for these changes to be available to all other organizations as soon as possible.

### Problem Example

MCHS Trading has a number of physical stores (shops). Customers sometimes visit one store and ask for information about other stores in different areas. How do the stores keep each other informed of local news for each store, such as opening hours, location, related amenities, holiday cover, staff opportunities, and rotations?

### Forces

- Disparate copies—Information that is duplicated across multiple systems is often stored in different formats with different validation rules and currency.

### Solution Description

Each organization is responsible for broadcasting all changes to its peers, who are then responsible for incorporating these changes in their information collections.

This could be achieved with an Information Broadcast Process running in a Queue Manager. The peers in the exchange would have to agree to a canonical format that information payloads would follow and be responsible for translating between their internal format and the canonical format.

Figure 4.30 illustrates the peer exchange information supply chain.

### Solution Example

The MCHS Trading stores each have a local information node where they can maintain information about the local store. When this information is changed, it is broadcast to the other stores.

### Benefits

- No centrally funded hub is required.
- Each source system has its own copy of the information and so can continue operating even if the network or one of the peer systems is unavailable.

### Liabilities

- As the number of peers increases, the number of information exchanges increases. This can become expensive as the formats and information standards are likely to be different, too.
- The peers in the exchange need to operate in total trust that all information is being shared and that it is only being used for the intended purposes.
- Any change to information—particularly creates and updates—are made independently by each peer and then replicated to the other peers. This process creates possibilities that changes are made (creates, updates, and deletes) simultaneously in different peers that need to be reconciled. If the peers are operating with different scopes of instances, then the reconciliation process is more complex because a create operation or delete operation in one peer may need to be translated to an update operation in another.

### Usage

This type of information supply chain occurs where there is clear ownership of resources so that incompatible simultaneous updates in different peers do not occur.

An example of this is in the synchronization of domain name system (DNS) servers for the Internet. There are few examples of this pattern in business systems.

### Search Keywords

- Patterns of Information Management
- Information Supply Chain
- Information Architecture

### Version Identifier

1.0

### Status

ACTIVE

____

