import math
import struct
from typing import BinaryIO

# Useful for detecting booleans, enums, indexes etc
valueSamples = {}


def sampleValue(tag: str, value):
    if not tag in valueSamples:
        valueSamples[tag] = {"min": math.inf, "max": -math.inf, "all": {}}
    if type(value) == int or type(value) == float:
        valueSamples[tag]["min"] = min(value, valueSamples[tag]["min"])
        valueSamples[tag]["max"] = max(value, valueSamples[tag]["max"])
    if not value in valueSamples[tag]["all"]:
        valueSamples[tag]["all"][value] = 0
    valueSamples[tag]["all"][value] += 1
    return value


dump_struct_debug_info = False


def getStructSize(struct_fields: list):
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


def readStructArray(byte_read: bytes, offset: int, length: int, struct_fields: list):
    decoded_struct_array = []
    read_head = offset
    struct_size = getStructSize(struct_fields)
    for i in range(length):
        decoded_struct_array.append(readStruct(byte_read, read_head, struct_fields))
        read_head += struct_size
    return decoded_struct_array


def readStruct(byte_read: bytes, offset: int, struct_fields: list):
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
            decoded_struct[field["name"]] = int.from_bytes(
                byte_read[read_head : read_head + field["size"]],
                byteorder="little",
                signed=True,
            )
        elif field["type"] == "uint":
            decoded_struct[field["name"]] = int.from_bytes(
                byte_read[read_head : read_head + field["size"]], byteorder="little"
            )
        elif field["type"] == float:
            field["size"] = 4
            decoded_struct[field["name"]] = struct.unpack(
                ">f", byte_read[read_head : read_head + 4]
            )[0]
        elif field["type"] == bool:
            decoded_struct[field["name"]] = (
                True
                if int.from_bytes(
                    byte_read[read_head : read_head + field["size"]], byteorder="little"
                )
                else False
            )
        elif field["type"] == bytes:
            decoded_struct[field["name"]] = (
                byte_read[read_head : read_head + field["size"]].hex(" ").upper()
            )
        else:
            print("Unknown field type in readStruct(): " + field["type"])

        if "index_of" in field:
            index_offset = 0
            if "index_offset" in field:
                index_offset = field["index_offset"]

            if decoded_struct[field["name"]] + index_offset < len(field["index_of"]):
                decoded_struct[field["name"] + "_name"] = field["index_of"][
                    decoded_struct[field["name"]] + index_offset
                ]
            else:
                decoded_struct[field["name"] + "_name"] = "Unknown " + hex(
                    decoded_struct[field["name"]] + index_offset
                )

        if "sample" in field:
            sampleName = (
                field["sample"] if type(field["sample"]) == str else field["name"]
            )
            sampleValue(sampleName, decoded_struct[field["name"]])

        read_head += field["size"]

    if dump_struct_debug_info:
        decoded_struct["DEBUG_File_Address"] = hex(offset)

    return decoded_struct


def writeStructArray(
    fh: BinaryIO,
    struct_array: list,
    struct_fields: list,
    include_count: bool = False,
    count_bytes: int = 0,
):
    if include_count:
        fh.write(len(struct_array).to_bytes(count_bytes, byteorder="little"))

    for struct_data in struct_array:
        writeStruct(fh, struct_data, struct_fields)


def writeStruct(fh: BinaryIO, struct_data: dict, struct_fields: list):
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
            fh.write(
                int(struct_data[field["name"]]).to_bytes(
                    field["size"], byteorder="little", signed=True
                )
            )
        elif field["type"] == "uint":
            fh.write(
                int(struct_data[field["name"]]).to_bytes(
                    field["size"], byteorder="little"
                )
            )
        elif field["type"] == float:
            fh.write(struct.pack(">f", struct_data[field["name"]]))
        elif field["type"] == bool:
            fh.write(bytes([1 if struct_data[field["name"]] else 0]))
        elif field["type"] == bytes:
            fh.write(bytes.fromhex(struct_data[field["name"]]))
        else:
            print("Unknown field type in readStruct(): " + field["type"])


# Ordered by in game species index, not by dex number!!!
speciesLookup = [
    "None",  # 0
    "Bulbasaur",  # 1
    "Ivysaur",  # 2
    "Venusaur",  # 3
    "Charmander",  # 4
    "Charmeleon",  # 5
    "Charizard",  # 6
    "Squirtle",  # 7
    "Wartortle",  # 8
    "Blastoise",  # 9
    "Caterpie",  # 10
    "Metapod",  # 11
    "Butterfree",  # 12
    "Weedle",  # 13
    "Kakuna",  # 14
    "Beedrill",  # 15
    "Pidgey",  # 16
    "Pidgeotto",  # 17
    "Pidgeot",  # 18
    "Rattata",  # 19
    "Raticate",  # 20
    "Spearow",  # 21
    "Fearow",  # 22
    "Ekans",  # 23
    "Arbok",  # 24
    "Pikachu",  # 25
    "Raichu",  # 26
    "Sandshrew",  # 27
    "Sandslash",  # 28
    "Nidoran♀",  # 29
    "Nidorina",  # 30
    "Nidoqueen",  # 31
    "Nidoran♂",  # 32
    "Nidorino",  # 33
    "Nidoking",  # 34
    "Clefairy",  # 35
    "Clefable",  # 36
    "Vulpix",  # 37
    "Ninetales",  # 38
    "Jigglypuff",  # 39
    "Wigglytuff",  # 40
    "Zubat",  # 41
    "Golbat",  # 42
    "Oddish",  # 43
    "Gloom",  # 44
    "Vileplume",  # 45
    "Paras",  # 46
    "Parasect",  # 47
    "Venonat",  # 48
    "Venomoth",  # 49
    "Diglett",  # 50
    "Dugtrio",  # 51
    "Meowth",  # 52
    "Persian",  # 53
    "Psyduck",  # 54
    "Golduck",  # 55
    "Mankey",  # 56
    "Primeape",  # 57
    "Growlithe",  # 58
    "Arcanine",  # 59
    "Poliwag",  # 60
    "Poliwhirl",  # 61
    "Poliwrath",  # 62
    "Abra",  # 63
    "Kadabra",  # 64
    "Alakazam",  # 65
    "Machop",  # 66
    "Machoke",  # 67
    "Machamp",  # 68
    "Bellsprout",  # 69
    "Weepinbell",  # 70
    "Victreebel",  # 71
    "Tentacool",  # 72
    "Tentacruel",  # 73
    "Geodude",  # 74
    "Graveler",  # 75
    "Golem",  # 76
    "Ponyta",  # 77
    "Rapidash",  # 78
    "Slowpoke",  # 79
    "Slowbro",  # 80
    "Magnemite",  # 81
    "Magneton",  # 82
    "Farfetch'D",  # 83
    "Doduo",  # 84
    "Dodrio",  # 85
    "Seel",  # 86
    "Dewgong",  # 87
    "Grimer",  # 88
    "Muk",  # 89
    "Shellder",  # 90
    "Cloyster",  # 91
    "Gastly",  # 92
    "Haunter",  # 93
    "Gengar",  # 94
    "Onix",  # 95
    "Drowzee",  # 96
    "Hypno",  # 97
    "Krabby",  # 98
    "Kingler",  # 99
    "Voltorb",  # 100
    "Electrode",  # 101
    "Exeggcute",  # 102
    "Exeggutor",  # 103
    "Cubone",  # 104
    "Marowak",  # 105
    "Hitmonlee",  # 106
    "Hitmonchan",  # 107
    "Lickitung",  # 108
    "Koffing",  # 109
    "Weezing",  # 110
    "Rhyhorn",  # 111
    "Rhydon",  # 112
    "Chansey",  # 113
    "Tangela",  # 114
    "Kangaskhan",  # 115
    "Horsea",  # 116
    "Seadra",  # 117
    "Goldeen",  # 118
    "Seaking",  # 119
    "Staryu",  # 120
    "Starmie",  # 121
    "Mr. Mime",  # 122
    "Scyther",  # 123
    "Jynx",  # 124
    "Electabuzz",  # 125
    "Magmar",  # 126
    "Pinsir",  # 127
    "Tauros",  # 128
    "Magikarp",  # 129
    "Gyarados",  # 130
    "Lapras",  # 131
    "Ditto",  # 132
    "Eevee",  # 133
    "Vaporeon",  # 134
    "Jolteon",  # 135
    "Flareon",  # 136
    "Porygon",  # 137
    "Omanyte",  # 138
    "Omastar",  # 139
    "Kabuto",  # 140
    "Kabutops",  # 141
    "Aerodactyl",  # 142
    "Snorlax",  # 143
    "Articuno",  # 144
    "Zapdos",  # 145
    "Moltres",  # 146
    "Dratini",  # 147
    "Dragonair",  # 148
    "Dragonite",  # 149
    "Mewtwo",  # 150
    "Mew",  # 151
    "Chikorita",  # 152
    "Bayleef",  # 153
    "Meganium",  # 154
    "Cyndaquil",  # 155
    "Quilava",  # 156
    "Typhlosion",  # 157
    "Totodile",  # 158
    "Croconaw",  # 159
    "Feraligatr",  # 160
    "Sentret",  # 161
    "Furret",  # 162
    "Hoothoot",  # 163
    "Noctowl",  # 164
    "Ledyba",  # 165
    "Ledian",  # 166
    "Spinarak",  # 167
    "Ariados",  # 168
    "Crobat",  # 169
    "Chinchou",  # 170
    "Lanturn",  # 171
    "Pichu",  # 172
    "Cleffa",  # 173
    "Igglybuff",  # 174
    "Togepi",  # 175
    "Togetic",  # 176
    "Natu",  # 177
    "Xatu",  # 178
    "Mareep",  # 179
    "Flaaffy",  # 180
    "Ampharos",  # 181
    "Bellossom",  # 182
    "Marill",  # 183
    "Azumarill",  # 184
    "Sudowoodo",  # 185
    "Politoed",  # 186
    "Hoppip",  # 187
    "Skiploom",  # 188
    "Jumpluff",  # 189
    "Aipom",  # 190
    "Sunkern",  # 191
    "Sunflora",  # 192
    "Yanma",  # 193
    "Wooper",  # 194
    "Quagsire",  # 195
    "Espeon",  # 196
    "Umbreon",  # 197
    "Murkrow",  # 198
    "Slowking",  # 199
    "Misdreavus",  # 200
    "Unown",  # 201
    "Wobbuffet",  # 202
    "Girafarig",  # 203
    "Pineco",  # 204
    "Forretress",  # 205
    "Dunsparce",  # 206
    "Gligar",  # 207
    "Steelix",  # 208
    "Snubbull",  # 209
    "Granbull",  # 210
    "Qwilfish",  # 211
    "Scizor",  # 212
    "Shuckle",  # 213
    "Heracross",  # 214
    "Sneasel",  # 215
    "Teddiursa",  # 216
    "Ursaring",  # 217
    "Slugma",  # 218
    "Magcargo",  # 219
    "Swinub",  # 220
    "Piloswine",  # 221
    "Corsola",  # 222
    "Remoraid",  # 223
    "Octillery",  # 224
    "Delibird",  # 225
    "Mantine",  # 226
    "Skarmory",  # 227
    "Houndour",  # 228
    "Houndoom",  # 229
    "Kingdra",  # 230
    "Phanpy",  # 231
    "Donphan",  # 232
    "Porygon2",  # 233
    "Stantler",  # 234
    "Smeargle",  # 235
    "Tyrogue",  # 236
    "Hitmontop",  # 237
    "Smoochum",  # 238
    "Elekid",  # 239
    "Magby",  # 240
    "Miltank",  # 241
    "Blissey",  # 242
    "Raikou",  # 243
    "Entei",  # 244
    "Suicune",  # 245
    "Larvitar",  # 246
    "Pupitar",  # 247
    "Tyranitar",  # 248
    "Lugia",  # 249
    "Ho_Oh",  # 250
    "Celebi",  # 251
    "Old_Unown_B",  # 252
    "Old_Unown_C",  # 253
    "Old_Unown_D",  # 254
    "Old_Unown_E",  # 255
    "Old_Unown_F",  # 256
    "Old_Unown_G",  # 257
    "Old_Unown_H",  # 258
    "Old_Unown_I",  # 259
    "Old_Unown_J",  # 260
    "Old_Unown_K",  # 261
    "Old_Unown_L",  # 262
    "Old_Unown_M",  # 263
    "Old_Unown_N",  # 264
    "Old_Unown_O",  # 265
    "Old_Unown_P",  # 266
    "Old_Unown_Q",  # 267
    "Old_Unown_R",  # 268
    "Old_Unown_S",  # 269
    "Old_Unown_T",  # 270
    "Old_Unown_U",  # 271
    "Old_Unown_V",  # 272
    "Old_Unown_W",  # 273
    "Old_Unown_X",  # 274
    "Old_Unown_Y",  # 275
    "Old_Unown_Z",  # 276
    "Treecko",  # 277
    "Grovyle",  # 278
    "Sceptile",  # 279
    "Torchic",  # 280
    "Combusken",  # 281
    "Blaziken",  # 282
    "Mudkip",  # 283
    "Marshtomp",  # 284
    "Swampert",  # 285
    "Poochyena",  # 286
    "Mightyena",  # 287
    "Zigzagoon",  # 288
    "Linoone",  # 289
    "Wurmple",  # 290
    "Silcoon",  # 291
    "Beautifly",  # 292
    "Cascoon",  # 293
    "Dustox",  # 294
    "Lotad",  # 295
    "Lombre",  # 296
    "Ludicolo",  # 297
    "Seedot",  # 298
    "Nuzleaf",  # 299
    "Shiftry",  # 300
    "Nincada",  # 301
    "Ninjask",  # 302
    "Shedinja",  # 303
    "Taillow",  # 304
    "Swellow",  # 305
    "Shroomish",  # 306
    "Breloom",  # 307
    "Spinda",  # 308
    "Wingull",  # 309
    "Pelipper",  # 310
    "Surskit",  # 311
    "Masquerain",  # 312
    "Wailmer",  # 313
    "Wailord",  # 314
    "Skitty",  # 315
    "Delcatty",  # 316
    "Kecleon",  # 317
    "Baltoy",  # 318
    "Claydol",  # 319
    "Nosepass",  # 320
    "Torkoal",  # 321
    "Sableye",  # 322
    "Barboach",  # 323
    "Whiscash",  # 324
    "Luvdisc",  # 325
    "Corphish",  # 326
    "Crawdaunt",  # 327
    "Feebas",  # 328
    "Milotic",  # 329
    "Carvanha",  # 330
    "Sharpedo",  # 331
    "Trapinch",  # 332
    "Vibrava",  # 333
    "Flygon",  # 334
    "Makuhita",  # 335
    "Hariyama",  # 336
    "Electrike",  # 337
    "Manectric",  # 338
    "Numel",  # 339
    "Camerupt",  # 340
    "Spheal",  # 341
    "Sealeo",  # 342
    "Walrein",  # 343
    "Cacnea",  # 344
    "Cacturne",  # 345
    "Snorunt",  # 346
    "Glalie",  # 347
    "Lunatone",  # 348
    "Solrock",  # 349
    "Azurill",  # 350
    "Spoink",  # 351
    "Grumpig",  # 352
    "Plusle",  # 353
    "Minun",  # 354
    "Mawile",  # 355
    "Meditite",  # 356
    "Medicham",  # 357
    "Swablu",  # 358
    "Altaria",  # 359
    "Wynaut",  # 360
    "Duskull",  # 361
    "Dusclops",  # 362
    "Roselia",  # 363
    "Slakoth",  # 364
    "Vigoroth",  # 365
    "Slaking",  # 366
    "Gulpin",  # 367
    "Swalot",  # 368
    "Tropius",  # 369
    "Whismur",  # 370
    "Loudred",  # 371
    "Exploud",  # 372
    "Clamperl",  # 373
    "Huntail",  # 374
    "Gorebyss",  # 375
    "Absol",  # 376
    "Shuppet",  # 377
    "Banette",  # 378
    "Seviper",  # 379
    "Zangoose",  # 380
    "Relicanth",  # 381
    "Aron",  # 382
    "Lairon",  # 383
    "Aggron",  # 384
    "Castform",  # 385
    "Volbeat",  # 386
    "Illumise",  # 387
    "Lileep",  # 388
    "Cradily",  # 389
    "Anorith",  # 390
    "Armaldo",  # 391
    "Ralts",  # 392
    "Kirlia",  # 393
    "Gardevoir",  # 394
    "Bagon",  # 395
    "Shelgon",  # 396
    "Salamence",  # 397
    "Beldum",  # 398
    "Metang",  # 399
    "Metagross",  # 400
    "Regirock",  # 401
    "Regice",  # 402
    "Registeel",  # 403
    "Kyogre",  # 404
    "Groudon",  # 405
    "Rayquaza",  # 406
    "Latias",  # 407
    "Latios",  # 408
    "Jirachi",  # 409
    "Deoxys",  # 410
    "Chimecho",  # 411
    "Egg",  # 412
]

# Ordered by dex, not by species index in game
pokemonNames = [
    "??????????",
    "Bulbasaur",
    "Ivysaur",
    "Venusaur",
    "Charmander",
    "Charmeleon",
    "Charizard",
    "Squirtle",
    "Wartortle",
    "Blastoise",
    "Caterpie",
    "Metapod",
    "Butterfree",
    "Weedle",
    "Kakuna",
    "Beedrill",
    "Pidgey",
    "Pidgeotto",
    "Pidgeot",
    "Rattata",
    "Raticate",
    "Spearow",
    "Fearow",
    "Ekans",
    "Arbok",
    "Pikachu",
    "Raichu",
    "Sandshrew",
    "Sandslash",
    "Nidoran♀",
    "Nidorina",
    "Nidoqueen",
    "Nidoran♂",
    "Nidorino",
    "Nidoking",
    "Clefairy",
    "Clefable",
    "Vulpix",
    "Ninetales",
    "Jigglypuff",
    "Wigglytuff",
    "Zubat",
    "Golbat",
    "Oddish",
    "Gloom",
    "Vileplume",
    "Paras",
    "Parasect",
    "Venonat",
    "Venomoth",
    "Diglett",
    "Dugtrio",
    "Meowth",
    "Persian",
    "Psyduck",
    "Golduck",
    "Mankey",
    "Primeape",
    "Growlithe",
    "Arcanine",
    "Poliwag",
    "Poliwhirl",
    "Poliwrath",
    "Abra",
    "Kadabra",
    "Alakazam",
    "Machop",
    "Machoke",
    "Machamp",
    "Bellsprout",
    "Weepinbell",
    "Victreebel",
    "Tentacool",
    "Tentacruel",
    "Geodude",
    "Graveler",
    "Golem",
    "Ponyta",
    "Rapidash",
    "Slowpoke",
    "Slowbro",
    "Magnemite",
    "Magneton",
    "Farfetch'D",
    "Doduo",
    "Dodrio",
    "Seel",
    "Dewgong",
    "Grimer",
    "Muk",
    "Shellder",
    "Cloyster",
    "Gastly",
    "Haunter",
    "Gengar",
    "Onix",
    "Drowzee",
    "Hypno",
    "Krabby",
    "Kingler",
    "Voltorb",
    "Electrode",
    "Exeggcute",
    "Exeggutor",
    "Cubone",
    "Marowak",
    "Hitmonlee",
    "Hitmonchan",
    "Lickitung",
    "Koffing",
    "Weezing",
    "Rhyhorn",
    "Rhydon",
    "Chansey",
    "Tangela",
    "Kangaskhan",
    "Horsea",
    "Seadra",
    "Goldeen",
    "Seaking",
    "Staryu",
    "Starmie",
    "Mr. Mime",
    "Scyther",
    "Jynx",
    "Electabuzz",
    "Magmar",
    "Pinsir",
    "Tauros",
    "Magikarp",
    "Gyarados",
    "Lapras",
    "Ditto",
    "Eevee",
    "Vaporeon",
    "Jolteon",
    "Flareon",
    "Porygon",
    "Omanyte",
    "Omastar",
    "Kabuto",
    "Kabutops",
    "Aerodactyl",
    "Snorlax",
    "Articuno",
    "Zapdos",
    "Moltres",
    "Dratini",
    "Dragonair",
    "Dragonite",
    "Mewtwo",
    "Mew",
    "Chikorita",
    "Bayleef",
    "Meganium",
    "Cyndaquil",
    "Quilava",
    "Typhlosion",
    "Totodile",
    "Croconaw",
    "Feraligatr",
    "Sentret",
    "Furret",
    "Hoothoot",
    "Noctowl",
    "Ledyba",
    "Ledian",
    "Spinarak",
    "Ariados",
    "Crobat",
    "Chinchou",
    "Lanturn",
    "Pichu",
    "Cleffa",
    "Igglybuff",
    "Togepi",
    "Togetic",
    "Natu",
    "Xatu",
    "Mareep",
    "Flaaffy",
    "Ampharos",
    "Bellossom",
    "Marill",
    "Azumarill",
    "Sudowoodo",
    "Politoed",
    "Hoppip",
    "Skiploom",
    "Jumpluff",
    "Aipom",
    "Sunkern",
    "Sunflora",
    "Yanma",
    "Wooper",
    "Quagsire",
    "Espeon",
    "Umbreon",
    "Murkrow",
    "Slowking",
    "Misdreavus",
    "Unown",
    "Wobbuffet",
    "Girafarig",
    "Pineco",
    "Forretress",
    "Dunsparce",
    "Gligar",
    "Steelix",
    "Snubbull",
    "Granbull",
    "Qwilfish",
    "Scizor",
    "Shuckle",
    "Heracross",
    "Sneasel",
    "Teddiursa",
    "Ursaring",
    "Slugma",
    "Magcargo",
    "Swinub",
    "Piloswine",
    "Corsola",
    "Remoraid",
    "Octillery",
    "Delibird",
    "Mantine",
    "Skarmory",
    "Houndour",
    "Houndoom",
    "Kingdra",
    "Phanpy",
    "Donphan",
    "Porygon2",
    "Stantler",
    "Smeargle",
    "Tyrogue",
    "Hitmontop",
    "Smoochum",
    "Elekid",
    "Magby",
    "Miltank",
    "Blissey",
    "Raikou",
    "Entei",
    "Suicune",
    "Larvitar",
    "Pupitar",
    "Tyranitar",
    "Lugia",
    "Ho-Oh",
    "Celebi",
    "Treecko",
    "Grovyle",
    "Sceptile",
    "Torchic",
    "Combusken",
    "Blaziken",
    "Mudkip",
    "Marshtomp",
    "Swampert",
    "Poochyena",
    "Mightyena",
    "Zigzagoon",
    "Linoone",
    "Wurmple",
    "Silcoon",
    "Beautifly",
    "Cascoon",
    "Dustox",
    "Lotad",
    "Lombre",
    "Ludicolo",
    "Seedot",
    "Nuzleaf",
    "Shiftry",
    "Taillow",
    "Swellow",
    "Wingull",
    "Pelipper",
    "Ralts",
    "Kirlia",
    "Gardevoir",
    "Surskit",
    "Masquerain",
    "Shroomish",
    "Breloom",
    "Slakoth",
    "Vigoroth",
    "Slaking",
    "Nincada",
    "Ninjask",
    "Shedinja",
    "Whismur",
    "Loudred",
    "Exploud",
    "Makuhita",
    "Hariyama",
    "Azurill",
    "Nosepass",
    "Skitty",
    "Delcatty",
    "Sableye",
    "Mawile",
    "Aron",
    "Lairon",
    "Aggron",
    "Meditite",
    "Medicham",
    "Electrike",
    "Manectric",
    "Plusle",
    "Minun",
    "Volbeat",
    "Illumise",
    "Roselia",
    "Gulpin",
    "Swalot",
    "Carvanha",
    "Sharpedo",
    "Wailmer",
    "Wailord",
    "Numel",
    "Camerupt",
    "Torkoal",
    "Spoink",
    "Grumpig",
    "Spinda",
    "Trapinch",
    "Vibrava",
    "Flygon",
    "Cacnea",
    "Cacturne",
    "Swablu",
    "Altaria",
    "Zangoose",
    "Seviper",
    "Lunatone",
    "Solrock",
    "Barboach",
    "Whiscash",
    "Corphish",
    "Crawdaunt",
    "Baltoy",
    "Claydol",
    "Lileep",
    "Cradily",
    "Anorith",
    "Armaldo",
    "Feebas",
    "Milotic",
    "Castform",
    "Kecleon",
    "Shuppet",
    "Banette",
    "Duskull",
    "Dusclops",
    "Tropius",
    "Chimecho",
    "Absol",
    "Wynaut",
    "Snorunt",
    "Glalie",
    "Spheal",
    "Sealeo",
    "Walrein",
    "Clamperl",
    "Huntail",
    "Gorebyss",
    "Relicanth",
    "Luvdisc",
    "Bagon",
    "Shelgon",
    "Salamence",
    "Beldum",
    "Metang",
    "Metagross",
    "Regirock",
    "Regice",
    "Registeel",
    "Latias",
    "Latios",
    "Kyogre",
    "Groudon",
    "Rayquaza",
    "Jirachi",
    "Deoxys",
]

# Ability to look up dex number by name
pokedexLookup = {}

for index, pokemon in enumerate(pokemonNames):
    pokedexLookup[pokemon] = index

move_names = [
    "-",
    "Pound",
    "Karate Chop",
    "Doubleslap",
    "Weather Ball",
    "Mega Punch",
    "Pay Day",
    "Fire Punch",
    "Ice Punch",
    "Thunderpunch",
    "Scratch",
    "Weather Ball",
    "Guillotine",
    "Razor Wind",
    "Swords Dance",
    "Cut",
    "Gust",
    "Wing Attack",
    "Whirlwind",
    "Fly",
    "Bind",
    "Slam",
    "Vine Whip",
    "Stomp",
    "Double Kick",
    "Mega Kick",
    "Jump Kick",
    "Rolling Kick",
    "Sand-Attack",
    "Headbutt",
    "Horn Attack",
    "Fury Attack",
    "Drill Run",
    "Tackle",
    "Body Slam",
    "Wrap",
    "Take Down",
    "Thrash",
    "Double-Edge",
    "Tail Whip",
    "Poison Sting",
    "Twineedle",
    "Pin Missile",
    "Leer",
    "Bite",
    "Growl",
    "Roar",
    "Sing",
    "Supersonic",
    "Sonicboom",
    "Disable",
    "Acid",
    "Ember",
    "Flamethrower",
    "Mist",
    "Water Gun",
    "Hydro Pump",
    "Surf",
    "Ice Beam",
    "Blizzard",
    "Psybeam",
    "Bubblebeam",
    "Aurora Beam",
    "Hyper Beam",
    "Peck",
    "Drill Peck",
    "Hidden Power (Psychic)",
    "Low Kick",
    "Counter",
    "Seismic Toss",
    "Strength",
    "Absorb",
    "Mega Drain",
    "Leech Seed",
    "Growth",
    "Razor Leaf",
    "Solarbeam",
    "Poisonpowder",
    "Stun Spore",
    "Sleep Powder",
    "Petal Dance",
    "String Shot",
    "Dragon Rage",
    "Fire Spin",
    "Thundershock",
    "Thunderbolt",
    "Thunder Wave",
    "Thunder",
    "Rock Throw",
    "Earthquake",
    "Earth Power",
    "Dig",
    "Toxic",
    "Confusion",
    "Psychic",
    "Hypnosis",
    "Meditate",
    "Agility",
    "Quick Attack",
    "Rage",
    "Teleport",
    "Night Shade",
    "Mimic",
    "Screech",
    "Double Team",
    "Recover",
    "Harden",
    "Minimize",
    "Smokescreen",
    "Confuse Ray",
    "Withdraw",
    "Defense Curl",
    "Barrier",
    "Light Screen",
    "Haze",
    "Reflect",
    "Focus Energy",
    "Bide",
    "Metronome",
    "Mirror Move",
    "Selfdestruct",
    "Egg Bomb",
    "Lick",
    "Smog",
    "Sludge Bomb",
    "Bone Club",
    "Fire Blast",
    "Waterfall",
    "Clamp",
    "Swift",
    "Head Smash",
    "Hidden Power (Fire)",
    "Hidden Power (Grass)",
    "Amnesia",
    "Kinesis",
    "Softboiled",
    "Hi Jump Kick",
    "Glare",
    "Dream Eater",
    "Hidden Power (Ice)",
    "Hidden Power (Ghost)",
    "Leech Life",
    "Lovely Kiss",
    "Sky Attack",
    "Transform",
    "Bubble",
    "Dizzy Punch",
    "Spore",
    "Flash",
    "Psywave",
    "Hidden Power (Water)",
    "Acid Armor",
    "Crabhammer",
    "Explosion",
    "Fury Swipes",
    "Bonemerang",
    "Rest",
    "Rock Slide",
    "Hyper Fang",
    "Hidden Power (Dark)",
    "Conversion",
    "Tri Attack",
    "Super Fang",
    "Slash",
    "Substitute",
    "Struggle",
    "Sketch",
    "Hidden Power (Rock)",
    "Thief",
    "Spider Web",
    "Mind Reader",
    "Nightmare",
    "Flame Wheel",
    "Snore",
    "Curse",
    "Flail",
    "Conversion 2",
    "Aeroblast",
    "Hidden Power (Electric)",
    "Reversal",
    "Spite",
    "Powder Snow",
    "Protect",
    "Mach Punch",
    "Scary Face",
    "Faint Attack",
    "Sweet Kiss",
    "Belly Drum",
    "Gunk Shot",
    "Mud-Slap",
    "Octazooka",
    "Spikes",
    "Zap Cannon",
    "Foresight",
    "Destiny Bond",
    "Perish Song",
    "Icy Wind",
    "Detect",
    "Bone Rush",
    "Lock-On",
    "Hidden Power (Ground)",
    "Sandstorm",
    "Giga Drain",
    "Endure",
    "Charm",
    "Rollout",
    "False Swipe",
    "Swagger",
    "Milk Drink",
    "Wild Charge",
    "X-Scissors",
    "Steel Wing",
    "Mean Look",
    "Attract",
    "Sleep Talk",
    "Heal Bell",
    "Return",
    "Present",
    "Frustration",
    "Safeguard",
    "Pain Split",
    "Sacred Fire",
    "Magnitude",
    "Dynamicpunch",
    "Megahorn",
    "Dragonbreath",
    "Baton Pass",
    "Encore",
    "Pursuit",
    "Rapid Spin",
    "Sweet Scent",
    "Iron Tail",
    "Metal Claw",
    "Vital Throw",
    "Morning Sun",
    "Synthesis",
    "Moonlight",
    "Hidden Power",
    "Cross Chop",
    "Twister",
    "Rain Dance",
    "Sunny Day",
    "Crunch",
    "Mirror Coat",
    "Psych Up",
    "Extremespeed",
    "Ancientpower",
    "Shadow Ball",
    "Hidden Power (Fighting)",
    "Rock Smash",
    "Whirlpool",
    "Beat Up",
    "Fake Out",
    "Uproar",
    "Stockpile",
    "Spit Up",
    "Swallow",
    "Heat Wave",
    "Hail",
    "Torment",
    "Flatter",
    "Will-O-Wisp",
    "Memento",
    "Facade",
    "Focus Punch",
    "Smellingsalt",
    "Follow Me",
    "Nature Power",
    "Charge",
    "Taunt",
    "Helping Hand",
    "Hidden Power (Flying)",
    "Role Play",
    "Wish",
    "Assist",
    "Ingrain",
    "Superpower",
    "Magic Coat",
    "Recycle",
    "Revenge",
    "Brick Break",
    "Yawn",
    "Knock Off",
    "Endeavor",
    "Draco Meteor",
    "Skill Swap",
    "Imprison",
    "Refresh",
    "Grudge",
    "Snatch",
    "Secret Power",
    "Dive",
    "Force Palm",
    "Camouflage",
    "Tail Glow",
    "Luster Purge",
    "Mist Ball",
    "Featherdance",
    "Teeter Dance",
    "Blaze Kick",
    "Mud Sport",
    "Ice Ball",
    "Needle Arm",
    "Slack Off",
    "Hyper Voice",
    "Poison Fang",
    "Crush Claw",
    "Blast Burn",
    "Hydro Cannon",
    "Meteor Mash",
    "Shadow Sneak",
    "Weather Ball",
    "Aromatherapy",
    "Fake Tears",
    "Air Slash",
    "Overheat",
    "Odor Sleuth",
    "Rock Tomb",
    "Silver Wind",
    "Flash Cannon",
    "Grasswhistle",
    "Tickle",
    "Cosmic Power",
    "Water Spout",
    "Signal Beam",
    "Shadow Punch",
    "Extrasensory",
    "Sky Uppercut",
    "Sand Tomb",
    "Sheer Cold",
    "Muddy Water",
    "Bullet Seed",
    "Aerial Ace",
    "Ice Shard",
    "Iron Defense",
    "Block",
    "Howl",
    "Dragon Claw",
    "Frenzy Plant",
    "Bulk Up",
    "Bounce",
    "Mud Shot",
    "Poison Tail",
    "Hidden Power (Bug)",
    "Volt Tackle",
    "Magical Leaf",
    "Water Sport",
    "Calm Mind",
    "Leaf Blade",
    "Dragon Dance",
    "Rock Blast",
    "Shock Wave",
    "Water Pulse",
    "Doom Desire",
    "Psycho Boost",
]

eggGroups = [
    "None",  # 0
    "Monster",  # 1
    "Water 1",  # 2
    "Bug",  # 3
    "Flying",  # 4
    "Field",  # 5
    "Fairy",  # 6
    "Grass",  # 7
    "Human Like",  # 8
    "Water 3",  # 9
    "Mineral",  # 10
    "Amorphous",  # 11
    "Water 2",  # 12
    "Ditto",  # 13
    "Dragon",  # 14
    "Undiscovered",  # 15
]

types = [
    "Normal",  # 0
    "Fighting",  # 1
    "Flying",  # 2
    "Poison",  # 3
    "Ground",  # 4
    "Rock",  # 5
    "Bug",  # 6
    "Ghost",  # 7
    "Steel",  # 8
    "Unknown 9",  # Hmmmmm
    "Fire",  # 10
    "Water",  # 11
    "Grass",  # 12
    "Electric",  # 13
    "Psychic",  # 14
    "Ice",  # 15
    "Dragon",  # 16,
    "Dark",  # 17
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

items = [
    "None",  # 0
    # Balls
    "Master Ball",  # 1
    "Ultra Ball",  # 2
    "Great Ball",  # 3
    "Poke Ball",  # 4
    "Safari Ball",  # 5
    "Net Ball",  # 6
    "Dive Ball",  # 7
    "Nest Ball",  # 8
    "Repeat Ball",  # 9
    "Timer Ball",  # 10
    "Luxury Ball",  # 11
    "Premier Ball",  # 12
    # Pokemon Items
    "Potion",  # 13
    "Antidote",  # 14
    "Burn Heal",  # 15
    "Ice Heal",  # 16
    "Awakening",  # 17
    "Paralyze Heal",  # 18
    "Full Restore",  # 19
    "Max Potion",  # 20
    "Hyper Potion",  # 21
    "Super Potion",  # 22
    "Full Heal",  # 23
    "Revive",  # 24
    "Max Revive",  # 25
    "Fresh Water",  # 26
    "Soda Pop",  # 27
    "Lemonade",  # 28
    "Moomoo Milk",  # 29
    "Energy Powder",  # 30
    "Energy Root",  # 31
    "Heal Powder",  # 32
    "Revival Herb",  # 33
    "Ether",  # 34
    "Max Ether",  # 35
    "Elixir",  # 36
    "Max Elixir",  # 37
    "Lava Cookie",  # 38
    "Blue Flute",  # 39
    "Yellow Flute",  # 40
    "Red Flute",  # 41
    "Black Flute",  # 42
    "White Flute",  # 43
    "Berry Juice",  # 44
    "Sacred Ash",  # 45
    "Shoal Salt",  # 46
    "Shoal Shell",  # 47
    "Red Shard",  # 48
    "Blue Shard",  # 49
    "Yellow Shard",  # 50
    "Green Shard",  # 51
    "034",  # 52
    "035",  # 53
    "036",  # 54
    "037",  # 55
    "038",  # 56
    "039",  # 57
    "03A",  # 58
    "03B",  # 59
    "03C",  # 60
    "03D",  # 61
    "03E",  # 62
    "HP Up",  # 63
    "Protein",  # 64
    "Iron",  # 65
    "Carbos",  # 66
    "Calcium",  # 67
    "Rare Candy",  # 68
    "PP Up",  # 69
    "Zinc",  # 70
    "PP Max",  # 71
    "048",  # 72
    "Guard Spec",  # 73
    "Dire Hit",  # 74
    "X Attack",  # 75
    "X Defend",  # 76
    "X Speed",  # 77
    "X Accuracy",  # 78
    "X Special",  # 79
    "Poke Doll",  # 80
    "Fluffy Tail",  # 81
    "052",  # 82
    "Super Repel",  # 83
    "Max Repel",  # 84
    "Escape Rope",  # 85
    "Repel",  # 86
    "057",  # 87
    "058",  # 88
    "059",  # 89
    "05A",  # 90
    "05B",  # 91
    "05C",  # 92
    "Sun Stone",  # 93
    "Moon Stone",  # 94
    "Fire Stone",  # 95
    "Thunder Stone",  # 96
    "Water Stone",  # 97
    "Leaf Stone",  # 98
    "063",  # 99
    "064",  # 100
    "065",  # 101
    "066",  # 102
    # Unusable
    "Tiny Mushroom",  # 103
    "Big Mushroom",  # 104
    "069",  # 105
    "Pearl",  # 106
    "Big Pearl",  # 107
    "Stardust",  # 108
    "Star Piece",  # 109
    "Nugget",  # 110
    "Heart Scale",  # 111
    "070",  # 112
    "071",  # 113
    "072",  # 114
    "073",  # 115
    "074",  # 116
    "075",  # 117
    "076",  # 118
    "077",  # 119
    "078",  # 120
    # Mails
    "Orange Mail",  # 121
    "Harbor Mail",  # 122
    "Glitter Mail",  # 123
    "Mech Mail",  # 124
    "Wood Mail",  # 125
    "Wave Mail",  # 126
    "Bead Mail",  # 127
    "Shadow Mail",  # 128
    "Tropic Mail",  # 129
    "Dream Mail",  # 130
    "Fab Mail",  # 131
    "Retro Mail",  # 132
    # Berries
    "Cheri Berry",  # 133
    "Chesto Berry",  # 134
    "Pecha Berry",  # 135
    "Rawst Berry",  # 136
    "Aspear Berry",  # 137
    "Leppa Berry",  # 138
    "Oran Berry",  # 139
    "Persim Berry",  # 140
    "Lum Berry",  # 141
    "Sitrus Berry",  # 142
    "Figy Berry",  # 143
    "Wiki Berry",  # 144
    "Mago Berry",  # 145
    "Aguav Berry",  # 146
    "Iapapa Berry",  # 147
    "Razz Berry",  # 148
    "Bluk Berry",  # 149
    "Nanab Berry",  # 150
    "Wepear Berry",  # 151
    "Pinap Berry",  # 152
    "Pomeg Berry",  # 153
    "Kelpsy Berry",  # 154
    "Qualot Berry",  # 155
    "Hondew Berry",  # 156
    "Grepa Berry",  # 157
    "Tamato Berry",  # 158
    "Cornn Berry",  # 159
    "Magost Berry",  # 160
    "Rabuta Berry",  # 161
    "Nomel Berry",  # 162
    "Spelon Berry",  # 163
    "Pamtre Berry",  # 164
    "Watmel Berry",  # 165
    "Durin Berry",  # 166
    "Belue Berry",  # 167
    "Liechi Berry",  # 168
    "Ganlon Berry",  # 169
    "Salac Berry",  # 170
    "Petaya Berry",  # 171
    "Apicot Berry",  # 172
    "Lansat Berry",  # 173
    "Starf Berry",  # 174
    "Enigma Berry",  # 175
    "Unused Berry 1",  # 176
    "Unused Berry 2",  # 177
    "Unused Berry 3",  # 178
    # Battle Held items
    "Bright Powder",  # 179
    "White Herb",  # 180
    "Macho Brace",  # 181
    "EXP Share",  # 182
    "Quick Claw",  # 183
    "Soothe Bell",  # 184
    "Mental Herb",  # 185
    "Choice Band",  # 186
    "Kings Rock",  # 187
    "Silver Powder",  # 188
    "Amulet Coin",  # 189
    "Cleanse Tag",  # 190
    "Soul Dew",  # 191
    "Deep Sea Tooth",  # 192
    "Deep Sea Scale",  # 193
    "Smoke Ball",  # 194
    "Everstone",  # 195
    "Focus Band",  # 196
    "Lucky Egg",  # 197
    "Scope Lens",  # 198
    "Metal Coat",  # 199
    "Leftovers",  # 200
    "Dragon Scale",  # 201
    "Light Ball",  # 202
    "Soft Sand",  # 203
    "Hard Stone",  # 204
    "Miracle Seed",  # 205
    "Black Glasses",  # 206
    "Black Belt",  # 207
    "Magnet",  # 208
    "Mystic Water",  # 209
    "Sharp Beak",  # 210
    "Poison Barb",  # 211
    "Never Melt Ice",  # 212
    "Spell Tag",  # 213
    "Twisted Spoon",  # 214
    "Charcoal",  # 215
    "Dragon Fang",  # 216
    "Silk Scarf",  # 217
    "Up Grade",  # 218
    "Shell Bell",  # 219
    "Sea Incense",  # 220
    "Lax Incense",  # 221
    "Lucky Punch",  # 222
    "Metal Powder",  # 223
    "Thick Club",  # 224
    "Stick",  # 225
    "0E2",  # 226
    "0E3",  # 227
    "0E4",  # 228
    "0E5",  # 229
    "0E6",  # 230
    "0E7",  # 231
    "0E8",  # 232
    "0E9",  # 233
    "0EA",  # 234
    "0EB",  # 235
    "0EC",  # 236
    "0ED",  # 237
    "0EE",  # 238
    "0EF",  # 239
    "0F0",  # 240
    "0F1",  # 241
    "0F2",  # 242
    "0F3",  # 243
    "0F4",  # 244
    "0F5",  # 245
    "0F6",  # 246
    "0F7",  # 247
    "0F8",  # 248
    "0F9",  # 249
    "0FA",  # 250
    "0FB",  # 251
    "0FC",  # 252
    "0FD",  # 253
    # Contest held items
    "Red Scarf",  # 254
    "Blue Scarf",  # 255
    "Pink Scarf",  # 256
    "Green Scarf",  # 257
    "Yellow Scarf",  # 258
    # Key Items
    "Mach Bike",  # 259
    "Coin Case",  # 260
    "Itemfinder",  # 261
    "Old Rod",  # 262
    "Good Rod",  # 263
    "Super Rod",  # 264
    "SS Ticket",  # 265
    "Contest Pass",  # 266
    "10B",  # 267
    "Wailmer Pail",  # 268
    "Devon Goods",  # 269
    "Soot Sack",  # 270
    "Basement Key",  # 271
    "Acro Bike",  # 272
    "Pokeblock Case",  # 273
    "Letter",  # 274
    "Eon Ticket",  # 275
    "Red Orb",  # 276
    "Blue Orb",  # 277
    "Scanner",  # 278
    "Go Goggles",  # 279
    "Meteorite",  # 280
    "Room 1 Key",  # 281
    "Room 2 Key",  # 282
    "Room 4 Key",  # 283
    "Room 6 Key",  # 284
    "Storage Key",  # 285
    "Root Fossil",  # 286
    "Claw Fossil",  # 287
    "Devon Scope",  # 288
    # TMs/HMs
    "TM01",  # 289
    "TM02",  # 290
    "TM03",  # 291
    "TM04",  # 292
    "TM05",  # 293
    "TM06",  # 294
    "TM07",  # 295
    "TM08",  # 296
    "TM09",  # 297
    "TM10",  # 298
    "TM11",  # 299
    "TM12",  # 300
    "TM13",  # 301
    "TM14",  # 302
    "TM15",  # 303
    "TM16",  # 304
    "TM17",  # 305
    "TM18",  # 306
    "TM19",  # 307
    "TM20",  # 308
    "TM21",  # 309
    "TM22",  # 310
    "TM23",  # 311
    "TM24",  # 312
    "TM25",  # 313
    "TM26",  # 314
    "TM27",  # 315
    "TM28",  # 316
    "TM29",  # 317
    "TM30",  # 318
    "TM31",  # 319
    "TM32",  # 320
    "TM33",  # 321
    "TM34",  # 322
    "TM35",  # 323
    "TM36",  # 324
    "TM37",  # 325
    "TM38",  # 326
    "TM39",  # 327
    "TM40",  # 328
    "TM41",  # 329
    "TM42",  # 330
    "TM43",  # 331
    "TM44",  # 332
    "TM45",  # 333
    "TM46",  # 334
    "TM47",  # 335
    "TM48",  # 336
    "TM49",  # 337
    "TM50",  # 338
    "HM01",  # 339
    "HM02",  # 340
    "HM03",  # 341
    "HM04",  # 342
    "HM05",  # 343
    "HM06",  # 344
    "HM07",  # 345
    "HM08",  # 346
    # Unknown
    "15B",  # 347
    "15C",  # 348
    # FireRed/LeafGreen
    "Oaks Parcel",  # 349
    "Poke Flute",  # 350
    "Secret Key",  # 351
    "Bike Voucher",  # 352
    "Gold Teeth",  # 353
    "Old Amber",  # 354
    "Card Key",  # 355
    "Lift Key",  # 356
    "Helix Fossil",  # 357
    "Dome Fossil",  # 358
    "Silph Scope",  # 359
    "Bicycle",  # 360
    "Town Map",  # 361
    "VS Seeker",  # 362
    "Fame Checker",  # 363
    "Tm Case",  # 364
    "Berry Pouch",  # 365
    "Teachy Tv",  # 366
    "Tri Pass",  # 367
    "Rainbow Pass",  # 368
    "Tea",  # 369
    "Mystic Ticket",  # 370
    "Aurora Ticket",  # 371
    "Powder Jar",  # 372
    "Ruby",  # 373
    "Sapphire",  # 374
    # Emerald
    "Magma Emblem",  # 375
    "Old Sea Map",  # 376
]

pkmn_file_struct = [
    {"type": "byte", "name": "hp"},  # 0x0
    {"type": "byte", "name": "attack"},  # 0x1
    {"type": "byte", "name": "defense"},  # 0x2
    {"type": "byte", "name": "speed"},  # 0x3
    {"type": "byte", "name": "specialAttack"},  # 0x4
    {"type": "byte", "name": "specialDefense"},  # 0x5
    {"type": "byte", "name": "type1", "index_of": types},  # 0x6
    {"type": "byte", "name": "type2", "index_of": types},  # 0x7
    {"type": "byte", "name": "catchRate"},  # 0x8
    {"type": "byte", "name": "EXPYield"},  # 0x9
    {"type": "byte", "name": "unkA"},
    {"type": "byte", "name": "unkB"},
    {"type": "byte", "name": "unkC"},
    {"type": "byte", "name": "unkD"},
    {"type": "byte", "name": "unkE"},
    {"type": "byte", "name": "unkF"},
    {
        "type": "byte",
        "name": "genderRatio",
    },  # "index_of": genderRatios}, # 0x10 - male 0, female 254, genderless 255, half 31, 75% female 127
    {"type": "byte", "name": "hatchRate"},  # 0x11
    {"type": "byte", "name": "baseHappiness"},  # 0x12
    {"type": "byte", "name": "EXPGrowthRate"},  # 0x13
    {"type": "byte", "name": "eggGroup1", "index_of": eggGroups},  # 0x14
    {"type": "byte", "name": "eggGroup2", "index_of": eggGroups},  # 0x15
    {"type": "byte", "name": "ability1", "index_of": abilities},  # 0x16
    {"type": "byte", "name": "ability2", "index_of": abilities},  # 0x17
    {"type": "byte", "name": "safariZoneRunRate"},  # 0x18
    {"type": "byte", "name": "color"},  # 0x19
]


def decodePKMNFile(encoded_filename: str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        return readStruct(byte_read, 0, pkmn_file_struct)


trainerClasses = [
    "Pokémon Trainer",  # 0
    "Pokémon Trainer",  # 1
    "Hiker",  # 2
    "Team Aqua",  # 3
    "Pokémon Breeder",  # 4
    "Cooltrainer",  # 5
    "Bird Keeper",  # 6
    "Collector",  # 7
    "Swimmer ♂",  # 8
    "Team Magma",  # 9
    "Expert",  # A
    "Aqua Admin",  # B
    "Black Belt",  # C,
    "Aqua Leader",  # D
    "Hex Maniac",  # E
    "Aroma Lady",  # F
    "Ruin Maniac",  # 10
    "Interviewer",  # 11
    "Tuber",  # 12
    "Tuber",  # 13
    "Lady",  # 14
    "Beauty",  # 15
    "Rich Boy",  # 16
    "Pokémaniac",  # 17
    "Guitarist",  # 18
    "Kindler",  # 19
    "Camper",  # 1A
    "Picnicker",  # 1B
    "Bug Maniac",  # 1C
    "Psychic",  # 1D
    "Gentleman",  # 1E
    "Elite Four",  # 1F
    "Leader",  # 20
    "School Kid",  # 21
    "Sr. and Jr.",  # 22
    "Winstrate",  # 23
    "Pokéfan",  # 24
    "Youngster",  # 25
    "Champion",  # 26
    "Fisherman",  # 27
    "Triathlete",  # 28
    "Dragon Tamer",  # 29
    "Ninja Boy",  # 2A
    "Battle Girl",  # 2B
    "Parasol Lady",  # 2C
    "Swimmer ♀",  # 2D
    "Twins",  # 2E
    "Sailor",  # 2F
    "Cooltrainer",  # 30
    "Magma Admin",  # 31
    "Pokémon Trainer",  # 32
    "Bug Catcher",  # 33
    "Pokémon Ranger",  # 34
    "Magma Leader",  # 35
    "Lass",  # 36
    "Young Couple",  # 37
    "Old Couple",  # 38
    "Sis and Bro",  # 39
    "Salon Maiden",  # 3A
    "Dome Ace",  # 3B
    "Palace Maven",  # 3C
    "Arena Tycoon",  # 3D
    "Superboss",  # 3E
    "Pike Queen",  # 3F
    "Pyramid King",  # 40
    "Pokémon Trainer",  # 41
]

trainer_file_struct = [
    # Name, string with length byte at the start
    {"type": "byte", "name": "class", "index_of": trainerClasses},
    {"type": "byte", "name": "gender"},
    {"type": "byte", "name": "sprite"},
    {"type": "byte", "name": "music"},
    {"type": "ushort", "name": "item1", "index_of": items},
    {"type": "ushort", "name": "item2", "index_of": items},
    {"type": "ushort", "name": "item3", "index_of": items},
    {"type": "ushort", "name": "item4", "index_of": items},
    {"type": bool, "size": 1, "name": "isDoubleBattle"},
    {"type": bool, "size": 1, "name": "hasCustomAttacks"},
    {"type": bool, "size": 1, "name": "hasHeldItems"},
    {"type": int, "size": 4, "name": "partyCount"},
    # Array of structs for trainer pokemon party using count
]

trainer_pokemon_struct = [
    {"type": "ushort", "name": "species", "index_of": speciesLookup},
    {"type": "ushort", "name": "level"},
    {"type": "ushort", "name": "EVs"},
    {"type": "ushort", "name": "item", "index_of": items},
    {"type": "ushort", "name": "move1", "index_of": move_names},
    {"type": "ushort", "name": "move2", "index_of": move_names},
    {"type": "ushort", "name": "move3", "index_of": move_names},
    {"type": "ushort", "name": "move4", "index_of": move_names},
]


def decodeTrainerFile(encoded_filename: str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()

        # Read first byte to get length of name string
        read_head = 0
        nameLength = int.from_bytes(
            byte_read[read_head : read_head + 1], byteorder="little"
        )

        # Read byte array starting at 1 as string
        read_head = read_head + 1
        name = byte_read[read_head : read_head + nameLength].decode("ASCII").title()

        # Read trainer file struct from offset at end of string
        read_head = read_head + nameLength
        trainerData = readStruct(byte_read, read_head, trainer_file_struct)
        trainerData["name"] = name

        # Read party struct array from offset at end of trainer struct with count from trainer struct
        read_head = read_head + getStructSize(trainer_file_struct)
        trainerData["team"] = readStructArray(
            byte_read, read_head, trainerData["partyCount"], trainer_pokemon_struct
        )

        return trainerData


move_struct = [
    {"type": "byte", "name": "effect"},
    {"type": "byte", "name": "power"},
    {"type": "byte", "name": "type", "index_of": types},
    {"type": "byte", "name": "accuracy"},
    {"type": "byte", "name": "pp"},
    {"type": "byte", "name": "secondaryEffectChance"},
    {"type": "byte", "name": "target"},
    {"type": int, "size": 1, "name": "priority"},
    {"type": "byte", "name": "flags"},
]


def decodeMoveFile(encoded_filename):
    with open(encoded_filename, "r") as fh:
        byte_read = fh.readlines()
        moveInfo = {
            "index": int(
                encoded_filename.replace(".ini", "").replace(".\\moves\\", "")
            ),
        }
        for line in byte_read:
            # Fix up their weird formatting
            splitString = (
                line.replace("\n", "").replace("\\n", " ").replace("\\x", "").split("=")
            )
            if len(splitString) == 2:
                fieldName = splitString[0]
                fieldValue = splitString[1]
                if fieldName == "AttackName":
                    moveInfo["name"] = fieldValue.title()
                if fieldName == "AttackDescription":
                    moveInfo["description"] = fieldValue
                if fieldName == "ContestData":
                    moveInfo["contestData"] = fieldValue
                if fieldName == "AttackData":
                    # Decode move_struct from byte version of fieldValue
                    attackDataRaw = bytes.fromhex(fieldValue)
                    moveInfo["attackData"] = readStruct(attackDataRaw, 0, move_struct)
        return moveInfo
