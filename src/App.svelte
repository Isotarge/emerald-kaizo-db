<script>
    import PartyPokemonPanel from "./lib/PartyPokemonPanel.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import { pokemonNames, pokemon } from "./state";
    // TODO: Party presets
    // TODO: Search all presets for good matchups
    // TODO: Import pokemon from .sav?
    const partyPokemon = [
        { name: "Scizor" },
        { name: "Vileplume" },
        { name: "Gyarados" },
        { name: "Flygon" },
        { name: "Spinda" },
        { name: "Electrode" },
    ];

    let selectedOpponentPreset = "Red (Victory Road)";
    // TODO: Remove .map once schema is set in stone and full pokemon can be passed to panel as prop
    $: opponentPokemon = [
        ...opponentPresets.find(
            (preset) => preset.name === selectedOpponentPreset
        ).team,
    ];
    const opponentPresets = [
        {
            name: "Beauty Connie (Juan's Gym #1)",
            weather: "Rain",
            team: [
                {
                    name: "Qwilfish",
                },
                {
                    name: "Seaking",
                },
                {
                    name: "Whiscash",
                },
                {
                    name: "Masquerain",
                },
                {
                    name: "Manectric",
                },
                {
                    name: "Mawile",
                },
            ],
        },
        {
            name: "Ranger Andrea (Juan's Gym #2)",
            weather: "Rain",
            team: [
                {
                    name: "Venusaur",
                },
                {
                    name: "Glalie",
                },
                {
                    name: "Pinsir",
                },
                {
                    name: "Huntail",
                },
                {
                    name: "Lanturn",
                },
                {
                    name: "Pelipper",
                },
            ],
        },
        {
            name: "Parasol Lady Daphne (Juan's Gym #3)",
            weather: "Rain",
            team: [
                {
                    name: "Porygon2",
                },
                {
                    name: "Walrein",
                },
                {
                    name: "Whiscash",
                },
                {
                    name: "Politoed",
                },
                {
                    name: "Victreebel",
                },
                {
                    name: "Ampharos",
                },
            ],
        },
        {
            name: "Pokéfan Bethany (Juan's Gym)",
            weather: "Rain",
            team: [
                {
                    name: "Jolteon",
                },
                {
                    name: "Politoed",
                },
                {
                    name: "Dewgong",
                },
                {
                    name: "Meganium",
                },
                {
                    name: "Quagsire",
                },
                {
                    name: "Clefable",
                },
            ],
        },
        {
            name: "Triathlete Brianna (Juan's Gym)",
            weather: "Rain",
            team: [
                {
                    name: "Electrode",
                },
                {
                    name: "Sceptile",
                },
                {
                    name: "Octillery",
                },
                {
                    name: "Golduck",
                },
                {
                    name: "Starmie",
                },
                {
                    name: "Magneton",
                },
            ],
        },
        {
            name: "Battle Girl Crissy (Juan's Gym)",
            weather: "Rain",
            team: [
                {
                    name: "Medicham",
                },
                {
                    name: "Feraligatr",
                },
                {
                    name: "Poliwrath",
                },
                {
                    name: "Azumarill",
                },
                {
                    name: "Electabuzz",
                },
                {
                    name: "Scizor",
                },
            ],
        },
        {
            name: "PKMN Breeder Bridget (Juan's Gym)",
            weather: "Rain",
            team: [
                {
                    name: "Mantine",
                },
                {
                    name: "Forretress",
                },
                {
                    name: "Mr. Mime",
                },
                {
                    name: "Quagsire",
                },
                {
                    name: "Tentacruel",
                },
                {
                    name: "Blastoise",
                },
            ],
        },
        {
            name: "Expert Annika (Juan's Gym)",
            weather: "Rain",
            team: [
                {
                    name: "Gengar",
                },
                {
                    name: "Dragonite",
                },
                {
                    name: "Omastar",
                },
                {
                    name: "Vaporeon",
                },
                {
                    name: "Metagross",
                },
                {
                    name: "Golduck",
                },
            ],
        },
        {
            name: "Cooltrainer Olivia (Juan's Gym)",
            weather: "Rain",
            team: [
                {
                    name: "Gorebyss",
                },
                {
                    name: "Kabutops",
                },
                {
                    name: "Wailord",
                },
                {
                    name: "Snorlax",
                },
                {
                    name: "Salamence",
                },
            ],
        },
        {
            name: "Wallace (Juan's Gym)",
            weather: "Rain",
            team: [
                {
                    name: "Kingdra",
                },
                {
                    name: "Swampert",
                },
                {
                    name: "Castform",
                },
                {
                    name: "Milotic",
                },
                {
                    name: "Ludicolo",
                },
                {
                    name: "Lapras",
                },
            ],
        },
        {
            name: "Juan (Double Battle)",
            weather: "Rain",
            team: [
                {
                    name: "Kingdra",
                },
                {
                    name: "Lapras",
                },
                {
                    name: "Castform",
                },
                {
                    name: "Vaporeon",
                },
                {
                    name: "Lanturn",
                },
                {
                    name: "Ludicolo",
                },
            ],
        },
        {
            name: "Archie",
            weather: "Rain",
            team: [
                {
                    name: "Raikou",
                },
                {
                    name: "Suicune",
                },
                {
                    name: "Qwilfish",
                },
                {
                    name: "Kingdra",
                },
                {
                    name: "Metagross",
                },
                {
                    name: "Dragonite",
                },
            ],
        },
        {
            name: "Cooltrainer Albert (Victory Road)",
            team: [
                {
                    name: "Ninjask",
                },
                {
                    name: "Ursaring",
                },
                {
                    name: "Marowak",
                },
                {
                    name: "Medicham",
                },
                {
                    name: "Grumpig",
                },
                {
                    name: "Ampharos",
                },
            ],
        },
        {
            name: "Cooltrainer Hope (Victory Road)",
            team: [
                {
                    name: "Smeargle",
                },
                {
                    name: "Espeon",
                },
                {
                    name: "Jolteon",
                },
                {
                    name: "Vaporeon",
                },
                {
                    name: "Umbreon",
                },
                {
                    name: "Solrock",
                },
            ],
        },
        {
            name: "Wally (Victory Road)",
            team: [
                {
                    name: "Meganium",
                },
                {
                    name: "Gardevoir",
                },
                {
                    name: "Blissey",
                },
                {
                    name: "Hitmontop",
                },
                {
                    name: "Raichu",
                },
                {
                    name: "Vaporeon",
                },
            ],
        },
        {
            name: "Expert Samuel (Victory Road)",
            team: [
                {
                    name: "Nidoking",
                },
                {
                    name: "Cradily",
                },
                {
                    name: "Jynx",
                },
                {
                    name: "Feraligatr",
                },
                {
                    name: "Lanturn",
                },
            ],
        },
        {
            name: "Expert Shannon (Victory Road)",
            team: [
                {
                    name: "Ditto",
                },
                {
                    name: "Blastoise",
                },
                {
                    name: "Manectric",
                },
                {
                    name: "Gligar",
                },
                {
                    name: "Tyranitar",
                },
                {
                    name: "Venomoth",
                },
            ],
        },
        {
            name: "Red (Victory Road)",
            team: [
                {
                    name: "Ho-Oh",
                },
                {
                    name: "Celebi",
                },
                {
                    name: "Lapras",
                },
                {
                    name: "Mew",
                },
                {
                    name: "Snorlax",
                },
                {
                    name: "Dragonite",
                },
            ],
        },
        {
            name: "E4 Sydney",
            team: [
                {
                    name: "Sableye",
                },
                {
                    name: "Jolteon",
                },
                {
                    name: "Tauros",
                },
                {
                    name: "Alakazam",
                },
                {
                    name: "Machamp",
                },
                {
                    name: "Houndoom",
                },
            ],
        },
        {
            name: "E4 Phoebe",
            team: [
                {
                    name: "Gengar",
                },
                {
                    name: "Ludicolo",
                },
                {
                    name: "Crobat",
                },
                {
                    name: "Gardevoir",
                },
                {
                    name: "Sableye",
                },
                {
                    name: "Dusclops",
                },
            ],
        },
        {
            name: "E4 Glacia",
            team: [
                {
                    name: "Glalie",
                },
                {
                    name: "Wailord",
                },
                {
                    name: "Regice",
                },
                {
                    name: "Dewgong",
                },
                {
                    name: "Swampert",
                },
                {
                    name: "Lapras",
                },
            ],
        },
        {
            name: "E4 Drake",
            team: [
                {
                    name: "Latios",
                },
                {
                    name: "Tyranitar",
                },
                {
                    name: "Salamence",
                },
                {
                    name: "Kingdra",
                },
                {
                    name: "Dragonite",
                },
                {
                    name: "Latias",
                },
            ],
        },
        {
            name: "E4 Champion",
            team: [
                {
                    name: "Metagross",
                },
                {
                    name: "Starmie",
                },
                {
                    name: "Jirachi",
                },
                {
                    name: "Mewtwo",
                },
                {
                    name: "Aerodactyl",
                },
                {
                    name: "Deoxys",
                },
            ],
        },
        {
            name: "Littleroot Water",
            team: [
                {
                    name: "Totodile",
                },
                {
                    name: "Croconaw",
                },
                {
                    name: "Squirtle",
                },
            ],
        },
        {
            name: "Littleroot Old Rod",
            team: [
                {
                    name: "Goldeen",
                },
                {
                    name: "Luvdisc",
                },
            ],
        },
        {
            name: "Littleroot Good Rod",
            team: [
                {
                    name: "Goldeen",
                },
                {
                    name: "Corphish",
                },
            ],
        },
        {
            name: "Littleroot Super Rod",
            team: [
                {
                    name: "Seaking",
                },
                {
                    name: "Luvdisc",
                },
            ],
        },
        {
            name: "Route 101 Grass",
            team: [
                {
                    name: "Caterpie",
                },
                {
                    name: "Wurmple",
                },
                {
                    name: "Sentret",
                },
                {
                    name: "Poochyena",
                },
                {
                    name: "Ratata",
                },
                {
                    name: "Zigzagoon",
                },
                {
                    name: "Pidgey",
                },
                {
                    name: "Togepi",
                },
                {
                    name: "Cleffa",
                },
                {
                    name: "Igglybuff",
                },
                {
                    name: "Weedle",
                },
            ],
        },
        {
            name: "Oldale Grass",
            team: [
                {
                    name: "Vulpix",
                },
                {
                    name: "Slugma",
                },
                {
                    name: "Numel",
                },
                {
                    name: "Ponyta",
                },
                {
                    name: "Growlithe",
                },
                {
                    name: "Magby",
                },
                {
                    name: "Charmander",
                },
            ],
        },
        {
            name: "Route 102 Grass",
            team: [
                {
                    name: "Spinarak",
                },
                {
                    name: "Gulpin",
                },
                {
                    name: "Electrike",
                },
                {
                    name: "Meowth",
                },
                {
                    name: "Sandshrew",
                },
                {
                    name: "Nidoran♂",
                },
            ],
        },
        {
            name: "Route 102 Water",
            team: [
                {
                    name: "Seaking",
                },
                {
                    name: "Luvdisc",
                },
                {
                    name: "Poliwrath",
                },
            ],
        },
        {
            name: "Petalburg Water",
            team: [
                {
                    name: "Golduck",
                },
            ],
        },
        {
            name: "Route 103 Grass",
            team: [
                {
                    name: "Sunkern",
                },
                {
                    name: "Spoink",
                },
                {
                    name: "Mareep",
                },
                {
                    name: "Spearow",
                },
                {
                    name: "Ledyba",
                },
                {
                    name: "Ekans",
                },
                {
                    name: "Wingull",
                },
                {
                    name: "Skitty",
                },
                {
                    name: "Hoppip",
                },
                {
                    name: "Poliwag",
                },
            ],
        },
        {
            name: "Route 103 Water",
            team: [
                {
                    name: "Kingler",
                },
                {
                    name: "Seaking",
                },
            ],
        },
        {
            name: "Route 103 Old Rod",
            team: [
                {
                    name: "Remoraid",
                },
                {
                    name: "Tentacool",
                },
            ],
        },
        {
            name: "Route 103 Good Rod",
            team: [
                {
                    name: "Octillery",
                },
            ],
        },
        {
            name: "Route 103 Super Rod",
            team: [
                {
                    name: "Octillery",
                },
            ],
        },
        {
            name: "Route 104 Grass",
            team: [
                {
                    name: "Elekid",
                },
                {
                    name: "Venonat",
                },
                {
                    name: "Natu",
                },
                {
                    name: "Cubone",
                },
                {
                    name: "Nidoran♀",
                },
                {
                    name: "Seedot",
                },
            ],
        },
        {
            name: "Rustboro Grass",
            team: [
                {
                    name: "Seedot",
                },
                {
                    name: "Bellsprout",
                },
                {
                    name: "Oddish",
                },
                {
                    name: "Exeggcute",
                },
                {
                    name: "Bulbasaur",
                },
                {
                    name: "Chikorita",
                },
                {
                    name: "Cacnea",
                },
                {
                    name: "Shroomish",
                },
            ],
        },
        {
            name: "Route 116 Grass",
            team: [
                {
                    name: "Grimer",
                },
                {
                    name: "Natu",
                },
                {
                    name: "Yanma",
                },
                {
                    name: "Makuhita",
                },
                {
                    name: "Metapod",
                },
                {
                    name: "Unown",
                },
                {
                    name: "Ralts",
                },
                {
                    name: "Spoink",
                },
                {
                    name: "Paras",
                },
                {
                    name: "Voltorb",
                },
                {
                    name: "Chimecho",
                },
                {
                    name: "Voltorb",
                },
            ],
        },
        {
            name: "Dewford Grass",
            team: [
                {
                    name: "Makuhita",
                },
                {
                    name: "Machop",
                },
                {
                    name: "Mankey",
                },
                {
                    name: "Meditite",
                },
                {
                    name: "Tyrogue",
                },
            ],
        },
        {
            name: "Slateport Grass",
            team: [
                {
                    name: "Minun",
                },
                {
                    name: "Elekid",
                },
                {
                    name: "Magnemite",
                },
                {
                    name: "Electrike",
                },
                {
                    name: "Pichu",
                },
                {
                    name: "Mareep",
                },
            ],
        },
        {
            name: "Slateport Old Rod",
            team: [
                {
                    name: "Corsola",
                },
                {
                    name: "Chinchou",
                },
            ],
        },
        {
            name: "Slateport Good Rod",
            team: [
                {
                    name: "Mantine",
                },
                {
                    name: "Remoraid",
                },
            ],
        },
        {
            name: "Slateport Super Rod",
            team: [
                {
                    name: "Sharpedo",
                },
                {
                    name: "Octillery",
                },
            ],
        },
        {
            name: "Slateport Water",
            team: [
                {
                    name: "Octillery",
                },
                {
                    name: "Mantine",
                },
                {
                    name: "Pelipper",
                },
            ],
        },
        {
            name: "Route 120 Grass",
            team: [
                {
                    name: "Azumarill",
                },
                {
                    name: "Pinsir",
                },
                {
                    name: "Zangoose",
                },
                {
                    name: "Seviper",
                },
                {
                    name: "Spoink",
                },
                {
                    name: "Tangela",
                },
                {
                    name: "Kecleon",
                },
                {
                    name: "Primeape",
                },
                {
                    name: "Scyther",
                },
                {
                    name: "Scizor",
                },
                {
                    name: "Absol",
                },
            ],
        },
        {
            name: "Route 120 Water",
            team: [
                {
                    name: "Azumarill",
                },
                {
                    name: "Fearow",
                },
                {
                    name: "Seaking",
                },
                {
                    name: "Whiscash",
                },
            ],
        },
        {
            name: "Route 120 Super Rod",
            team: [
                {
                    name: "Kingler",
                },
                {
                    name: "Crawdaunt",
                },
            ],
        },
        {
            name: "Route 121 Grass",
            team: [
                {
                    name: "Weepinbell",
                },
                {
                    name: "Exeggcute",
                },
                {
                    name: "Pidgeot",
                },
                {
                    name: "Rapidash",
                },
                {
                    name: "Pinsir",
                },
                {
                    name: "Arcanine",
                },
                {
                    name: "Absol",
                },
                {
                    name: "Tropius",
                },
                {
                    name: "Gloom",
                },
                {
                    name: "Exploud",
                },
                {
                    name: "Jumpluff",
                },
                {
                    name: "Stantler",
                },
            ],
        },
        {
            name: "Route 122 Water",
            team: [
                {
                    name: "Golduck",
                },
                {
                    name: "Golbat",
                },
                {
                    name: "Pelipper",
                },
            ],
        },
        {
            name: "Mt. Pyre Floor 2",
            team: [
                {
                    name: "Golbat",
                },
                {
                    name: "Persian",
                },
                {
                    name: "Shuppet",
                },
                {
                    name: "Murkrow",
                },
                {
                    name: "Drowzee",
                },
                {
                    name: "Gastly",
                },
            ],
        },
        {
            name: "Lilycove Grass",
            team: [
                {
                    name: "Jumpluff",
                },
                {
                    name: "Bellossom",
                },
                {
                    name: "Granbull",
                },
                {
                    name: "Lickitung",
                },
                {
                    name: "Feraligatr",
                },
                {
                    name: "Blastoise",
                },
                {
                    name: "Vileplume",
                },
                {
                    name: "Togetic",
                },
                {
                    name: "Wigglytuff",
                },
            ],
        },
        {
            name: "Mossdeep Grass",
            team: [
                {
                    name: "Abra",
                },
                {
                    name: "Ralts",
                },
                {
                    name: "Slowpoke",
                },
                {
                    name: "Exeggcute",
                },
                {
                    name: "Spoink",
                },
                {
                    name: "Jynx",
                },
                {
                    name: "Mr. Mime",
                },
                {
                    name: "Girafarig",
                },
                {
                    name: "Drowzee",
                },
                {
                    name: "Chimecho",
                },
                {
                    name: "Xatu",
                },
                {
                    name: "Espeon",
                },
            ],
        },
        {
            name: "Mossdeep Water",
            team: [
                {
                    name: "Mantine",
                },
                {
                    name: "Octillery",
                },
                {
                    name: "Seaking",
                },
                {
                    name: "Relicanth",
                },
                {
                    name: "Tentacruel",
                },
            ],
        },
        {
            name: "Mossdeep Old Rod",
            team: [
                {
                    name: "Slowpoke",
                },
                {
                    name: "Shellder",
                },
            ],
        },
        {
            name: "Mossdeep Good Rod",
            team: [
                {
                    name: "Huntail",
                },
                {
                    name: "Slowbro",
                },
            ],
        },
        {
            name: "Mossdeep Super Rod",
            team: [
                {
                    name: "Cloyster",
                },
                {
                    name: "Crawdaunt",
                },
                {
                    name: "Gorebyss",
                },
                {
                    name: "Kingler",
                },
            ],
        },
        {
            name: "Route 110 Grass",
            team: [
                {
                    name: "Murkrow",
                },
                {
                    name: "Togetic",
                },
                {
                    name: "Roselia",
                },
                {
                    name: "Nuzleaf",
                },
                {
                    name: "Delcatty",
                },
                {
                    name: "Tropius",
                },
                {
                    name: "Lickitung",
                },
            ],
        },
        {
            name: "Route 111 Desert Sand",
            team: [
                {
                    name: "Diglett",
                },
                {
                    name: "Sandslash",
                },
            ],
        },
        {
            name: "Route 112 Grass",
            team: [
                {
                    name: "Spoink",
                },
                {
                    name: "Vulpix",
                },
                {
                    name: "Ponyta",
                },
                {
                    name: "Absol",
                },
            ],
        },
        {
            name: "Route 113 Grass",
            team: [
                {
                    name: "Teddiursa",
                },
                {
                    name: "Rhyhorn",
                },
                {
                    name: "Numel",
                },
                {
                    name: "Shroomish",
                },
                {
                    name: "Koffing",
                },
                {
                    name: "Parasect",
                },
            ],
        },
        {
            name: "Rustruf Tunnel",
            team: [
                {
                    name: "Nosepass",
                },
                {
                    name: "Dunsparce",
                },
                {
                    name: "Geodude",
                },
                {
                    name: "Swinub",
                },
                {
                    name: "Phanpy",
                },
                {
                    name: "Onix",
                },
                {
                    name: "Rhyhorn",
                },
                {
                    name: "Cubone",
                },
                {
                    name: "Whismur",
                },
                {
                    name: "Zubat",
                },
            ],
        },
        {
            name: "Mauville Grass",
            team: [
                {
                    name: "Pikachu",
                },
                {
                    name: "Elekid",
                },
                {
                    name: "Voltorb",
                },
                {
                    name: "Magnemite",
                },
            ],
        },
        {
            name: "Fallarbor Grass",
            team: [
                {
                    name: "Sudowoodo",
                },
                {
                    name: "Aron",
                },
                {
                    name: "Stantler",
                },
                {
                    name: "Noctowl",
                },
                {
                    name: "Mawile",
                },
            ],
        },
        {
            name: "Route 114 Grass",
            team: [
                {
                    name: "Pikachu",
                },
                {
                    name: "Swablu",
                },
                {
                    name: "Spinda",
                },
            ],
        },
        {
            name: "Meteor Falls Entrance",
            team: [
                {
                    name: "Clefairy",
                },
                {
                    name: "Dunsparce",
                },
                {
                    name: "Porygon",
                },
                {
                    name: "Solrock",
                },
                {
                    name: "Unown",
                },
                {
                    name: "Golbat",
                },
                {
                    name: "Parasect",
                },
            ],
        },
        {
            name: "Meteor Falls Room After Waterfall",
            team: [
                {
                    name: "Clefable",
                },
                {
                    name: "Lunatone",
                },
            ],
        },
        {
            name: "Meteor Falls Deepest Room Old Rod",
            team: [
                {
                    name: "Feebas",
                },
            ],
        },
        {
            name: "Meteor Falls Deepest Room Good Rod",
            team: [
                {
                    name: "Armaldo",
                },
                {
                    name: "Gyarados",
                },
            ],
        },
        {
            name: "Meteor Falls Deepest Room Super Rod",
            team: [
                {
                    name: "Milotic",
                },
            ],
        },
        {
            name: "Meteor Falls Deepest Room Water",
            team: [
                {
                    name: "Gyarados",
                },
            ],
        },
        {
            name: "Route 115 Grass",
            team: [
                {
                    name: "Swablu",
                },
                {
                    name: "Wigglytuff",
                },
                {
                    name: "Absol",
                },
                {
                    name: "Bagon",
                },
                {
                    name: "Beldum",
                },
                {
                    name: "Metang",
                },
                {
                    name: "Kangaskhan",
                },
                {
                    name: "Swellow",
                },
                {
                    name: "Eevee",
                },
                {
                    name: "Clefairy",
                },
            ],
        },
        {
            name: "Scorched Slab",
            team: [
                {
                    name: "Manectric",
                },
                {
                    name: "Rapidash",
                },
                {
                    name: "Vulpix",
                },
                {
                    name: "Ninetails",
                },
                {
                    name: "Growlithe",
                },
                {
                    name: "Magby",
                },
                {
                    name: "Magmar",
                },
                {
                    name: "Quilava",
                },
                {
                    name: "Flareon",
                },
                {
                    name: "Charmeleon",
                },
            ],
        },
        {
            name: "Scorched Slab Old Rod",
            team: [
                {
                    name: "Grimer",
                },
                {
                    name: "Muk",
                },
            ],
        },
        {
            name: "Jagged Pass Grass",
            team: [
                {
                    name: "Machoke",
                },
                {
                    name: "Numel",
                },
                {
                    name: "Ponyta",
                },
                {
                    name: "Magcargo",
                },
                {
                    name: "Spoink",
                },
                {
                    name: "Mankey",
                },
                {
                    name: "Onix",
                },
                {
                    name: "Doduo",
                },
            ],
        },
        {
            name: "Route 117 Grass",
            team: [
                {
                    name: "Dustox",
                },
                {
                    name: "Butterfree",
                },
                {
                    name: "Beautifly",
                },
                {
                    name: "Ledian",
                },
                {
                    name: "Oddish",
                },
                {
                    name: "Volbeat",
                },
                {
                    name: "Illumise",
                },
                {
                    name: "Beedrill",
                },
                {
                    name: "Nuzleaf",
                },
                {
                    name: "Ariados",
                },
                {
                    name: "Vulpix",
                },
                {
                    name: "Shroomish",
                },
            ],
        },
        {
            name: "Route 126 Seafloor",
            team: [
                {
                    name: "Huntail",
                },
                {
                    name: "Lanturn",
                },
            ],
        },
        {
            name: "Route 127 Water",
            team: [
                {
                    name: "Mantine",
                },
                {
                    name: "Sharpedo",
                },
            ],
        },
        {
            name: "Route 128 Water",
            team: [],
        },
        {
            name: "Route 129 Water",
            team: [
                {
                    name: "Pelipper",
                },
            ],
        },
        {
            name: "Sootopolis Grass",
            team: [
                {
                    name: "Heracross",
                },
                {
                    name: "Lotad",
                },
                {
                    name: "Lombre",
                },
            ],
        },
        {
            name: "Sootopolis Water",
            team: [
                {
                    name: "Mantine",
                },
                {
                    name: "Relicanth",
                },
                {
                    name: "Octillery",
                },
                {
                    name: "Magikarp",
                },
            ],
        },
        {
            name: "Sootopolis Super Rod",
            team: [
                {
                    name: "Armaldo",
                },
                {
                    name: "Omastar",
                },
                {
                    name: "Gorebyss",
                },
                {
                    name: "Sharpedo",
                },
                {
                    name: "Cradily",
                },
            ],
        },
        {
            name: "Route 134 Old Rod",
            team: [
                {
                    name: "Horsea",
                },
            ],
        },
        {
            name: "Ever Grande City Grass",
            team: [
                {
                    name: "Treecko",
                },
                {
                    name: "Grovyle",
                },
                {
                    name: "Sceptile",
                },
                {
                    name: "Torchic",
                },
                {
                    name: "Combusken",
                },
                {
                    name: "Blaziken",
                },
                {
                    name: "Marshtomp",
                },
                {
                    name: "Swampert",
                },
                {
                    name: "Eevee",
                },
            ],
        },
        {
            name: "Victory Road Entrance",
            team: [
                {
                    name: "Dodrio",
                },
                {
                    name: "Crobat",
                },
                {
                    name: "Dugtrio",
                },
                {
                    name: "Medicham",
                },
                {
                    name: "Wobbuffet",
                },
                {
                    name: "Jynx",
                },
                {
                    name: "Electrode",
                },
            ],
        },
    ];
    // TODO: Add ability to input available moves for pokemon in a panel
    // TODO: For each opponent, compute most effective available move
    // TODO: For each opponent, compute safest defensive typing
    // TODO: Add ability to export and import party and moves
    // opponentPresets.push({
    //     name: "National Dex",
    //     team: pokemonNames,
    // });
</script>

<main>
    <h1>Pokémon Emerald Kaizo DB</h1>
    <h2>Your Party</h2>
    <div id="party">
        {#each partyPokemon as _}
            <PartyPokemonPanel
                bind:selectedPokemon={_}
                opponents={opponentPokemon}
            />
        {/each}
    </div>
    <h2>Opponents</h2>
    Preset: <AutoComplete
        items={opponentPresets.map((preset) => preset.name)}
        hideArrow="true"
        bind:selectedItem={selectedOpponentPreset}
    />
    <div id="opponent">
        {#each opponentPokemon as _}
            <PartyPokemonPanel
                bind:selectedPokemon={_}
                opponents={partyPokemon}
            />
        {/each}
    </div>
</main>

<style>
    #party,
    #opponent {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
    }
</style>
