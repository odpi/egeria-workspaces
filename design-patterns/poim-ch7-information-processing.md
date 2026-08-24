<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**Information Processing**

Dr.Egeria commands for the design patterns in Chapter 7, "Information Processing", of *Patterns of
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

Information Trigger

### Qualified Name

DesignPattern::Information Trigger

### Category

Information Trigger Patterns

### Description

When the event is detected, trigger a mechanism that is able to request the initiation of the information process on an appropriate information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information processes support the activities of the organization. These activities are triggered when particular events occur.

### Problem Statement

An information process must be started when a particular event occurs.

Events may occur both inside and outside of an organization, and be detected by a person or technology such as a sensor. When an event is significant to an organization, it is typical to create an instance of an information process to manage the response to the event. How is this information process started?

### Problem Example

When MCHS Trading receives a payment for an order, it must be processed to ensure the organization receives the money.

### Forces

- An event occurs in a context. This context defines the specific information that is relevant to the activity. This context must be captured and passed to the information process.

### Solution Description

When the event is detected, trigger a mechanism that is able to request the initiation of the information process on an appropriate information node.

This mechanism is called an information trigger. It is responsible for monitoring for a particular type of event, capturing details of the event, and the context in which it occurred, into an Information Event structure and initiating a new instance of an appropriate information process. The information event is used to pass the context onto the information process as the information process starts up. This is shown in Figure 7.2. The numbers on the diagram in Figure 7.2 refer to these notes:

1. The information trigger detects the event.
2. The information trigger gathers information about the event into an information event structure.
3. The information trigger initiates the information process and passes the information event to it.

### Solution Example

When a payment is received, a Process Payment information process is started in the Invoicing application. The information event it is passed contains details of the order that the payment is for, and how much it covers.

### Benefits

- Information triggers provide well-defined mechanisms for capturing events and initiating new processes. Recording the associated information event defines why the processing was initiated. This is the responsibility of an Information Probe.

### Liabilities

- Information triggers react to events that are often happening outside the control of the organization. In unusual circumstances, there may be a sudden increase in the number of events. This results in an unusually high number of information process instances being started, which in turn can cause other resources to become overwhelmed. It is good practice to ensure that there is enough spare capacity available to handle reasonable peaks in the number of events being processed and contingency to handle unexpected high loads. For example, thresholds could ensure the triggers will throttle back on the number of processes created during peak loads and complete the deferred activity once the peak subsides.

### Usage

IT systems are essentially passive. They need to be triggered by "something" happening for processing to start. This triggering is an example of an information trigger. There are many types of implementations of information triggers from buttons on user interface menus to command lines, environmental sensors, triggers in databases, timers, and many more. The other patterns in this pattern group cover further examples.

### Search Keywords

- Patterns of Information Management
- Information Trigger
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Manual Information Trigger

### Qualified Name

DesignPattern::Manual Information Trigger

### Category

Information Trigger Patterns

### Description

Provide a command line or user interface to enable an Information User to initiate the information process.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information Processes support the activities of the organization. These activities are triggered when particular events occur. Events may occur both inside and outside of an organization, and be detected by a person or technology such as a sensor. When an event is significant to an organization, it is typical to create an information process to manage the response to the event.

### Problem Statement

There is no simple way to automatically detect the event and trigger the appropriate information process.

This is often the case where the event is initiated outside the control of the organization.

### Problem Example

A customer phones the MCHS Trading call center to notify the company that she has changed her address.

### Forces

- People initiate processes—An information process needs to be started at an appropriate time, on the right Information Node, and must be passed the appropriate context in an Information Event.
- Volume of events may overwhelm individuals—People can only process so many items in a given span of time.
- Insufficient information—There may not be sufficient information for an individual to trigger a process. This may be due to lack of training, misunderstanding of the content, issues with timing of information delivery, or other factors. This can result in significant process delays.

### Solution Description

Provide a command line or user interface to enable an Information User to initiate the information process.

The information user must manually enter the description of the event to provide the context for the information process. This is shown in Figure 7.3.

### Solution Example

The customer service representative clicks on a menu option on his or her user interface to invoke the Change of Customer Address information process. This guides him or her through a series of steps to validate the identity of the customer and update the address if appropriate.

### Benefits

- This pattern is effective at handling ad hoc activities—particularly those driven by events coming from outside of the organization.

### Liabilities

- The manual information trigger needs to have appropriate Information Guards protecting it to ensure only authorized and appropriate information processes are started up.

### Usage

Manual information triggers are typically implemented via user interfaces (menus, buttons, mouse clicks, or similar prompts) or via operating system scripts or commands. The user interface may request additional information before creating the information process. This is passed to the information process in the information event.

### Search Keywords

- Patterns of Information Management
- Information Trigger
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Scheduled Information Trigger

### Qualified Name

DesignPattern::Scheduled Information Trigger

### Category

Information Trigger Patterns

### Description

S P Use a Chedulingrocess to initiate the information process at the required time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information processes support the activities of the organization. These activities are triggered when particular events occur. Events may occur both inside and outside of an organization, and be detected by a person or technology such as a sensor. When an event is significant to an organization, it is typical to create an information process to manage the response to the event.

### Problem Statement

An information process needs to run to a regular timetable—such as once an hour.

### Problem Example

The orders made by MCHS Trading's outlet stores are accumulated in the Stores application. At the end of the trading day, they must be transmitted to the Shipping application for processing.

### Forces

- People are not always present—People cannot be relied on to always perform an activity to a fixed timetable because they may be distracted by other work. Therefore, the triggering mechanism for this problem must be automated.
- Expected conditions must be met—Information processes are implemented using particular assumptions on the location and state of the information they are working with. If these conditions are not met, the information process may appear to execute successfully but produce incorrect results.
- Volume may exceed processing capacity—When a process is triggered, if it lacks the capacity to complete its task before the next trigger occurs, there may be significant processing issues (e.g., contention for resources, locking of information collections).

### Solution Description

Use a Scheduling Process to initiate the information process at the required time.

Information may be passed to the scheduling process when the information trigger is set up. This is added to the Information Event created by the scheduling process when it triggers the new information process. See Figure 7.4. The numbers on the diagram refer to these notes:

1. An information user or an information process sets up the schedule for the triggering mechanism in a scheduling process.
2. Whenever the schedule requires it, the scheduling process creates a timer event and passes it to the information trigger to initiate the appropriate information process.

### Solution Example

The Stores application accumulates orders into an Information Collection hosted in a Staging Area during each trading day. There is an Information Process that is scheduled to run each evening that moves the orders to the Shipping application.

### Benefits

- This pattern automates the initialization of regular processing.

### Liabilities

- The scheduled information process is started independently of all other activity in the information nodes. It must be written defensively to validate that any processing that should have run before it has happened. Otherwise, it may fail to produce the correct results because, for example, the information that it should process has not been copied in the information collection it uses.

### Usage

Scheduling information processes is a common practice in information provisioning where a batch of information must be transmitted at regular intervals. The information to send is accumulated in an information collection and the scheduled information process retrieves the information and moves it to the required destination.

### Search Keywords

- Patterns of Information Management
- Information Trigger
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Service Trigger

### Qualified Name

DesignPattern::Information Service Trigger

### Category

Information Trigger Patterns

### Description

Trigger a local information process to use a Remote Information Service to call the appropriate information trigger in the remote information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information processes support the activities of the organization. These activities are triggered when particular events occur. Events may occur both inside and outside of an organization, and be detected by a person or technology such as a sensor. When an event is significant to an organization, it is typical to create an information process to manage the response to the event.

### Problem Statement

An information process needs to be triggered on a remote information node.

This situation arises when the event is detected on a different information node to where it will be processed.

### Problem Example

The New Product Introduction information process running in MCHS Trading's Product Hub application needs to distribute new product details to the order-processing application once they have been approved.

### Forces

- Changes to the location of information—The most appropriate information node to host the information process may change over time. It is a balance between placing the information process close to the information it uses, while ensuring the information node it is hosted on has both the functionality and the capacity to support it.
- Availability of remote information nodes—Changes in the availability of information nodes impacts triggering and delivery of information.
- Volume of requests may exceed processing capacity—When a process is triggered, if the information node lacks the capacity to support the volume of triggered requests, there may be significant processing issues (e.g., contention for resources, locking of information collections, delays in information delivery).

### Solution Description

Trigger a local information process to use a Remote Information Service to call the appropriate information trigger in the remote information node.

See Figure 7.5. The numbers on the diagram refer to these notes:

1. The remote information service is called.
2. It creates an Information Payload to hold the parameters passed to it and calls an Information Request to invoke a Triggering Information Service. The specific information request may be:
- Event Information Request—When the caller does not know which process to initiate, so the decision is delegated to the triggering information service.
- Run Process Information Request—When a specific information process is to be called and the caller will wait for the process to complete in order to get its results. This is for short-running information processes that have no user interaction.
- Initiate Process Information Request—When a specific process is to be started and the caller just needs an acknowledgment that it has started successfully.
3. The triggering information service creates an Information Event from the information payload and initiates the appropriate information process, passing the event. It creates a response to the information request and returns it to the caller.

### Solution Example

When the New Product Introduction information process detects that some product details have been approved, it calls a remote information service to trigger the Distribute Product Details information process in an Information Broker. This is a type of Information Deployment Process that is the initial information process in the Partitioned Distribution information flow.

### Benefits

- This pattern allows information processes to be initiated on remote information nodes. The remote information service owns the decision on which information node to host the information process. It could be using a static implementation, or a dynamic lookup to locate the target information node. It also introduces the flexibility to explicitly request a particular process, or delegate the selection of the information process to the target information node.

### Liabilities

- If the remote information node is not running, the request to run the process may be lost without special coding in the calling information node.

### Usage

This approach is used in workload management systems to distribute work across a number of information nodes. It is also used in Service-Oriented Integration (SOI) to request that information processes are run by remote systems.

### Search Keywords

- Patterns of Information Management
- Information Trigger
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Change Trigger

### Qualified Name

DesignPattern::Information Change Trigger

### Category

Information Trigger Patterns

### Description

Set up a monitoring mechanism to watch for the change in information. Trigger the appropriate information process as required.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information processes support the activities of the organization. These activities are triggered when particular events occur. Events may occur both inside and outside of an organization, and be detected by a person or technology such as a sensor. When an event is significant to an organization, it is typical to create an information process to manage the response to the event.

### Problem Statement

An information process needs to be started whenever information arrives at a certain location, is accessed, is changed, or is removed.

### Problem Example

Whenever new product details are available for the E-Shop application, they are posted in an Information Collection located in a Staging Area. They need to be transformed and loaded into E-Shop's internal product details information collection as soon as they are available.

### Forces

- Multiple sources of change—There may be many information processes that are updating the same information. This can result in many events that could be processed by a single information process.
- Volume of change—The number of changes occurring against a particular piece of information may hamper response if processing capacity is insufficient or may obscure what changes have occurred.

### Solution Description

Set up a monitoring mechanism to watch for the change in information. Trigger the appropriate information process as required.

The Information Event that is passed to the triggered information process describes the nature of the change to the information. See Figure 7.6.

### Solution Example

New product details are created by the Product Hub application. When they are approved, the Distribute Product Details information process copies the product details into the information collection in the staging area.

### Benefits

- With this pattern, every change to the information collection results in an information trigger—irrespective of the information process that made the change.

### Liabilities

- The context information passed to the triggered information process can be pretty limited because there is no knowledge of the business reason for the information change at this level of the architecture.

### Usage

Database triggers follow this pattern, as do operating system processes that are triggered when files change.

Often, when the triggering mechanism runs in a database, the work to trigger the information process runs under the same transaction as the work to make the change to the information. The positive effect of this approach is that if the change is rolled back, the new information process is not triggered. The downside is that it can slow down the information process making the original update.

### Search Keywords

- Patterns of Information Management
- Information Trigger
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

External Sensor Trigger

### Qualified Name

DesignPattern::External Sensor Trigger

### Category

Information Trigger Patterns

### Description

The sensor's data is packaged into an information event and passed to an appropriate information process.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information processes support the activities of the organization. These activities are triggered when particular events occur. Events may occur both inside and outside of an organization, and be detected by a person or technology such as a sensor. When an event is significant to an organization, it is typical to create an information process to manage the response to the event.

### Problem Statement

A sensor has detected an event, or made a measurement that needs to be processed.

How is this processing initiated (bearing in mind that there will probably be many sensors and/or many measurements coming from an individual sensor)?

### Problem Example

The warehouses have sensors on its exits that detect the movement of particular goods that either have very high value or require regulatory control. These sensors detect the RFID tag stuck to these types of goods and record which goods left a particular exit and when this occurred. This information must be checked to ensure the movement of these goods is authorized. The check has to be made immediately so the truck containing the goods can pass through the final security gate.

### Forces

- Large volumes of information—Sensors can generate a huge amount of information—particularly in moments of crisis, or when unusual situations arise. When this happens, the events need to be triaged very quickly to ensure the most important events are processed first.
- All events look the same—The events produced by sensors are undistinguished until an Information Process organizes and distinguishes them.

### Solution Description

The sensor's data is packaged into an information event and passed to an appropriate information process.

The sensor is part of a small processor that is connected to the network. It takes a reading and then sends the data to a collection point. The collection point triggers the information process when the reading is received. See Figure 7.7.

### Solution Example

The sensors in the warehouse doors trigger an information process that checks the RFID tag data against orders that are due for dispatch.

### Benefits

- Using external sensors can improve the reaction time of the organization to external events.

### Liabilities

- External sensor triggers must be able to handle sudden peaks of events appropriately, ensuring the most important are processed first.

### Usage

Examples of external sensors include RFID tag sensors, audio and video monitoring, liquid levels, digital metering, bar code sensors, and infrared beams. In general, the price of these sensors is reducing, along with their associated tags. In addition, the price of hardware to process the information generated from these sensors is also reducing, making it affordable for many organizations to collect information from the environment. The result is that external sensor triggers and the related processing are becoming more common.

### Search Keywords

- Patterns of Information Management
- Information Trigger
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Process

### Qualified Name

DesignPattern::Information Process

### Category

Information Process Patterns

### Description

Formally define and implement the processing for that activity and host it in an information node. Ensure this processing has access to the information it needs.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization performs activities to fulfill its purpose.

### Problem Statement

An organization has to process information to support one of its activities.

This processing involves the retrieval, creation, updating, and deleting of information.

### Problem Example

MCHS Trading needs to maintain a product catalogue. This involves the following:

- Introducing new products, including assessing the market need, describing the product for the catalog, finding suitable suppliers, and deciding on the price
- Retiring products that are either not popular or are no longer manufactured
- Reviewing pricing and defining special offers
- Improving product descriptions

### Forces

- Activities are complicated by the real world—The activities of a business are often complicated by the inconsistencies in the organization and the world beyond.
- An activity may involve contributions from multiple people.
- An activity may involve complex or specialized processing.
- An activity takes time (minutes, days, weeks, or years)—Any IT infrastructure supporting the activity may fail, or be replaced or upgraded during the lifetime of an activity.

### Solution Description

Formally define and implement the processing for that activity and host it in an information node. Ensure this processing has access to the information it needs.

The implementation of the processing for such an activity is called an information process. An information process is made up of a number of logical steps. There may be decisions, calculations, or loops in the process, but there will always be a well-defined starting point and one or more ending points.

Often the behavior of an information process is described using a flowchart, use case model, or other diagram that shows the steps and decision points. These flowcharts or diagrams can be used simply as a documented description of the information process, or, as in the case of an Agile Business Process, form part of the information process's implementation itself. See Figure 7.8.

Information is made available to an information process via a number of routes, as shown in Figure 7.9. An information process is started by an Information Trigger. The trigger may pass the information process some information to give it some context for its work. This information is in the form of an Information Event. An information process may return some information values to the trigger once it is completed.

The information process may both obtain and produce additional information. Specifically, an information process may receive a supply of information either from users interacting directly with it, or from stored information. Stored information is available to the information process through the Information Services.

The Information Provisioning pattern provides more detail on the working of these mechanisms.

An information process works with all types of information (called Information Elements). For example, it maintains its in-memory working variable in an Information Processing Variables element. It creates an Information Activity to store details of the work it is performing. This information activity serves as a permanent record of the work performed by the information process.

The information process will also use Information Assets during its processing. Often, the relevant information assets will be referred to in the information record. For example, customer details may be referred to in an order record. This linking provides valuable business context to the information record, enabling the organization to understand who or what is involved in the most valuable work going on in the organization.

### Solution Example

In the case of MCHS Trading's product catalog, the bulleted activities are each implemented as a different information process in the Product Hub application. More details for this example are shown in the specialized pattern Collaborative Editing Process.

### Benefits

- Information processes provide repeatable capability. They organize the work between people and provide a record of the work of the organization and help to normalize many aspects of the work.

### Liabilities

- Because the behavior of an information process is hard-coded, it can be expensive to change. The business process implementation must be flexible enough to handle the unusual cases.

### Usage

Information processes provide the core IT capabilities for an organization. There are many implementation approaches from direct coding to model-driven processes and declarative systems. There are more detailed descriptions of implementation approaches in the more specific information processes that follow.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Bespoke Application Process

### Qualified Name

DesignPattern::Bespoke Application Process

### Category

Information Process Patterns

### Description

Implement the information process using an in-house or consultant team ensuring it meets the needs of the organization.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an Information Process to support one of its activities.

### Problem Statement

An information process needs highly specialized behavior to support an activity in an organization.

In many large organizations, it is necessary to divide the teams into autonomous groups and provide IT services to them that are specialized to their needs. Some of these teams need bespoke function for areas that are critical to its success, particularly if it gives them a competitive advantage or it is supporting fast-changing regulations or business environment.

### Problem Example

When MCHS Trading was first started, the organization needed an application to manage the orders coming in from its clients, either via the telephone or mail order. This order processing was central to the business and, the organization believed this had to be specially tailored to its needs.

### Forces

- Many organizations believe they are special and unique—This leads to the internal development of more function than is strictly necessary.
- Applications affect behavior—The way an application is implemented will have a profound influence on the way the organization operates around it. It is often hard to separate those operational aspects that are dictated by the existing applications and those that are requirements of the organization's business.
- Workarounds are common—Where an application does not completely meet the needs of an organization, the people using it find ways to work around it. This can involve putting information into attributes designed for different purposes, or changing values in files/databases after the application has finished processing. Often this creates inconsistencies in recording the current state of processing.

### Solution Description

Implement the information process using an in-house or consultant team ensuring it meets the needs of the organization.

Such bespoke information processes are typically self-contained, running in their own information node with their own user interfaces and all of the information they use managed in local information collections. They are often implemented and maintained by in-house staff.

Change to these applications happens slowly because it is costly to the organization. However, provided the IT team has retained the source code and appropriate documentation, the behavior of the information processes it supports is both understood and can be changed to meet new business needs.

### Solution Example

MCHS Trading implemented its own Mail-Shop application to take orders from customers received either though the post (mail), or through the call center. This application is efficient at entering new orders. It requires the customer details to be entered for each order and does not keep a history of an individual's orders longer than a month.

### Benefits

- The information process is tailored to the needs of the organization.

### Liabilities

- Creating software may not be the core competency of the organization and so these applications may not be best-of-breed.

### Usage

This pattern represents the many types of business application built by organizations to support their business.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Packaged Application Process

### Qualified Name

DesignPattern::Packaged Application Process

### Category

Information Process Patterns

### Description

Buy a software package to support the information process. This will either come as a standalone application or a software library that needs to be integrated into an application.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an Information Process to support one of its activities.

### Problem Statement

All or part of an information process is too expensive or too complex for the organization to implement.

### Problem Example

When MCHS Trading wanted to create an Internet-based shop, it had no in-house experience with web technology. They needed a professional website that was secure and easy to use.

### Forces

- Many organizations believe they are special and unique—This leads to the internal development of more function than is strictly necessary.
- Applications affect behavior—The way an application is implemented will have a profound influence on the way the organization operates around it. It is often hard to separate those operational aspects that are dictated by the existing applications and those that are requirements of the organization's business.
- Workarounds are common—Where an application does not completely meet the needs of an organization, the people using it find ways to work around it. This can involve putting information into attributes designed for different purposes, or changing values in files/databases after the application has finished processing. Often this creates inconsistencies in recording the current state of processing.

### Solution Description

Buy a software package to support the business process.

This will either come as a standalone application or a software library that needs to be integrated into an application.

### Solution Example

MCHS Trading bought a specialist e-commerce package that was used to create the E-Shop application. This software provided the catalog web pages for browsing and selecting goods, a shopping basket, secure customer account, and management of payment details. This package also offered an external interface for loading product information and working with the customer and order data.

### Benefits

- Specialized expertise is encoded in the function of the package that would be too expensive for the organization to write itself. This is particularly valuable if the subject area is evolving rapidly and is not part of the organization's differentiating or core capability.

### Liabilities

- The function, and to some extent, the information, within a packaged application is opaque to the organization. When changes are needed, the organization will typically need the help of the package supplier. Also a package imposes a business operations model on the organization. It is typically most cost effective to adopt the package's assumed business operations model rather than modify the package to the organization's existing model.

### Usage

Packaged applications are used extensively in the IT industry today. They are often called "Custom off-the-shelf" (COTS) packages.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Agile Business Process

### Qualified Name

DesignPattern::Agile Business Process

### Category

Information Process Patterns

### Description

Implement the information process in a workflow engine that is interpreting a business process model. The model can be updated as the business changes and redeployed to the workflow engine.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an Information Process to support one of its activities.

### Problem Statement

An information process needs to be regularly updated to meet the changing needs of the business.

### Problem Example

MCHS Trading wants to improve its customer service. It is aware that its customers want more information and control over the progress of their orders. However, the precise details of the capabilities that its customers will appreciate are still a little hazy. MCHS Trading is looking for an approach that will allow it to experiment with new features without incurring too much cost.

### Forces

- Many organizations believe they are special and unique—This leads to the internal development of more function than is strictly necessary.
- Applications affect behavior—The way an application is implemented will have a profound influence on the way the organization operates around it. It is often hard to separate those operational aspects that are dictated by the existing applications and those that are requirements of the organization's business.
- Workarounds are common—Where an application does not completely meet the needs of an organization, the people using it find ways to work around it. This can involve putting information into attributes designed for different purposes, or changing values in files/databases after the application has finished processing. Often this creates inconsistencies in recording the current state of processing.

### Solution Description

Implement the information process in a workflow engine that is interpreting a business process model. The model can be updated as the business changes and redeployed to the workflow engine.

A business process model describes the steps and decisions that implement the required behavior. Each step is implemented by a web service or local procedure. Some steps may involve displaying user interface screens to selected people to provide information or review a proposed change.

### Solution Example

MCHS Trading introduces a new application called Customer-Care that is implemented with a workflow engine. The workflow engine runs a number of agile business processes that implement the new customer service capability.

Figure 7.10 shows a sample process definition for canceling an order.

The agile business process makes calls to the other applications to find out the status of the order and cancel the order if necessary. This includes a new application called Order-Tracking (which contains a State Driven Process that monitors the state of the orders as they flow between the applications). The Shipping application is responsible for actually canceling the order. This cancellation request may arrive before the original order arrives, in which case the cancel request is stored and matched with the order request when it arrives.

### Benefits

- Using business process modeling enables the organization to review how the information process will behave. Some business people may even be involved in the creation of the definition. When the business needs change, the model can be changed and redeployed.

### Liabilities

- An agile business process may run slower than a hard-coded one. These types of processes also work with information from remote information nodes. The information collections and information processes that originally supported it need to be checked to make sure the new use case introduced by the agile business process is not going to impact the existing operation.

### Usage

Workflow and business process management engines support this pattern. The business process flows are typically models in BPMN2.0 or UML.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

State Driven Process

### Qualified Name

DesignPattern::State Driven Process

### Category

Information Process Patterns

### Description

Create a state machine that defines the behavior of the information process for each event it has to react to.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an Information Process to support one of its activities.

### Problem Statement

An information process must be driven by events in other information processes.

This information process is passive, dependent on the calling information processes to pass it information. It is responsible for reacting to the events as they arrive.

### Problem Example

MCHS Trading would like to maintain the current state of each order as the orders pass between the applications. This information is not currently maintained by any of the applications. It is implicit in how far the order record has progress through the applications.

### Forces

- No activity may be a problem—If an information process fails, it may not send an event to the state driven process.
- The correct action to take may depend on what has occurred in the past—For example, if a business transaction is canceled, then the work to undo what has been done so far will depend on how far the processing had reached.
- The order in which events occur may vary in a distributed environment—When work is split between information nodes, it is sometimes hard to be sure of the exact sequence of activity.

### Solution Description

Create a state machine that defines the behavior of the information process for each event it has to react to.

The state driven process is responsible for maintaining a state value. This is stored as an attribute in an information entry within an information collection.

Typically, an information service is called to trigger the state driven process. This service passes the process an Information Event and the Information Key for the state machine. The information key is used to retrieve the information entry with the current state attribute in it. The event and the current state are fed into the state machine to determine the new current state. The new current state is saved into the information entry and returned to the caller.

Extensions to this can include the following:

- Calls to the state driven process are scheduled to check that it has not been in the same state too long. If no state change has occurred since the last time check, then an alert is raised. If the state change occurred, then the time check is ignored.
- The state driven process may invoke information services to save data or to initiate another information process when a particular state change, or state, occurs.
- The events may be logged in an information collection for future reference—particularly auditing or troubleshooting.
- Additional information in the information events, such as links to related information activities and information assets, can be added to the information entry. This is useful for events that can occur at any time prior to a certain state transition.

### Solution Example

MCHS Trading introduced a new application called Order-Tracking that manages the state of all orders as they pass through other applications. The other applications use specific information services available from Order-Tracking to pass information events as they occur.

Figure 7.11 shows the state machine. The labels on the arcs (such as Payment Made, Order Canceled, etc.) represent the types of events that the state driven process can receive. The ellipses represent the state of the order. There are a couple of interesting points to notice:

- The state machine restricts when certain events are permitted. For example, Order Canceled is only permitted if the current state is Active Order or Delayed Order.
- Payment Received can occur in many states, and does not cause a state change. The Payment Received event includes the amount received. The state driven process is accumulating the payments and will not transition to Completed Order until the payments match the order value.

### Benefits

- Consolidation of state changes increases the consistency and reliability of applications that must make decisions based on the state of the information. Changes to the behavior of specific states can be consolidated, reducing the management cost.

### Liabilities

- The number of states in the state machine can become large if events can happen in a nondeterministic order. One way to combat this is to supplement the state value stored in the local information collection with additional information that is received in the events that count occurrences, record activity, and point to related Information Activities and Information Assets.

### Usage

State machines are particularly useful when monitoring Daisy Chain Provisioning, or for case management systems where a case has to pass through particular states to be resolved.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Collaborative Editing Process

### Qualified Name

DesignPattern::Collaborative Editing Process

### Category

Information Process Patterns

### Description

Define an information process that coordinates the collection of the information values from the relevant individuals and then stores the combined results in an information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an Information Process to support one of its activities.

### Problem Statement

Introduction of a new entry in an information collection needs values from a variety of individuals.

These individuals may be from different parts of the organization and have different skill sets and vocabularies. This requirement is common when either introducing or making significant changes to instances of Information Assets—for example, products, employees, suppliers, or a new account for a customer.

### Problem Example

Introducing a new product into the MCHS Trading catalog requires a market to be identified, suppliers to be identified and contacted, pricing and advertising to be worked out, relevant regulatory provision to be enabled, and entries to be coordinated into the information collections that require the product details.

### Forces

- The way an application is implemented will have a profound influence on the way the organization operates around it—It is often hard to separate those operational aspects that are dictated by the existing applications and those that are requirements of the organization's business. This can make it hard to change the implementation of information processes, particularly when previously independent teams need to coordinate their activities.
- Information growth requires new approaches—Increasing volumes of information can dramatically impact the ability to process information through human interaction points.

### Solution Description

Define a business process that coordinates the collection of the information values from the relevant individuals and then stores the combined results in an information collection.

Each step in the process creates a task for an individual to provide the information values he or she is responsible for, or to approve information values that have already been provided. As the process progresses, more of the attributes in the new information entry are filled in and approved.

With this approach, people from different teams are able to contribute and control the subset of the attributes that are relevant to their work. Behind the scenes, the information is assembled, validated, and consolidated into one or more information entries in one or more information collections.

### Solution Example

The Product Hub information processing for adding a new product is an automated business process that assigns and coordinates the work of the teams involved.

Figure 7.12 shows the steps involved. For each product to be defined, the Product Hub application assigns a task to an appropriate individual to supply information or approve some of the information that has already been provided.

### Benefits

- This pattern coordinates the collection of new information values for an information entry from independent teams, along with the necessary approval cycles, while automating validation and distribution of the resulting information entry to one or more information collections. The result is coherent information capture. It enables the creation of shared information collections with broader coverage in organizations where the independent teams would naturally elect to have private information collections.

### Liabilities

- The collaborative editing process must take into account that people have vacations, sick leave, and change jobs. It must enable the reallocation and delegation of work when individuals are not available so that work is not halted when someone is absent.

### Usage

Most common are business processes that incorporate human input, editing, and review around the creation of new entities. These are sometimes called human-centric workflows. Examples include the introduction of new products as shown in the example, the introduction of new employees, the creation of a new account for a customer, or the tracking and update of customer service calls.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Reporting Process

### Qualified Name

DesignPattern::Information Reporting Process

### Category

Information Process Patterns

### Description

Use a variety of visualization approaches to display the information so that the information users can understand the trends, exceptions, and relationships in the information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an Information Process to support one of its activities.

### Problem Statement

The business needs reports that present information on past performance and possible projected performance.

### Problem Example

When management at MCHS Trading wanted to get more insight into the trends in customer purchases across specific demographics and geographies, it found that the reporting within its existing applications was not sufficient to provide this view and custom programming to collect the diverse information did not provide timely or consistent reporting.

### Forces

- Information growth requires new approaches—Increasing volumes of information can dramatically impact the amount of resources and time required to process it.
- Servicing requests for information takes processing effort—Additional queries on an information collection will add load to its information node.
- Remote requests for information have greater latency than local requests— Retrieving information from a remote system each time you need to include it introduces a delay and puts extra load on the system hosting the information.
- Additional copies of information add cost—Copying information so it is local to the processing reduces latency in retrieving information but takes additional storage and adds a requirement to synchronize the copies.
- Variety of formats—Information is not stored in the same format in every information node.

### Solution Description

Use a variety of visualization approaches to display the information so that the information users can understand the trends, exceptions, and relationships in the information.

The information reporting process is responsible for the effective display of complex sets of information. It must support a variety of visualization techniques to allow a person to review the information from different perspectives and levels of detail.

An industry model can define a best-practice structure for consolidating information from multiple information supply chains to support a particular report. Information elements from the differing supply chains can be deployed, replicated, or federated into the modeled structure at detailed and summarized levels to support and optimize reporting queries and dashboards.

### Solution Example

MCHS Trading introduces a new information node called Decision-Center that supports specialized information reporting processes to generate and display standardized daily, weekly, monthly, and annual reports, as well as dashboard views for management. The Decision-Center is provisioned with information from the Reporting Hub. This is a Historical System Of Record solution where customer, product, orders and sales, shipping, and inventory information are collected and synchronized.

### Benefits

- Consolidated and consistent views across multiple information supply chains can be established, providing greater insight into business results.

### Liabilities

- An information reporting process is likely to require additional information collections to be established with the associated costs.
- The quality of the reports and dashboards produced by this process is only as good as the information supply chains provisioning it.

### Usage

Information reporting processes are found in applications and in business intelligence and reporting packages. They are able to visualize information in many different ways. Examples of visualizations can be found at http://www-958.ibm.com/software/data/cognos/manyeyes/page/ Visualization_Options.html.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Profile Tracking Process

### Qualified Name

DesignPattern::Information Profile Tracking Process

### Category

Information Process Patterns

### Description

Periodically run an information process to create an Information Values Profile report and compare the values from the recent profile with those of previous runs. Report on the changes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to automate the quality management of its information.

### Problem Statement

An organization does not understand the profile of its information or know when the profile of one of its critical information collections changes.

The profile of an information collection describes the information values that it contains. This includes the range of values in an attribute, the frequency that a particular value occurs in an attribute, and the relationships between information values in different attributes. This is useful to know when assessing the quality of the information within the collection.

### Problem Example

In an initial test of its new Customer Hub, MCHS Trading wants to understand the characteristics of its customers.

### Forces

- The information explains how the information processes are really working—Most information collections have an information schema that describes the structure of the information attributes stored in each information entry and the relationships between them. There may also be design documents that describe what type of information is stored in each attribute. However, the software developer can receive late requests to support new functions and find they need to manage and store information in attributes that were intended for different purposes. It is not until the information processes are running, and the information values in the information collections are checked, that these expediencies come to light.
- The profile of an information collection changes over time—This may be because the quality is improving, or simply that the characteristics of the world it is describing are changing. This changing profile may affect the information processes that are using the information because they are coded with assumptions about the information they are using.
- Information growth requires new approaches—Increasing volumes of information can dramatically impact the amount of resources and time required to process it. Statistical sampling or other approaches may be needed to support ongoing tracking.
- Cost to store/track full profile—Information profiling requires dedicated processing time and storage to maintain and track.
- Cost to correct may not be cost-justified—The cost to fix specific errors in the information vales must be measured against the cost to the business in increased risk, added business costs, or loss of revenue.

### Solution Description

Periodically run an information process to create an Information Values Profile report and compare the values from the recent profile with those of previous runs. Report on the changes.

The frequency of evaluation and review corresponds to the criticality and volatility of the information. New sources of information should be evaluated at the point of acquisition. Old information value profiles need to be regularly archived or purged, striking a balance between usefulness and relevance.

### Solution Example

MCHS Trading runs an information profile tracking process on the customer information used in the initial Customer Hub test. They find that the customer tax ID stored in the Stores' Sales Account collection includes hyphens in the values, whereas the tax ID stored in the E-Shop Customer collection does not. They determine that an Information Reengineering Step, specifically a Standardize Data step, is needed in the Information Deployment Process to ensure correct loading of the new customer information collection in the Customer Hub.

MCHS Trading schedules a monthly refresh of the Information Value Profiles to maintain trust in the Customer Hub.

### Benefits

- Using information profile tracking enables the organization to identify, understand, and track the information values with a goal of delivering effective information processes that work with and move data, reducing risk during project implementation or migration of new data into existing information collections. Such understanding also becomes a foundational aspect of a broader Information Governance Program.

### Liabilities

- Many information values have a business context that requires business knowledge to interpret—review can be labor-intensive particularly if the information profile is applied to too many information collections without appropriate focus. There is also a cost to storing and retaining information value profiles.

### Usage

Advanced information profiling tools offer the capability to schedule profiling and validation jobs so that they run against critical information collections on a regular basis. Where the information profiling tools do not offer this facility, it may be possible to schedule a script or program to manage the invocation of the profiling process and analysis of the results.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Clerical Review Process

### Qualified Name

DesignPattern::Clerical Review Process

### Category

Information Process Patterns

### Description

Create a task to inform the information steward that its assistance is required. This task is populated with details of the work that needs to be completed.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to automate the quality management of its information.

### Problem Statement

An information process is not able to complete the processing of a request without input from an information steward.

The role of the information steward in this process is often to simply confirm a proposed change to the information (such as the enrichment of information). However, there are other circumstances where the information steward needs to make a decision (such as whether two records should be merged) or select some information values (such as which values to use from two information entries that are being merged).

### Problem Example

MCHS Trading implements its new Customer Hub incorporating processes to match and merge information entries that relate to the same person. (See the Information Matching Process for more information on this type of processing.) Subsequent calls to the Customer-Care center indicate that some customers' orders were sent to the wrong individuals because some customer records were inappropriately merged together. Examples of incorrect customer record merging include the following:

- "Thomas Jones, 104 W. Elm St., Black Rock, WI" merged with "Thomas Jonas, 104 Elm Ave., Black Rock, WI"
- "Wm Holden, 128A Maine Sq, Carmelton, II" merged with "Will Holden, 128 Main Sq, Carmelton, IL" and "Willa Holden, 128C Maine Sq, Carmelton, IL" Subtle differences in spelling and location, errors, or a lack of sufficient information values can impact the reliability of such automated processes.

### Forces

- Manual processes add latency—The time for an information steward to review a case adds latency into the process.
- Manual correction of issues are limited by volume—High volumes of information or a high proportion of issues in the information will require prioritization of which changes are reviewed, and when.
- Automated correction of issues is limited by data complexity—The complexity of the information or requirements for specialized knowledge may preclude automated remediation or ever-greening options.
- Cost to correct may not be cost-justified—The cost to review specific types of clerical records must be measured against the cost to the business in increased risk, added business costs, or loss of revenue.

### Solution Description

Create a task to inform the information steward that his or her assistance is required. This task is populated with details of the work that needs to be completed.

The information steward regularly reviews the tasks on his or her list and processes each in turn. When he or she selects a task, details of the proposed change are displayed and the information steward is able to make updates and accept or reject the changes. The decision the information steward makes is recorded and may be passed to another information steward or supervisor for review/approval.

Once the change is approved, it is applied to the information collection. It is important that these changes are applied as soon as possible before new updates to the affected information entries are made.

Not all information collections, even those within the same subject area, require the same level of manual review. For example, duplicate customer information for a marketing campaign may be merged automatically without a clerical review as the consequences of a mistake are minimal, whereas customer information used for orders must be kept distinct to ensure that the right goods reach the right person.

### Solution Example

MCHS Trading modifies the thresholds on the Information Matching Process in the Customer Hub to include a clerical review whenever information entries are to be merged that are only a close match rather than an exact match. This clerical review helps to prevent the erroneous merging of information going forward.

MCHS Trading also uses clerical review to check the merges that have already taken place, so information entries can be split apart again if they were merged in error. This is possible because the Customer Hub keeps archived copies of the original information entries and creates a new information entry for the merged result.

### Benefits

- Using clerical review enables the organization to verify and approve changes that information processes are proposing to make to an information collection.

### Liabilities

- Clerical review requires dedicated resources to resolve issues. The people involved must understand the information values and business context. Clerical review may be perceived as expensive, particularly if they are not directed to information nodes of high value to the organization from a revenue, cost, or risk standpoint.

### Usage

Clerical review processes are often a key component of Master Data Management (MDM) hubs that are continuously validating and matching new information as it is received. The clerical review process provides a rapid confirmation of changes that are proposed by the hub information processes that have a certain level of doubt to them.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Remediation Process

### Qualified Name

DesignPattern::Information Remediation Process

### Category

Information Process Patterns

### Description

Gather together errors and then triage and remediate them, focusing on the most critical errors first.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to automate the quality management of its information.

### Problem Statement

Errors in the organization's information are being detected all of the time but never fixed.

This is because the organization needs a person with knowledge of the subject area to review the information values, perform some investigation, and make changes. How is this manual correction of information managed?

### Problem Example

The MCHS Trading Mail-Shop application is used by the call center to enter new customer orders. It is an older system that has limited validation of the information that is entered. The result is that the Shipping application sometimes receives order details with errors in them. Examples of these errors include customer name spelled incorrectly, incomplete or incorrect address, or an order for an unknown product. How does MCHS Trading process these orders?

### Forces

- Manual processes add latency—The time to remediate an issue adds latency into the process—remediation may have to be applied after the fact.
- Manual correction of issues are limited by volume—High volume of data or a high proportion of issues in the data will preclude manual remediation of information.
- Automated correction of issues is limited by data complexity—The complexity of the information or requirements for specialized knowledge may preclude automated remediation or ever-greening options.
- Cost to correct may not be cost-justified—The cost to fix specific types of data errors must be measured against the cost to the business in increased risk, added business costs, or loss of revenue.

### Solution Description

Gather together errors, and then triage and remediate them, focusing on the most critical errors first.

When errors are detected, they should be flagged and added to the list of errors that need correcting. An individual, or a team, must be responsible for processing the errors found. The errors should be prioritized and processed in the most cost-effective order. The person working on an error needs to investigate why the value is wrong, find the correct value, change the information so the correct values are introduced into the information supply chain, and record what was changed and why. This explanation provides an audit trail of changes being made to the information.

From time to time, the records from the remediation process should be reviewed to determine if there are changes that could be made to the information supply chain to reduce the chances of similar errors being introduced in the future.

### Solution Example

An Information Validation Process situated in the Information Flow that moves new orders from E-Shop, Mail-Shop, and Stores is used to check all orders before they are passed to Shipping. Most orders are correct and they are passed directly to Shipping. Orders that have errors in them are moved to a Staging Area. They are corrected by the Shipping team who focus on high-value orders and orders from high-value customers first before processing the rest. The Shipping team keeps detailed records of the changes that they are making to the incorrect orders, and may call the customer to verify the order. These details of the changes and comments from the Shipping team are fed into the Customer Hub so the Customer-Care center can answer questions from a customer if the order is not what they expected.

### Benefits

- Using information remediation processes enables the organization to identify and respond to errors with a goal of improving the overall quality of its information (and rules and processes applied to the data). Such corrective action becomes an aspect of a broader Information Governance Program.

### Liabilities

- Information remediation requires dedicated resources to resolve issues. These resources may be perceived as expenses or costs to the organization, particularly if they are not directed to information nodes of high value to the organization from a revenue, cost, or risk standpoint.

### Usage

Information quality and information governance initiatives incorporate information remediation processes at all levels of maturity, though at lower levels the approach is reactive rather than preventative. ETL, messaging, or ever-greening processes and any other information management routines that incorporate information validation processes to identify errors often feed remediation processes.

The software that supports a remediation process may simply maintain the list of outstanding errors; support the triaging of these errors and the recording of the remediation action taken. More sophisticated systems may also incorporate Agile Business Processes to coordinate the correction, review, and approval of changes made to the information.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Validation Process

### Qualified Name

DesignPattern::Information Validation Process

### Category

Information Process Patterns

### Description

Run an information process to step through the information and execute the appropriate validation rules. Report on the errors found.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to automate the quality management of its information.

### Problem Statement

An organization does not know whether its information conforms to the validation rules it has defined.

How do you understand how well an information supply chain is working when its processing is so varied and distributed?

### Problem Example

MCHS Trading uses specific product categories in its Information Reporting Processes to identify broad sales and buying trends. For each category, there are specific Valid Values Definitions that are supposed to be adhered to. The buyers notice unexpected sales trends in one product category, with sales much lower than expected in another. How do they determine if the reports are correct?

### Forces

- Rapidly changing content—Changes in information quality rules can result in incorrect information validation results if such changes are not properly synchronized across the entire information supply chain.
- Some information must always be processed—Errors found in the information values cannot always halt the information from further processing.
- Acquired information may have different context or format—New or acquired information may not be based on the same criteria or be structured in the same manner.
- Business context poorly understood—Old systems, lack of knowledgeable personnel, or lack of documentation may significantly limit the understanding of what rules to apply to the data.

### Solution Description

Run an information process to step through the information and execute the appropriate validation rules. Report on the errors found.

The information process will iterate through the information values, using a Validate Data step to check that it conforms to the appropriate valid values definitions. It will record the errors discovered for later remediation.

### Solution Example

Based on discoveries from an Information Values Profile pattern, MCHS adds an Information Validation Process to check the consistency of products and product categories between the Stores system and the Product Hub. MCHS Trading looks to identify the most problematic items in the Store system and establish tighter information controls on entering and changing product categories in the Stores.

### Benefits

- Validating the completeness, consistency, reliability, and quality of information will improve the information used by an organization for key decision making, resulting in cost savings, mitigated risk, or potential revenue opportunity. Such information validation becomes an aspect of a broader Information Governance Program.

### Liabilities

- Information validation is only useful if the results are acted upon through an Information Remediation Process. This takes time, qualified people, and resources.
- Information validation processes must be kept in sync with changes to business processes and rules, potentially adding time and cost to implement such changes. Having centralized management of validation rules can minimize this work because the information verification processes will pick up the changes immediately.

### Usage

Information quality and information governance initiatives incorporate information validation processes at various levels of maturity. ETL and other data integration routines incorporate information monitoring to ensure that required information has been received and that the same information is not processed multiple times.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Matching Process

### Qualified Name

DesignPattern::Information Matching Process

### Category

Information Process Patterns

### Description

Use matching technology to score the similarity between the information entries from the different sources and combine them as appropriate.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

An information process needs to combine related information entries that have come from multiple sources.

These information entries represent the same person, organization, place, account, object....

### Problem Example

MCHS Trading has customer information arriving from its E-Shop, Mail-Shop, and Stores systems. Review of the Customer Hub shows many similar names with common addresses or email addresses as well as addresses that match but have distinct names.

Multiple instances of the same or similar records in the Customer Hub cause inconsistent customer views as well as generating customer care issues.

### Forces

- Insufficient information to match together—There may be insufficient information values to support the matching of information entries.
- Information is time sensitive—Time dependencies may require that incorrect or unlinked information be loaded into the target information node and matched after that point.
- Information volatility may impact matching—The addition of differing "population" groups to a given subject area may significantly impact matching processes.

### Solution Description

Use matching technology to score the similarity between the information entries from the different sources and combine them as appropriate.

This process is implemented using the following steps:

- Certain Information Reengineering Steps, such as Enrich Data and Standardize Data, may be needed to improve the accuracy of matching.
- The information entries to be matched are compared and their similarity is scored against a variety of criteria and weightings.
- Based on the score, the match is classified into one of three groups. The thresholds for these groups are typically configurable values:
1. Weak match—The score is too low, which means the information entries are for different "things."
2. Close match—The score indicates the match is close, but not close enough to be sure. This pair is passed to a Clerical Review Process.
3. Strong match—The information entries are matched and should either be linked together (see Link Entries) or merged into a single information entry (see Merge Entries).
- Finally, the new and updated information is saved into the destination.

### Solution Example

MCHS Trading uses an Information Ever-Greening Process to trawl through the existing information entries in the Customer Hub and call the information matching process to detect information entries that should be merged. Some entries are automatically merged; others are merged after a Clerical Review Process.

The process of adding and updating information entries in the Customer Hub is also changed to use an information matching process to detect if new information is in fact an update of an existing information entry rather than a creation of a new information entry. This enhancement is called the unique entries pattern that is part of the information entry pattern group.

### Benefits

- The information matching process provides the mechanism to effectively link and consolidate related information together.

### Liabilities

- Individuals familiar with the requirements of the subject area must tune this process to ensure appropriate grouping and consolidation of data. Incorrect grouping can have significant ramifications and risks to an organization because the matching is typically applied to core subject areas, such as Customer, Account, or Product.

### Usage

Information matching is a core component of Master Data Management (MDM) solutions particularly for core subject areas, such as Person, Party, Location, and Product. Information matching processes may be incorporated into business processes, information provisioning processes, and information quality processes.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Ever-Greening Process

### Qualified Name

DesignPattern::Information Ever-Greening Process

### Category

Information Process Patterns

### Description

Set up a regular process that steps through the entries in the information collection and runs various validation checks against them, raising alerts where information values are found to be incorrect or stale.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to automate the quality management of its information.

### Problem Statement

Information about the real world decays over time. The existing information processes are not able to guarantee that the contents of an information collection are up to date.

### Problem Example

MCHS Trading wants to send promotional emails to its customers from time to time. When a new customer registers with E-Shop, he or she is asked to provide an email address, which will be used when sending the promotional material. In the United States, it is estimated that people change contact information, such as email addresses, on average about once every 3 months. This means that over time, the email addresses in the customer details in E-Shop are gradually becoming obsolete.

### Forces

- Unused information is out of date—It is typically the information that is not being accessed that is the most likely to be out of date.
- There is an increasing load on information nodes—Additional queries on an information collection will add load to its information node.
- Information is time sensitive—Time dependencies may require that incorrect or unlinked data be loaded into the target information node and linked and merged after that point.
- Many conditions cannot be automated—Issues from upstream in the information supply chain and some validation checks cannot be handled automatically and must be remediated through manual review.

### Solution Description

Set up a regular process that steps through the entries in the information collection and runs various validation checks against them, raising alerts where information values are found to be incorrect or stale.

An information ever-greening process provides continuous patching of the values within an information collection. It typically runs on the information node where the information collection is located, or in an Information Broker that has access to the information collection.

### Solution Example

MCHS Trading has an integration job that systematically scans the customer details entries in the E-Shop application and flags those entries where the email address has not been verified for over 2 months. When a customer connects to the E-Shop, the flag is checked for his or her entry and if it is set, the customer is asked to verify that the email and phone number are correct.

### Benefits

- The ever-greening process detects and flags information that is potentially out of date.

### Liabilities

- There may be some latency introduced by the information ever-greening process to the information supply chain. It can result in additional processing load to the information node that hosts the information collections, affecting all information processes that use the information. The information ever-greening process should be throttled back to minimize the impact.

### Usage

Ever-greening is typically supported by Master Data Management (MDM) products for detecting data decay and duplicate suspects. Ever-greening may trigger other automated processes such as requesting that customers provide updated address and phone information.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Archiving Process

### Qualified Name

DesignPattern::Information Archiving Process

### Category

Information Process Patterns

### Description

Set up a regular archiving process to move the information that is no longer needed operationally to an archive store where it can be retrieved if necessary.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization wants to automate the quality management of its information.

### Problem Statement

Eventually, entries in an information collection are no longer needed operationally, but must be retained for reference.

Once this happens, their presence in the information collection can start to impact the performance of the information processes using it.

### Problem Example

The E-Shop application stores details of each customer's orders. Three months after the order has been completed, this information is likely to be obsolete.

### Forces

- Increasing volume degrades query performance—Additional volume of data and queries on an information collection will degrade the performance of an information node.
- Regulations and policies set retention requirements—For some types of information, there are legal regulations that require an organization to retain information for many years. This retention period may be longer than the useful life of the originating application.

### Solution Description

Set up a regular archiving process to move the information that is no longer needed operationally to an archive store where it can be retrieved if necessary.

The information archiving process may run on the information node where the information collection is hosted, or on a remote information node (for example, where the information archive is located).

### Solution Example

Due to tax reporting requirements, MCHS Trading cannot simply delete the details of each customer's orders for several years. However, to save storage costs and reduce processing time, MCHS Trading implements an archiving process to move the order details to an offline archive store once it has been complete for 3 months.

### Benefits

- The information collection that receives regular housekeeping, such as archiving of obsolete information, benefits from improved processing time and reduced online storage costs.

### Liabilities

- Information that has been archived needs to be associated with descriptive information that records where the information came from, how to read it, how long to keep it, and what level of security it should be given. If archived information must be kept for a long time, it must be read back and rearchived from time to time to refresh the media and ensure it is located on viable hardware for retrieval.

### Usage

Information archiving is widely used by IT departments to remove older information to cheaper storage once the information processes running the business no longer need it. The archive repository provides a safeguard against an unusual circumstance where the old information is required.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Replication Process

### Qualified Name

DesignPattern::Information Replication Process

### Category

Information Process Patterns

### Description

Create an information process that is monitoring changes to the information collection and replicating them to the copy.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

An exact copy of an information collection needs to be maintained.

This copy is kept in a different information collection, which may be on the same information node or a different one.

Reasons for creating this copy include the following:

- For use as a backup in case a system error or loss of facility destroys the original information collection
- To bring the information closer to one or more information processes that need reliable, high-speed access to the information.

### Problem Example

The information collections stored in the Customer Hub need to be copied to a set of information collections located in MCHS Trading's disaster recovery facility.

### Forces

- Retrieval adds delay—Retrieving information from a remote system each time you use it introduces a delay and puts extra load on the system hosting the information.
- Local copies reduce delay, but require synchronization—Copying information so it is local to the processing reduces latency in retrieving information but adds a requirement to synchronize the copies.
- Transfer of information may be interrupted—Network and system failures may interfere with the transfer of information. These disruptions must be recovered from once the failing components have been recovered.

### Solution Description

Create a process that is monitoring changes to the information collection and replicating them to the copy.

The process of replicating an information collection can be thought of in two parts. First, there is the initial load. This is where the existing contents of the information collection are copied into the replica information collection. Then there is the ongoing trickle feed of updates that must be copied across to keep the replica synchronized with the original. This requires the following:

- A mechanism for monitoring for updates in the original information collection. For example, using a database trigger, or even better, monitoring the transaction log of the database. These are examples of Information Change Triggers.
- The ability to extract the information values that have changed.
- An information flow to move the information values to the replica information collection(s).

### Solution Example

A replication process is set up to monitor changes to the Customer Hub information collections and then sends them to the disaster recovery site.

### Benefits

- This information process provides a simple mechanism for maintaining an exact copy of an information collection.

### Liabilities

- Inevitably there is some latency introduced by the replication process.
- The information replication process may impact the performance of the information node where the original information collection resides. However, this impact is likely to be lower than having remote information processes access it directly.
- The replica information collection should have Reference Usage or Sandbox Usage because changes to it are not reflected back into the original copy.

### Usage

Replication can be used for many purposes. There is the disaster recovery scenario as described in the example. It may also be used to replicate code tables or other types of reference data to systems on different premises or in different countries.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Deployment Process

### Qualified Name

DesignPattern::Information Deployment Process

### Category

Information Process Patterns

### Description

Create a process that is able to extract the required information, perform any necessary reengineering on it, and send it to the destination information collection(s).

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

Information must be proactively transformed and either (1) introduced into the information supply chain or (2) copied between two or more information collections within the information supply chain.

### Problem Example

When new products are defined in the Product Hub application, they need to be distributed to MCHS Trading's order-processing applications and the Reporting Hub.

### Forces

- Retrieval adds delay—Retrieving information from a remote system each time you use it introduces a delay and puts extra load on the system hosting the information.
- Local copies reduce delay, but require synchronization—Copying information so it is local to the processing reduces latency in retrieving information but adds a requirement to synchronize the copies.
- Information collections have differing structures—The structure of the information that needs to be deployed is not necessarily the same as the destination(s).
- Quality may be an issue—The level of quality of the information may not be sufficient for the destination information collection(s).
- Not all information is needed—A destination might only need a subset of the information that is available.

### Solution Description

Create a process that is able to extract the required information, perform any necessary reengineering on it, and send it to the destination information collection(s).

This process is implemented using the following steps:

- The information to be deployed is copied into some form of staging area.
- Working from the staging area, it performs the following types of Information Reengineering Steps where required:
1. Standardize Data—For the complex structures such as addresses
2. Validate Data—Using lookups to ensure values conform to known values
3. Enrich Data—To add values that are missing
4. Restructure Data—To modify the structure of the information to match the destination
- Finally, the reengineered information is saved into the destination.

### Solution Example

See Figure 7.13. Product details in the Product Hub application include details of the channels through which the product will be sold. There is a Staging Area for each of the applications that will receive product details. When the Product Hub application has new product information to distribute, it pushes a copy of it into the appropriate staging areas. There is an integration job dedicated to each of the staging topics. When product details are added into a topic, it triggers the integration job to transform and deliver them to the appropriate application.

Note: In this example, the Product Hub application supplies information that is sufficient quality that it only needs to be restructured for the target application.

### Benefits

- The information deployment process provides the mechanism to provide information to new processes by transforming it and placing it in a more convenient location.

### Liabilities

- This process has created one or more copies of the information. These copies need to be managed in an appropriate manner. This includes updating it at appropriate points and deleting it when it is no longer needed.

### Usage

This is the most common process that is used to flow information between nodes in the information supply chain—primarily because it is the most versatile and caters for the differences in the information support offered by each information node. The typical implementation of the integration job is an extract, transform, load (ETL) process. However, it may be performed by an extract, load, transform (ELT) process.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Relocation Process

### Qualified Name

DesignPattern::Information Relocation Process

### Category

Information Process Patterns

### Description

Create a recoverable process that is able to read and delete information from the source location and write it to the target system.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

Information must be moved from one location to another.

The information needs transforming, enriching, or validating as part of the transfer.

### Problem Example

When the Mail-Shop application is in the process of being decommissioned in favor of the new M-Shop application, details of the employees in the customer call center have to be moved to M-Shop when they transfer between the two applications. MCHS Trading wants to ensure that when an employee transfers over to M-Shop, he or she can no longer log in to Mail-Shop.

### Forces

- Coordination of updates can be challenging—It is difficult to coordinate the updating of information across multiple information nodes.

### Solution Description

Create a recoverable process that is able to read and delete information from the source location and write it to the target location.

Typically, this process runs in the source information node and moves (create in the new and then delete from the old) the information to an intermediary information node that supports distributed transactions. The information is then retrieved from the intermediary node, transformed, and stored in the target information node. Once it is in the target information node, it is removed from the intermediary.

The purpose of the intermediary is to safely remove it from the source information node to prevent any more updates to it until it is safely installed in the target information node. The intermediary can be used to stage any information reengineering or remediation that is required before the information can be added to the target node.

### Solution Example

When an employee is ready to transfer over to M-Shop, his or her profile is removed from MailShop and stored in a Queue Manager using an Information Queuing Process. The profile is immediately picked up from the queue manager, transformed, and inserted into M-Shop. The employee can now log on to M-Shop and his or her preferences will have been transferred over. The employee will no longer be able to log on to Mail-Shop.

### Benefits

- This type of process moves information from one part of the supply chain to another without duplicating information. It is also able to transform the information as it moves it.

### Liabilities

- It is very hard to make sure all of the timing windows and failure scenarios are covered, particularly when the technology involved cannot be included in a two-phase commit (distributed transaction).

### Usage

This type of process is used where information must move between two information collections without duplication.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Federation Process

### Qualified Name

DesignPattern::Information Federation Process

### Category

Information Process Patterns

### Description

Create an information process that is able to retrieve and combine information from multiple information collections on demand.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

An information process needs up-to-date information that is stored in multiple information collections.

Due to either the volume of information, or the frequency it is updated, it is not practical to keep a local copy of the information.

### Problem Example

The Customer-Care application needs to retrieve information about a product and its current stock level. The product details are available from the Product Hub application. The current stock level is available from the Shipping application.

### Forces

- Retrieval adds delay—Retrieving information from a remote system each time you use it introduces a delay and puts extra load on the system hosting the information.
- Availability of remote information varies—If remote information is not consistently available, work and decisions may be impacted.
- Local copies reduce delay, but require synchronization—Copying information so it is local to the processing reduces latency in retrieving information but adds a requirement to synchronize the copies.
- Information collections have differing structures and keys—Information is not stored in the same format in every information node and differences in keys may limit the ability to connect together.
- The information context varies—Information retrieved from one system may be needed to formulate the request to a subsequent system.

### Solution Description

Create an information process that is able to retrieve and combine information from multiple information collections on demand.

A Triggering Information Service initiates the information federation process. Once started, the information federation process makes calls to other information services to extract and assemble information from multiple information collections. It must be able to perform the following:

- Break the request into parts that each correspond to a request for information from a separate location.
- For each part request, use an information service to retrieve the required information.
- Transform and correlate the received information together.
- Return it to the requesting information process.

### Solution Example

The product availability process uses an information service to extract the product details and supplier information from the Product Hub application. It then retrieves the current stock levels from the Shipping application using another information service. The results are combined together to provide details of current stock levels and how long each supplier would need to get more.

### Benefits

- The information federation process is able to combine information from different information collections together without creating copies of it. This is particularly important when the information collections are large or changing rapidly because maintaining copies of them would be expensive.

### Liabilities

- Retrieving information using federation is likely to be slower than working with a prejoined and formatted local copy. Therefore, it is not suitable where there are a large number of requests for information on a fairly static collection.

### Usage

There are several of ways of approaches to implementing this pattern:

- Using federated database queries—The database is able to split up the query and push down parts of the request to other databases. It then combines the results to satisfy the original query.
- Using a composite service—The federation process runs on an Information Broker. It is invoked via an Information Service. It extracts information from service interfaces of various applications, combines the information, and returns the results to the caller.
- Using a local procedure—Implement the federation process on the local information node. This is useful when the retrieve information is also to be combined with local information.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Queuing Process

### Qualified Name

DesignPattern::Information Queuing Process

### Category

Information Process Patterns

### Description

Use a recoverable queue to store the information and pass it on to the downstream information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

Information must be reliably passed between two information nodes even though they are not always available at the same time.

This means they need to use an intermediary information node that is always available that they can use to act as a reliable place to put information and retrieve it later. This intermediary node must pass the information payloads to the destination in the same order that the source sent them and be careful not to lose any of them, or send them more than once.

### Problem Example

New orders can be raised on the E-Shop at any time because its website is available twenty-four hours a day, seven days a week (24/7). The Shipping application needs 2 hours downtime each evening for backups and maintenance. What happens to orders from E-Shop when Shipping is down?

### Forces

- Information can arrive at any time—When some information nodes are available and others are not, information still needs to be processed.
- Information collections have differing structures—Information is not stored in the same format in every information node.
- Issues in one node can impact others—A source information node must not hang when another information node is not available, or underperforming. Otherwise, a situation called sympathy-sickness occurs where an issue in one of the information nodes spreads to others. If a target information node is not available, the source information node will have to save the information payload and retry.

### Solution Description

Use a recoverable queue to store the information and pass it on to the downstream information node.

An information queuing process runs on a queue manager. The queue manager is a robust information node with very high availability. Each instance of an information queuing process either puts an information payload onto a first in, first out (FIFO) queue or takes an information payload out of a queue. The information payloads in the queue are written to storage so they are not lost in the unlikely event of a failure.

### Solution Example

See Figure 7.14. The E-Shop application (along with the Mail-Shop and Stores applications) writes the order into a distributed queue whenever they have a new order. When the Shipping application is available, it is listening for orders from the queue and processing them.

### Benefits

- The queuing mechanism is easy to use, understand, and implement.

### Liabilities

- The queuing process offers no opportunity to reformat the information payload being sent.
- The applications using the queue have to be modified to put information payloads on the queue and get the information payloads from it.

### Usage

Information queuing processes are implemented by message-oriented middleware. This style of information passing is used extensively in Enterprise Application Integration (EAI).

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Broadcasting Process

### Qualified Name

DesignPattern::Information Broadcasting Process

### Category

Information Process Patterns

### Description

Use a recoverable publish/subscribe mechanism to provide a topic that source information nodes can post to and other information nodes can subscribe to.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

Information must be broadcast to a varying group of information nodes.

This information must be sent to all information nodes that are registered to receive it. The list of registered information nodes will vary over time.

### Problem Example

The MCHS Trading order-taking applications exchange order records with the Shipping application using an information queuing process. This works well until the new orders need to also be distributed to the Reporting Hub via an Information Activity Node.

If the queuing mechanism is retained, new order records will either go to Shipping or to the information activity node but never both.

### Forces

- Interest in certain types of information varies—The number of information processes interested in information payloads passing through a certain point in the information supply chain may vary over time.

### Solution Description

Use a recoverable publish/subscribe mechanism to provide a topic that source information nodes can post to and other information nodes can subscribe to. A publish/subscribe mechanism has three parts to it:

1. The ability to define a set of topics that information can be published to. These topics can be thought of as letterboxes where Information Payloads can be posted.
2. The ability for an information node to subscribe to one or more topics and nominate an information process to call when an information payload is posted to it.
3. The ability for an information process to post an information payload to a topic by calling an Information Service.

### Solution Example

In Figure 7.15, the information queuing process shown in Figure 7.14 is replaced with an information broadcasting process. The Shipping application is updated to listen for the payloads on the "New Order" topic rather than the "New Order" queue. The information process that transfers new orders to the operational snapshot store also listens on the "New Order" topic.

### Benefits

- Using topics means another information node could subscribe and receive the information payloads without updating the source or other destination information nodes.

### Liabilities

- Similar to the information queuing process, the information broadcast process offers no opportunity to provide the payloads in different formats for different consumers. This is why, for information supply chains that make heavy use of this type of information integration, there are canonical payload formats that are used throughout the information supply chain. This means every information node has to understand the canonical payloads, but a payload can be distributed to multiple destinations and be understood.

### Usage

The use of publish/subscribe technology is used to provide very loose coupling between multiple sources and multiple destinations. It is implemented in message-oriented middleware and is commonly referred to as a pub-sub engine.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Summarizing Process

### Qualified Name

DesignPattern::Information Summarizing Process

### Category

Information Process Patterns

### Description

Summarize the important information into a new information collection, enabling the fine-grained detail to be archived or deleted.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

Keeping the fine-grained detailed information created by the operational systems uses a lot of storage for the value it delivers.

This information is necessary while they are part of the current activity. It is useful for the first few reporting cycles, and then its value diminishes.

### Problem Example

In MCHS Trading, when a package is shipped, details of the packaging style, truck, batch, drivers, route, intermediary depots, weather, and a full set of timings for each stage of the journey are recorded. This is to make it possible to locate a lost shipment, or prove the goods were delivered, or similar types of incidents. They also use it to monitor the effectiveness of the delivery companies they use. However, once the package is delivered, the value of this information starts to diminish.

### Forces

- It is hard to know what information you might need in the future—The temptation is to keep it all just in case.
- The value of information can diminish over time—As such, it may not be cost effective to keep it forever.
- Information must be viewed in context for it to be understood correctly—Not everyone in an organization will use the same terminology, precision, or validation rules or have the same expectations for information quality and timeliness.
- Storing information that is never going to be used is wasteful—Storage costs money to buy and power to operate.

### Solution Description

Summarize the important information into a new information collection, enabling the finegrained details to be archived or deleted.

### Solution Example

The detailed shipping information is summarized into two Information Summary information elements as follows:

- A summary of the package shipment, including order number, package number, shipment date/time, delivery date/time, and shipping company
- A summary of each shipping incident, including incident number, order number, package number, incident raise date/time, incident type, incident description, incident resolution type, and incident completion date/time These two types of summaries cover the minimal information about a shipment for most packages that are delivered without incident. When issues occur, additional information is kept about the shipping incident.

### Benefits

- Summarizing information will reduce the storage necessary for keeping historical information. More important, designing information summary information elements for this purpose means the information kept includes the context in which it was created.

### Liabilities

- It is possible that information needed in the future was not anticipated and is discarded in the summary process. Also, the summarizing logic requires an additional information process to be maintained and run.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Scavenging Process

### Qualified Name

DesignPattern::Information Scavenging Process

### Category

Information Process Patterns

### Description

Use text analytics to extract facts from the corpus of unstructured information and store them in an information collection that can feed the information supply chain.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support the provisioning of information along an Information Supply Chain.

### Problem Statement

What is the appropriate approach to introduce information extracted from a huge corpus of unstructured information?

### Problem Example

MCHS Trading is interested in understanding the feedback of people who have bought the types of products that MCHS Trading sells. This information is located in various support forums and social media sites.

### Forces

- Unstructured data is difficult to use directly—Unstructured data such as pictures, video, websites, and documents are the largest growing sector of information. They contain useful information for the information supply chain, but their format, and the informal way they are typically created and managed, makes it hard to use them directly in an information supply chain.

### Solution Description

Use text analytics to extract facts from the corpus of unstructured information and store them in an information collection that can feed the information supply chain.

The facts that are extracted include direct references to the subject matter of interest and relationships to other things.

### Solution Example

MCHS Trading implements an information scavenging process to scan popular social media sites looking for instances where customers are discussing MCHS Trading. This information is collated and analyzed to understand if there are any issues in general that should be addressed.

### Benefits

- Business processes can respond faster to emerging feedback about the organization, its products, or its processes.

### Liabilities

- Information scavenging processes must revalidate their data continuously and ensure they are still targeting the best sources of unstructured data.
- Unstructured information generally ages quickly (often in hours or days).
- The volumes of unstructured data have storage and processing costs that must be addressed.

### Usage

Information scavenging processes are beginning to appear in larger organizations that need to extract value from unstructured information. Examples of this type of processing include sentiment analysis, social network analysis, and financial relationships of public companies.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Pattern Discovery Process

### Qualified Name

DesignPattern::Information Pattern Discovery Process

### Category

Information Process Patterns

### Description

Use data mining and other analytical techniques to discover the patterns in the information that seems to coincide with a predicted outcome.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to discover new patterns or trends about its business.

### Problem Statement

What are the key predictive indicators within the information that the organization is collecting?

Predictive indicators are combinations of information values that suggest either a particular event is about to occur or the person, object, place, activity, or asset that the information values are about should be classified and processed in a particular way. If an organization understands which information values are key predictive indicators and what the different combinations of values predict, it is able to react to situations before they arise or discover new opportunities in time to act on them.

### Problem Example

MCHS Trading is interested in discovering what types of products its individual customers like to buy so it can make personal product recommendations to them.

### Forces

- Difficult to correlate certain information—Different information sources hold related pieces of information that may contain useful information but their content is not easily correlated.
- Many possible combinations of information—There are a lot of information values to consider, in many combinations.
- Some relevant information may be external—Information that may be necessary to make specific correlations and pattern discoveries may not be available through existing systems (e.g., customer demographics, geographic or regional-based characteristics). Often this information must be acquired from third parties.

### Solution Description

Use data mining and other analytical techniques to discover the patterns in the information that seems to coincide with a predicted outcome.

Data mining tools are designed to hunt out patterns in information (see Figure 7.16). They typically work on information stored in Information Mining Stores. The result is an analytics model that can be used to analyze the organization's information. (See Information Pattern Detecting Process for more information on using an analytics model.)

### Solution Example

MCHS Trading creates an information mining store that hosts correlated information collections covering customer demographics, the orders each customer has made, when they make them, and the types of products they buy. MCHS Trading then uses the information pattern discovery process to understand the following:

- Which products the same person typically buys
- Whether there is a common sequence in the purchase order of these products
- Whether there are common traits associated with people who bought the same products This knowledge enables MCHS Trading to classify its customers into groups based on their characteristics and make meaningful product recommendations both through E-Shop and through direct mail (post). Over time, fashion and consumer taste change and so these key predictive indicators will change, too. MCHS Trading continuously monitors whether customers buy the recommended products and checks that this process is increasing sales. Every month they rerun the information pattern discovery process to tune the key predictive indicators.

### Benefits

- When an organization understands its key predictive indicators, it can be more proactive in how it manages its business and interaction with customers and suppliers.

### Liabilities

- Information pattern discovery processes must reassess the models regularly to ensure that the previously discovered patterns are still correlated.
- Information pattern discovery processes use Data Scientists to establish the right tests or evaluate the results properly.

### Usage

Information pattern discovery processes describe the general class of data mining tools that use statistical models and other techniques to seek out patterns in information.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Decision Definition Process

### Qualified Name

DesignPattern::Information Decision Definition Process

### Category

Information Process Patterns

### Description

Combine business rules with the results of data mining to create an automated decision process that can be included in operational activities.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities.

### Problem Statement

An organization needs to improve the consistency and quality of its operational decision-making process.

The organization wants to insert business rules into the operational information processes.

### Problem Example

MCHS Trading believes that contact details for its customers should be checked about once every six months. Some contact details are fairly stable, such as home address, whereas email addresses tend to change more rapidly.

MCHS Trading has used an Information Pattern Discovery Process to create an analytics model to detect if contact details are likely to have changed. This model uses knowledge about when the contact details were last checked—and the types of orders the customer is making—to indicate which of the contact details of the customer should be validated. MCHS Trading decides that this analytics model should be run no more than once every 3 months when the customer uses any of the channels.

### Forces

- People forget to do ancillary tasks—Most people are busy, focused on their main tasks. They often skip additional tasks that get in the way of their main task—particularly if it will not be noticed. Therefore, it is often necessary to automate these tasks, or the prompts to ask a person to do them.
- Certain decisions are complex—Decisions may follow many steps with many possible branches to get to the end result.

### Solution Description

Combine business rules with the results of data mining to create an automated decision process that can be included in operational activities.

Data mining (or information pattern discovery process) tools enable a Data Scientist to produce an analytics model. Combining the analytics model with business rules created by a Business Analyst results in a decision model that can be inserted as a decision step in the operational information processes. See Figure 7.17.

### Solution Example

MCHS Trading designs a decision model that combines the analytics model with a business rule that ensures the customer is only asked at most once every 3 months to verify that his or her contact details are still correct.

### Benefits

- Consistent decisions can be deployed across multiple channels and lines of business. The business rules can easily be updated and redeployed as necessary.

### Liabilities

- The results of the decision model should be captured and regularly assessed to ensure they are delivering the best results. It is likely that both the analytics model and the decision model will need to be refined over time.

### Usage

Decision models may be incorporated into operational business processes. Decision models that combine rules and analytics are a common approach for real-time predictive analytics. The analytics typically give better results than rules alone, and the business rules define the policies that control when the analytics should run.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Pattern Detecting Process

### Qualified Name

DesignPattern::Information Pattern Detecting Process

### Category

Information Process Patterns

### Description

Run either an analytics model or a decision model against the organization's information to detect when patterns occur in the organization's information that predicts a particular outcome.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities.

### Problem Statement

Where are the key predictive indicators occurring in the information collected by the organization?

Predictive indicators are combinations of information values that suggest an event is likely to occur in the near future. The sooner they are detected and acted upon, the more effective the organization will be.

### Problem Example

MCHS Trading is interested in understanding how the availability and timeliness of phone responses affects its Mail-Shop business and customer call center service.

### Forces

- Key predictive indicators are forever changing—They need to be constantly monitored and tuned to meet the current operational needs.

### Solution Description

Run either an analytics model or a decision model against the organization's information to detect when patterns occur in the organization's information that predicts a particular outcome.

The information pattern detecting process (see Figure 7.18) takes the context passed to it from the information trigger and combines it with information in the information collection to invoke either an analytics model or a decision model. The results of the model and the information used to call it are stored in an information collection for later analysis. The results are passed back to trigger for action. The results of the action are saved at a later date with the results of the model when they are known.

### Solution Example

MCHS Trading adds an information pattern detecting process in association with its new information streaming process. By analyzing new information on the length of time to answer and place a call in the queue, to route a call, and to engage a service representative, MCHS Trading can identify the frequency with which issues in customer response result in lost or canceled orders.

### Benefits

- The organization can respond faster and more consistently to situations that can be detected and resolved before a problem occurs, or an opportunity is lost.

### Liabilities

- The models that detect the predictive indicators must be regularly assessed to ensure they are still accurate. It is often necessary to tune these models as the predictive indicators change over time.

### Usage

Information pattern detecting processes are beginning to appear in larger organizations that need to extract value from their existing information. Examples of this type of processing include event prediction, such as traffic analysis, disease, or network virus spread.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Crawling Process

### Qualified Name

DesignPattern::Information Crawling Process

### Category

Information Process Patterns

### Description

Run search crawlers to build a map of where information is located.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Where is all of the interesting information located?

### Solution Description

Run search crawlers to build a map of where information is located.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Indexing Process

### Qualified Name

DesignPattern::Information Indexing Process

### Category

Information Process Patterns

### Description

Build an index that links topic to file/location.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

What type of information does the organization store on each topic?

### Solution Description

Build an index that links topic to file/location.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Search Process

### Qualified Name

DesignPattern::Information Search Process

### Category

Information Process Patterns

### Description

Provide a user interface to allow an individual to request a list of files that cover a particular topic.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Where is a particular type of information?

### Solution Description

Provide a user interface to allow an individual to request a list of files that cover a particular topic.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Operational Health Monitoring Process

### Qualified Name

DesignPattern::Operational Health Monitoring Process

### Category

Information Process Patterns

### Description

Add operational health probes to the information infrastructure to detect when systems and networks fail or experience problems.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities.

### Problem Statement

Is the information infrastructure that supports the information supply chain working?

The information processes that support the information supply chain, and the information collections they use, are hosted by information nodes. These information nodes must be operating correctly for the information supply chain to function. How does an organization ensure all of its critical information nodes are working correctly?

### Problem Example

MCHS Trading relies heavily on its order-processing systems such as Mail-Shop, E-Shop, and Shipping. Failures in these key information processes disrupt order fulfillment and have a high impact on customer satisfaction and retention.

### Forces

- Issues in IT impact the business—The issues in the IT infrastructure often complicate the activities of a business.
- An activity takes time—Any IT infrastructure supporting the activity may fail during that processing time.
- Issues incur cost and time—Addressing issues after failure incurs higher costs in problem determination and resolution, and adds time to the information process.

### Solution Description

Add Operational Health Probes to the information infrastructure to detect when systems and networks fail or experience problems.

These information probes are checking that the information nodes are operating correctly. They will check that each node is processing work and has enough resources (CPU, memory, disk) to continue to do so. It also looks for failing information processes because they may indicate that the information node is incorrectly configured.

### Solution Example

MCHS Trading adds operational health monitoring processes through these key information processes to ensure that orders are not lost or remain unfulfilled.

### Benefits

- This monitoring will detect when an information node is not running correctly, or has failed completely. It has the information to determine why the information node failed so that the infrastructure operators can correct the problem and restart the information node.

### Liabilities

- Information health monitoring can generate a huge amount of information to monitor. When a catastrophic event occurs, such as a power outage, the number of alerts raised can be overwhelming for the infrastructure operators.

### Usage

Operational monitoring processes are present in IT infrastructure monitoring software. This software collects information from probes and analyzes it, looking for significant situations. When information nodes are found to be down, or not operating correctly, they raise alerts for infrastructure operators to take action.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Node Management Process

### Qualified Name

DesignPattern::Information Node Management Process

### Category

Information Process Patterns

### Description

At the heart of an information node is a controlling information process that is responsible for starting and stopping the information node and monitoring its operation while it is running.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities.

### Problem Statement

What ensures an information node is available and operating correctly?

An information node is a server that must be started before it can run any information processes. It must be configured with the computing resources it needs and when it is not needed, it should be shut down so it does not waste power.

### Problem Example

MCHS Trading notices that orders are not being received by the Shipping application.

### Forces

- Issues in IT impact the business—The issues in the IT infrastructure often complicate the activities of a business.
- An activity takes time—Any IT infrastructure supporting the activity may fail during that processing time.
- Issues incur cost and time—Addressing issues after failure incurs higher costs in problem determination and resolution, and adds time to the information process.

### Solution Description

At the heart of an information node is a controlling information process that is responsible for starting and stopping the information node and monitoring its operation while it is running.

The information node management process is present in every information node. It provides a command line and user interface for a person to start, stop, and configure an information node. Calls to this information process may be made from a script to automate the management of the information node.

### Solution Example

MCHS Trading discovers that the Information Broker responsible for transferring orders from E-Shop and Mail-Shop to Shipping is not running. It uses the information broker's information node management process to start it up and very quickly the new orders start to flow to the Shipping application.

### Benefits

- This process provides the mechanism to manage and configure an information node so its availability and use of resources can be managed.

### Liabilities

- There is very little standardization of information node management processes between different types of information nodes. The result is that individual infrastructure operators tend to need to specialize on one or two particular types of information nodes. It makes it hard to standardize the operations of a large and varied IT operation.

### Usage

Any information node (server) will have commands and menu options to start and stop its server and to configure it with settings. The information node management process implements these commands and property sheets.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Scheduling Process

### Qualified Name

DesignPattern::Scheduling Process

### Category

Information Process Patterns

### Description

Create an information process that can trigger other processes according to a schedule.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 7, "Information Processing".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization requires an information process to support one of its activities.

### Problem Statement

Information processes need to run at regular time intervals.

### Problem Example

MCHS Trading generated invoices based on received orders. This created inefficiencies and customer dissatisfaction as canceled orders, insufficient inventory to complete shipments, and other events required generation of offsetting or credit invoices.

### Forces

- The real world impacts the business's activities—The activities of a business are often complicated by the inconsistencies in the organization and the world beyond.
- An activity may involve contributions from multiple processes.
- An activity may involve complex or specialized processing.
- An activity takes time (minutes, days, weeks, or years)—Any IT infrastructure supporting the activity may fail.

### Solution Description

Create an information process that can trigger other processes according to a schedule.

This information process makes use of the operating system services to regularly check the time and trigger information processes at the time that has been specified in its configuration.

### Solution Example

MCHS Trading introduces a scheduling process to run invoice generation once per day after daily shipments are complete. This allows MCHS Trading to achieve tighter control over invoice processing and more accurate invoices, improving customer satisfaction.

### Benefits

- Activities or events prior to the scheduled process can be consolidated, ensuring that specific sequences are handled or outside changes are incorporated.
- Scheduling may potentially reduce the cost of running specific processes by reducing frequency of occurrence.

### Liabilities

- Scheduling introduces latency into an information supply chain, which may result in missed opportunities.

### Usage

Scheduling is used to initiate processing that must be performed at regular intervals. Most ETL platforms and application servers incorporate some form of scheduler for this purpose. The scheduling may be part of some polling logic, looking for work to do, or as a means to initiate new processing.

### Search Keywords

- Patterns of Information Management
- Information Process
- Information Processing

### Version Identifier

1.0

### Status

ACTIVE

____

