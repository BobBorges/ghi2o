# Github issues to org-mode

Python script to dump github issues from a repo to an org-mode file.


## Installation

- clone repo
- set bash alias (suggested: org-issues) pointing to main.py


## usage 

Make sure the Github CLI is installed and you're authenticated. 

Navigate to an existing repo and call the program via the alias. 

```
usage: main.py [-h] [-o ORG_FILE] [-s {open,closed,all}] [-n NUMBER]

Generate an org file from github issues.
    The `gh` command must be installed on $PATH.
    You must be authenticated.

optional arguments:
  -h, --help            show this help message and exit
  -o ORG_FILE, --org-file ORG_FILE
                        Path/filename of output org file.
  -s {open,closed,all}, --state {open,closed,all}
                        What kind of issues you want? (default: open)
  -n NUMBER, --number NUMBER
                        Number of issue to fetch.

```
