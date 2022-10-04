import math
import struct
from typing import BinaryIO

# Useful for detecting booleans, enums, indexes etc
valueSamples = {}
def sampleValue(tag : str, value):
    if not tag in valueSamples:
        valueSamples[tag] = {
            "min": math.inf,
            "max": -math.inf,
            "all": {}
        }
    if type(value) == int or type(value) == float:
        valueSamples[tag]["min"] = min(value, valueSamples[tag]["min"])
        valueSamples[tag]["max"] = max(value, valueSamples[tag]["max"])
    if not value in valueSamples[tag]["all"]:
        valueSamples[tag]["all"][value] = 0
    valueSamples[tag]["all"][value] += 1
    return value

dump_struct_debug_info = False

def getStructSize(struct_fields : list):
    totalSize = 0
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["size"] = 1
        elif field["type"] == "short":
            field["size"] = 2
        elif field["type"] == "ushort":
            field["size"] = 2
        elif field["type"] == float:
            field["size"] = 4

        totalSize += field["size"]

    return totalSize

def readStructArray(byte_read : bytes, offset : int, length : int, struct_fields : list):
    decoded_struct_array = []
    read_head = offset
    struct_size = getStructSize(struct_fields)
    for i in range(length):
        decoded_struct_array.append(readStruct(byte_read, read_head, struct_fields))
        read_head += struct_size
    return decoded_struct_array

def readStruct(byte_read : bytes, offset : int, struct_fields : list):
    read_head = offset
    decoded_struct = {}
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["type"] = "uint"
            field["size"] = 1
        if field["type"] == "short":
            field["type"] = int
            field["size"] = 2
        elif field["type"] == "ushort":
            field["type"] = "uint"
            field["size"] = 2

        # Actual reads
        if field["type"] == int:
            decoded_struct[field["name"]] = int.from_bytes(byte_read[read_head:read_head + field["size"]], byteorder="big", signed=True)
        elif field["type"] == "uint":
            decoded_struct[field["name"]] = int.from_bytes(byte_read[read_head:read_head + field["size"]], byteorder="big")
        elif field["type"] == float:
            field["size"] = 4
            decoded_struct[field["name"]] = struct.unpack('>f', byte_read[read_head:read_head+4])[0]
        elif field["type"] == bool:
            decoded_struct[field["name"]] = True if int.from_bytes(byte_read[read_head:read_head + field["size"]], byteorder="big") else False
        elif field["type"] == bytes:
            decoded_struct[field["name"]] = byte_read[read_head:read_head + field["size"]].hex(" ").upper()
        else:
            print("Unknown field type in readStruct(): " + field["type"])

        if "index_of" in field:
            index_offset = 0
            if "index_offset" in field:
                index_offset = field["index_offset"]

            if decoded_struct[field["name"]] + index_offset < len(field["index_of"]):
                decoded_struct[field["name"] + "_name"] = field["index_of"][decoded_struct[field["name"]] + index_offset]
            else:
                decoded_struct[field["name"] + "_name"] = "Unknown " + hex(decoded_struct[field["name"]] + index_offset)

        if "sample" in field:
            sampleName = field["sample"] if type(field["sample"]) == str else field["name"]
            sampleValue(sampleName, decoded_struct[field["name"]])

        read_head += field["size"]
    
    if dump_struct_debug_info:
        decoded_struct["DEBUG_File_Address"] = hex(offset)

    return decoded_struct

def writeStructArray(fh : BinaryIO, struct_array : list, struct_fields: list, include_count : bool = False, count_bytes : int = 0):
    if include_count:
        fh.write(len(struct_array).to_bytes(count_bytes, byteorder="big"))
    
    for struct_data in struct_array:
        writeStruct(fh, struct_data, struct_fields)

def writeStruct(fh : BinaryIO, struct_data : dict, struct_fields : list):
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["type"] = "uint"
            field["size"] = 1
        elif field["type"] == "short":
            field["type"] = int
            field["size"] = 2
        elif field["type"] == "ushort":
            field["type"] = "uint"
            field["size"] = 2

        # Actual reads
        if field["type"] == int:
            fh.write(int(struct_data[field["name"]]).to_bytes(field["size"], byteorder="big", signed=True))
        elif field["type"] == "uint":
            fh.write(int(struct_data[field["name"]]).to_bytes(field["size"], byteorder="big"))
        elif field["type"] == float:
            fh.write(struct.pack('>f', struct_data[field["name"]]))
        elif field["type"] == bool:
            fh.write(bytes([1 if struct_data[field["name"]] else 0]))
        elif field["type"] == bytes:
            fh.write(bytes.fromhex(struct_data[field["name"]]))
        else:
            print("Unknown field type in readStruct(): " + field["type"])

eggGroups = [
    "None", # 0
    "Monster", # 1
    "Water 1", # 2
    "Bug", # 3
    "Flying", # 4
    "Field", # 5
    "Fairy", # 6
    "Grass", # 7
    "Human Like", # 8
    "Water 3", # 9
    "Mineral", # 10
    "Amorphous", # 11
    "Water 2", # 12
    "Ditto", # 13
    "Dragon", # 14
    "Undiscovered", # 15
]

types = [
    "Normal", # 0
    "Fighting", # 1
    "Flying", # 2
    "Poison", # 3
    "Ground", # 4
    "Rock", # 5
    "Bug", # 6
    "Ghost", # 7
    "Steel", # 8
    "Unknown 9", # Hmmmmm
    "Fire", # 10 
    "Water", # 11
    "Grass", # 12
    "Electric", # 13
    "Psychic", # 14
    "Ice", # 15
    "Dragon", # 16,
    "Dark", # 17
]

abilities = [
    "None",
    "Stench",
    "Drizzle",
    "Speed Boost",
    "Battle Armor",
    "Sturdy",
    "Damp",
    "Limber",
    "Sand Veil",
    "Static",
    "Volt Absorb",
    "Water Absorb",
    "Oblivious",
    "Cloud Nine",
    "Compound Eyes",
    "Insomnia",
    "Color Change",
    "Immunity",
    "Flash Fire",
    "Shield Dust",
    "Own Tempo",
    "Suction Cups",
    "Intimidate",
    "Shadow Tag",
    "Rough Skin",
    "Wonder Guard",
    "Levitate",
    "Effect Spore",
    "Synchronize",
    "Clear Body",
    "Natural Cure",
    "Lightning Rod",
    "Serene Grace",
    "Swift Swim",
    "Chlorophyll",
    "Illuminate",
    "Trace",
    "Huge Power",
    "Poison Point",
    "Inner Focus",
    "Magma Armor",
    "Water Veil",
    "Magnet Pull",
    "Soundproof",
    "Rain Dish",
    "Sand Stream",
    "Pressure",
    "Thick Fat",
    "Early Bird",
    "Flame Body",
    "Run Away",
    "Keen Eye",
    "Hyper Cutter",
    "Pickup",
    "Truant",
    "Hustle",
    "Cute Charm",
    "Plus",
    "Minus",
    "Forecast",
    "Sticky Hold",
    "Shed Skin",
    "Guts",
    "Marvel Scale",
    "Liquid Ooze",
    "Overgrow",
    "Blaze",
    "Torrent",
    "Swarm",
    "Rock Head",
    "Drought",
    "Arena Trap",
    "Vital Spirit",
    "White Smoke",
    "Pure Power",
    "Shell Armor",
    "Cacophony",
    "Air Lock",
]

pkmn_file_struct = [
    {"type": "byte", "name": "hp"}, # 0x0
	{"type": "byte", "name": "attack"}, # 0x1
	{"type": "byte", "name": "defense"}, # 0x2
	{"type": "byte", "name": "speed"}, # 0x3
	{"type": "byte", "name": "specialAttack"}, # 0x4
	{"type": "byte", "name": "specialDefense"}, # 0x5
	{"type": "byte", "name": "type1", "index_of": types}, # 0x6
	{"type": "byte", "name": "type2", "index_of": types}, # 0x7
	{"type": "byte", "name": "catchRate"}, # 0x8
	{"type": "byte", "name": "EXPYield"}, # 0x9
	{"type": "byte", "name": "unkA"},
	{"type": "byte", "name": "unkB"},
	{"type": "byte", "name": "unkC"},
	{"type": "byte", "name": "unkD"},
	{"type": "byte", "name": "unkE"},
	{"type": "byte", "name": "unkF"},
	{"type": "byte", "name": "genderRatio"},# "index_of": genderRatios}, # 0x10 - male 0, female 254, genderless 255, half 31, 75% female 127
	{"type": "byte", "name": "hatchRate"}, # 0x11
	{"type": "byte", "name": "baseHappiness"}, # 0x12
	{"type": "byte", "name": "EXPGrowthRate"}, # 0x13
	{"type": "byte", "name": "eggGroup1", "index_of": eggGroups}, # 0x14
	{"type": "byte", "name": "eggGroup2", "index_of": eggGroups}, # 0x15
	{"type": "byte", "name": "ability1", "index_of": abilities}, # 0x16
	{"type": "byte", "name": "ability2", "index_of": abilities}, # 0x17
	{"type": "byte", "name": "safariZoneRunRate"}, # 0x18
	{"type": "byte", "name": "color"}, # 0x19
]

def decodePKMNFile(encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        return readStruct(byte_read, 0, pkmn_file_struct)