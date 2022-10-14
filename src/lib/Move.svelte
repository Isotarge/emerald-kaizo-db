<script>
    import Type from "./Type.svelte";
    import { movesByName, pokemonByName } from "../state.js";
    export let moveName = "Pound";
    export let user = pokemonByName["Scizor"];
    $: specialAttackBias = user.specialAttack - user.attack;
    $: specialDefenseBias = user.specialDefense - user.defense;
    export let opponents = [];
    $: moveData = movesByName[moveName];
    $: STAB =
        (user.type1 === moveData.type || user.type2 === moveData.type) &&
        moveData.power > 0;
</script>

<p>
    <Type whichType={moveData.type} specialDefenseBias={-specialAttackBias} />
    <!-- {user.name} -->
    <!-- {moveName} -->
    {#if STAB}
        <b>{moveData.name}</b>
    {:else}
        <span>{moveData.name}</span>
    {/if}
</p>

<style>
</style>
