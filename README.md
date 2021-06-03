# hackerone2threadfix
This script enables a quick, automatic conversion from HackerOne .csv export to a compatible format for upload to ThreadFix.

HackerOne offers the ability to quickly export reports from a program via .csv file. This script takes the .csv file downloaded from HackerOne and converts it to a format that can be ingested by ThreadFix via their SSVL Converter tool.

## Reference Documentation
- HackerOne: create report export .csv file
    - https://docs.hackerone.com/programs/export-reports.html#export-select-reports-to-a-csv-file 
- ThreadFix: SSVL Converter tool can be used with mappings and changes specified below
    - formatting guidelines: https://denimgroup.atlassian.net/wiki/spaces/TDOC/pages/24088548/SSVL+Converter
    - tool reference: https://denimgroup.atlassian.net/wiki/spaces/TDOC/pages/496009270/ThreadFix+File+Format

## Field Mapping

| SSVL Field | H1 CSV Equivalent Field | Modification to H1 Field |
|---|---|---|
| Severity | severity_rating | capitalize first letter of values. SSLV converter doesn’t accept 'none' as a severity value in this column so replace 'None' with 'Info' |
| CWE | weakness | must be converted to integer representing the CWE. currently HackerOne exports it as text strings |
| Source | none | value for all reports should be 'HackerOne' |
| url | none | build from 'https://hackerone.com/reports/' + id |
| paramter | none | leave blank |
| NativeID | id | none |
| ShortDescription | title | none |
| LongDescription | none | need to snag report body |
| IssueID | none | leave blank |
| Date | reported_at | change date format to dd/mm/yyyy |
| SourceFileName | none | leave blank |
| LineNumber | none | SSVL converter expects this column to have a value since the input type is integer, otherwise it throws an exception. Value for all reports can be '1' |
| ColumnNumber | none | SSVL converter expects this column to have a value since the input type is integer, otherwise it throws an exception. Value for all reports can be '1' |
| LineText | none | leave blank |
