<script>
    import {
        pokemonByName,
        movesByName,
        computeMoveEffectiveness,
    } from "../state";
    import Move from "./Move.svelte";

    export let yourPokemon;
    export let opponent;
    export let showAllMoves;
    export let justTheArrows;
    export let debug;
    export let yourBestEffectiveness = 0;
    export let opponentBestEffectiveness = 0;

    $: yourPokemonData = pokemonByName[yourPokemon.name];
    $: opponentData = pokemonByName[opponent.name];
    $: yourPokemon, opponent, updateEffectiveness();

    let yourEffectiveness = [];
    let opponentEffectiveness = [];
    function updateEffectiveness() {
        if (debug) {
            console.log("Updating effectiveness");
        }
        yourEffectiveness = [];
        opponentEffectiveness = [];
        if (yourPokemon.moves) {
            yourPokemon.moves.forEach((moveName) =>
                yourEffectiveness.push({
                    moveName,
                    score: computeMoveEffectiveness(
                        movesByName[moveName],
                        yourPokemon,
                        opponent
                    ),
                })
            );
            yourEffectiveness = yourEffectiveness.sort(
                (a, b) => b.score - a.score
            );
        }
        if (opponent.moves) {
            opponent.moves.forEach((moveName) =>
                opponentEffectiveness.push({
                    moveName,
                    score: computeMoveEffectiveness(
                        movesByName[moveName],
                        opponent,
                        yourPokemon
                    ),
                })
            );
            opponentEffectiveness = opponentEffectiveness.sort(
                (a, b) => b.score - a.score
            );
        }
        yourBestEffectiveness = yourEffectiveness[0]?.score || 0;
        opponentBestEffectiveness = opponentEffectiveness[0]?.score || 0;
    }
</script>

{#if debug}
    {yourBestEffectiveness - opponentBestEffectiveness}
{:else}
    {#if yourBestEffectiveness > opponentBestEffectiveness}
        <span style="color: #393"
            >⮝ POWER ({yourBestEffectiveness - opponentBestEffectiveness})</span
        >
    {:else if yourBestEffectiveness < opponentBestEffectiveness}
        <span style="color: #933"
            >⮜ POWER ({yourBestEffectiveness - opponentBestEffectiveness})</span
        >
    {:else}
        <span style="color: #980">= POWER</span>
    {/if}
    <br />
    {#if yourPokemonData.speed > opponentData.speed}
        <span style="color: #393">⮝ SPEED</span>
    {:else if yourPokemonData.speed < opponentData.speed}
        <span style="color: #933">⮜ SPEED</span>
    {:else}
        <span style="color: #980">= SPEED</span>
    {/if}
    {#if !justTheArrows}
        <table>
            {#if showAllMoves}
                {#if yourEffectiveness.length > 0}
                    <tr
                        ><td colspan="2"><b>{yourPokemon.name} moves</b></td><td
                            ><b>Score</b></td
                        ></tr
                    >
                    {#each yourEffectiveness as _}
                        <Move
                            moveName={_.moveName}
                            user={yourPokemon}
                            readOnly={true}
                            score={_.score}
                        />
                    {/each}
                {/if}
                {#if opponentEffectiveness.length > 0}
                    <tr
                        ><td colspan="2"><b>{opponent.name} moves</b></td><td
                            ><b>Score</b></td
                        ></tr
                    >
                    {#each opponentEffectiveness as _}
                        <Move
                            moveName={_.moveName}
                            user={opponent}
                            readOnly={true}
                            score={_.score}
                        />
                    {/each}
                {/if}
            {:else}
                {#if yourEffectiveness.length > 0}
                    <tr
                        ><td colspan="2"><b>{yourPokemon.name} best move</b></td
                        ><td><b>Score</b></td></tr
                    >
                    <Move
                        moveName={yourEffectiveness[0].moveName}
                        user={yourPokemon}
                        readOnly={true}
                        score={yourEffectiveness[0].score}
                    />
                {/if}
                {#if opponentEffectiveness.length > 0}
                    <tr
                        ><td colspan="2"><b>{opponent.name} best move</b></td
                        ><td><b>Score</b></td></tr
                    >
                    <Move
                        moveName={opponentEffectiveness[0].moveName}
                        user={opponent}
                        readOnly={true}
                        score={opponentEffectiveness[0].score}
                    />
                {/if}
            {/if}
        </table>
    {/if}
{/if}
