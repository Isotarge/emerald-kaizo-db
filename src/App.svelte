<script>
    import PartyPokemonPanel from "./lib/PartyPokemonPanel.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import { pokemonNames, pokemon } from "./state";
    // TODO: Party presets
    // TODO: Search all presets for good matchups
    // TODO: Import pokemon from .sav?
    // const partyPokemon = [
    //     "Absol",
    //     "Scizor",
    //     "Alakazam",
    //     "Vileplume",
    //     "Octillery",
    //     "Swampert",
    // ];
    // const partyPokemon = [
    //     "Spinda",
    //     "Octillery",
    //     "Alakazam",
    //     "Exeggutor",
    //     "Swampert",
    //     "Scizor",
    // ];
    // const partyPokemon = [
    //     "Spinda",
    //     "Octillery",
    //     "Alakazam",
    //     "Electrode",
    //     "Swampert",
    //     "Scizor",
    // ];
    const partyPokemon = [
        "Scizor",
        "Vileplume",
        "Gyarados",
        "Flygon",
        "Spinda",
        "Electrode",
    ];

    // Archie Fight
    let selectedOpponentPreset = "Red (Victory Road)";
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
                "Qwilfish", // Level 70
                "Seaking", // Level 74
                "Whiscash", // Level 73, Earthquake
                "Masquerain", // Level 72 (Intimidate)
                "Manectric", // Level 70 (Intimidate)
                "Mawile", // Level 71 (Intimidate)
            ],
        },
        {
            name: "Ranger Andrea (Juan's Gym #2)",
            weather: "Rain",
            team: [
                "Venusaur", // Level 70, Weather Ball, Sleep Powder
                "Glalie", // Level 71 (Lum Berry) (Intimidate), Earthquake
                "Pinsir", // Level 70 (Intimidate), Earthquake
                "Huntail", // Level 73
                "Lanturn", // Level 72, Ice Beam, Surf
                "Pelipper", // Level 74, Hydro Pump
            ],
        },
        {
            name: "Parasol Lady Daphne (Juan's Gym #3)",
            weather: "Rain",
            team: [
                "Porygon2", // Level 70, Tri Attack
                "Walrein", // Level 73
                "Whiscash", // Level 74, Earthquake
                "Politoed", // Level 72, Belly Drum
                "Victreebel", // Sleep Powder
                "Ampharos", // Level 71, Thunder
            ],
        },
        {
            name: "Pokéfan Bethany (Juan's Gym)",
            weather: "Rain",
            team: [
                "Jolteon", // Level 70 (Petaya Berry), Substitute, Thunder
                "Politoed", // Level 74
                "Dewgong", // Level 73
                "Meganium", // Level 71 (Leftovers), Earthquake
                "Quagsire", // Level 73
                "Clefable", // Level 71, Clefable
            ],
        },
        {
            name: "Triathlete Brianna (Juan's Gym)",
            weather: "Rain",
            team: [
                "Electrode", // Level 70, Substitute, Explosion
                "Sceptile", // Level 71
                "Octillery", // Level 74
                "Golduck", // Level 73
                "Starmie", // Level 70
                "Magneton", // Level 72, Thunder
            ],
        },
        {
            name: "Battle Girl Crissy (Juan's Gym)",
            weather: "Rain",
            team: [
                "Medicham", // Level 70, Fake Out
                "Feraligatr", // Level 74
                "Poliwrath", // Level 74
                "Azumarill", // Level 74
                "Electabuzz",
                "Scizor", // Level 73
            ],
        },
        {
            name: "PKMN Breeder Bridget (Juan's Gym)",
            weather: "Rain",
            team: [
                "Mantine", // Level 74
                "Forretress", // Level 73, Earthquake
                "Mr. Mime", // Level 72, Fake Out, Thunder
                "Quagsire", // Level 74
                "Tentacruel", // Level 74
                "Blastoise", // Level 73
            ],
        },
        {
            name: "Expert Annika (Juan's Gym)",
            weather: "Rain",
            team: [
                "Gengar", // Level 74, Ice Punch
                "Dragonite", // Level 73 (Leftovers), Thunder
                "Omastar", // Level 75, Ice Beam
                "Vaporeon", // Level 73 (Leftovers), Muddy Water
                "Metagross", // Level 73, Earthquake
                "Golduck", // Level 73, Surf
            ],
        },
        {
            name: "Cooltrainer Olivia (Juan's Gym)",
            weather: "Rain",
            team: [
                "Gorebyss", // Level 75
                "Kabutops",
                "Wailord", // Level 75, Water Spout
                "Snorlax",
                "Salamence", // Level 73
            ],
        },
        {
            name: "Wallace (Juan's Gym)",
            weather: "Rain",
            team: [
                "Kingdra", // Level 76
                "Swampert", // Level 77, Yawn
                "Castform", // Level 76, Weather Ball
                "Milotic", // Level 77, Hypnosis
                "Ludicolo", // Level 76, Surf
                "Lapras", // Level 76 (Lum Berry), Surf, Thunder, Ice Beam
            ],
        },
        {
            name: "Juan (Double Battle)",
            weather: "Rain",
            team: [
                "Kingdra", // Level 77, Octazooka
                "Lapras", // Level 76
                "Castform", // Level 76, Hidden Power
                "Vaporeon", // Level 77
                "Lanturn", // Level 77
                "Ludicolo", // Level 77
            ],
        },
        {
            name: "Archie",
            weather: "Rain",
            team: [
                "Raikou",
                "Suicune",
                "Qwilfish",
                "Kingdra",
                "Metagross",
                "Dragonite",
            ],
        },
        {
            name: "Cooltrainer Albert (Victory Road)",
            team: [
                "Ninjask", // Level 82
                "Ursaring", // Level 81 (Leftovers), Swords Dance
                "Marowak", // Level 81, Earthquake
                "Medicham", // Level 81, Bulk Up, Brick Break
                "Grumpig", // Level 81 (Leftovers), Psychic
                "Ampharos", // Level 81, Hidden Power
            ],
        },
        {
            name: "Cooltrainer Hope (Victory Road)",
            team: [
                "Smeargle", // Level 83, Ingrain
                "Espeon", // Level 81, Calm Mind
                "Jolteon", // Level 81 (Leftovers), Substitute, Thunderbolt
                "Vaporeon", // Level 81 (Leftovers), Wish
                "Umbreon", // Level 81 (Leftovers), Wish
                "Solrock", // Level 81
            ],
        },
        {
            name: "Wally (Victory Road)",
            team: [
                "Meganium", // Level 85, Earthquake
                "Gardevoir", // Level 88, Fire Punch, Psychic, Calm Mind
                "Blissey", // Level 85 (Leftovers), Counter, Softboiled
                "Hitmontop", // Level 85 (Intimidate) (Lum Berry), Brick Break
                "Raichu", // Level 85 (Lum Berry), Extremespeed, Hidden Power
                "Vaporeon", // Level 85 (Leftovers), Ice Beam, Muddy Water
            ],
        },
        {
            name: "Expert Samuel (Victory Road)",
            team: [
                "Nidoking", // Poison Tail
                "Cradily",
                "Jynx",
                "Feraligatr",
                "Lanturn",
            ],
        },
        {
            name: "Expert Shannon (Victory Road)",
            team: [
                "Ditto", // Level 87
                "Blastoise", // Level 84
                "Manectric", // Level 84 (Intimidate), Hidden Power
                "Gligar", // Level 85, Earthquake
                "Tyranitar", // Level 84 (Intimidate)
                "Venomoth", // Level 85, Signal Beam, Psychic, Hidden Power (Fire)
            ],
        },
        {
            name: "Red (Victory Road)",
            team: [
                "Ho-Oh", // Level 87, Sky Attack, Sacred Fire, Earthquake
                "Celebi", // Level 88, Hidden Power (Fire), Giga Drain
                "Lapras", // Level 89, Ice Beam, Surf
                "Mew", // Level 88, Heat Wave, Psychic
                "Snorlax", // Level 89, Body Slam
                "Dragonite", // Level 89, Draco Meteor, Extremespeed, Hidden Power (Flying)
            ],
        },
        {
            name: "E4 Sydney",
            team: [
                "Sableye",
                "Jolteon",
                "Tauros",
                "Alakazam",
                "Machamp",
                "Houndoom",
            ],
        },
        {
            name: "E4 Phoebe",
            team: [
                "Gengar",
                "Ludicolo",
                "Crobat",
                "Gardevoir",
                "Sableye",
                "Dusclops",
            ],
        },
        {
            name: "E4 Glacia",
            team: [
                "Glalie",
                "Wailord",
                "Regice",
                "Dewgong",
                "Swampert",
                "Lapras",
            ],
        },
        {
            name: "E4 Drake",
            team: [
                "Latios", // Soul Dew, Draco Meteor, Luster Purge, Hidden Power, Recover
                "Tyranitar", // Lum Berry, Dragon Dance, Ancientpower, Earthquake, Hidden Power
                "Salamence", // Lum Berry, Draco Meteor, Air Slash, Earthquake, Flamethrower
                "Kingdra", // Lum Berry, Draco Meteor, Octazooka, Ice Beam, Hidden Power
                "Dragonite", // Lum Berry, Dragon Dance, Earthquake, Rock Slide, Extremespeed
                "Latias", // Soul Dew, Dragon Clar, Hidden Power, Calm Mind, Recover
            ],
        },
        {
            name: "E4 Champion",
            team: [
                "Metagross", // Lum Berry, Agility, Meteor Mash, Earthquake, Explosion
                "Starmie", // Lum Berry, Psychic, Hydro Pump, Thunderbolt, Ice Beam
                "Jirachi", // Lum Berry, Meteor Mash, Extrasensory, Fire Punch, Thunderbolt
                "Mewtwo", // Lum Berry, Psychic, Shadow Ball, Brick Break, Flamethrower
                "Aerodactyl", // Lum Berry, Sky Attack, Ancientpower, Earthquake, Flamethrower
                "Deoxys", // Lum Berry, Psycho Boost, Superpower, Shadow Ball, Fire Punch
            ],
        },
        {
            name: "Littleroot Water",
            team: [
                "Totodile", // Level 44, Ice Punch, Crunch, Superpower
                "Croconaw", // Level 44, Ice Punch, Crunch
                "Squirtle", // Level 44, Ice Punch, Body Slam, Aurora Beam, Bubblebeam
            ],
        },
        {
            name: "Littleroot Old Rod",
            team: [
                "Goldeen", // Level 5
                "Luvdisc", // Level 4
            ],
        },
        {
            name: "Littleroot Good Rod",
            team: [
                "Goldeen", // Level 20, Supersonic
                "Corphish", // Level 20, Metal Claw
            ],
        },
        {
            name: "Littleroot Super Rod",
            team: [
                "Seaking", // Level 65, Waterfall, Drill Run, Double-Edge
                "Luvdisc", // Level 65, Sweet Kiss, Attract, Surf, Flail
            ],
        },
        {
            name: "Route 101 Grass",
            team: [
                "Caterpie", // Level 2
                "Wurmple", // Level 2-3
                "Sentret", // Level 3, Quick Attack
                "Poochyena", // Level 2-3, Tackle
                "Ratata", // Level 3 (Rare I think)
                "Zigzagoon", // Level 3
                "Pidgey", // Level 3, Quick Attack
                "Togepi", // Level 2-3, Double-Edge
                "Cleffa", // Level 3
                "Igglybuff", // Level 2 (Rare I think)
                "Weedle", // Level 3
            ],
        },
        {
            name: "Oldale Grass",
            team: [
                "Vulpix", // Level 4-5, Quick Attack
                "Slugma", // Level 5
                "Numel", // Level 5
                "Ponyta", // Level 4
                "Growlithe", // Level 3-5
                "Magby", // Level 5
                "Charmander", // Level 4 (Rare I think)
            ],
        },
        {
            name: "Route 102 Grass",
            team: [
                "Spinarak", // Level 7
                "Gulpin", // Level 6
                "Electrike", // Level 6
                "Meowth", // Level 6
                "Sandshrew", // Level 6
                "Nidoran\u2642", // Level 6, Poison Sting
            ],
        },
        {
            name: "Route 102 Water",
            team: [
                "Seaking", // Level 43
                "Luvdisc", // Level 43
                "Poliwrath", // Level 43, Hypnosis, Mud Shot, Brick Break, Refresh
            ],
        },
        {
            name: "Petalburg Water",
            team: [
                "Golduck", // Level 43, Bubblebeam, Cross Chop, Psychic, Hypnosis
            ],
        },
        {
            name: "Route 103 Grass",
            team: [
                "Sunkern", // Level 4
                "Spoink", // Level 4
                "Mareep", // Level 4
                "Spearow", // Level 4
                "Ledyba", // Level 4, Silver Wind
                "Ekans", // Level 4
                "Wingull", // Level 4
                "Skitty", // Level 4, Assist, Sing
                "Hoppip", // Level 4 (Rare)
                "Poliwag", // Level 4 (Rare)
            ],
        },
        {
            name: "Route 103 Water",
            team: [
                "Kingler", // Level 43, Mud Shot
                "Seaking", // Level 43, Drill Run, Waterfall
            ],
        },
        {
            name: "Route 103 Old Rod",
            team: [
                "Remoraid", // Level 5, Psybeam
                "Tentacool", // Level 5, Poison Sting
            ],
        },
        {
            name: "Route 103 Good Rod",
            team: [
                "Octillery", // Level 20
            ],
        },
        {
            name: "Route 103 Super Rod",
            team: [
                "Octillery", // Level 65
            ],
        },
        {
            name: "Route 104 Grass",
            team: [
                "Elekid",
                "Venonat", // Level 7
                "Natu", // Level 7
                "Cubone", // Level 7
                "Nidoran\u2640", // Level 7
                "Seedot", // Level 7
            ],
        },
        {
            name: "Rustboro Grass",
            team: [
                "Seedot", // Level 9
                "Bellsprout", // Level 9
                "Oddish", // Level 9
                "Exeggcute", // Level 9
                "Bulbasaur", // Level 9, Vine Whip
                "Chikorita", // Level 9, Razor Leaf, Poisonpowder
                "Cacnea", // Level 9
                "Shroomish", // Level 9
            ],
        },
        {
            name: "Route 116 Grass",
            team: [
                "Grimer", // Level 9
                "Natu", // Level 9
                "Yanma", // Level 9
                "Makuhita", // Level 9
                "Metapod", // Level 9
                "Unown", // Level 9
                "Ralts", // Level 9
                "Spoink", // Level 9
                "Paras", // Level 9
                "Voltorb", // Level 9
                "Chimecho", // Level 9
                "Voltorb", // Level 9
            ],
        },
        {
            name: "Dewford Grass",
            team: [
                "Makuhita", // Level 15
                "Machop", // Level 15
                "Mankey", // Level 15
                "Meditite", // Level 15
                "Tyrogue", // Level 9
            ],
        },
        {
            name: "Slateport Grass",
            team: [
                "Minun", // Level 15
                "Elekid", // Level 15 (Static), Quick Attack
                "Magnemite", // Level 15
                "Electrike", // Level 15, Quick Attack
                "Pichu", // Level 15
                "Mareep", // Level 15
            ],
        },
        {
            name: "Slateport Old Rod",
            team: [
                "Corsola", // Level 15, Aurora Beam
                "Chinchou", // Level 15, Thundershock, Shock Wave, Water Gun
            ],
        },
        {
            name: "Slateport Good Rod",
            team: [
                "Mantine", // Level 20
                "Remoraid", // Level 20
            ],
        },
        {
            name: "Slateport Super Rod",
            team: [
                "Sharpedo", // Level 65, Crunch
                "Octillery", // Level 65, Signal Beam
            ],
        },
        {
            name: "Slateport Water",
            team: [
                "Octillery", // Level 43
                "Mantine", // Level 43, Air Slash
                "Pelipper", // Level 43, Water Pulse, Ice Beam
            ],
        },
        {
            name: "Route 120 Grass",
            team: [
                "Azumarill", // Level 47
                "Pinsir", // Level 47
                "Zangoose", // Level 47
                "Seviper", // Level 47
                "Spoink", // Level 47
                "Tangela", // Level 47
                "Kecleon", // Level 47
                "Primeape", // Level 47
                "Scyther", // Level 47
                "Scizor", // Level 47 (Rare)
                "Absol", // Level 47
            ],
        },
        {
            name: "Route 120 Water",
            team: [
                "Azumarill", // Level 47
                "Fearow", // Level 47
                "Seaking", // Level 47
                "Whiscash", // Level 47
            ],
        },
        {
            name: "Route 120 Super Rod",
            team: [
                "Kingler", // Level 65
                "Crawdaunt", // Level 65
            ],
        },
        {
            name: "Route 121 Grass",
            team: [
                "Weepinbell", // Level 50
                "Exeggcute", // Level 50, Sleep Powder, Stun Spore
                "Pidgeot", // Level 50, Heat Wave, Steel Wing
                "Rapidash", // Level 50
                "Pinsir", // Level 50
                "Arcanine", // Level 50
                "Absol", // Level 50
                "Tropius", // Level 50, Synthesis
                "Gloom", // Level 50
                "Exploud", // Level 50, Hyper Beam, Brick Break, Body Slam
                "Jumpluff", // Level 50
                "Stantler", // Level 50, Thunder Wave, Megahorn, Hypnosis
            ],
        },
        {
            name: "Route 122 Water",
            team: [
                "Golduck", // Level 51, Hypnosis, Ice Beam, Hydro Pump
                "Golbat", // Level 51, Air Slash
                "Pelipper", // Level 51
            ],
        },
        {
            name: "Mt. Pyre Floor 2",
            team: [
                "Golbat", // Level 51
                "Persian", // Level 51
                "Shuppet", // Level 51
                "Murkrow", // Level 51
                "Drowzee", // Level 51
                "Gastly", // Level 51
            ],
        },
        {
            name: "Lilycove Grass",
            team: [
                "Jumpluff", // Level 55, Synthesis, Stun Spore, Giga Drain
                "Bellossom", // Level 55, Double-Edge, Sleep Powder
                "Granbull", // Level 55 (Intimidate), Crunch, Superpower, Shadow Ball
                "Lickitung", // Level 55
                "Feraligatr", // Level 55
                "Blastoise", // Level 55, Seismic Toss, Ice Punch, Body Slam, Bubblebeam
                "Vileplume", // Level 55, Petal Dance
                "Togetic", // Level 55, Extremespeed, Safeguard
                "Wigglytuff", // Level 55 (Cute Charm), Hyper Voice, Shadow Ball
            ],
        },
        {
            name: "Mossdeep Grass",
            team: [
                "Abra", // Teleport
                "Ralts", // Level 65, Teleport, Hypnosis, Signal Beam, Imprison
                "Slowpoke", // Level 65, Extrasensory, Slack Off, Psychic, Aurora Beam
                "Exeggcute", // Level 65, Sleep Powder, Psychic, Egg Bomb
                "Spoink", // Level 65, Body Slam, Thunder Wave, Psychic
                "Jynx", // Rare
                "Mr. Mime", // Level 65 (Rare), Psychic, Hypnosis, Teeter Dance
                "Girafarig", // Level 65, Earthquake, Hyper Voice
                "Drowzee", // Level 65, Hypnosis
                "Chimecho", // Level 65
                "Xatu", // Level 65
                "Espeon", // Level 65, Psychic, Morning Sun
            ],
        },
        {
            name: "Mossdeep Water",
            team: [
                "Mantine", // Level 65, Air Slash, Confuse Ray, Ice Beam, Surf
                "Octillery", // Level 65, Ice Beam, Signal Beam, Octazooka, Flamethrower
                "Seaking", // Level 65, Megahorn
                "Relicanth", // Level 65, Head Smash, Double-Edge, Earthquake
                "Tentacruel", // Level 65
            ],
        },
        {
            name: "Mossdeep Old Rod",
            team: [
                "Slowpoke", // Level 65
                "Shellder", // Level 65, Selfdestruct, Bubblebeam, Ice Beam, Ice Shard
            ],
        },
        {
            name: "Mossdeep Good Rod",
            team: [
                "Huntail", // Level 65, Confuse Ray, Muddy Water, Ice Beam, Super Fang
                "Slowbro", // Level 65, Slack Off, Ice Punch, Psychic, Water Pulse
            ],
        },
        {
            name: "Mossdeep Super Rod",
            team: [
                "Cloyster", // Level 65, Ice Shard
                "Crawdaunt", // Level 65, Crabhammer
                "Gorebyss", // Level 65, Bounce
                "Kingler", // Level 65, Crush Claw, X-Scissors, Crabhammer, Superpower
            ],
        },
        {
            name: "Route 110 Grass",
            team: [
                "Murkrow", // Level 15
                "Togetic", // Level 15, Double-Edge
                "Roselia", // Level 15
                "Nuzleaf", // Level 15
                "Delcatty", // Level 15
                "Tropius", // Level 15
                "Lickitung", // Level 15
            ],
        },
        {
            name: "Route 111 Desert Sand",
            team: [
                "Diglett", // Level 40, Dig
                "Sandslash", // Level 39, Poison Sting
            ],
        },
        {
            name: "Route 112 Grass",
            team: [
                "Spoink", // Level 27
                "Vulpix", // Level 27
                "Ponyta", // Level 27
                "Absol", // Level 27
            ],
        },
        {
            name: "Route 113 Grass",
            team: [
                "Teddiursa", // Level 30, Slash
                "Rhyhorn", // Level 30, Drill Run, Rock Throw, Rock Blast
                "Numel", // Level 30, Body Slam
                "Shroomish", // Level 30, Stun Spore
                "Koffing", // Level 30, Smog, Selfdestruct
                "Parasect", // Level 30, Spore
            ],
        },
        {
            name: "Rustruf Tunnel",
            team: [
                "Nosepass", // Level 10-12, Magnitude
                "Dunsparce", // Level 10-12
                "Geodude", // Level 10-12
                "Swinub", // Level 10-12
                "Phanpy", // Level 10-12
                "Onix", // Level 10-12
                "Rhyhorn", // Level 10-12
                "Cubone", // Level 10-12
                "Whismur", // Level 10 (Rare)
                "Zubat", // Level 10 (Rare)
            ],
        },
        {
            name: "Mauville Grass",
            team: [
                "Pikachu", // Level 20
                "Elekid", // Level 20
                "Voltorb", // Level 20
                "Magnemite", // Level 20
            ],
        },
        {
            name: "Fallarbor Grass",
            team: [
                "Sudowoodo", // Level 34, Rock Tomb, Rock Slide, Earth Power
                "Aron", // Level 34, Flash Cannon, Rock Slide, Iron Tail, Double-Edge
                "Stantler", // Level 34, Disable, Megahorn, Jump Kick
                "Noctowl", // Level 34
                "Mawile", // Level 34
            ],
        },
        {
            name: "Route 114 Grass",
            team: [
                "Pikachu", // Level 34, Wild Charge
                "Swablu", // Level 34, Hyper Voice, Refresh
                "Spinda", // Level 34, Shadow Ball, Superpower
            ],
        },
        {
            name: "Meteor Falls Entrance",
            team: [
                "Clefairy", // Level 35, Helping Hand
                "Dunsparce", // Level 35, Endevaour
                "Porygon", // Level 35 (20%) It can flee???
                "Solrock", // Level 35
                "Unown", // Level 35
                "Golbat", // Level 35
                "Parasect", // Level 35
            ],
        },
        {
            name: "Meteor Falls Room After Waterfall",
            team: [
                "Clefable", // Level 70 (Cute Charm), Endeavour, Wish, Recycle
                "Lunatone", // Level 70, Hypnosis, Ancientpower
            ],
        },
        {
            name: "Meteor Falls Deepest Room Old Rod",
            team: [
                "Feebas", // Level 70, Flail, Tackle
            ],
        },
        {
            name: "Meteor Falls Deepest Room Good Rod",
            team: [
                "Armaldo", // Level 70
                "Gyarados", // Level 70 (Intimidate), Bounce
            ],
        },
        {
            name: "Meteor Falls Deepest Room Super Rod",
            team: [
                "Milotic", // Level 70, Whirlpool, Water Sport, Ice Beam, Hydro Pump
            ],
        },
        {
            name: "Meteor Falls Deepest Room Water",
            team: [
                "Gyarados", // Level 70 (Intimidate), Bounce, Hydro Pump, Double-Edge
            ],
        },
        {
            name: "Route 115 Grass",
            team: [
                "Swablu", // Level 43
                "Wigglytuff", // Level 43
                "Absol", // Level 43
                "Bagon", // Level 43
                "Beldum", // Level 19, 43
                "Metang", // Level 40
                "Kangaskhan", // Level 43
                "Swellow", // Level 43
                "Eevee", // Level 43
                "Clefairy", // Level 43
            ],
        },
        {
            name: "Scorched Slab",
            team: [
                "Manectric", // Level 50
                "Rapidash", // Level 50
                "Vulpix", // Level 50
                "Ninetails", // Level 50
                "Growlithe", // Level 50
                "Magby", // Level 50
                "Magmar", // Level 50
                "Quilava", // Level 50
                "Flareon", // Level 50
                "Charmeleon", // Level 50
            ],
        },
        {
            name: "Scorched Slab Old Rod",
            team: [
                "Grimer", // Level 45, Toxic
                "Muk", // Level 45, Toxic, Shadow Ball, Sludge Bomb
            ],
        },
        {
            name: "Jagged Pass Grass",
            team: [
                "Machoke", // Level 36, Seismic Toss, Vital Throw
                "Numel", // Level 36
                "Ponyta", // Level 36
                "Magcargo", // Level 36
                "Spoink", // Level 36
                "Mankey", // Level 36
                "Onix", // Level 36
                "Doduo", // Level 36
            ],
        },
        {
            name: "Route 117 Grass",
            team: [
                "Dustox", // Level 20, Moonlight, Toxic
                "Butterfree", // Level 20
                "Beautifly", // Level 20
                "Ledian", // Level 20
                "Oddish", // Level 20
                "Volbeat", // Level 20
                "Illumise", // Level 20
                "Beedrill", // Level 20
                "Nuzleaf", // Level 20
                "Ariados", // Level 20
                "Vulpix", // Level 20
                "Shroomish", // Level 20
            ],
        },
        {
            name: "Route 126 Seafloor",
            team: [
                "Huntail", // Level 68, Super Fang, Confuse Ray, Ice Beam, Muddy Water
                "Lanturn", // Level 68, Thunderbolt, Confuse Ray, Hydro Pump, Thunder Wave
            ],
        },
        {
            name: "Route 127 Water",
            team: [
                "Mantine", // Level 65
                "Sharpedo", // Level 65
            ],
        },
        {
            name: "Route 128 Water",
            team: [],
        },
        {
            name: "Route 129 Water",
            team: [
                "Pelipper", // Level 65, Sky Attack
            ],
        },
        {
            name: "Sootopolis Grass",
            team: [
                "Heracross", // Level 6,8,9,10
                "Lotad", // Level 11,12,17,18,19,20,22,40
                "Lombre", // Level 12,15,17,20,25
            ],
        },
        {
            name: "Sootopolis Water",
            team: [
                "Mantine", // Level 70, Confuse Ray, Air Slash, Ice Beam
                "Relicanth", // Level 70, Double-Edge
                "Octillery", // Level 70, Water Spout, Flamethrower
                "Magikarp", // Level 70 (Rare), Flail, Bounce
            ],
        },
        {
            name: "Sootopolis Super Rod",
            team: [
                "Armaldo",
                "Omastar",
                "Gorebyss", // Rare?
                "Sharpedo", // Rare
                "Cradily", // Rare
            ],
        },
        {
            name: "Route 134 Old Rod",
            team: [
                "Horsea", // Level 43
            ],
        },
        {
            name: "Ever Grande City Grass",
            team: [
                "Treecko", // Level 70 (Oran Berry), Thunderpunch, Crunch, Giga Drain
                "Grovyle", // Level 70, Crush Claw, Crunch
                "Sceptile", // Level 70, Crush Claw, Dragon Claw, Leaf Blade
                "Torchic", // Level 70 (Speed Boost), Quick Attack, Crush Claw, Flamethrower
                "Combusken", // Level 70, Flamethrower, Sky Uppercut, Quick Attack, Crush Claw
                "Blaziken", // Level 70, Quick Attack, Crush Claw
                "Marshtomp", // Level 70, Endeavour, Ice Punch
                "Swampert", // Level 70, Endeavour, Ice Punch
                "Eevee", // Level 70, Bite, Body Slam, Quick Attack
            ],
        },
        {
            name: "Victory Road Entrance",
            team: [
                "Dodrio", // Level 72, Steel Wing
                "Crobat", // Level 72, Confuse Ray, Mean Look, Poison Fang, Air Slash
                "Dugtrio", // Level 72, Earthquake, Slash
                "Medicham", // Level 72, Reversal, Hi Jump Kick
                "Wobbuffet", // Level 72 (Shadow Tag), Destiny Bond, Counter
                "Jynx", // Level 72, Lovely Kiss, Psychic, Ice Beam, Teleport
                "Electrode", // Level 72, Signal Beam, Thunderbolt
            ],
        },
    ];
    // TODO: Add ability to input available moves for pokemon in a panel
    // TODO: For each opponent, compute most effective available move
    // TODO: For each opponent, compute safest defensive typing
    // TODO: Add ability to export and import party and moves
    opponentPresets.push({
        name: "National Dex",
        team: pokemonNames,
    });

    const search = {
        HP: 0,
        attack: 0,
        defense: 0,
        specialAttack: 0,
        specialDefense: 0,
        speed: 0,
        totalBaseStats: 0,
    };

    $: search, doSearch();
    let searchResults = [];
    function doSearch() {
        searchResults = pokemon.filter(
            (p) =>
                p.hp >= search.HP &&
                p.attack >= search.attack &&
                p.defense >= search.defense &&
                p.specialAttack >= search.specialAttack &&
                p.specialDefense >= search.specialDefense &&
                p.speed >= search.speed &&
                p.totalBaseStats >= search.totalBaseStats
        );
    }
    let searchEnabled = false;
    function toggleSearch() {
        searchEnabled = !searchEnabled;
    }
</script>

<main>
    <h1>Pokémon Emerald Kaizo DB</h1>
    <h2>Your Party</h2>
    <div id="party">
        {#each partyPokemon as _}
            <PartyPokemonPanel
                bind:selectedPokemonName={_}
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
                bind:selectedPokemonName={_}
                opponents={partyPokemon}
            />
        {/each}
    </div>
    <h2>Search</h2>
    <button on:click={toggleSearch}>Toggle</button>
    {#if searchEnabled}
        <table>
            <tr>
                <td>HP</td>
                <td
                    ><input
                        type="range"
                        min="0"
                        max="255"
                        bind:value={search.HP}
                    /></td
                >
                <td>{search.HP}</td>
            </tr>
            <tr>
                <td>Attack</td>
                <td
                    ><input
                        type="range"
                        min="0"
                        max="255"
                        bind:value={search.attack}
                    /></td
                >
                <td>{search.attack}</td>
            </tr>
            <tr>
                <td>Defense</td>
                <td
                    ><input
                        type="range"
                        min="0"
                        max="255"
                        step="1"
                        bind:value={search.defense}
                    /></td
                >
                <td>{search.defense}</td>
            </tr>
            <tr>
                <td>Special Attack</td>
                <td
                    ><input
                        type="range"
                        min="0"
                        max="255"
                        step="1"
                        bind:value={search.specialAttack}
                    /></td
                >
                <td>{search.specialAttack}</td>
            </tr>
            <tr>
                <td>Special Defense</td>
                <td
                    ><input
                        type="range"
                        min="0"
                        max="255"
                        step="1"
                        bind:value={search.specialDefense}
                    /></td
                >
                <td>{search.specialDefense}</td>
            </tr>
            <tr>
                <td>Speed</td>
                <td
                    ><input
                        type="range"
                        min="0"
                        max="255"
                        step="1"
                        bind:value={search.speed}
                    /></td
                >
                <td>{search.speed}</td>
            </tr>
            <tr>
                <td>Total</td>
                <td
                    ><input
                        type="range"
                        min="0"
                        max="1530"
                        step="1"
                        bind:value={search.totalBaseStats}
                    /></td
                >
                <td>{search.totalBaseStats}</td>
            </tr>
        </table>
        {searchResults.length} / {pokemon.length}
        <ul>
            {#each searchResults as _}
                <li>{_.name}</li>
            {/each}
        </ul>
    {/if}
</main>

<style>
    #party,
    #opponent {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
    }
</style>
