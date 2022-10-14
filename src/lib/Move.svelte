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

<tr>
    <td>
        <Type
            whichType={moveData.type}
            specialDefenseBias={-specialAttackBias}
        />
    </td>
    <td>
        {#if STAB}
            <b>{moveData.name}</b>
        {:else}
            <span>{moveData.name}</span>
        {/if}
    </td>
    <td>
        {#if moveData.power > 1}
            {moveData.power}
        {/if}
    </td>
    <td>
        {#if moveData.accuracy > 0}
            {moveData.accuracy}%
        {/if}
    </td>
    <td>
        {moveData.pp}
    </td>
</tr>

<style>
</style>
