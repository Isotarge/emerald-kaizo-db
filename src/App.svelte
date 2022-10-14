<script>
    import PokemonPanel from "./lib/PokemonPanel.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import { encounterPresets } from "./state";
    import trainerPresets from "./trainers.json";
    import moves from "./moves.json";

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

    const opponentPresets = [...encounterPresets, ...trainerPresets];

    let selectedOpponentPreset = opponentPresets[0].name;
    $: opponentPokemon = [
        ...opponentPresets.find(
            (preset) => preset.name === selectedOpponentPreset
        ).team,
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
</main>

<style>
    #party,
    #opponent {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
    }
</style>
