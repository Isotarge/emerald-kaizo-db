<script>
    import Type from "./Type.svelte";
    import { movesByName, pokemonByName, moveDoesDamage } from "../state.js";
    export let moveName = "Pound";
    export let user = pokemonByName["Scizor"];
    export let readOnly = false;
    export let score = 0;
    $: specialAttackBias = user.specialAttack - user.attack;
    // $: specialDefenseBias = user.specialDefense - user.defense;
    $: moveData = movesByName[moveName];
    $: STAB =
        (user.type1 === moveData.type || user.type2 === moveData.type) &&
        moveDoesDamage(moveData);
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
    {#if !readOnly}
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
    {/if}
    {#if score > 0}
        <td>
            {score}
        </td>
    {/if}
</tr>

<style>
</style>
