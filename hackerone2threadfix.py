#!/usr/bin/env python3
import pandas
import requests

# read csv file. By default HackerOne will export as 'export.csv'
df = pandas.read_csv("export.csv")
lines = len(df.index)  # row count

# update column names
df = df.rename(columns={"severity_rating": "Severity"})
df = df.rename(columns={"weakness": "CWE"})
df = df.rename(columns={"id": "NativeID"})
df = df.rename(columns={"title": "ShortDescription"})
df = df.rename(columns={"reported_at": "Date"})  # needs dd/mm/yyyy

# add new columns
df.insert(0, "Source", "HackerOne")
df.insert(0, "url", "")
df.insert(0, "parameter", "")
df.insert(0, "LongDescription", "")
df.insert(0, "IssueID", "")
df.insert(0, "SourceFileName", "")
df.insert(0, "LineNumber", 1)
df.insert(0, "ColumnNumber", 1)
df.insert(0, "LineText", "")

# reorder columns
df = df[
    [
        "Severity",
        "CWE",
        "Source",
        "url",
        "parameter",
        "NativeID",
        "ShortDescription",
        "LongDescription",
        "IssueID",
        "Date",
        "SourceFileName",
        "LineNumber",
        "ColumnNumber",
        "LineText",
    ]
]

# fix severity values
df.replace(to_replace="critical", value="Critical", inplace=True)
df.replace(to_replace="high", value="High", inplace=True)
df.replace(to_replace="medium", value="Medium", inplace=True)
df.replace(to_replace="low", value="Low", inplace=True)
df.replace(to_replace="none", value="Info", inplace=True)

# convert CWE string to integer


# write file
df.to_csv("h1-export-modified.csv", index=False)

print(df)