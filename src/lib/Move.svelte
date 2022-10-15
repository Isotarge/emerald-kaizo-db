<script>
    import Type from "./Type.svelte";
    import {
        movesByName,
        pokemonByName,
        typeData,
        checkTypeEffectivenessSTAB,
        moveDoesDamage,
    } from "../state.js";
    export let moveName = "Pound";
    export let user = pokemonByName["Scizor"];
    $: specialAttackBias = user.specialAttack - user.attack;
    $: specialDefenseBias = user.specialDefense - user.defense;
    export let opponents = [];
    $: moveData = movesByName[moveName];
    $: STAB =
        (user.type1 === moveData.type || user.type2 === moveData.type) &&
        moveDoesDamage(moveData);

    $: moveName, updateEffectiveness();

    let effectiveness = [];
    function updateEffectiveness() {
        effectiveness = [];
        opponents.forEach((opponent) =>
            effectiveness.push({
                name: opponent.name,
                effectiveness: computeMoveEffectiveness(
                    moveData,
                    user,
                    opponent
                ),
            })
        );
        effectiveness = effectiveness.sort(
            (a, b) => b.effectiveness - a.effectiveness
        );
    }

    function computeMoveEffectiveness(moveData, user, opponent) {
        // Move is not attacking, save some cycles
        if (!moveDoesDamage(moveData)) {
            return 0;
        }

        // Base power
        let effectiveness = moveData.power;

        // Base stat synergy
        const opponentData = pokemonByName[opponent.name];
        const type = typeData[moveData.type];
        if (type.contact === "Physical") {
            effectiveness += user.attack;
            effectiveness -= (opponentData.hp + opponentData.defense) / 2;
        } else if (type.contact === "Special") {
            effectiveness += user.specialAttack;
            effectiveness -=
                (opponentData.hp + opponentData.specialDefense) / 2;
        }

        // TODO: Held items
        // Black Belt
        // Black Glasses
        // Charcoal
        // Dragon Fang
        // Magnet
        // Miracle Seed
        // Mystic Water
        // Never-Melt Ice
        // Sea Incense
        // Sharp Beak
        // Silk Scarf
        // Silver Powder
        // Soft Sand
        // Spell Tag
        // Twisted Spoon

        // Soul Dew
        // Stick
        // Thick Club
        // Light Ball

        // STAB & Opponent type matchup
        effectiveness *= checkTypeEffectivenessSTAB(
            user.type1,
            user.type2,
            opponentData.type1,
            opponentData.type2,
            moveData.type
        );

        // Accuracy
        if (moveData.accuracy > 0) {
            effectiveness *= moveData.accuracy / 100;
        }

        return Math.round(effectiveness);
    }
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
{#each effectiveness as effective}
    <tr>
        <td colspan="5">
            {effective.effectiveness} effectiveness against
            {effective.name}
        </td>
    </tr>
{/each}

<style>
</style>
