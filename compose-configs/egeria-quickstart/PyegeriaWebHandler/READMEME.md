<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Pyegeria Web Handler
The Pyegeria Web Handler is a python module that provides a web handler for the pyegeria command line interface. It is
used to execute Dr.Egeria commands from anything that can make a REST call - and that shares the same filesystem as
the Egeria runtime.

## Maintenance Notes
I seemed to have to put a version of dr_egeria_md.py in the root of the pyegeria-web-handler directory rather than 
just calling it from the md_processing module of pyegeria. I'm not sure why. However, what this does mean is that after
significant change (generally additions) to the Dr.Egeria md_processing module, you will need to copy the new version
of dr_egeria_md.py into the root of the pyegeria-web-handler directory and make a few checks and changes.

Check that the imports are correct. The name of the main routine is process_markdown_file. So if this changes in the
future, you will need to change either pyegeria_handler or dr_egeria_md.py to match. Other than that is should be a drop
in replacement.
