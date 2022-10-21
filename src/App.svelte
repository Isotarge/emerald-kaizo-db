<script>
    import PokemonPanel from "./lib/PokemonPanel.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import {
        encounterPresets,
        givePokemonDefaultMoves,
        pokemonByName,
        movesByName,
        computeMoveEffectiveness,
    } from "./state";
    import trainerPresets from "./trainers.json";
    import Matchup from "./lib/Matchup.svelte";

    // TODO: Import pokemon from .sav?
    // TODO: Add ability to export and import party
    const partyPresets = [
        {
            name: "Isotarge Mid/Late game team",
            team: [
                {
                    name: "Scizor",
                    item: "Silver Powder",
                    moves: [
                        "X-Scissors",
                        "Steel Wing",
                        "Air Slash",
                        "Double-Edge",
                    ],
                },
                {
                    name: "Vileplume",
                    item: "Miracle Seed",
                    moves: ["Sludge Bomb", "Cut", "Petal Dance", "Toxic"],
                },
                {
                    name: "Gyarados",
                    item: "Silk Scarf",
                    moves: ["Strength", "Surf", "Rock Smash", "Waterfall"],
                },
                {
                    name: "Flygon",
                    item: "Soft Sand",
                    moves: ["Fly", "Earthquake", "Dragon Claw", "Strength"],
                },
                {
                    name: "Spinda",
                    moves: [
                        "Hyper Voice",
                        "Superpower",
                        "Shadow Ball",
                        "Hypnosis",
                    ],
                },
                {
                    name: "Electrode",
                    moves: [
                        "Thunderbolt",
                        "Signal Beam",
                        "Explosion",
                        "Thunder Wave",
                    ],
                },
            ],
        },
        {
            name: "Isotarge E4 Ideas",
            team: [
                {
                    name: "Hariyama",
                    moves: [
                        "Superpower",
                        "Body Slam",
                        "Rock Slide",
                        "Shadow Punch",
                    ],
                },
                {
                    name: "Tauros",
                    item: "Silk Scarf",
                    moves: [
                        "Double-Edge",
                        "Earth Power",
                        "Quick Attack",
                        "Iron Tail",
                    ],
                },
                {
                    name: "Lapras",
                    item: "Mystic Water",
                    moves: [
                        "Ice Beam",
                        "Hydro Pump",
                        "Signal Beam",
                        "Ancientpower",
                    ],
                },
                {
                    name: "Scizor",
                    item: "Silver Powder",
                    moves: [
                        "X-Scissors",
                        "Steel Wing",
                        "Air Slash",
                        "Double-Edge",
                    ],
                },
                {
                    name: "Heracross",
                    item: "Silver Powder",
                    moves: [
                        "Megahorn",
                        "Brick Break",
                        "Rock Slide",
                        "Double-Edge",
                    ],
                },
                {
                    name: "Magikarp",
                },
            ],
        },
        {
            name: "Pokemon Challenges E4 Team",
            team: [
                {
                    name: "Dusclops",
                    moves: [
                        "Shadow Ball",
                        "Shadow Sneak",
                        "Earthquake",
                        "Ice Beam",
                    ],
                },
                {
                    name: "Wobbuffet",
                    moves: ["Destiny Bond", "Mirror Coat", "Encore", "Counter"],
                },
                {
                    name: "Ludicolo",
                    moves: [
                        "Fake Out",
                        "Giga Drain",
                        "Magical Leaf",
                        "Ice Beam",
                    ],
                },
                {
                    name: "Slowbro",
                    moves: ["Surf", "Flamethrower", "Slack Off", "Fire Blast"],
                },
                {
                    name: "Relicanth",
                    moves: [
                        "Head Smash",
                        "Ancientpower",
                        "Earthquake",
                        "Ice Beam",
                    ],
                },
                {
                    name: "Salamence",
                    moves: [
                        "Brick Break",
                        "Dragon Claw",
                        "Rock Slide",
                        "Rock Tomb",
                    ],
                },
            ],
        },
    ];

    const opponentPresets = [
        ...encounterPresets,
        ...trainerPresets,
        // { name: "National Dex", team: pokemonNames.map((pkmn) => {
        //     return { name: pkmn };
        // } },
        {
            name: "Elite Four",
            team: [
                ...trainerPresets.find(
                    (preset) => preset.name === "Elite Four Sidney"
                ).team,
                ...trainerPresets.find(
                    (preset) => preset.name === "Elite Four Phoebe"
                ).team,
                ...trainerPresets.find(
                    (preset) => preset.name === "Elite Four Glacia"
                ).team,
                ...trainerPresets.find(
                    (preset) => preset.name === "Elite Four Drake"
                ).team,
                ...trainerPresets.find(
                    (preset) => preset.name === "Champion Steven (2)"
                ).team,
            ],
        },
    ];

    let collapseOpponent = false;
    let selectedPartyPreset = partyPresets[0].name;
    $: partyPokemon = [
        ...partyPresets.find((preset) => preset.name === selectedPartyPreset)
            .team,
    ];
    let selectedOpponentPreset = opponentPresets[0].name;
    $: opponentPokemon = [
        ...opponentPresets.find(
            (preset) => preset.name === selectedOpponentPreset
        ).team,
    ];
    $: partyPokemon, opponentPokemon, recomputeMovesets();
    function recomputeMovesets() {
        if (debug) {
            console.log("Recomputing default movesets...");
        }
        partyPokemon.forEach(givePokemonDefaultMoves);
        opponentPokemon.forEach(givePokemonDefaultMoves);
    }

    let showAllMoves = false;
    let justTheArrows = true;

    // TODO: Better condition here, seems a bit too eager to recompute everything
    // I would like it to only recompute on the following changes:
    // - Pokemon count
    // - Pokemon species
    // - Pokemon moves
    // - Pokemon held item
    // But currently it's also recomputing when changing tab from learnset to moves
    $: opponentPokemon.length, partyPokemon.length, initMatchupArray();
    let debug = false;

    function updateEffectiveness(yourPokemon, opponent) {
        if (debug) {
            console.log("Updating effectiveness");
        }
        const state = {
            yourBestEffectiveness: 0,
            opponentBestEffectiveness: 0,
            yourEffectiveness: [],
            opponentEffectiveness: [],
        };
        if (yourPokemon.moves) {
            yourPokemon.moves.forEach((moveName) =>
                state.yourEffectiveness.push({
                    moveName,
                    score: computeMoveEffectiveness(
                        movesByName[moveName],
                        yourPokemon,
                        opponent
                    ),
                })
            );
            state.yourEffectiveness = state.yourEffectiveness.sort(
                (a, b) => b.score - a.score
            );
        }
        if (opponent.moves) {
            opponent.moves.forEach((moveName) =>
                state.opponentEffectiveness.push({
                    moveName,
                    score: computeMoveEffectiveness(
                        movesByName[moveName],
                        opponent,
                        yourPokemon
                    ),
                })
            );
            state.opponentEffectiveness = state.opponentEffectiveness.sort(
                (a, b) => b.score - a.score
            );
        }

        state.yourBestEffectiveness = state.yourEffectiveness[0]?.score || 0;
        state.opponentBestEffectiveness =
            state.opponentEffectiveness[0]?.score || 0;

        // Add the result of the computation to the party pokemon object
        yourPokemon.effectiveness.push(state);

        // Flip the perspective of the computations and add the result to the opponent object
        opponent.effectiveness.push({
            yourEffectiveness: state.opponentEffectiveness,
            yourBestEffectiveness: state.opponentBestEffectiveness,
            opponentEffectiveness: state.yourEffectiveness,
            opponentBestEffectiveness: state.yourBestEffectiveness,
        });
    }

    let totalCoverage = 0;
    function initMatchupArray() {
        if (debug) {
            console.log("Initting matchup array");
        }

        // Compute all permutations of effectiveness
        partyPokemon.forEach((pokemon) => {
            pokemon.effectiveness = [];
        });
        opponentPokemon.forEach((opponent) => {
            opponent.effectiveness = [];
        });
        partyPokemon.forEach((pokemon) => {
            opponentPokemon.forEach((opponent) => {
                updateEffectiveness(pokemon, opponent);
            });
        });

        // Compute totals
        partyPokemon.forEach((pokemon) => {
            pokemon.totalEffectiveness = pokemon.effectiveness.reduce(
                (a, v) =>
                    a + (v.yourBestEffectiveness - v.opponentBestEffectiveness),
                0
            );
        });
        totalCoverage = 0;
        opponentPokemon.forEach((pokemon) => {
            pokemon.totalEffectiveness = pokemon.effectiveness.reduce(
                (a, v) =>
                    a + (v.yourBestEffectiveness - v.opponentBestEffectiveness),
                0
            );
            pokemon.minEffectiveness = pokemon.effectiveness.reduce(
                (a, v) =>
                    Math.min(
                        a,
                        v.yourBestEffectiveness - v.opponentBestEffectiveness
                    ),
                Infinity
            );
            totalCoverage += pokemon.minEffectiveness;
        });
    }
</script>

<main>
    <h1>Pokémon Emerald Kaizo DB</h1>
    <h2>Your Party</h2>
    Preset: <AutoComplete
        items={partyPresets.map((preset) => preset.name)}
        hideArrow="true"
        bind:selectedItem={selectedPartyPreset}
    />
    <div id="party">
        {#each partyPokemon as _}
            <PokemonPanel bind:selectedPokemon={_} />
        {/each}
    </div>
    <h2>Opponents</h2>
    Preset: <AutoComplete
        items={opponentPresets.map((preset) => preset.name)}
        hideArrow="true"
        bind:selectedItem={selectedOpponentPreset}
    /> <input type="checkbox" bind:checked={collapseOpponent} /> Hide
    {#if !collapseOpponent}
        <div id="opponent">
            {#each opponentPokemon as _}
                <PokemonPanel bind:selectedPokemon={_} />
            {/each}
        </div>
    {/if}
    <h2>Matchup</h2>
    <input type="checkbox" bind:checked={showAllMoves} /> Show All Moves
    <input type="checkbox" bind:checked={justTheArrows} /> Just The Arrows
    <input type="checkbox" bind:checked={debug} /> Debug
    <div id="matchup">
        <table>
            <tr>
                <td>Coverage: {-totalCoverage}</td>
                {#each partyPokemon as yourPokemon}
                    <td
                        ><img
                            src="pokemon_sprites/{pokemonByName[
                                yourPokemon.name
                            ].dex}.png"
                            alt={yourPokemon.name}
                        /><br />{yourPokemon?.totalEffectiveness || 0}</td
                    >
                {/each}
            </tr>
            {#each opponentPokemon as opponent, opponentIndex (opponent)}
                <tr>
                    <td
                        ><img
                            src="pokemon_sprites/{pokemonByName[opponent.name]
                                .dex}.png"
                            alt={opponent.name}
                        /><br />Total: {opponent?.totalEffectiveness || 0}<br
                        />Min: {#if (opponent?.minEffectiveness || 0) < 0}
                            <span style="color: #393"
                                >{opponent?.minEffectiveness || 0}</span
                            >
                        {:else if (opponent?.minEffectiveness || 0) > 0}
                            <span style="color: #933"
                                >{opponent?.minEffectiveness || 0}</span
                            >
                        {:else}
                            0
                        {/if}</td
                    >
                    {#each partyPokemon as yourPokemon, yourPokemonIndex (yourPokemon)}
                        <td>
                            <Matchup
                                {debug}
                                bind:opponent
                                bind:yourPokemon
                                {showAllMoves}
                                {justTheArrows}
                                yourEffectiveness={yourPokemon.effectiveness[
                                    opponentIndex
                                ].yourEffectiveness}
                                opponentEffectiveness={opponent.effectiveness[
                                    yourPokemonIndex
                                ].yourEffectiveness}
                                yourBestEffectiveness={yourPokemon
                                    .effectiveness[opponentIndex]
                                    .yourBestEffectiveness}
                                opponentBestEffectiveness={opponent
                                    .effectiveness[yourPokemonIndex]
                                    .yourBestEffectiveness}
                            />
                        </td>
                    {/each}
                </tr>
            {/each}
        </table>
    </div>
</main>

<style>
    #party,
    #opponent {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
    }
    #matchup table,
    #matchup th,
    #matchup td {
        padding: 4px;
        border: 1px solid black;
        border-collapse: collapse;
    }
</style>
