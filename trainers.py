import os
import json
from encoders import decodeTrainerFile

trainerNameDedupe = {}
trainers = []

directory = os.path.join(".", "trainers")
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".trainer"):
            trainerData = decodeTrainerFile(os.path.join(".", "trainers", file))
            trainerData["name"] = f'{trainerData["class_name"]} {trainerData["name"]}'
            # Check if the name has already been seen
            if trainerData["name"] in trainerNameDedupe:
                trainerNameDedupe[trainerData["name"]] = (
                    trainerNameDedupe[trainerData["name"]] + 1
                )
                trainerData[
                    "name"
                ] = f'{trainerData["name"]} ({trainerNameDedupe[trainerData["name"]]})'
            else:
                trainerNameDedupe[trainerData["name"]] = 1
            # If so, add a suffix to deduplicate the name
            del trainerData["class_name"]
            del trainerData["class"]
            del trainerData["partyCount"]
            trainerData["item1"] = trainerData["item1_name"]
            trainerData["item2"] = trainerData["item2_name"]
            trainerData["item3"] = trainerData["item3_name"]
            trainerData["item4"] = trainerData["item4_name"]
            del trainerData["item1_name"]
            del trainerData["item2_name"]
            del trainerData["item3_name"]
            del trainerData["item4_name"]
            if trainerData["item1"] == "None":
                del trainerData["item1"]
            if trainerData["item2"] == "None":
                del trainerData["item2"]
            if trainerData["item3"] == "None":
                del trainerData["item3"]
            if trainerData["item4"] == "None":
                del trainerData["item4"]
            for pkmn in trainerData["team"]:
                pkmn["name"] = pkmn["species_name"]
                del pkmn["species"]
                del pkmn["species_name"]
                pkmn["item"] = pkmn["item_name"]
                del pkmn["item_name"]
                if pkmn["item"] == "None":
                    del pkmn["item"]
                if trainerData["hasCustomAttacks"] == False:
                    del pkmn["move1"]
                    del pkmn["move2"]
                    del pkmn["move3"]
                    del pkmn["move4"]

            trainers.append(trainerData)

with open(os.path.join(".", "src", "trainers.json"), "w") as fjson:
    json.dump(trainers, fjson, indent=4, default=str)
