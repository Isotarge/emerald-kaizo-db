<script>
    import PartyPokemonPanel from "./lib/PartyPokemonPanel.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import { encounterPresets } from "./state";

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
        ...encounterPresets,
    ];
    // TODO: Add ability to input available moves for pokemon in a panel
    // TODO: For each opponent, compute most effective available move
    // TODO: For each opponent, compute safest defensive typing
    // TODO: Add ability to export and import party and moves
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
