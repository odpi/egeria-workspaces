# Introduction to Dr.Egeria

Dr.Egeria is an Egeria markdown language and command set that allows users to write text-based markdown to exchange information with Egeria. It provides a simple yet powerful way for both business and technical users to collaborate and share information with the Egeria platform.
Several tutorial videos are available for [Dr.Egeria](https://youtu.be/s-lITSDRG8U?si=4aO0QAFAiBp5eQkd)

## What is Dr.Egeria?

Dr.Egeria is a specialized markdown language designed for interacting with the Egeria open metadata platform. Key features include:

- **Markdown-Based**: Uses familiar markdown syntax for easy readability and writing
- **Embedded Commands**: Special commands that can be interpreted by Egeria
- **Flexible Integration**: Can be embedded in plain text files or Jupyter Notebooks
- **Narrative Flow**: Commands can be interspersed with regular text, allowing for a natural narrative flow

## How Dr.Egeria Works

Dr.Egeria works through a simple process:

1. **Write**: Create markdown documents with embedded Dr.Egeria commands
2. **Place**: Put these documents in the dr-egeria-inbox directory
3. **Process**: Using either the command `dr_egeria_md` or selecting the same from `hey_egeria tui` to have Egeria process the commands
4. **Output**: Results are placed in the dr-egeria-outbox directory

## Use Cases for Dr.Egeria

Dr.Egeria can be used for a wide range of documents and purposes:

- **Policy Documents**: Define governance policies in a readable format
- **Design Documents**: Document system designs with embedded metadata
- **Data Specifications**: Define data structures and relationships
- **Analysis**: Perform and document metadata analysis in Jupyter notebooks
- **Collaboration**: Share metadata insights with both technical and non-technical team members
- **Documenting**: Dr.Egeria commands allow you to output Reports (in Markdown)
- **Testing**: Use Dr.Egeria files to automate testing of an Egeria deployment

## Getting Started with Dr.Egeria

To start using Dr.Egeria:

1. Explore the templates in the dr-egeria-outbox directory
2. Check out the [Dr.Egeria Templates](/Dr-Egeria-Samples/Dr.Egeria%20Templates.md) and the `dr_egeria_help` command for help in writing Dr.Egeria files.
3. Create your own markdown documents with Dr.Egeria commands
4. Place your documents in the dr-egeria-inbox directory
5. Run the `dr_egeria_md` command to process your markdown files. 
6. Check the dr-egeria-outbox directory for results

Dr.Egeria is continuously evolving with new capabilities and features being added regularly. Feedback and suggestions are welcome to help improve this powerful tool.
