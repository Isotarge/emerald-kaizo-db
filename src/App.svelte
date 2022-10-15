<script>
    import PokemonPanel from "./lib/PokemonPanel.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import { encounterPresets } from "./state";
    import trainerPresets from "./trainers.json";

    // TODO: Party presets
    // TODO: Import pokemon from .sav?
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
