# hackerone2threadfix
This script enables a quick, API-based export from HackerOne to a compatible .csv format for fast upload to ThreadFix.

HackerOne offers the ability to quickly export reports from a program via its API. This script takes HackerOne program data and converts it to a format that can be ingested by ThreadFix via their SSVL Converter tool.

## Installation
Python 3 recommended.

### Dependencies
These dependencies can optinally be installed using the requirements file:

```
sudo pip install -r requirements.txt
```

### Clone Repo
```
git clone https://github.com/whiskeykilosec/hackerone2threadfix.git
```

### API Authentication
1. Make sure you've created a HackerOne API token according to the instructions [here](https://docs.hackerone.com/programs/api-tokens.html).
2. Add your HackerOne API identifier as an OS environment variable named "H1_IDENTIFIER" and the token itself as "H1_TOKEN".

## Usage
For all options and instructions run: `python hackerone2threadfix.py -h`

## Reference Documentation
- HackerOne
    - https://api.hackerone.com
    - https://docs.hackerone.com
- ThreadFix: SSVL Converter tool can be used with mappings and changes specified below
    - formatting guidelines: https://denimgroup.atlassian.net/wiki/spaces/TDOC/pages/24088548/SSVL+Converter
    - tool reference: https://denimgroup.atlassian.net/wiki/spaces/TDOC/pages/496009270/ThreadFix+File+Format