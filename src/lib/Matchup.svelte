<script>
    import { pokemonByName, movesByName, moveDoesDamage } from "../state";
    import Move from "./Move.svelte";

    export let yourPokemon;
    export let opponent;
    export let yourEffectiveness;
    export let opponentEffectiveness;
    export let showAllMoves;
    export let justTheArrows;
    export let debug;
    export let yourBestEffectiveness;
    export let opponentBestEffectiveness;

    function pokemonHasPriority() {
        let opponentPriority = -Infinity;
        let yourPriority = -Infinity;

        yourPokemon.moves.forEach((move) => {
            let moveData = movesByName[move];
            if (moveDoesDamage(moveData)) {
                yourPriority = Math.max(yourPriority, moveData.priority);
            }
        });

        opponent.moves.forEach((move) => {
            let moveData = movesByName[move];
            if (moveDoesDamage(moveData)) {
                opponentPriority = Math.max(
                    opponentPriority,
                    moveData.priority
                );
            }
        });

        return yourPriority - opponentPriority;
    }

    $: yourPokemonData = pokemonByName[yourPokemon.name];
    $: opponentData = pokemonByName[opponent.name];
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
        <span style="color: #393">⮝ SPEED </span>
    {:else if yourPokemonData.speed < opponentData.speed}
        <span style="color: #933">⮜ SPEED </span>
    {:else}
        <span style="color: #980">= SPEED </span>
    {/if}
    {#if pokemonHasPriority() > 0}<span style="color: #393">!</span
        >{:else if pokemonHasPriority() < 0}<span style="color: #933">!</span
        >{/if}
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
