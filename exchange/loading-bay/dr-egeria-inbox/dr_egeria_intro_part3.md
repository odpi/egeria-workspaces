# Adding more to the Egeria-Markdown Glossary

In the first two files created the Egeria-Markdown glossary with a few terms. In the second, we added a couple of
categories and then updated the existing terms to use them. In this installment, we will add a number of terms to the
glossary to make it a truly useful aid for the Dr.Egeria user. Once we have added the terms, we'll discuss how we can
continue to work with the terms using the `hey_egeria` commands.
___ 

# Create Term

## Term Name

Display

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Processing Dr.Egeria Markdown

## Summary

This is a processing directive to Dr.Egeria to request that the input text be processed for display only.

## Description

This is a processing directive to Dr.Egeria commands to request that the input text be processed and displaying. This is
useful to validate that the command processor is able to open the input text and shows that the environment is able to
process the text.

## Abbreviation

## Examples

## Usage

## Version

## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Validate

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Processing Dr.Egeria Markdown

## Summary
A processing directive to Dr.Egeria to request that the input text be validated for conformance to Dr. Egeria syntax
with the results being displayed and, depending on results, an output file incorporating suggested changes will be produced.
## Description
A processing directive to Dr.Egeria to request that the input text be validated for conformance to Dr. Egeria syntax. 

The results are displayed in the console, and include labeled messages. The labels may be:
* Info - just an information notice, for example, an optional field is empty.
* Warning - an issue was found, but we can automatically try to repair it or it doesn't prevent further processing.
* Error - A non-recoverable error input error was found - this command won't be processed further - for example if we encounter
a `Create Term` command and find that the term already exists.

Additional descriptive messages are also displayed. In some cases, for example if we detect a `Create` command for an 
object that already exists, we will also produce an output file that replaces the `Create` with an `Update` command.


## Abbreviation

## Examples
Default values for key environment variables in the **Egeria Workspaces** environment:
* EGERIA_ROOT_PATH=/home/jovyan
* EGERIA_INBOX_PATH=loading-bay/dr-egeria-inbox
* EGERIA_OUTBOX_PATH=distribution-hub/dr-egeria-outbox
* EGERIA_LOCAL_QUALIFIER=EGERIA

So place input files in the `loading-bay/dr-egeria-inbox` folder and look for output files in `distribution-hub/dr-egeria-outbox`.

## Usage
The EGERIA_ROOT_PATH is generally going to be set depending on what kind of environment you are using. For **Egeria Workspaces**,
when using the Jupyter environment, it will be set to Jupyter's default, which is `/home/jovyan`. 
* The location of the input file is based on the environment variables EGERIA_ROOT_PATH and EGERIA_INPUT_PATH.
* The output file will be written to the directory specified by the EGERIA_ROOT_PATH and EGERIA_OUTPUT_PATH environment
variables.

## Version
.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Process

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Processing Dr.Egeria Markdown

## Summary
The process directive indicates that we should apply the requested commands to Egeria if they are valid. 

## Description
The process directive indicates that we should apply the requested commands to Egeria if they are valid. Informational 
messages are provided on the console. A new file is produced that reflects the updates made and is designed to make
it easy to make further changes using the contents. For example, `Create` commands from the input file are written
out as `Update` statements in the output file. Qualified names and GUIDs generated during the create process are added
to the definitions in the output file.

## Abbreviation

## Examples
Default values for key environment variables in the **Egeria Workspaces** environment:
* EGERIA_ROOT_PATH=/home/jovyan
* EGERIA_INBOX_PATH=loading-bay/dr-egeria-inbox
* EGERIA_OUTBOX_PATH=distribution-hub/dr-egeria-outbox
* EGERIA_LOCAL_QUALIFIER=EGERIA

## Usage
During processing, informational messages will be displayed on the console. Please see the term entry for `Validate` for 
further description.

The EGERIA_ROOT_PATH is generally going to be set depending on what kind of environment you are using. For **Egeria Workspaces**,
when using the Jupyter environment, it will be set to Jupyter's default, which is `/home/jovyan`. 
* The location of the input file is based on the environment variables EGERIA_ROOT_PATH and EGERIA_INPUT_PATH.
* The output file will be written to the directory specified by the EGERIA_ROOT_PATH and EGERIA_OUTPUT_PATH environment
variables.

## Version
0.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Create Glossary

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary
Create a new Egeria glossary.

## Description
Create a new Egeria glossary with attributes for:
* Language
* Description
* Usage

## Abbreviation

## Examples


## Usage

## Version
0.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Update Glossary

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary
Updates the definition of an existing Egeria glossary.

## Description
This updates an existing Egeria glossary. The supplied attribute values are merged into the existing definition.

## Abbreviation

## Examples

## Usage

## Version
0.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Create Category

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary
Create a new glossary category in the specified glossary.

## Description
Creates a new glossary category in the specified glossary. Categories can be used to categorize glossary terms.
A category has an optional description.

## Abbreviation

## Examples

## Usage
Glossary categories have the following attributes:


| Attribute Name  | Input Required? | Read Only | Generated/Default? | Unique? | Notes                                                                                                    |
|:----------------|:----------------|-----------|:-------------------|:--------|:---------------------------------------------------------------------------------------------------------|
| Category Name   | Yes             | No        | No                 | No      | A display name (informal name).                                                                          |
| Owning Glossary | Yes             | No        | No                 | Yes     | This is the qualified name of the glossary that owns this category.                                      |
| Description     | No              | No        | No                 | No      | A textual description of this category                                                                   |
| Qualified Name  | No              | No        | Yes                | Yes     | The qualified name can either be provided by the user or generated. If generated, a pattern is followed. |
| GUID            | No              | Yes       | Yes                | Yes     | GUIDs are always generated by Egeria. They are meant for automation, not people.                         |
| Table           | No              | Yes       | Yes                | No      | Under development                                                                                        |
| Graph           | No              | Yes       | Yes                | No      | Under Development                                                                                        |

## Version
0.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Update Category

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary
Updates the definition of an existing Egeria category.


## Description
Updates the definition of an existing category. Currently the only field that can be updated is the `Description`.

## Abbreviation

## Examples

## Usage
Glossary categories have the following attributes:


| Attribute Name  | Input Required? | Read Only | Generated/Default? | Unique? | Notes                                                                                                    |
|:----------------|:----------------|-----------|:-------------------|:--------|:---------------------------------------------------------------------------------------------------------|
| Category Name   | Yes             | No        | No                 | No      | A display name (informal name).                                                                          |
| Owning Glossary | Yes             | No        | No                 | Yes     | This is the qualified name of the glossary that owns this category.                                      |
| Description     | No              | No        | No                 | No      | A textual description of this category                                                                   |
| Qualified Name  | No              | No        | Yes                | Yes     | The qualified name can either be provided by the user or generated. If generated, a pattern is followed. |
| GUID            | No              | Yes       | Yes                | Yes     | GUIDs are always generated by Egeria. They are meant for automation, not people.                         |
| Table           | No              | Yes       | Yes                | No      | Under development                                                                                        |
| Graph           | No              | Yes       | Yes                | No      | Under Development                                                                                        |

## Version
0.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Create Term

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary
Create a new glossary term with the given attributes in the specified Egeria glossary.

## Description
The process directive indicates that we should apply the requested commands to Egeria if they are valid. Informational 
messages are provided on the console. A new file is produced that reflects the updates made and is designed to make
it easy to make further changes using the contents. For example, `Create` commands from the input file are written
out as `Update` statements in the output file. Qualified names and GUIDs generated during the create process are added
to the definitions in the output file.

## Abbreviation

## Examples

## Usage
A glossary term has the following core attributes. Additional attributes, relationships and classifications can be added.


| Attribute Name  | Input Required? | Read Only | Generated/Default? | Unique? | Notes                                                                                                                 |
|:----------------|:----------------|:----------|:-------------------|:--------|:----------------------------------------------------------------------------------------------------------------------|
| Term Name       | Yes             | No        | No                 | No      | A display name (informal name).                                                                                       |
| Owning Glossary | Yes             | No        | No                 | Yes     | This is the qualified name of the glossary that owns this term.                                                       |
| Categories      | No              | No        | No                 | Yes     | This is the qualified (unique) name of the category. Multiple categories can be assigned, separated by a `,` or line. | 
| Description     | No              | No        | No                 | No      | A textual description of this term                                                                                    |
| Qualified Name  | No              | Yes       | No                 | Yes     | The qualified name can either be provided by the user or generated. If generated, a pattern is followed.              |
| GUID            | No              | Yes       | Yes                | Yes     | GUIDs are always generated by Egeria. They are meant for automation, not people.                                      |
| Table           | No              | Yes       | Yes                | No      | Under development                                                                                                     |
| Graph           | No              | Yes       | Yes                | No      | Under Development                                                                                                     |

## Version
0.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Update Term

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary
Updates the definition of an existing Egeria glossary term.

## Description
Updates the definition of an existing Egeria glossary term. Updated attributes are merged with the existing term values.

## Abbreviation

## Examples

## Usage
A glossary term has the following core attributes. Additional attributes, relationships and classifications can be added.


| Attribute Name  | Input Required? | Read Only | Generated/Default? | Unique? | Notes                                                                                                                 |
|:----------------|:----------------|:----------|:-------------------|:--------|:----------------------------------------------------------------------------------------------------------------------|
| Term Name       | Yes             | No        | No                 | No      | A display name (informal name).                                                                                       |
| Owning Glossary | Yes             | No        | No                 | Yes     | This is the qualified name of the glossary that owns this term.                                                       |
| Categories      | No              | No        | No                 | Yes     | This is the qualified (unique) name of the category. Multiple categories can be assigned, separated by a `,` or line. | 
| Description     | No              | No        | No                 | No      | A textual description of this term                                                                                    |
| Qualified Name  | No              | Yes       | No                 | Yes     | The qualified name can either be provided by the user or generated. If generated, a pattern is followed.              |
| GUID            | No              | Yes       | Yes                | Yes     | GUIDs are always generated by Egeria. They are meant for automation, not people.                                      |
| Table           | No              | Yes       | Yes                | No      | Under development                                                                                                     |
| Graph           | No              | Yes       | Yes                | No      | Under Development                                                                                                     |


## Version
0.1
## Status

DRAFT

## Qualified Name


___

# Create Term

## Term Name

Provenance

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Processing Dr.Egeria Markdown

## Summary
The `Provenance` command is used by Dr.Egeria to indicate the history of the Dr.Egeria input file.

## Description
When a Dr.Egeria input file is processed, it will look for a `Provenance` command. If one is not found, 
a new `Provenance` section will be created. Processing information (name of the file and timestamp) are appended
to this section. If a Dr.Egeria file is processed multiple times, a history of this processing will be created (presuming
the text is not deleted by the user). This simple, informal mechanism can be useful for basic scenarios. More sophisticated
scenarios would make use of more robust mechanisms such as version control and document management systems. 

Additionally, it is important to note that Egeria automatically maintains an audit history for each element. Additional
features for maintaining an update journal are also planned for Dr.Egeria.

## Abbreviation

## Examples
Default values for key environment variables in the **Egeria Workspaces** environment:
* EGERIA_ROOT_PATH=/home/jovyan
* EGERIA_INBOX_PATH=loading-bay/dr-egeria-inbox
* EGERIA_OUTBOX_PATH=distribution-hub/dr-egeria-outbox
* EGERIA_LOCAL_QUALIFIER=EGERIA

## Usage
During processing, informational messages will be displayed on the console. Please see the term entry for `Validate` for 
further description.

The EGERIA_ROOT_PATH is generally going to be set depending on what kind of environment you are using. For **Egeria Workspaces**,
when using the Jupyter environment, it will be set to Jupyter's default, which is `/home/jovyan`. 
* The location of the input file is based on the environment variables EGERIA_ROOT_PATH and EGERIA_INPUT_PATH.
* The output file will be written to the directory specified by the EGERIA_ROOT_PATH and EGERIA_OUTPUT_PATH environment
variables.

## Version
0.1
## Status

DRAFT

## Qualified Name


___

# Create Term

## Term Name

Create Personal Project

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary

This command defines a new personal project within Egeria. 
## Description
As the name suggests, personal projects are used by individuals to help projects that only involve them. While Egeria supports
several kinds of project, personal projects may be of particular interest to data scientists looking to track their
experiments.

## Abbreviation

## Examples

## Usage
Dr.Egeria processes uses the following attributes for a personal project:


| Attribute Name     | Input Required? | Read Only | Generated/Default? | Unique? | Notes                                                                                                    |
|:-------------------|:----------------|-----------|:-------------------|:--------|:---------------------------------------------------------------------------------------------------------|
| Project Name       | Yes             | No        | No                 | No      | A display name (informal name) of the project.                                                           |
| Project Identifier | No              | No        | No                 | No      | An optional shorthand name for the project.                                                              |
| Project Status     | No              | No        | No                 | No      | Status of the project, often from a list of Valid Values.                                                | 
| Description        | No              | No        | No                 | No      | A textual description of this project.                                                                   |
| Project Phase      | No              | No        | No                 | No      | Phase of the project, often from a list of Valid Values.                                                 |
| Project Health     | No              | No        | No                 | No      | Health of the project, often from a list of Valid Values.                                                |
| Start Date         | No              | No        | No                 | No      | Start date in the form YYYY-MM-DD                                                                        |
| Planned End Date   | No              | No        | No                 | No      | Planned completion date of the form YYY-MM-DD                                                            |
| Qualified Name     | No              | No        | Yes                | Yes     | The qualified name can either be provided by the user or generated. If generated, a pattern is followed. |
| GUID               | No              | Yes       | Yes                | Yes     | GUIDs are always generated by Egeria. They are meant for automation, not people.                         |
| Table              | No              | Yes       | Yes                | No      | Under development                                                                                        |
| Graph              | No              | Yes       | Yes                | No      | Under Development                                                                                        |

## Version
0.1
## Status

DRAFT

## Qualified Name

___

# Create Term

## Term Name

Update Personal Project

## Owning Glossary

Glossary::Egeria-Markdown

## Categories

Writing Dr.Egeria Markdown

## Summary

Update an existing Egeria personal project.

## Description

Update an en existing Egeria personal project.

## Abbreviation

## Examples

## Usage
Dr.Egeria processes uses the following attributes for a personal project:


| Attribute Name     | Input Required? | Read Only | Generated/Default? | Unique? | Notes                                                                                                    |
|:-------------------|:----------------|-----------|:-------------------|:--------|:---------------------------------------------------------------------------------------------------------|
| Project Name       | Yes             | No        | No                 | No      | A display name (informal name) of the project.                                                           |
| Project Identifier | No              | No        | No                 | No      | An optional shorthand name for the project.                                                              |
| Project Status     | No              | No        | No                 | No      | Status of the project, often from a list of Valid Values.                                                | 
| Description        | No              | No        | No                 | No      | A textual description of this project.                                                                   |
| Project Phase      | No              | No        | No                 | No      | Phase of the project, often from a list of Valid Values.                                                 |
| Project Health     | No              | No        | No                 | No      | Health of the project, often from a list of Valid Values.                                                |
| Start Date         | No              | No        | No                 | No      | Start date in the form YYYY-MM-DD                                                                        |
| Planned End Date   | No              | No        | No                 | No      | Planned completion date of the form YYY-MM-DD                                                            |
| Qualified Name     | No              | No        | Yes                | Yes     | The qualified name can either be provided by the user or generated. If generated, a pattern is followed. |
| GUID               | No              | Yes       | Yes                | Yes     | GUIDs are always generated by Egeria. They are meant for automation, not people.                         |
| Table              | No              | Yes       | Yes                | No      | Under development                                                                                        |
| Graph              | No              | Yes       | Yes                | No      | Under Development                                                                                        |

## Version
0.2
## Status

DRAFT

## Qualified Name


___

# Provenance

* Results from processing file dr_egeria_intro_part3.md on 2025-03-20 16:56