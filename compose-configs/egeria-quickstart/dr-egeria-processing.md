Two deployments of Egeria are provided in this repository: *quickstart* and *freshstart*. The *freshstart* deployment
includes a secrets location that is seeded with template secrets on first run. This allows you to customize the secrets
for your environment without modifying the image or source repository, and without worrying about losing them during
upgrades or if containers are destroyed. The secrets location is `runtime-volumes/freshstart-platform-data/secrets` on
the host, and is mounted to `/deployments/secrets` inside the container. You can place any secrets files you need here,
and they will be available to Egeria at runtime.

Both deployments support the processing of Markdown files containing Dr. Egeria commands.

The deployments contain a PyegeriaWebHandler server that monitors the `landing-area` directory for new markdown files.
When a new file is added, it is automatically processed by the PyegeriaWebHandler, which executes the Dr. Egeria
commands contained within the file and generates output in the `distribution-hub` directory. These commands are
currently
triggered by an Obsidian Plugin ( found in, for example
exchange-quickstart/.obsidian/plugins/egeria-obsidian-plugin/README.md )

The egeria-quickstart version of PyegeriageWebHandler is currently more advanced than the egeria-freshstart version, and
includes support for a wider range of Dr. Egeria commands. The egeria-freshstart version is more basic and only supports
a limited set of commands, but it is designed to be easily extensible so that you can add support for additional
commands as needed.

The PyegeriaWebHandler uses the capabilities and libraries of pyegeria - which includes the Dr. Egeria md_processing
module - to process the markdown files and execute the commands. This means that any updates or improvements to
pyegeria's command handling will also benefit the PyegeriaWebHandler, as long as the relevant command handlers are
re-exported in `pyegeria.view.md_processing_utils` and the main processing routine in `dr_egeria_md.py` is kept up to
date with any changes to the command handler interfaces.

There are a number of design, debugging and implementation issues to resolve. 
1) Currently, PyegeriaWebHandler does not support the full command set of Dr.Egeria. Dr.Egeria currently has 10 command families and over 120 commands - and continues to expand.
2) Because Dr.Egeria continues to evolve, it would be best if the PyegeriaWebHandler could automatically support new commands as they are added to Dr.Egeria, without needing manual updates to the handler. 
This would require some way for the handler to discover available command handlers from pyegeria and dispatch to them dynamically, rather than relying on a hardcoded list of supported commands.
During deployment, the latest version of pyegeria can be installed from pypi - and potentially refreshed at need.
3) The Obsidian plugin is currently the only way to invoke PyegeruaWebHandler - it would be nice to consider how to 
generalize this to support a form of (initially) local MCP from other tools.
4) The Obsidian plugin itself may need updating to bring javascript/typescript code up to date and ensure no deprecated dependencies. It would also be nice if the error handling was improved to be more helpful.
5) I'm open to other opportunities to simplify deployment, maintenance and use Dr Egeria and its use from Obsidian and MCP, and to make it more robust and user friendly. For example, it would be nice if the PyegeriaWebHandler could automatically refresh its pyegeria installation to pick up new command handlers without needing a manual restart. It would also be good to have better logging and error handling to help users troubleshoot issues with their markdown files and commands.
6) After testing and approval, this work will also need to be supported in egeria-freshstart deployments.