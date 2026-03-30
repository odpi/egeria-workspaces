#!/usr/local/apache2/venv/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import pkg_resources

# Enable detailed error reporting
cgitb.enable()

# Print HTTP headers
print("Content-Type: application/json")
print()  # Empty line to separate headers from body

try:
    # Get Python version
    python_version = sys.version

    # Get installed packages
    installed_packages = [f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set]

    # Check if pyegeria is installed
    pyegeria_installed = any(pkg.startswith("pyegeria==") for pkg in installed_packages)

    # Return environment information
    response = {
        "status": "success",
        "python_version": python_version,
        "cgi_available": "cgi" in sys.modules,
        "cgitb_available": "cgitb" in sys.modules,
        "pyegeria_installed": pyegeria_installed,
        "installed_packages": installed_packages
    }

    print(f'{{"status": "success", "python_version": "{python_version}", "cgi_available": {response["cgi_available"]}, "cgitb_available": {response["cgitb_available"]}, "pyegeria_installed": {response["pyegeria_installed"]}}}')

except Exception as e:
    # Return an error response if something goes wrong
    print('{"status": "error", "message": "An error occurred: ' + str(e) + '"}')
