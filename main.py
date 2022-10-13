import os
import json
from encoders import decodePKMNFile, pokedexLookup

pokemon = []


def formatGenderRatio(genderRatio: int):
    if genderRatio == 0:
        return "Always Male"
    if genderRatio == 254:
        return "Always Female"
    if genderRatio == 255:
        return "Genderless"
    return f"{round(genderRatio / 254 * 100)}% Female"


directory = os.path.join(".", "pkmn")
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".pkmn"):
            pkmnData = decodePKMNFile(os.path.join(".", "pkmn", file))
            pkmnData["name"] = file.replace(".pkmn", "").title()
            pkmnData["type1"] = pkmnData["type1_name"]
            pkmnData["type2"] = pkmnData["type2_name"]
            del pkmnData["type1_name"]
            del pkmnData["type2_name"]
            pkmnData["ability1"] = pkmnData["ability1_name"]
            pkmnData["ability2"] = pkmnData["ability2_name"]
            del pkmnData["ability1_name"]
            del pkmnData["ability2_name"]
            pkmnData["eggGroup1"] = pkmnData["eggGroup1_name"]
            pkmnData["eggGroup2"] = pkmnData["eggGroup2_name"]
            del pkmnData["eggGroup1_name"]
            del pkmnData["eggGroup2_name"]
            pkmnData["genderRatio"] = formatGenderRatio(pkmnData["genderRatio"])
            del pkmnData["unkA"]
            del pkmnData["unkB"]
            del pkmnData["unkC"]
            del pkmnData["unkD"]
            del pkmnData["unkE"]
            del pkmnData["unkF"]
            pkmnData["dex"] = pokedexLookup[pkmnData["name"]]
            pkmnData["dex"] = pokedexLookup[pkmnData["name"]]
            pokemon.append(pkmnData)

with open(os.path.join(".", "src", "pkmn.json"), "w") as fjson:
    json.dump(pokemon, fjson, indent=4, default=str)
