import csv
import os
import json
from tokenize import Number

locations = []

# "Pokemon" columns
safeColumns = []


def getLocationByColIndex(index: int):
    for location in locations:
        if location["encounterIndex"] == index:
            return location


def getRoomByColIndex(location: dict, index):
    for room in location["rooms"]:
        if room["encounterIndex"] == index:
            return room


# TODO: Rock smash
# TODO: Seafloor
with open("encounters.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    i = 0
    for row in reader:
        rowIndex = i + 1
        # Extract locations from header
        if rowIndex == 5:
            for colIndex, col in enumerate(row):
                if col != "" and colIndex != 341:
                    finalName = col.split("**")[0].strip()
                    if finalName == "Cave of Origins":
                        finalName = "Cave of Origin"
                    location = {
                        "name": finalName,
                        "encounterIndex": colIndex,
                        "rooms": [
                            {
                                "name": "main",
                                "encounterIndex": colIndex,
                                "grass": [],
                                "surf": [],
                                "oldRod": [],
                                "goodRod": [],
                                "superRod": [],
                            }
                        ],
                    }
                    locations.append(location)

        # Extract sublocations from header
        if rowIndex == 6:
            for colIndex, col in enumerate(row):
                if col != "" and colIndex != 341:
                    location = getLocationByColIndex(colIndex)
                    if not location:
                        # Search for previous location
                        for tempColIndex in reversed(range(0, colIndex)):
                            location = getLocationByColIndex(tempColIndex)
                            if location:
                                break

                    if location:
                        room = getRoomByColIndex(location, colIndex)
                        if room:
                            # Overwrite the default name "main"
                            room["name"] = col
                        else:
                            # Insert a new room
                            location["rooms"].append(
                                {
                                    "name": col,
                                    "encounterIndex": colIndex,
                                    "grass": [],
                                    "surf": [],
                                    "oldRod": [],
                                    "goodRod": [],
                                    "superRod": [],
                                }
                            )

        # Extract safe columns
        if rowIndex == 7:
            for colIndex, col in enumerate(row):
                if col == "Pokemon":
                    safeColumns.append(colIndex)

        # Map encounters to locations
        if rowIndex >= 8 and rowIndex <= 35:
            for colIndex, col in enumerate(row):
                location = getLocationByColIndex(colIndex)
                if not location:
                    # Search for previous location
                    for tempColIndex in reversed(range(0, colIndex)):
                        location = getLocationByColIndex(tempColIndex)
                        if location:
                            break
                if col != "" and location and colIndex in safeColumns:
                    room = getRoomByColIndex(location, colIndex)
                    if room:
                        # Correct some typos in the original spreadsheet
                        col = col.strip()
                        if col == "Nidoran (M)":
                            col = "Nidoran♂"
                        elif col == "Nidoran (F)":
                            col = "Nidoran♀"
                        elif col == "Quilfish":
                            col = "Qwilfish"
                        elif col == "Luvdics":
                            col = "Luvdisc"
                        elif col == "Farfetch'd":
                            col = "Farfetch'D"
                        elif col == "Wishcash":
                            col = "Whiscash"
                        elif col == "Flaafy" or col == "Flaafly":
                            col = "Flaaffy"
                        elif col == "Charmleon":
                            col = "Charmeleon"
                        elif col == "Sandslah":
                            col = "Sandslash"
                        elif col == "Primape":
                            col = "Primeape"
                        elif col == "Tarkoal":
                            col = "Torkoal"
                        elif col == "Venasaur":
                            col = "Venusaur"
                        elif col == "Weeking":
                            col = "Weezing"
                        elif col == "Rhydpon":
                            col = "Rhydon"
                        elif col == "Sowbro":
                            col = "Slowbro"

                        encounterPreset = {
                            "name": col,
                            "encounterChance": int(row[colIndex + 1].replace("%", "")),
                            "level": row[colIndex + 2],
                        }
                        if "," in encounterPreset["level"]:
                            splitLevel = encounterPreset["level"].split(",")
                            encounterPreset["minLevel"] = int(splitLevel[0].strip())
                            encounterPreset["maxLevel"] = int(splitLevel[1].strip())
                        elif "-" in encounterPreset["level"]:
                            splitLevel = encounterPreset["level"].split("-")
                            encounterPreset["minLevel"] = int(splitLevel[0])
                            encounterPreset["maxLevel"] = int(splitLevel[1])
                        else:
                            encounterPreset["level"] = int(encounterPreset["level"])
                            encounterPreset["minLevel"] = encounterPreset["level"]
                            encounterPreset["maxLevel"] = encounterPreset["level"]

                        del encounterPreset["level"]

                        if rowIndex >= 8 and rowIndex <= 20:
                            room["grass"].append(encounterPreset)
                        elif rowIndex >= 21 and rowIndex <= 25:
                            room["surf"].append(encounterPreset)
                        elif rowIndex >= 26 and rowIndex <= 27:
                            room["oldRod"].append(encounterPreset)
                        elif rowIndex >= 28 and rowIndex <= 30:
                            room["goodRod"].append(encounterPreset)
                        elif rowIndex >= 30 and rowIndex <= 35:
                            room["superRod"].append(encounterPreset)
        i = i + 1

for location in locations:
    del location["encounterIndex"]
    for room in location["rooms"]:
        del room["encounterIndex"]
        if len(room["grass"]) == 0:
            del room["grass"]
        if len(room["surf"]) == 0:
            del room["surf"]
        if len(room["oldRod"]) == 0:
            del room["oldRod"]
        if len(room["goodRod"]) == 0:
            del room["goodRod"]
        if len(room["superRod"]) == 0:
            del room["superRod"]

with open(os.path.join(".", "src", "encounters.json"), "w") as fjson:
    json.dump(locations, fjson, indent=4, default=str)
