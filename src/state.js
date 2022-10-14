import POKEMON from "./pkmn.json";
import abilityData from "./abilities.json";
import typeData from "./types.json";
import encounters from "./encounters.json";
import moves from "./moves.json";

// Used to fill in the pokemon selector dropdown
export const pokemonNames = POKEMON.map(p => p.name);

POKEMON.forEach(p => p.totalBaseStats = p.hp + p.attack + p.defense + p.specialAttack + p.specialDefense + p.speed);

// Quick lookup for pokemon by name based on JSON data
function computePokemonByName() {
    const byName = {};
    POKEMON.forEach(pokemonData => byName[pokemonData.name] = pokemonData);
    return byName;
}
export const pokemonByName = computePokemonByName();

// Quick lookup for move by name based on JSON data
function computeMovesByName() {
    const byName = {};
    moves.forEach(moveData => byName[moveData.name] = moveData);
    return byName;
}
export const movesByName = computeMovesByName();

export { POKEMON as pokemon };

// Compute the base stat total of a given pokemon
export function getBaseStatTotal(pokemonData) {
    return (
        pokemonData.hp +
        pokemonData.attack +
        pokemonData.defense +
        pokemonData.specialAttack +
        pokemonData.specialDefense +
        pokemonData.speed
    );
}

// Compute the highest base stat total in the database
export const MAX_TOTAL_BASE_STATS = Object.values(POKEMON)
    .map(getBaseStatTotal)
    .reduce((a, b) => Math.max(a, b), -Infinity);

// 0.0 - 2.0
export function checkSingleTypeEffectiveness(attackingType, defendingType) {
    if (typeData[attackingType].matchup.offensive.superEffective.includes(defendingType)) {
        return 2.0;
    }
    if (typeData[attackingType].matchup.offensive.notVeryEffective.includes(defendingType)) {
        return 0.5;
    }
    if (typeData[attackingType].matchup.offensive.immune.includes(defendingType)) {
        return 0;
    }
    return 1.0;
}

// 0.0 - 4.0
export function checkTypeEffectiveness(attackingType, defendingType1, defendingType2) {
    const defendingType1Lookup = checkSingleTypeEffectiveness(attackingType, defendingType1);
    // Single type
    if (defendingType1 === defendingType2) {
        return defendingType1Lookup;
    }
    // Dual type
    const defendingType2Lookup = checkSingleTypeEffectiveness(attackingType, defendingType2);
    return defendingType1Lookup * defendingType2Lookup;
}

// 0.0 - 6.0
export function checkTypeEffectivenessSTAB(attackerType1, attackerType2, defenderType1, defenderType2, moveType) {
    const STABMultiplier = (attackerType1 === moveType || attackerType2 === moveType) ? 1.5 : 1.0;
    return checkTypeEffectiveness(moveType, defenderType1, defenderType2) * STABMultiplier;
}

// Compute opponent presets for all encounters
const encounterPresets = [];
encounters.forEach(location => {
    location.rooms.forEach(room => {
        let roomName = location.name;
        if (room.name !== 'main') {
            roomName = `${roomName} - ${room.name}`;
        }
        if (room.hasOwnProperty("grass")) {
            encounterPresets.push({
                name: roomName,
                team: room.grass,
            });
        }
        if (room.hasOwnProperty("surf")) {
            encounterPresets.push({
                name: `${roomName} - Surf`,
                team: room.surf,
            });
        }
        if (room.hasOwnProperty("oldRod")) {
            encounterPresets.push({
                name: `${roomName} - Old Rod`,
                team: room.oldRod,
            });
        }
        if (room.hasOwnProperty("goodRod")) {
            encounterPresets.push({
                name: `${roomName} - Good Rod`,
                team: room.goodRod,
            });
        }
        if (room.hasOwnProperty("superRod")) {
            encounterPresets.push({
                name: `${roomName} - Super Rod`,
                team: room.superRod,
            });
        }
    })
});

export { encounterPresets as encounterPresets };
export { abilityData as abilityData };
export { typeData as typeData };