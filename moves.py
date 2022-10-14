import os
import json
from encoders import decodeMoveFile

moveNameDedupe = {}
moves = []

directory = os.path.join(".", "moves")
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".ini"):
            moveData = decodeMoveFile(os.path.join(".", "moves", file))
            moves.append(moveData)


# Sort by index
movesSorted = sorted(moves, key=lambda x: int(x["index"]))

# Clean up the data
for move in movesSorted:
    del move["index"]
    # Move all fields from attackData to base object, equivalent of spread
    for key in move["attackData"]:
        move[key] = move["attackData"][key]

    del move["attackData"]

    move["type"] = move["type_name"]
    del move["type_name"]
    # Fix hidden power names
    if move["name"] == "Hidden Power" and move["power"] == 70:
        move["name"] = f'{move["name"]} ({move["type"]})'
        del move["description"]

with open(os.path.join(".", "src", "moves.json"), "w") as fjson:
    json.dump(movesSorted, fjson, indent=4, default=str)
