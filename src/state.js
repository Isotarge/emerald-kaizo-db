import POKEMON from "./pkmn.json";
import abilityData from "./abilities.json";
import typeData from "./types.json";
import encounters from "./encounters.json";
import moves from "./moves.json";

// Used to fill in the pokemon selector dropdown
export const pokemonNames = POKEMON.map(p => p.name);
export const moveNames = moves.map(p => p.name);

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

export function givePokemonDefaultMoves(pokemon) {
    // TODO: See GiveBoxMonInitialMoveset for implementation
}

export function moveDoesDamage(move) {
    return move.power > 0;
}

export function computeMoveEffectiveness(moveData, user, opponent) {
    // Move is not attacking, save some cycles
    if (!moveDoesDamage(moveData)) {
        return 0;
    }

    // Base power
    let effectiveness = moveData.power;

    // Base stat synergy
    const userData = pokemonByName[user.name];
    const opponentData = pokemonByName[opponent.name];
    const type = typeData[moveData.type];
    if (type.contact === "Physical") {
        effectiveness += userData.attack;
        effectiveness -= (opponentData.hp + opponentData.defense) / 2;
    } else if (type.contact === "Special") {
        effectiveness += userData.specialAttack;
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
        userData.type1,
        userData.type2,
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

export { POKEMON as pokemon };

// Compute the highest base stat total in the database
export const MAX_TOTAL_BASE_STATS = Object.values(POKEMON)
    .map(p => p.totalBaseStats)
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