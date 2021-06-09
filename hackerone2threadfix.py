#!/usr/bin/env python3
import os
import pandas
import requests

headers = {"Accept": "application/json"}  # H1 API headers

# get H1 API creds from OS variables
user = os.environ.get("H1_IDENTIFIER")
token = os.environ.get("H1_TOKEN")

# read csv file. By default HackerOne will export as 'export.csv'
df = pandas.DataFrame()

# add columns
df.insert(0, "LineText", "")
df.insert(0, "ColumnNumber", 1)
df.insert(0, "LineNumber", 1)
df.insert(0, "SourceFileName", "")
df.insert(0, "Date", "")
df.insert(0, "IssueID", "")
df.insert(0, "LongDescription", "")
df.insert(0, "ShortDescription", "")
df.insert(0, "NativeID", "")
df.insert(0, "parameter", "")
df.insert(0, "url", "")
df.insert(0, "Source", "HackerOne")
df.insert(0, "CWE", "")
df.insert(0, "Severity", "")

# fix severity values
df.replace(to_replace="critical", value="Critical", inplace=True)
df.replace(to_replace="high", value="High", inplace=True)
df.replace(to_replace="medium", value="Medium", inplace=True)
df.replace(to_replace="low", value="Low", inplace=True)
df.replace(to_replace="none", value="Info", inplace=True)

# write file
df.to_csv("h1-export.csv", index=False)

print(df)