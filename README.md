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
or just grab the python file

### API Authentication
1. Make sure you've created a HackerOne API token according to the instructions [here](https://docs.hackerone.com/programs/api-tokens.html)
2. Add your HackerOne credentials as OS environment variables
    - the identifier as "H1_IDENTIFIER" 
    - the token as "H1_TOKEN"

## Usage
For all options and instructions run: `python hackerone2threadfix.py -h`

## Reference Documentation
HackerOne
- https://api.hackerone.com
- https://docs.hackerone.com

ThreadFix: SSVL Converter tool can be used with mappings and changes specified below
- formatting guidelines: https://denimgroup.atlassian.net/wiki/spaces/TDOC/pages/24088548/SSVL+Converter
- tool reference: https://denimgroup.atlassian.net/wiki/spaces/TDOC/pages/496009270/ThreadFix+File+Format

## Field Mapping

| SSVL Field | H1 API Equivalent Field | Modification to H1 Field |
|---|---|---|
| Severity | data.relationships.severity.data.attributes.rating | capitalize first letter of values. SSLV converter doesn’t accept 'none' as a severity value in this column so replace 'None' with 'Info' |
| CWE | data.relationships.weakness.data.attributes.external_id | trim “cwe-“ off the front |
| Source | none | value for all reports should be 'HackerOne' |
| url | none | build from 'https://hackerone.com/reports/' + data.id |
| parameter | none | leave blank |
| NativeID | data.id | none |
| ShortDescription | data.attributes.title | none |
| LongDescription | data.attributes.vulnerability_information | none |
| IssueID | none | leave blank |
| Date | data.attributes.created_at | comes in as ISO 8601. change date format to dd/mm/yyyy |
| SourceFileName | none | leave blank |
| LineNumber | none | SSVL converter expects this column to have a value since the input type is integer, otherwise it throws an exception. Value for all reports can be '1' |
| ColumnNumber | none | SSVL converter expects this column to have a value since the input type is integer, otherwise it throws an exception. Value for all reports can be '1' |
| LineText | none | leave blank |
