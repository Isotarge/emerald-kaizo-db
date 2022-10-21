<script>
    import Type from "./Type.svelte";
    import AutoComplete from "simple-svelte-autocomplete";
    import {
        MAX_TOTAL_BASE_STATS,
        pokemonByName,
        pokemonNames,
        abilityData,
        typeData,
        checkTypeEffectiveness,
        pokemon,
    } from "../state";
    import Move from "./Move.svelte";

    export let selectedPokemon;
    $: selectedPokemonData = pokemonByName[selectedPokemon.name];

    $: typeMatchup = computeTypeMatchup(selectedPokemonData);
    $: doubleSuperEffectiveTypes = typeMatchup
        .filter((v) => v.effectiveness === 4)
        .map((v) => v.type);
    $: superEffectiveTypes = typeMatchup
        .filter((v) => v.effectiveness === 2)
        .map((v) => v.type);
    $: notVeryEffectiveTypes = typeMatchup
        .filter((v) => v.effectiveness === 0.5)
        .map((v) => v.type);
    $: doubleNotVeryEffectiveTypes = typeMatchup
        .filter((v) => v.effectiveness === 0.25)
        .map((v) => v.type);
    $: immuneTypes = typeMatchup
        .filter((v) => v.effectiveness === 0)
        .map((v) => v.type);

    export let selectedPanel = "Stats";

    function hasAbility(pokemonData, abilityName) {
        return (
            pokemonData.ability1 === abilityName ||
            pokemonData.ability2 === abilityName
        );
    }

    function computeTypeMatchup(pokemonData) {
        const matchup = [];
        Object.keys(typeData).forEach((type) => {
            let singleMatchup = checkTypeEffectiveness(
                type,
                pokemonData.type1,
                pokemonData.type2
            );
            if (hasAbility(pokemonData, "Levitate") && type === "Ground") {
                singleMatchup = 0;
            }
            if (hasAbility(pokemonData, "Flash Fire") && type === "Fire") {
                singleMatchup = 0;
            }
            if (
                hasAbility(pokemonData, "Thick Fat") &&
                (type === "Fire" || type === "Ice")
            ) {
                singleMatchup /= 2;
                // TODO: This is wrong, should be 12.5% but it wouldn't display if we used that value
                if (singleMatchup < 0.25 && singleMatchup > 0) {
                    singleMatchup = 0.25;
                }
            }
            if (hasAbility(pokemonData, "Volt Absorb") && type === "Electric") {
                singleMatchup = 0;
            }
            if (hasAbility(pokemonData, "Water Absorb") && type === "Water") {
                singleMatchup = 0;
            }
            if (hasAbility(pokemonData, "Wonder Guard") && singleMatchup < 2) {
                singleMatchup = 0;
            }
            matchup.push({
                type,
                effectiveness: singleMatchup,
            });
        });
        return matchup;
    }

    function getGistOfPokemon(pokemonData) {
        let attackType = "Mixed Attacker";
        let defenseType = "Mixed Defender";
        if (pokemonData.specialAttackBias > 0) {
            attackType = "Special Attacker";
        } else if (pokemonData.specialAttackBias < 0) {
            attackType = "Physical Attacker";
        }
        if (pokemonData.specialDefenseBias > 0) {
            defenseType = "Special Defender";
        } else if (pokemonData.specialDefenseBias < 0) {
            defenseType = "Physical Defender";
        }
        return `${attackType} (${pokemonData.specialAttackBias}), ${defenseType} (${pokemonData.specialDefenseBias})`;
    }

    function deleteHoldItem() {
        delete selectedPokemon.item;
        selectedPokemon = selectedPokemon;
    }
</script>

<div>
    <p>
        <AutoComplete
            items={pokemonNames}
            bind:selectedItem={selectedPokemon.name}
            hideArrow="true"
        />
        <img
            src="pokemon_sprites/{selectedPokemonData.dex}.png"
            alt={selectedPokemonData.name}
            style="margin-top:-20px"
        /><br />
    </p>
    <Type
        whichType={selectedPokemonData.type1}
        specialDefenseBias={-selectedPokemonData.specialAttackBias}
    />
    {#if selectedPokemonData.type2 !== selectedPokemonData.type1}
        <Type
            whichType={selectedPokemonData.type2}
            specialDefenseBias={-selectedPokemonData.specialAttackBias}
        />
    {/if}
    <p>
        {#if selectedPokemon.encounterChance}
            {selectedPokemon.encounterChance}% Chance
        {/if}
        {#if selectedPokemon.level}
            @ Level {selectedPokemon.level}
        {:else if selectedPokemon.minLevel || selectedPokemon.maxLevel}
            {#if selectedPokemon.minLevel === selectedPokemon.maxLevel}
                @ Level {selectedPokemon.minLevel}
            {:else}
                @ Level {selectedPokemon.minLevel}-{selectedPokemon.maxLevel}
            {/if}
        {/if}
    </p>
    <p>
        {#if selectedPokemon.item}
            Holding: {selectedPokemon.item}
            <button on:click={deleteHoldItem}>X</button>
        {/if}
    </p>
    <table style="margin: auto; min-height: 4rem;">
        <tr>
            <td><b>{selectedPokemonData.ability1}</b></td>
            <td>{abilityData[selectedPokemonData.ability1]}</td>
        </tr>
        {#if selectedPokemonData.ability2 !== selectedPokemonData.ability1 && selectedPokemonData.ability2 !== "None"}
            <tr>
                <td><b>{selectedPokemonData.ability2}</b></td>
                <td>{abilityData[selectedPokemonData.ability2]}</td>
            </tr>
        {/if}
    </table>
    <p>
        {getGistOfPokemon(selectedPokemonData)}
    </p>
    <button on:click={() => (selectedPanel = "Stats")}>Stats</button>
    <button on:click={() => (selectedPanel = "Weaknesses")}>Weaknesses</button>
    <button on:click={() => (selectedPanel = "Moves")}>Moves</button>
    <button on:click={() => (selectedPanel = "Learnset")}>Learnset</button>
    <button on:click={() => (selectedPanel = "TM/HM")}>TM/HM</button>
    {#if selectedPanel === "Stats"}
        <table style="margin: auto">
            <tr>
                <td>HP</td>
                <td>{selectedPokemonData.hp}</td>
                <td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max="255"
                        value={selectedPokemonData.hp}
                    /></td
                >
            </tr>
            <tr
                ><td>Attack</td><td>{selectedPokemonData.attack}</td><td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max="255"
                        value={selectedPokemonData.attack}
                    /></td
                ></tr
            >
            <tr
                ><td>Defense</td><td>{selectedPokemonData.defense}</td><td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max="255"
                        value={selectedPokemonData.defense}
                    /></td
                ></tr
            >
            <tr
                ><td>Sp. Attack</td><td>{selectedPokemonData.specialAttack}</td
                ><td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max="255"
                        value={selectedPokemonData.specialAttack}
                    /></td
                ></tr
            >
            <tr
                ><td>Sp. Defense</td><td
                    >{selectedPokemonData.specialDefense}</td
                ><td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max="255"
                        value={selectedPokemonData.specialDefense}
                    /></td
                ></tr
            >
            <tr
                ><td>Speed</td><td>{selectedPokemonData.speed}</td><td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max="255"
                        value={selectedPokemonData.speed}
                    /></td
                ></tr
            >
            <tr
                ><td>Total</td><td>{selectedPokemonData.totalBaseStats}</td><td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max={MAX_TOTAL_BASE_STATS}
                        value={selectedPokemonData.totalBaseStats}
                    /></td
                ></tr
            >
            <tr>
                <td>Catch Rate</td>
                <td>{selectedPokemonData.catchRate}</td>
                <td
                    ><input
                        disabled
                        type="range"
                        min="0"
                        max="255"
                        value={selectedPokemonData.catchRate}
                    /></td
                >
            </tr>
        </table>
    {:else if selectedPanel === "Weaknesses"}
        {#if doubleSuperEffectiveTypes.length > 0}
            <h3 class="type-heading">4x Effective</h3>
            <div class="type-table">
                {#each doubleSuperEffectiveTypes as type}
                    <Type
                        whichType={type}
                        specialDefenseBias={selectedPokemonData.specialDefenseBias}
                    />
                {/each}
            </div>
        {/if}
        {#if superEffectiveTypes.length > 0}
            <h3 class="type-heading">Super Effective</h3>
            <div class="type-table">
                {#each superEffectiveTypes as type}
                    <Type
                        whichType={type}
                        specialDefenseBias={selectedPokemonData.specialDefenseBias}
                    />
                {/each}
            </div>
        {/if}
        {#if notVeryEffectiveTypes.length > 0}
            <h3 class="type-heading">Not Very Effective</h3>
            <div class="type-table">
                {#each notVeryEffectiveTypes as type}
                    <Type
                        whichType={type}
                        specialDefenseBias={selectedPokemonData.specialDefenseBias}
                    />
                {/each}
            </div>
        {/if}
        {#if doubleNotVeryEffectiveTypes.length > 0}
            <h3 class="type-heading">0.25x Effective</h3>
            <div class="type-table">
                {#each doubleNotVeryEffectiveTypes as type}
                    <Type
                        whichType={type}
                        specialDefenseBias={selectedPokemonData.specialDefenseBias}
                    />
                {/each}
            </div>
        {/if}
        {#if immuneTypes.length > 0}
            <h3 class="type-heading">Immune</h3>
            <div class="type-table">
                {#each immuneTypes as type}
                    <Type
                        whichType={type}
                        specialDefenseBias={selectedPokemonData.specialDefenseBias}
                    />
                {/each}
            </div>
        {/if}
    {:else if selectedPanel === "Moves"}
        {#if selectedPokemon.moves}
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Move</th>
                        <th>Power</th>
                        <th>Accuracy</th>
                        <th>PP</th>
                    </tr>
                </thead>
                {#each selectedPokemon.moves as move}
                    <Move bind:moveName={move} bind:user={selectedPokemon} />
                {/each}
            </table>
        {/if}
    {:else if selectedPanel === "Learnset"}
        {#if selectedPokemonData.learnset}
            <table>
                <thead>
                    <tr>
                        <th>Level</th>
                        <th>Type</th>
                        <th>Move</th>
                        <th>Power</th>
                        <th>Accuracy</th>
                        <th>PP</th>
                    </tr>
                </thead>
                {#each selectedPokemonData.learnset as move}
                    <Move
                        bind:moveName={move.move}
                        bind:user={selectedPokemon}
                        readOnly={true}
                        learnset={true}
                        level={move.level}
                    />
                {/each}
            </table>
        {/if}
    {:else if selectedPanel === "TM/HM"}
        {#if selectedPokemonData.TMHM}
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Move</th>
                        <th>Power</th>
                        <th>Accuracy</th>
                        <th>PP</th>
                    </tr>
                </thead>
                {#each selectedPokemonData.TMHM as move}
                    <Move
                        bind:moveName={move}
                        bind:user={selectedPokemon}
                        readOnly={true}
                        TMHM={true}
                    />
                {/each}
            </table>
        {/if}
    {/if}
</div>

<style>
    img {
        image-rendering: -moz-crisp-edges;
        image-rendering: -webkit-crisp-edges;
        image-rendering: -o-crisp-edges;
        image-rendering: pixelated;
        image-rendering: crisp-edges;
        -ms-interpolation-mode: nearest-neighbor;
    }
    .type-heading {
        background-color: #343434;
        margin-bottom: 0;
        padding: 4px;
        text-align: center;
        border: 1px solid black;
        border-bottom: none;
    }
    .type-table {
        padding: 4px;
        display: grid;
        gap: 10px;
        grid-template-columns: repeat(4, 1fr);
        background-color: #343434;
        border: 1px solid black;
        border-top: none;
    }
</style>
