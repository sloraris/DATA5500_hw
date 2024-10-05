# api to call: https://api.covidtracking.com/v1/states/{state}/daily.json

import os
import requests
import json
import numpy as np
from datetime import datetime


# Read states from file
filepath = os.getcwd()
file = open(f"{filepath}/states_territories.txt", "r")
states = file.readlines()

# DEV: Testing states list (you know, so I don't create 50 files every time I test)
# tst = ["ca", "ut", "mn"]

# remove whitespace and call api for each state
for state in states:
    state = state.strip()
    req = requests.get(f"https://api.covidtracking.com/v1/states/{state}/daily.json")

    # convert json to dictionary
    data = json.loads(req.text)

    # write json to file
    with open(f"{state}.json", "w") as file:
        file.write(req.text)

    # facts to gather
    facts = {}
    facts["average_new_cases"] = 0
    facts["positive_increases"] = []
    facts["largest_increase"] = [0, 0]
    facts["recent_no_new_cases"] = 0
    facts["monthly_totals"] = {}

    # loop through days
    for day in data:
        # Convert date string to datetime object
        date = datetime.strptime(str(day["date"]), "%Y%m%d")
        month_key = date.strftime("%Y-%m")  # Format: YYYY-MM

        # Grab positive increases for each day
        facts["positive_increases"].append(day["positiveIncrease"])

        # Update day of largest increase in cases if necessary
        if day["positiveIncrease"] > facts["largest_increase"][1]:
            facts["largest_increase"][0] = day["date"]
            facts["largest_increase"][1] = day["positiveIncrease"]

        # Update most recent day with no new increases if necessary
        if day["date"] > facts["recent_no_new_cases"] and day["positiveIncrease"] == 0:
            facts["recent_no_new_cases"] = day["date"]

        # Add daily increase to relevant monthly total increase
        if month_key not in facts["monthly_totals"]:
            facts["monthly_totals"][month_key] = 0
        facts["monthly_totals"][month_key] += day["positiveIncrease"]

    # Calculate average number of new daily confirmed cases
    facts["average_new_cases"] = np.mean(facts["positive_increases"])

    # Find month with highest and lowest increase
    highest_month = max(facts["monthly_totals"], key=facts["monthly_totals"].get)
    lowest_month = min(facts["monthly_totals"], key=facts["monthly_totals"].get)

    # Output facts to console
    print(f"\nState: {state}")
    print(f"Average daily increase: {facts['average_new_cases']:.2f}")
    print(f"Day of highest increase: {facts['largest_increase']}")
    print(f"Most recent day with no increase: {facts['recent_no_new_cases']}")
    print(f"Month with highest increase: {highest_month} ({facts['monthly_totals'][highest_month]})")
    print(f"Month with lowest increase: {lowest_month} ({facts['monthly_totals'][lowest_month]})")
