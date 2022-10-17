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
    export let user;
    export let readOnly = false;
    export let learnset = false;
    export let TMHM = false;
    export let level = 0;
    export let score = 0;

    $: userData = pokemonByName[user.name];
    $: moveData = movesByName[moveName];
    $: STAB =
        (userData.type1 === moveData.type ||
            userData.type2 === moveData.type) &&
        moveDoesDamage(moveData);
</script>

<tr>
    {#if level > 0}
        <td>{level}</td>
    {/if}
    <td>
        <Type
            whichType={moveData.type}
            specialDefenseBias={-userData.specialAttackBias}
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
    {#if !readOnly || learnset || TMHM}
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
