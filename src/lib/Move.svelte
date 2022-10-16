<script>
    import AutoComplete from "simple-svelte-autocomplete";
    import Type from "./Type.svelte";
    import {
        moveNames,
        movesByName,
        pokemonByName,
        moveDoesDamage,
    } from "../state.js";

    export let moveName = "Pound";
    // TODO: Don't pass in userData
    export let user = pokemonByName["Scizor"];
    export let readOnly = false;
    export let score = 0;

    $: moveData = movesByName[moveName];
    $: STAB =
        (user.type1 === moveData.type || user.type2 === moveData.type) &&
        moveDoesDamage(moveData);
</script>

<tr>
    <td>
        <Type
            whichType={moveData.type}
            specialDefenseBias={-user.specialAttackBias}
        />
    </td>
    <td>
        {#if readOnly}
            {#if STAB}
                <b>{moveData.name}</b>
            {:else}
                <span>{moveData.name}</span>
            {/if}
        {:else}
            <AutoComplete
                items={moveNames}
                bind:selectedItem={moveName}
                hideArrow="true"
            />
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
    td {
        padding: 4px;
    }
</style>
