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

    const isoTMBag = [
        // Already in bag
        "Focus Punch",
        "Dragon Claw",
        "Water Pulse",
        "Roar",
        "Toxic",
        "Seismic Toss",
        "Blizzard",
        "Light Screen",
        "Giga Drain",
        "Safeguard",
        "Iron Tail",
        "Earthquake",
        "Return",
        "Dig",
        "Shadow Ball",
        "Brick Break",
        "Reflect",
        "Sludge Bomb",
        "Fire Blast",
        "Rock Tomb",
        "Aerial Ace",
        "Facade",
        "Secret Power",
        "Steel Wing",
        "Skill Swap",
        "Overheat",
    ];

    const TMHMRenewable = [
        // Game Corner
        "Draco Meteor",
        "Psychic",
        "Flamethrower",
        "Thunderbolt",
        "Ice Beam",
        // Lilycove Mart
        "Fire Blast",
        "Sludge Bomb",
        "Blizzard",
        "Steel Wing",
        "Aerial Ace",
        "Safeguard",
        "Reflect",
        "Light Screen",
        // HMs
        "Cut",
        "Fly",
        "Surf",
        "Strength",
        "Flash",
        "Rock Smash",
        "Waterfall",
        "Dive",
    ];

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
    {#if TMHM}
        {#if TMHMRenewable.includes(moveData.name)}
            <td style="color: #393"><b>R</b></td>
        {:else if isoTMBag.includes(moveData.name)}
            <td style="color: #980"><b>B</b></td>
        {:else}
            <td />
        {/if}
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
