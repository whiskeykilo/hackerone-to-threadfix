#!/usr/bin/env python3
import os
import sys
import pandas
import requests
import argparse
import json
from datetime import datetime

## Usage
parser = argparse.ArgumentParser(
    description="""Script that enables a quick, API-based export from HackerOne to a compatible .csv format for fast upload to ThreadFix."""
)
parser.add_argument("h1_program_handle", help="your HackerOne program handle")
args = parser.parse_args()

## Variables
# API variables
headers = {"Accept": "application/json"}
url = "https://api.hackerone.com/v1/"

# get H1 API creds from OS variables
user = os.environ.get("H1_IDENTIFIER")
token = os.environ.get("H1_TOKEN")
program = os.environ.get("H1_PROGRAM")


## Functions
def json_extract(obj, key):
    """
    Recursively fetch values from nested JSON.
    """
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def query_api():
    """
    This function queries the HackerOne API for all reports in a given program
    """
    global raw
    # get all program reports from the H1 API
    raw = requests.get(
        "https://api.hackerone.com/v1/reports/",
        auth=(user, token),
        params={"filter[program][]": [sys.argv[1]]},
        headers=headers,
    )


def check_auth():
    """
    This function check that authentication & authorization is correct
    """
    # Check authentication & authorization
    if raw.status_code == 404:
        print("\nThe H1 API returned no data.\n")
        print(
            "There may be an issue with your authentication or authorization. Please check that your H1 API identifier, API token, program handle, and program permissions are all correct.\n"
        )
        print(
            "Helpful references:\n- https://api.hackerone.com\n- https://docs.hackerone.com"
        )
        exit()


def create_csv():
    """
    This function creates the CSV file from the API response
    """
    # create dataframe
    df = pandas.DataFrame()

    # convert response to json format
    response = raw.json()

    # Report IDs - data.id
    id_list = [response["data"][id]["id"] for id in range(len(response["data"]))]
    print("\nNumber of H1 reports found: " + str(len(id_list)) + "\n")
    # add to dataframe
    df["NativeID"] = id_list

    # Weaknesses - data.relationships.weakness.data.attributes.external_id
    cwe_list = []
    for id in range(len(id_list)):
        temp = response["data"][id]["relationships"]
        temp2 = "".join(json_extract(temp, "external_id"))
        cwe_list.append(temp2[4:])
    # add to dataframe
    df["CWE"] = cwe_list

    # Severities - data.relationships.severity.data.attributes.rating
    sev_list = []
    for id in range(len(id_list)):
        temp = response["data"][id]["relationships"]
        temp2 = "".join(json_extract(temp, "rating"))
        sev_list.append(temp2)
    # add to dataframe
    df["Severity"] = sev_list

    # Report Title - data.attributes.title
    title_list = []
    for id in range(len(id_list)):
        temp = response["data"][id]["attributes"]
        temp2 = "".join(json_extract(temp, "title"))
        title_list.append(temp2)
    # add to dataframe
    df["ShortDescription"] = title_list

    # Report Body - data.attributes.vulnerability_information
    body_list = []
    for id in range(len(id_list)):
        temp = response["data"][id]["attributes"]
        temp2 = "".join(json_extract(temp, "vulnerability_information"))
        body_list.append(temp2)
    # add to dataframe
    df["LongDescription"] = body_list

    # Date - data.attributes.created_at - 2021-04-07T17:34:57.748Z
    date_list = []
    for id in range(len(id_list)):
        temp = response["data"][id]["attributes"]
        temp2 = "".join(json_extract(temp, "created_at"))
        temp3 = temp2[:10]
        date = datetime.strptime(temp3, "%Y-%m-%d")
        date = date.strftime("%d/%m/%Y")
        date_list.append(date)
    # add to dataframe
    df["Date"] = date_list

    # Individual Report URLs
    url_list = []
    for i in range(len(id_list)):
        temp = "https://hackerone.com/reports/" + id_list[i]
        url_list.append(temp)
    # add to dataframe
    df["url"] = url_list

    # add columns to dataframe
    df.insert(0, "LineText", "")
    df.insert(0, "ColumnNumber", 1)
    df.insert(0, "LineNumber", 1)
    df.insert(0, "SourceFileName", "")
    df.insert(0, "IssueID", "")
    df.insert(0, "parameter", "")
    df.insert(0, "Source", "HackerOne")

    # fix severity values
    df.replace(to_replace="critical", value="Critical", inplace=True)
    df.replace(to_replace="high", value="High", inplace=True)
    df.replace(to_replace="medium", value="Medium", inplace=True)
    df.replace(to_replace="low", value="Low", inplace=True)
    df.replace(to_replace="none", value="Info", inplace=True)

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

    # write file
    df.to_csv("h1-export.csv", index=False)
    print("Here's a quick preview of the ThreadFix .csv file:\n")
    print(df[["Severity", "CWE", "ShortDescription", "Date"]])


## Main
if __name__ == "__main__":
    query_api()
    check_auth()
    create_csv()
