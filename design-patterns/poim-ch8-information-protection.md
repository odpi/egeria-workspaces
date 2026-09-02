<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

**Information Protection**

Dr.Egeria commands for the design patterns in Chapter 8, "Information Protection", of *Patterns of
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

Information Reengineering Step

### Qualified Name

DesignPattern::Information Reengineering Step

### Category

Information Reengineering Step Patterns

### Description

Insert capability to transform the information so it is consumable by the information process.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

An information process is not able to consume the information it needs, as it currently exists.

This may be for structural or quality reasons.

### Problem Example

MCHS Trading's Stores application maintains details of customers with a store card. These customer details must be synchronized with the Customer Hub. However, there are significant differences between the way customer details are stored in the Stores and Customer Hub information collections. For example,

- The Stores application stores date fields in a character string format, whereas the Customer Hub uses a standard database date format.
- Similarly, the tax identifier is stored in a format with hyphens in the Stores application, but the Customer Hub uses only numeric data.
- The Stores application stores the customer name and address in single free-form fields, which are difficult to use to link customer records unlike the Customer Hub where the data is stored in parsed and well-defined fields.

### Forces

- Implementations differ—The information structures used with each information node cannot be changed (this is particularly true when the information originates from or is flowing to third parties, such as government agencies or existing or packaged applications).
- Information validation is sporadic—Not all information processes validate new information entered via its user interfaces or imported from external sources.

### Solution Description

Insert capability to transform the information so it is consumable by the information process.

This capability is called an information reengineering step. It executes as a step in an information process. This step may be in the original information process that needs the information, or in another information process that is preparing information in advance. See Figure 8.2.

### Solution Example

In the case of MCHS Trading's movement of Stores Account information into the Customer Hub, the bulleted activities are implemented as part of an Information Process that is implementing an Information Flow.

- Customer information, including name, address, and tax ID must be extracted from the Stores information collection.
- The customer name and address must be parsed and standardized to useful formats with separate fields, including first name, middle name, last name; and house number, directional value, street name, and street type using a Standardize Data pattern.
- Where multiple names are found on the same record, such as spouses holding a joint Stores account, a Separate Entries pattern is used to create one record per individual.
- The dates and tax ID fields are transformed into the appropriate structure and format for the customer information collection through a Restructure Data pattern.
- The customer information has an Enrich Data pattern that adds information from a third-party source with demographic data, such as date of birth and gender, and with geospatial data from another third-party source.
- Customer information entries representing the same person are connected through a Link Entries pattern on common criteria of standardized name, address, tax ID, date of birth, and gender.
- Where multiple representations of the same person are identified, the customer information uses a Merge Entries pattern with a preference given to the most complete and most recent data.
- The consolidated customer information entries are then loaded into the Customer information collection in the target information node.

### Benefits

- Information can be shared and synchronized between different information nodes.
- Information collections are enriched with associated and relevant information.
- Reengineering information dynamically whenever it is moved along the information supply chain means the information nodes are free to structure their information collections to suit their internal needs.

### Liabilities

- In reengineering information, there is the possibility that information may be lost, incorrectly transformed, or misapplied in the destination information node. The Information Identification patterns provide valuable guidance to the developer of an information reengineering step on how to work with the information.
- If there are many different information flows within the information supply chain, the burden of information reengineering can be high.

### Usage

Information reengineering is a primary activity in moving information from one information collection to another (extract, transform, load, or ETL, technologies being one example). Usage includes the following:

- Synchronizing multiple applications that host similar information collections
- Acquiring and merging (or consolidating) new information sources
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, Information Activity Hub, or Information Asset Hub
- Transforming and receiving Information Payloads from external systems If no alteration of data is required, then Information Reengineering patterns are not required (as in Messaging technology).

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Restructure Data

### Qualified Name

DesignPattern::Restructure Data

### Category

Information Reengineering Step Patterns

### Description

Use a mapping between the current structure and the intended structure to transform the information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

An information process is not able to consume information that is structured differently from the intended information collection.

Although two information nodes contain information collections for the same information subject area, there is no guarantee that the information nodes will store the information collections in the same format as each other. When information flows between the information nodes, this difference must be reconciled.

### Problem Example

MCHS Trading must move customer data from a Sales Account information collection to a Customer information collection and needs to restructure the data format:

- A tax ID is stored in the Sales Account collection as a character string consisting of three numbers, a hyphen, two numbers, a hyphen, and four numbers. The tax ID is stored in the Customer collection as a nine-digit integer.

### Forces

- Information structures cannot be changed—The structures used with each information collection cannot be changed (this is particularly true when the information originates from or is flowing to third parties, such as government agencies or existing or packaged applications).
- Information cannot be modified where it resides—The information nodes cannot restructure or modify the information directly (e.g., direct replication of the information cannot be applied).

### Solution Description

Use a mapping between the current structure and the intended structure to transform the information.

This restructuring could be done directly between the information nodes' structures or via a canonical information structure. The choice depends on how much other processing needs to be done in addition to the restructuring.

Develop common restructuring routines for known types of data to ensure consistent application of the transformation.

### Solution Example

In the case of MCHS Trading's movement of Sales Account information into the Customer Hub, for each field where there are inconsistent formats, convert the data to the target format:

- For the tax ID field, use functions to first trim any extraneous spaces from the Sales Account data, then remove all hyphens or other special characters from the data, and finally cast the remaining string of numeric values into an integer matching the format of the target information node.

### Benefits

- Consistent representation of information collections is achieved in the target information node without requiring modification of the source information node.
- Restructuring data dynamically whenever it is moved along the information supply chain means the information nodes are free to structure their information collections to suit their internal needs.

### Liabilities

- In restructuring information, there is the possibility that information may be lost, incorrectly transformed, or misapplied in the target information node.
- Changes made to content or format of the source information node may be missed or unhandled in the established data restructuring flow.
- If there are many different information flows within the information supply chain, the burden of data restructuring can be high.

### Usage

Restructuring data is a component of information reengineering and is achieved in technologies such as extract, transform, load (ETL) software and application programs.

Usage includes any situation where two different sources maintain different structural formats (e.g., character strings instead of integers) for the same information content, such as the following:

- Synchronizing information between multiple information nodes
- Acquiring and merging (or consolidating) new data sources
- Populating and maintaining information collections stored in an Information Warehouse, Information Mart, or Information Asset Hub
- Transforming and delivering messages from incoming information nodes to operational applications

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Standardize Data

### Qualified Name

DesignPattern::Standardize Data

### Category

Information Reengineering Step Patterns

### Description

Analyze and categorize the values in the information. Move them to the correct slots in the information structure.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information must flow and integrate from one information collection or node to another.

### Problem Statement

An information process is not able to consume some information because the values are not correctly stored in the information structure.

This is particularly common when the data originates from a user interface and it is entered with little validation. Names, addresses, and other free-form descriptive text typically suffer from this problem.

### Problem Example

MCHS Trading must move customer data from a Sales Account information collection to the Customer Hub and needs to standardize the data to make it consumable for additional reengineering purposes as well as the target information node:

- The customer name stored in the Sales Account collection is a free-form 50-character text field.
- The name may contain personal or organizational names.
- Personal names may include first name (actual, nickname, or initial), middle name, last name, salutation, title, and generational identifier (e.g., Dr. Anna M. Bowen, Mr. James Green Jr.).
- Organizational names may include company name, trading names (e.g., DBA, C/O), franchise information, division or department information, and contact details.

### Forces

- Information structures cannot be changed—The information structures used with each information node cannot be changed (this is particularly true when the information originates from or is flowing to third parties, such as government agencies or existing or packaged applications).
- Information cannot be modified where it resides—The information nodes cannot standardize or modify the information directly (e.g., direct replication of the information cannot be applied).
- Delays in delivery may occur—The information may not reach the target information node in a timely manner.
- Lack of understanding of the information—Contents of each information collection and node may not be understood, preventing standardization from being applied appropriately.
- Different requirements through the information supply chain—There may be differing requirements for standardization for the information flow (such as linking data for which highly parsed data is preferred) and the information node (for which a structured format may be needed).
- Too many patterns of data to handle—The total number of possible data format patterns or the presence of unrecognizable data format patterns in the source information node may preclude standardization of all information successfully.

### Solution Description

Analyze and categorize the values in the information. Move them to the correct slots in the information structure.

Parse the data and break it into its atomic parts, standardize the atomic values, and move/ reassemble the parts consistently back into the information structure.

Save and deliver the original data content if legal or organization requirements indicate this must be maintained.

This process requires domain knowledge to properly segment the data into atomic parts.

Establish reusable standardization routines to ensure consistent application to common data elements.

### Solution Example

In the case of MCHS Trading's movement of Sales Account information into the Customer Hub, the customer name information must be parsed and standardized to ensure correct usage later in the information supply chain:

- Identify and separate personal from organizational names.
- For personal names, separate (parse) the first, middle, and last names as well as title and generational values using known data patterns.
- Standardize the title and generational values.
- Identify a standardized first name based on common nickname values.
- Store the parsed and standardized values with the customer record for subsequent processing.

### Benefits

- Consistent representation of information collections is achieved in the target information node without requiring modification of the source information node.
- Standardizing data dynamically whenever it is moved along the information supply chain means the information nodes are free to structure their information collections to suit their internal needs.
- This pattern simplifies other information reengineering work, particularly linkage, enrichment, and merging of information, and should be done as early as possible in the information supply chain.

### Liabilities

- In standardizing information, there is the possibility that information may be lost, incorrectly standardized, or misapplied in the target information node.
- If there are many different information flows within the information supply chain, the burden of data standardization can be high.
- If there are many different formats of data within the source information node, the time to correctly identify standardization routines can be high and the processing time to standardize the data can be lengthy.

### Usage

Standardizing information is used in ETL processing typically as a precursor to linking or matching data. Standardization functions may be used in web services to ensure a canonical form, particularly after data entry of free-form text whether in operational applications or Master Data Management.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Enrich Data

### Qualified Name

DesignPattern::Enrich Data

### Category

Information Reengineering Step Patterns

### Description

Use either an authoritative source or an algorithm to add the missing information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

An information process is not able to consume some information because the values are incomplete.

This is particularly common where specific types of data such as postal verification files, geospatial data, government or industry standard data, or third-party, value-added information are from sources external to the organization.

### Problem Example

When new customer details are added to MCHS Trading's Customer Hub, they need to be enriched with geospatial coordinates used in regional customer marketing campaigns.

### Forces

- Information structures must be changed in order to enrich the data—Information may require restructuring or standardization before enrichment can be applied successfully.
- External sources are required—Information that cannot be calculated or derived from the originating information node must be acquired from external reference sources.

### Solution Description

Use either an authoritative source or an algorithm to add the missing information.

This may require human intervention if the missing information is unknown.

### Solution Example

The customer details do not contain geospatial data, but do contain address information, including street address, city, state, postal code, and country code. MCHS Trading has purchased a third-party geospatial data file. An enrich data reengineering step is added to the information process that accepts new customer details into the Customer Hub. This step will use the customer's address to look up and add the geospatial details to the appropriate information entry for this new customer.

### Benefits

- The destination information collection in the information supply chain will contain additional information unavailable in the originating information stores.

### Liabilities

- In enriching information, there is the possibility that information may be incorrectly enriched with the wrong information or misapplied in the target information node.
- If there are many different information flows within the information supply chain, data enrichment may be applied from differing "authoritative" sources.

### Usage

Enriching information is used when redeploying information to a different information node, and throughout its lifetime within an information node as more information attributes are discovered. Data enrichment may occur within ETL processing, through application programs, or through the use of web services.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Classify Data

### Qualified Name

DesignPattern::Classify Data

### Category

Information Reengineering Step Patterns

### Description

Step through the information values running the business rule, analytics model, or decision model against each group as appropriate. Record the classification based on the business rule.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

Information values need to be grouped according to a business rule, analytics model, or decision model.

How do you segment data within an information collection or an information payload?

### Problem Example

MCHS Trading must standardize and organize product data from multiple organizations before adding to the Product Hub but standardization and display requirements differ by type of product:

- The E-Shop and Mail-Shop Order applications distinguish five main categories (clothing, accessories, appliances, entertainment products, and grocery products) of products for purchase as well as additional subcategories.
- The product descriptions for each of these five main categories have unique requirements for standardization.
- There are particular rules based on a combination of UPC code, product name, and product description elements that determine the product category.

### Forces

- Information structures cannot be changed—The information structures used with each information node cannot be changed (this is particularly true when the information originates from or is flowing to third parties, such as government agencies or existing or packaged applications).
- Classification based on original information—Classification values must be calculated, retrieved, or derived from the data in the originating information store.
- Values need to be stored—Classification values may need to be stored in a reference collection if they change regularly for ease of maintenance.
- Lack of understanding of the information—Contents of each information collection and node may not be understood, preventing appropriate enrichment from occurring.

### Solution Description

Step through the information values running the business rule, analytics model, or decision model against each group as appropriate. Record the classification based on the business rule.

Evaluate and classify the values in the information nodes.

This process requires domain knowledge to properly segment the data into appropriate classifications.

Establish reusable classification routines to ensure consistent application to common data elements.

### Solution Example

In the case of MCHS Trading's Product Hub, the products must be classified to ensure correct usage later in the information supply chain:

- Identify the category of the UPC code by deriving the value from a reference source.
- Parse the product name and description for specific code attributes.
- Classify the product data into the current five categories by evaluating specific combinations of UPC category, product name attributes, and description attributes.
- Store the product classification for use on each product record.

### Benefits

- The destination information collection in the information supply chain will contain additional information unavailable in the originating information stores.

### Liabilities

- In classifying information, there is the possibility that information may be incorrectly classified with the wrong information or misapplied in the target information node, if the classification algorithms are not kept in sync with the incoming data.
- If there are many different information flows within the information supply chain, data classification may be applied from differing "authoritative" sources.

### Usage

Information classification is used to determine how information should be governed and managed. Classification is also used in ETL processing, in application programming, in web services, and in information reporting as a means to categorize data for subsequent use.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Check Data

### Qualified Name

DesignPattern::Check Data

### Category

Information Reengineering Step Patterns

### Description

Review the information values and flag those that are incorrect for remediation.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

An information collection must not store incorrect information.

How do you ensure the validity of information values within an information collection, or an information payload, or typed in by an information user?

### Problem Example

MCHS Trading has attempted to standardize the addresses on data from the Stores Account system to pass into the Customer Hub:

- The standardized addresses should have a combination of City, State, and Postal Code that are valid based on an authoritative postal reference source.
- The street address must be populated to ensure that invoices and mailings can be delivered to the customer.

### Forces

- Inconsistent validation—Different parts of an organization may have different definitions of the values that are valid for an attribute, and at which point in the processing the value must be in place. These differences may be because different silos of the organization developed them independently, or due to very different perspectives on how these values will be used. Either way, establishing consistent validation rules will require negotiation, compromise, and change—a common theme when setting up shared information resources.

### Solution Description

Review the information values and flag those that are incorrect for remediation.

Validation rules are defined in a Valid Values Definition. Step through the information values and check them against the valid values definition. Flag those that are incorrect for remediation.

This process requires domain knowledge to properly assign business rules for validation against the data.

Establish reusable validation routines to ensure consistent application to common information attributes.

### Solution Example

In the case of MCHS Trading's Stores Account address data, the addresses must be validated to ensure correct usage later in the information supply chain:

- Identify the valid values definition.
- Parse and standardize the addresses using the Standardize Data pattern to get optimal validation results.
- Check the combination of City, State, and Postal Code.
- Check the parsed Street Address for completeness.
- Mark the records with indicators where the rules were not passed and what rule violations occurred.
- Use the violation markings to classify the data as valid or invalid.
- Route the invalid data to a Staging Area against which the Correct Data pattern can be applied.

### Benefits

- The destination information collection in the information supply chain will contain valid information.

### Liabilities

- In validating information, there is the possibility that information may be incorrectly validated if the valid values definitions are not kept in sync with the incoming data content.
- If there are many different information flows within the information supply chain, data validation may be applied from differing "authoritative" sources.

### Usage

Validation of information should be used wherever information is received into an information node. It is typically applied in user interfaces or information services—either by its user interfaces or Information Services.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Correct Data

### Qualified Name

DesignPattern::Correct Data

### Category

Information Reengineering Step Patterns

### Description

Use either an authoritative source or an algorithm to correct the information. This may require human intervention.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

Information values are incorrect.

Information values need to be corrected based on one or more business rules relevant to the data, often requiring human intervention.

### Problem Example

MCHS Trading has attempted to standardize the addresses on data from the Stores Account system to pass into the Customer Hub:

- In using the Check Data pattern against the standardized addresses, 1% of the records have an incorrect combination of City, State, and Postal Code.
- Further, 100 records have no usable Street Address data.
- These records cannot be passed into the Customer Hub until the value issues are corrected.
- The incorrect records must be resolved and reprocessed.

### Forces

- Validation needed before use—The data content entering the information supply chain requires validation prior to loading into the target information node.
- Assessment based on original information—Valid data values, formats, and data combinations must be assessed from the data in the originating information store or from data standardized, enriched, or otherwise reengineered in the information supply chain.
- Information is time sensitive—Time dependencies may require that incorrect data be loaded into the target information node and corrected after that point.
- Invalid data must be stored and resolved—When incorrect data cannot be loaded into the target information node, the incorrect data must be held in a staging area or corrected in the originating information node.

### Solution Description

Use either an authoritative source or an algorithm to correct the information. This may require human intervention.

Check and evaluate the values in the information supply chain using the Check Data pattern.

Step through the information values reviewing the business rule that the data violated as appropriate. Record the correction based on the business rule.

If the incorrect records must flow into the target information node, then apply correction to the data at that point. The correction will likely require human intervention.

If the incorrect records cannot flow into the target, but can be captured in a staging area for review and correction, then apply correction to the data at that point. This may utilize algorithms where the appropriate correction can be system-generated or may need human intervention. This may be part of an Information Remediation Process pattern. Corrections may be routed back to the originating system as updates or may be recycled into the same or distinct Information Flow patterns.

### Solution Example

In the case of MCHS Trading's incorrect address data from the Stores Account information node, the addresses are first validated using the Check Data pattern:

- Identify the rule that the address data violated.
- Where the City, State, and Postal Code were not valid combinations, apply the Enrich Data pattern to provide the correct data and update the record. Recycle the record into the information supply chain.
- Where the City, State, and Postal Code were not valid combinations and could not be resolved through data enrichment or the address information cannot be resolved, manually review the data. Send a report or request to the Stores system to contact the customer and update the address.
- Once a record has been automatically resolved or manually reviewed, remove the record from the Staging Area.

### Benefits

- The destination information collection in the information supply chain will contain corrected data content.

### Liabilities

- If the volume of incorrect data is too high, particularly where manual review is required, data correction can be very costly.
- If there are many different information flows within the information supply chain, data correction may be applied from differing "authoritative" sources, resulting in further data quality issues across the information supply chain.

### Usage

Information should be corrected as soon at it is found to be invalid because it may cause confusion and mislead decision makers if it remains in its current state. Applications may incorporate steps to correct data. Data stewardship functions, particularly within Master Data Management, may include data correction. Web services and business processes may include steps to address and correct information.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Link Entries

### Qualified Name

DesignPattern::Link Entries

### Category

Information Reengineering Step Patterns

### Description

Link these information entries together so they can easily be retrieved as a group.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

Information entries in different information collections represent the same person, object, place, event, or activity.

The organization wants to document how the information entries in these information collections relate to one another.

### Problem Example

MCHS Trading is consolidating the customer account information from E-Shop and Stores along with details of recent orders from all of the order-taking applications together in Customer Hub. How should this information that related to a single person be brought together?

### Forces

- Information structures cannot be changed—The information structures used with each information collection often cannot be changed. This is particularly true when the information originates from or is flowing to third parties, such as government agencies or existing or packaged applications.
- Insufficient information to identify matching data—There may be insufficient information values stored in some of the information collections to determine which information entities should be linked together.
- Assessment based on original information—Information values in the different information collections may be inconsistent due to differences in the input validation, how well the information is kept up to date by the information processes managing the information collection, or human error.

### Solution Description

Link these information entries together so they can easily be retrieved as a group.

This linkage is recorded using Information Links. The information entries may be linked directly with one another, or a new information entry, possibly in a different information collection, is linked to the original information entries. Figure 8.3 illustrates the direct linking of information entries together. For an information entry to be linked to another, it needs to record the location and Information Key for the target information entry.

Figure 8.4 shows an alternative approach where a third information collection is used to hold the information links. This has the advantage that the linking does not impact the original information collections, although it is a bit more involved to navigate between the links.

### Solution Example

MCHS Trading elects to use the linking approach shown in Figure 8.4. The information collection that maintains the links contains customer details. It links to the account information and recent orders that comes from E-Shop, Mail-Shop, and Stores. (See Figure 8.5.)

### Benefits

- The relationship between the information elements is recorded and can be used by new information processes that need a more complete picture of the subject area than can be supplied by any one of the original information collections.

### Liabilities

- The information entries in the different information collections must be matched together accurately to ensure the right information entries are linked together. (See Information Matching Process.)
- The information links need to be maintained because information entries in any of the information collections may be updated or deleted, invalidating one or more links.

### Usage

Linking of related information entries is the philosophy of the linked data standards such as the Open Services Lifecycle and Collaboration (OSLC)1 standard. Data linkage or matching is utilized in ETL processing and Master Data Management (MDM) to connect related information entries and information payloads for subject areas such as Customer, Person, or Product.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Merge Entries

### Qualified Name

DesignPattern::Merge Entries

### Category

Information Reengineering Step Patterns

### Description

Create a new information entry that contains the best values from the information entries to be merged. Archive the previous information entries in case the merge needs to be reversed at a later time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

Multiple information entries in the same information collection represent the same person, event, object, place, or activity.

Multiple information entries representing the same "thing" can occur when there is ineffective input validation or when multiple independent sources of information have been merged.

### Problem Example

MCHS Trading has customer information arriving from its E-Shop, Mail-Shop, and Stores systems. Review of the Customer Hub shows many similar names with common addresses or email addresses as well as addresses that match but have distinct names:

- The multiple instances of similar or same records in the Customer Hub result in inconsistent customer views, marketing campaigns that either send out too much mail or miss likely customer targets.
- The multiple records for the same people also require more data storage and make information integration more complex.
1. http://open-services.net

### Forces

- Insufficient information to connect together—There may be insufficient information values to support matching of the information entries.
- Assessment based on original information—Information values in the different information collections may be inconsistent due to differences in the input validation, how well the information is kept up to date by the information processes managing the information collection, or human error.

### Solution Description

Create a new information entry that contains the best values from the information entries to be merged. Archive the previous information entries in case the merge needs to be reversed at a later time.

The best values to use in the merged information entry are determined by survivorship rules. These define rules for each attribute that may favor, say, the most recent value, or the value from the most reliable information node, or the value that is most commonly occurring in the information entries to be merged.

### Solution Example

MCHS Trading uses an Information Matching Process to establish which information entries should be merged together. The information stewards decide the survivorship rules and these information entries are merged into new information entries. The original information entries are archived in case any information entries are merged in error. An example of the merging of information entries is shown in Figure 8.6.

### Benefits

- Duplicated information is eliminated and a complete, coherent information entry is created.

### Liabilities

- If the merge happened in error, the information entries will need to be split apart again (see Separate Entries).

### Usage

Matching and merging information entries occurs when information is consolidated from multiple sources into a single information collection. Merging of data may occur in ETL processing or Master Data Management (MDM) solutions to consolidate related records in subject areas such as Customer, Person, or Product.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Separate Entries

### Qualified Name

DesignPattern::Separate Entries

### Category

Information Reengineering Step Patterns

### Description

Separate out the values into new information entries, one for each person, object, place, or activity. Archive the original information entry in case the split needs to be reversed or corrected at a later time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

A single information entry contains information about multiple people, objects, places, or activities.

How do you separate those data values and ensure correct content is reestablished within or across information collections or information payloads?

### Problem Example

MCHS Trading implements its new Customer Hub incorporating processes to match and merge information entries that relate to the same person. (See the Information Matching Process for more information on this type of processing.) Subsequent calls to the Customer-Care center indicate that some customers' orders were sent to the wrong individuals because some customer records were inappropriately merged together. Examples of incorrect customer record merging include the following:

- "Thomas Jones, 104 W. Elm St., Black Rock, WI" merged with "Thomas Jonas, 104 Elm Ave., Black Rock, WI"
- "Wm Holden, 128A Maine Sq, Carmelton, II" merged with "Will Holden, 128 Main Sq, Carmelton, IL" and "Willa Holden, 128C Maine Sq, Carmelton, IL" Subtle differences in spelling and location, errors, or a lack of sufficient information values can impact the reliability of such automated processes.

### Forces

- Re-creation of information may be required in the sources—When incorrectly merged data is already loaded into the target information node without the possibility of correctly separating the data, the incorrect data must be deleted in the target, and correct entries be re-created from the originating sources.

### Solution Description

Separate out the values into new information entries, one for each person, object, place, or activity. Archive the original information entry in case the split needs to be reversed or corrected at a later time.

### Solution Example

MCHS Trading modifies the thresholds on the Information Matching Process in the Customer Hub to include a clerical review whenever information entries are to be merged that are only a close match rather than an exact match. This clerical review helps to prevent the erroneous merging of information going forward.

MCHS Trading also uses clerical review to check the merges that have already taken place, so information entries can be split apart again if they were merged in error. This is possible because the Customer Hub keeps archived copies of the original information entries and creates a new information entry for the merged result.

### Benefits

- The destination information collection in the information supply chain will contain correctly segmented/separated data content.

### Liabilities

- If the volume of incorrectly merged data is too high, particularly where manual review is required, data separation can be very costly and could require a reload/remerge from the original sources.
- If there are many different information flows within the information supply chain, data separation may be applied from differing "authoritative" sources with differing merging and separation rules, resulting in further data quality issues across the information supply chain.

### Usage

Separating entries is required wherever they are being actively merged because mistakes occasionally happen. This capability is usually only found in Master Data Management (MDM) hubs.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Derive Value

### Qualified Name

DesignPattern::Derive Value

### Category

Information Reengineering Step Patterns

### Description

Only store the essential details and derive the other values when they are needed. (For example, age is derived from date of birth.)

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

Values within an information entry need to be consistent.

How do you ensure that those data values are consistent within or across information collections or data payloads?

### Problem Example

MCHS Trading has an array of customer information arriving from its E-Shop, Mail-Shop, and Stores systems that is subsequently passed to the Customer Hub, including the date of birth. The Reporting Hub does not require the demographic information for regular reports, but Marketing campaigns periodically require customer segmentation based on age (a value which changes over time).

### Forces

- Different levels of information required— Applications and information processes do not require the same level of information for specific information entries. Further, retention of information in multiple points increases both storage costs and the likelihood that synchronization issues will occur, resulting in incorrect information used or passed into subsequent processes.

### Solution Description

Only store the essential details and derive the other values when they are needed. (For example, age is derived from date of birth.)

### Solution Example

Only store a customer's demographic data, such as date of birth, in the Customer Hub. When a marketing campaign targets a specific customer segment based on age, retrieve the customers based on date of birth from the Customer Hub. Derive the value of customer age from the date of birth provided by the Customer Hub.

### Benefits

- Related attributes are kept consistent and use minimal storage.

### Liabilities

- If either the volume of data is high or the derivation of content is lengthy, then the timeliness of delivery in the information supply chain may not be sufficient to meet requirements.
- The algorithm used to derive the value must be the same throughout the information supply chain to ensure consistency.

### Usage

This type of processing is used in many systems to minimize the information that is stored and to ensure information entries are self-consistent. Examples of use can be found in application programming, information warehouses, and information reporting.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Derive Relationship

### Qualified Name

DesignPattern::Derive Relationship

### Category

Information Reengineering Step Patterns

### Description

Use analytics to detect common values that suggest a relationship.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

Are two or more information entries related in some way? How do you identify whether those information entries are connected when common keys or values are not present within or across information collections or data payloads?

Applications and information processes may need to associate information that is not related or not connected by common keys or values.

### Problem Example

MCHS Trading has an array of customer and order information in its E-Shop, Mail-Shop, and Stores systems that are subsequently passed to the Customer Hub. Which customers are parts of the same household?

### Forces

- Information structures cannot be changed—The information structures used with each information node cannot be changed (this is particularly true when the information originates from or is flowing to third parties, such as government agencies or existing or packaged applications).
- Insufficient data to determine relationships—There may be insufficient data to support derivation of relationships in the information nodes, requiring further enrichment or data collection.

### Solution Description

Use analytics to detect common values that suggest a relationship.

### Solution Example

MCHS Trading uses analysis of customer addresses to determine which individuals are in the same household.

### Benefits

- The information supply chain will derive or contain relationships otherwise unexpected in the original data sources.

### Liabilities

- The rules that derive relationships need to be carefully defined, and the results used with care, particularly when working with information about people, organizations, and external events because there are many exceptions in the real world.

### Usage

Deriving additional relationships occurs in information nodes where information is being aggregated and cross-referenced. Examples of use can be found in application programming, information warehouses, business analytics, and information reporting.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Smooth Data

### Qualified Name

DesignPattern::Smooth Data

### Category

Information Reengineering Step Patterns

### Description

Use a moving average to smooth out the effect of the outliers.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

A stream of information contains outlier values due to errors in data capture or initial data conditions.

How do you handle those data values within or across information collections or data payloads?

### Problem Example

MCHS Trading tracks customer order information arriving from its E-Shop, Mail-Shop, and Stores systems on a daily, weekly, and annual basis. Because the weeks are not consistent from year to year due to moving holidays and yearly start/end dates, certain anomalies occur, which skew inventory planning.

Can the customer order information be adjusted to compensate for the anomalies in data conditions at the time of information capture to correctly compare daily and weekly volumes from year to year?

### Forces

- Too costly to fix errors or outliers at initial input—For certain information, it is not possible or is too costly to fix errors or outliers introduced at the time of data capture. To smooth a data set is to create an approximating function that attempts to capture important patterns in the data, while leaving out noise or other fine-scale structures/rapid phenomena. Many different algorithms are used in smoothing such as the moving average.

### Solution Description

Use algorithms such as a moving average to smooth out the effect of data outliers or certain initial data conditions.

### Solution Example

In the case of MCHS Trading's customer order statistics, any aggregated information occurring during weeks with moving holidays must be smoothed:

- Identify the days and weeks that require smoothing across prior and subsequent days and weeks.
- Define and store algorithms to smooth data based on the targeted results.
- Smooth the data utilizing the established algorithms.
- Save the smoothed data in an information node if this is to be a regular process or in a report if this is a periodic request.

### Benefits

- The information supply chain will provide more consistent information that compensates for data outliers or differing initial data conditions.
- Smoothed data can be subsequently used for better reporting and analysis in the information supply chain.

### Liabilities

- Smoothed data only approximates possible data conditions and may mask important data anomalies or data conditions, which may not be understood at the time of reporting and analysis, and may result in inaccurate information products and delivery.

### Usage

Information smoothing is useful in monitoring of sensor data. Smoothing may also be used on data stored in the information warehouse or data marts to improve business intelligence and analytics results.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Sample Data

### Qualified Name

DesignPattern::Sample Data

### Category

Information Reengineering Step Patterns

### Description

Use information values profiling to understand the variability in the information and extract subsets of the information with the same characteristics.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An organization is designing how information collected for one purpose can be used for new purposes.

### Problem Statement

The volume of data is large, which requires a lot of capacity to process.

### Problem Example

MCHS Trading needs a representative sample of its customer details to support its Information Pattern Detection Process to create a predictive analytics model for its Next Best Action solution.

### Forces

- Timeliness of information is important—More data results in longer processing time.
- Difficult to identify a good sample—What is a representative sample of an information collection?

### Solution Description

Use information values profiling to understand the variability in the information and extract subsets of the information with the same characteristics.

### Solution Example

The Information Pattern Detection Process will use a private information collection of customer details and their related activities (Sandbox Usage). This information collection is populated from existing information collections in the Reporting Hub using Snapshot Provisioning. The Information Flow that implements the snapshot provisioning has a sample data step to select the information entries that will be added to the destination information collection.

### Benefits

- The information processes using the sampled information will execute quicker because they have less information to process.

### Liabilities

- If the sampling is not perfect, the resulting information collection will not represent a representative subset of the original information collections. An Information Values Profile will provide guidance on the range and frequency of information values within an information collection.

### Usage

Data sampling is a commonly used statistical technique for information analysis to reduce the volume of information required and the processing time necessary to perform the analysis.

### Search Keywords

- Patterns of Information Management
- Information Reengineering Step
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Guard

### Qualified Name

DesignPattern::Information Guard

### Category

Information Guard Patterns

### Description

Insert mechanisms into the information supply chain to verify that the right people are only using information for authorized purposes.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

Information has value to an organization. It is vulnerable to theft, loss, and damage; inappropriate use; and corruption.

### Problem Statement

The organization's information needs to be protected from inappropriate use and theft.

Information would be perfectly safe if no one could access it. It would also be irrelevant. So an organization creates access points in its IT systems to allow people and other systems to access the information.

The Internet has been a driving force and an enabler in terms of opening up the access to IT systems and linking them together. There is now a lot more information available and a higher expectation that an organization will make its information available to its customers, regulators, investors, the media, and the government.

Technology has become more sophisticated and organizations are able to put a variety of mechanisms in place to protect their information. At the same time, this sophistication means that the organization may not understand all of the capability it has running, creating loopholes for hackers and viruses.

How is an organization's information protected from theft, loss, and inappropriate use?

### Problem Example

MCHS Trading stores information about its customers. How can it be sure that this personal information is used appropriately?

### Forces

- Multiple copies of information—Valuable information is often needed by many information processes and so may be copied to multiple information nodes. Each copy represents a point of vulnerability.
- Selected users need access—Selected users will need different types of access to the information. It is unlikely that everyone will need all information.
- Appropriate protection—The level of protection given to information should be commensurate with its value or the harm it will do if it is compromised.
- Copying leaves no mark—When information is copied, the original is not affected. Therefore, copying has to be detected in the act as it is not possible to know that the information has been copied.

### Solution Description

Insert mechanisms into the information supply chain to verify that the right people are only using information for authorized purposes.

Information security must be deployed to every entry point to the systems. There are two basic underpinnings to information security:

- Authentication—Validating that a person or a system is who or what they claim to be. Typically, this is achieved through a user account that provides a user identifier and password. The password is secret to the individual (or system) and so it is assumed that anyone who knows the password is the person named in the user account. Alternatively, biometric information such as fingerprints and retinal scans may be used for high-security situations. Authentication is determined when a user or system first connects and remains active until they disconnect—or a time limit is reached.
- Authorization—Ensuring that an authenticated user is only given access to the resources that he or she is supposed to access. Typically, the resource owner manages authorization. The resource owner maintains a list of the users, or groups of users, that may have access to the resources and the level access permitted. Authorization is performed on every access to a resource. Once you know who a person or system is, and what they have access to, it is possible to enforce security around information, and audit that authorized users are using information appropriately. Because information can be morphed and copied, there are additional techniques that can be applied to reduce its sensitivity and make it suitable for broader uses. This includes the following:
- Masking—Blanking out information values that are sensitive, leaving other values intact so other people can use them.
- Anonymizing—Ensuring an individual cannot be identified from the information, while preserving the referential integrity of the information. For example, if the information showed details of five people living at a particular address, after anonymization, you would still know there were five people living at an address—but you would not know who they where or which address it was. This type of information is useful for research and trend analysis where the individual details are not significant.
- Encryption—This is the hiding of information using an algorithm that can only recover the information if a security key is provided. The intention is that only the originator and the intended recipients can read the information. Security and the protection of information take constant vigilance because the IT systems are constantly changing, and as a result, new points of vulnerability are being opened up.

### Solution Example

MCHS Trading has a number of mechanisms to protect customer information:

- All employees of MCHS Trading have their own user account (user ID/password) that they are not allowed to share. This means all use of information is attributable.
- A customer using the E-Shop has to log on to the site with his or her own user ID and password to review the customer details that the E-Shop stores or to place an order.
- Whenever payment details from a customer are displayed to an employee, or printed out, the account details are always masked with Xxxxx so they cannot be read.
- None of the information nodes will accept a request for customer details unless the request comes from an authenticated source (system/user).

### Benefits

- The information guard pattern provides mechanisms to ensure information is only available to the individuals who are authorized to use it.

### Liabilities

- Information guards take time to set up and maintain. They need constant maintenance to adapt to the changing user community and business use of the information. Using these mechanisms should not be too difficult for users or they will find ways to circumvent them. Examples of impractical security policies include the following:
- Setting password policies that are too complex results in users writing their passwords down (because no one can remember his or her password), and creates vulnerability.
- Making it too difficult to create a new user when a new person is brought into a team encourages the sharing of user accounts.
- Failing to delete a user account for an individual who has left the organization creates an opportunity for that user to continue to access the systems.

### Usage

The information guard patterns describe security and privacy features that are provided in the majority of commercial software, including applications, databases, and network systems. These include user logon credentials, encryption, anonymization and masking of data, physical security, detection of unusual patterns of use, and special procedures to ensure information is protected.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Data-Centric Access

### Qualified Name

DesignPattern::Data-Centric Access

### Category

Information Guard Patterns

### Description

Maintain lists of who is able to access each type of data and remove values that the caller is not authorized to see whenever he or she accesses the information.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to control who is able to see certain types of information.

### Solution Description

Maintain lists of who is able to access each type of data and remove values that the caller is not authorized to see whenever he or she accesses the information.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Function-Centric Access

### Qualified Name

DesignPattern::Function-Centric Access

### Category

Information Guard Patterns

### Description

Maintain lists of the actions each individual is able to perform and check these lists when the activity is requested.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to control who is able to perform a particular activity.

### Solution Description

Maintain lists of the actions each individual is able to perform and check these lists when the activity is requested.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Identity Propagation

### Qualified Name

DesignPattern::Identity Propagation

### Category

Information Guard Patterns

### Description

When a request is made for information from a remote information node, flow the identity of the requesting person and/ or process to the remote node to enable it to verify and record the request.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to identify who is performing actions on remote information.

### Solution Description

When a request is made for information from a remote information node, flow the identity of the requesting person and/ or process to the remote node to enable it to verify and record the request.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Identity Verification

### Qualified Name

DesignPattern::Identity Verification

### Category

Information Guard Patterns

### Description

Provide a unique electronic identifier for each person using the information systems and a mechanism, such as a password or biometric reader, to enable each individual to prove who he or she is.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to identify who is performing actions on local information.

### Solution Description

Provide a unique electronic identifier for each person using the information systems and a mechanism, such as a password or biometric reader, to enable each individual to prove who he or she is.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Trusted Node

### Qualified Name

DesignPattern::Trusted Node

### Category

Information Guard Patterns

### Description

Provide each information node with an identity that it is able to use to prove to the information nodes it is communicating with that it is an authorized member of the information supply chain.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to ensure an information node is legitimately part of the information supply chain.

### Solution Description

Provide each information node with an identity that it is able to use to prove to the information nodes it is communicating with that it is an authorized member of the information supply chain.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Anonymize Data

### Qualified Name

DesignPattern::Anonymize Data

### Category

Information Guard Patterns

### Description

Use algorithms to consistently replace real values with pseudonyms and securely record the mapping so the transformation can be applied consistently over time.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to hide the identity of an individual who is referenced in information flowing between information nodes. The information values still need to be valid values—but must hide the identity of the individual.

### Solution Description

Use algorithms to consistently replace real values with pseudonyms and securely record the mapping so the transformation can be applied consistently over time.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Collection Control

### Qualified Name

DesignPattern::Collection Control

### Category

Information Guard Patterns

### Description

Create information processes to control how collections of information are handled once they are exported outside of the care of the information supply chain.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to prevent collections of information from leaking outside of the information supply chain.

### Solution Description

Create information processes to control how collections of information are handled once they are exported outside of the care of the information supply chain.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Encrypt Data

### Qualified Name

DesignPattern::Encrypt Data

### Category

Information Guard Patterns

### Description

Use an encryption algorithm to transform information to make it unreadable to anyone except those possessing special knowledge, usually referred to as a key.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to prevent third parties from seeing information as it flows through the information supply chain.

### Solution Description

Use an encryption algorithm to transform information to make it unreadable to anyone except those possessing special knowledge, usually referred to as a key.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Interaction Analysis

### Qualified Name

DesignPattern::Interaction Analysis

### Category

Information Guard Patterns

### Description

Record the activity within the information supply chain and analyze for unexpected patterns as they are happening.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to detect fraudulent use of the information within the information supply chain.

### Solution Description

Record the activity within the information supply chain and analyze for unexpected patterns as they are happening.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Mask Data

### Qualified Name

DesignPattern::Mask Data

### Category

Information Guard Patterns

### Description

Use masking algorithms to obfuscate these values.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to hide certain data values as they are transmitted to parts of the information supply chain.

### Solution Description

Use masking algorithms to obfuscate these values.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Physical Security Zone

### Qualified Name

DesignPattern::Physical Security Zone

### Category

Information Guard Patterns

### Description

Keep the hardware in secure locations with access restricted to authorized people.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to prevent unauthorized people from accessing the hardware of the information supply chain.

### Solution Description

Keep the hardware in secure locations with access restricted to authorized people.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Separation of Duties

### Qualified Name

DesignPattern::Separation of Duties

### Category

Information Guard Patterns

### Description

Keep track of who is performing certain activities and the relationships between individuals. When a review or approval is required, ensure the person assigned to do it is not related to the original worker.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

It is necessary to ensure that certain activities are performed, reviewed, and approved by independent people.

### Solution Description

Keep track of who is performing certain activities and the relationships between individuals. When a review or approval is required, ensure the person assigned to do it is not related to the original worker.

### Search Keywords

- Patterns of Information Management
- Information Guard
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Probe

### Qualified Name

DesignPattern::Information Probe

### Category

Information Probe Patterns

### Description

Insert information probes into key points in the information supply chain to gather measurements for further analysis.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Context

An information centric organization is concerned with the efficient and accurate use of information.

### Problem Statement

The operation of an information supply chain needs to be monitored to ensure it is working properly.

### Problem Example

MCHS Trading wants to be sure that its information supply chains are working properly. For example, it wants to know that orders are being fulfilled on time, that its product descriptions are correct, and that its customer information is up to date. How does MCHS Trading achieve this?

### Forces

- Failures can occur at any time, in any place, for many reasons.
- Failures can ripple through the information supply chain—If a failure in an information supply chain is not detected and resolved in time, further failures can occur downstream as a consequence. For example, if information about monthly sales figures from one region is not loaded in time, the report that aggregates the sales figures for the whole organization will be wrong.
- Local knowledge is often required—It takes local knowledge to understand how a particular information process should be operating.
- Indiscriminant monitoring can generate a lot of data—The useful information is often buried within large volumes of data.

### Solution Description

Insert information probes into key points in the information supply chain to gather measurements for further analysis.

An information probe is a component that is called at key points in an information process. It is passed relevant information by the information process. It may simply store the information it is passed in an information collection, or perform some processing on it and then store the results, or perform some action, such as call a remote information service. Because it is operating in the mainline of the information process, it is designed to impose minimum overhead on the calling information process.

The information node that is hosting the information probe may offer facilities to configure the information probe. This configuration may control how much information is stored and any preprocessing that should be performed on the information passed to the information probe.

### Solution Example

MCHS Trading inserted information probes in each information process that supported its information supply chain and used the information from them to detect failures that would impact the quality of its information and operations.

### Benefits

- Information probes provide a flexible approach to extracting information about the internal behavior of an information process.

### Liabilities

- The processing within an information probe may slow down the operation of the calling information process.

### Usage

Information probes represent sensors, diagnostics tracing, monitoring probes, and other devices that generate information about the internal workings of an information process or information node.

The Common Base Event standard provides a comprehensive view of the type of information that should be emitted from an information probe: http://www.eclipse.org/tptp/platform/documents/resources/cbe101spec/CommonBaseEvent_ SituationData_V1.0.1.pdf

In particular, it describes the following situation types that cover most of the situations that a probe could report on:

- Start Situation—A component (such as an information node, information process, information service, or information trigger) is starting.
- Stop Situation—A component is stopping.
- Connect Situation—A component has connected to another. This means an information request has completed and the information guards in place have allowed the request.
- Configure Situation—A configuration has changed for a component.
- Request Situation—An information request has completed, either successfully or not.
- Feature Situation—An information process (or group of related information processes) is available, or no longer available.
- Dependency Situation—A component's dependency has either been met, or not.
- Create Situation—Something has been created, such as an information entry.
- Destroy Situation—Something has been deleted.
- Report Situation—A component is making a report about its current state or a subcomponent's state. This could be Performance, Security, Heartbeat, Status, Trace, Debug, or LOG.
- Available Situation—A component has completed its initialization and is available for work.
- Other Situation—Something else.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Access Auditing Probe

### Qualified Name

DesignPattern::Access Auditing Probe

### Category

Information Probe Patterns

### Description

Record the identity of who is accessing information and what activity he or she is performing from which information node.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Who is accessing and changing information?

### Solution Description

Record the identity of who is accessing information and what activity he or she is performing from which information node.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Entry Uniqueness Probe

### Qualified Name

DesignPattern::Entry Uniqueness Probe

### Category

Information Probe Patterns

### Description

Record the number of information entries that represent the same "thing" within the information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

How much duplicated information is located in an information collection?

### Solution Description

Record the number of information entries that represent the same "thing" within the information collection.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Environment Probe

### Qualified Name

DesignPattern::Environment Probe

### Category

Information Probe Patterns

### Description

Use sensors located at appropriate places in the environment and pipe the measurements they record into the information supply chain.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

When the state of the environment is changing, how do we incorporate its state into the information supply chain?

### Solution Description

Use sensors located at appropriate places in the environment and pipe the measurements they record into the information supply chain.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Information Flow Probe

### Qualified Name

DesignPattern::Information Flow Probe

### Category

Information Probe Patterns

### Description

Record details such as the number of payloads and amount of data and time, each time a data flow is initiated.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

How much information is flowing between two information nodes?

### Solution Description

Record details such as the number of payloads and amount of data and time, each time a data flow is initiated.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Operational Health Probe

### Qualified Name

DesignPattern::Operational Health Probe

### Category

Information Probe Patterns

### Description

Record operation health checks, such as availability, memory usage, CPU usage, and response times.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

Is a part of the information infrastructure operating successfully?

### Solution Description

Record operation health checks, such as availability, memory usage, CPU usage, and response times.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Profiling Rule Probe

### Qualified Name

DesignPattern::Profiling Rule Probe

### Category

Information Probe Patterns

### Description

Regularly run validation rules against all, or a representative subset, of the information values.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

What is the quality of the values in an information collection?

### Solution Description

Regularly run validation rules against all, or a representative subset, of the information values.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Sample Data Probe

### Qualified Name

DesignPattern::Sample Data Probe

### Category

Information Probe Patterns

### Description

Occasionally record samples of the values that are flowing between two nodes and analyze.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

What are the types of information values flowing between two information nodes?

### Solution Description

Occasionally record samples of the values that are flowing between two nodes and analyze.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

## Create Design Pattern
> Create or updates a design pattern.

### Display Name

Subject Area Probe

### Qualified Name

DesignPattern::Subject Area Probe

### Category

Information Probe Patterns

### Description

Compare the values from all, or a representative subset, of the related information entries in each information collection.

### Legal

Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter 8, "Information Protection".  © Copyright 2013 by International Business Machines Corporation.  All rights reserved.

### Problem Statement

How consistent are the values between a set of information collections from the same subject area?

### Solution Description

Compare the values from all, or a representative subset, of the related information entries in each information collection.

### Search Keywords

- Patterns of Information Management
- Information Probe
- Information Protection

### Version Identifier

1.0

### Status

ACTIVE

____

