<script>
    import PokemonPanel from "./lib/PokemonPanel.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import { encounterPresets, pokemonByName } from "./state";
    import trainerPresets from "./trainers.json";
    import Matchup from "./lib/Matchup.svelte";

    // TODO: Party presets
    // TODO: Import pokemon from .sav?
    // TODO: Add ability to input moveset for pokemon in a panel
    // TODO: Add ability to export and import party
    const partyPokemon = [
        {
            name: "Scizor",
            moves: ["X-Scissors", "Steel Wing", "Air Slash", "Double-Edge"],
        },
        {
            name: "Vileplume",
            moves: ["Sludge Bomb", "Cut", "Petal Dance", "Toxic"],
        },
        {
            name: "Gyarados",
            moves: ["Strength", "Surf", "Rock Smash", "Waterfall"],
        },
        {
            name: "Flygon",
            moves: ["Fly", "Earthquake", "Dragon Claw", "Strength"],
        },
        {
            name: "Spinda",
            moves: ["Hyper Voice", "Superpower", "Shadow Ball", "Hypnosis"],
        },
        {
            name: "Electrode",
            moves: ["Thunderbolt", "Signal Beam", "Explosion", "Thunder Wave"],
        },
    ];

    // const nationalDexPreset = pokemonNames.map((pkmn) => {
    //     return { name: pkmn };
    // });

    const opponentPresets = [
        ...encounterPresets,
        ...trainerPresets,
        // { name: "National Dex", team: nationalDexPreset },
    ];

    let selectedOpponentPreset = opponentPresets[0].name;
    $: opponentPokemon = [
        ...opponentPresets.find(
            (preset) => preset.name === selectedOpponentPreset
        ).team,
    ];

    let showAllMoves = false;
    let justTheArrows = false;
</script>

<main>
    <h1>Pokémon Emerald Kaizo DB</h1>
    <h2>Your Party</h2>
    <div id="party">
        {#each partyPokemon as _}
            <PokemonPanel
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
            <PokemonPanel bind:selectedPokemon={_} opponents={partyPokemon} />
        {/each}
    </div>
    <h2>Matchup</h2>
    <input type="checkbox" bind:checked={showAllMoves} /> Show All Moves
    <input type="checkbox" bind:checked={justTheArrows} /> Just The Arrows
    <div id="matchup">
        <table>
            <tr>
                <td />
                {#each partyPokemon as yourPokemon}
                    <td
                        ><img
                            src="pokemon_sprites/{pokemonByName[
                                yourPokemon.name
                            ].dex}.png"
                            alt={yourPokemon.name}
                        /></td
                    >
                {/each}
            </tr>
            {#each opponentPokemon as opponent}
                <tr>
                    <td
                        ><img
                            src="pokemon_sprites/{pokemonByName[opponent.name]
                                .dex}.png"
                            alt={opponent.name}
                        /></td
                    >
                    {#each partyPokemon as yourPokemon}
                        <td>
                            <Matchup
                                {opponent}
                                {yourPokemon}
                                bind:showAllMoves
                                bind:justTheArrows
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
