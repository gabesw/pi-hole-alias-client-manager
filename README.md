# Pi-hole Alias Client Manager
I created this project to make managing [alias clients](https://discourse.pi-hole.net/t/adding-alias-clients-to-pi-hole-ftl/37084) in your pi-hole more user-friendly, as no interface is provided by default. This is a work-in-progress and suggestions and PRs are welcome!

#### Contents
- [Overview](#overview)
- [Setup](#setup)

## Overview
This is a program written in [Python](https://www.python.org) by [@Gabesw](https://www.github.com/gabesw) that allows users to manage their alias clients in their pihole FTL database. As of right now, only an interactive CLI is provided, but a web-based GUI is to come.

## Setup
### Prerequisites
Ensure that Pi-hole is installed and configured and that Python 3 is installed.
### Getting Started
To run the CLI, navigate to the `src/` directory and run `sudo python3 cli.py` to start the interactive CLI. Root permissions are required to modify the FTL database.