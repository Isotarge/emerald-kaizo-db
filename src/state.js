import POKEMON from "./pkmn.json";
import abilityData from "./abilities.json";
import typeData from "./types.json";
import encounters from "./encounters.json";
import moves from "./moves.json";

// Used to fill in the pokemon selector dropdown
export const pokemonNames = POKEMON.map(p => p.name);
export const moveNames = moves.map(p => p.name);

const TMHMBitfieldLookup = [
    "Focus Punch", // TM01
    "Dragon Claw", // TM02
    "Water Pulse", // TM03
    "Calm Mind", // TM04
    "Roar", // TM05
    "Toxic", // TM06
    "Hail", // TM07
    "Seismic Toss", // TM08
    "Bullet Seed", // TM09
    "Hidden Power", // TM10
    "Sunny Day", // TM11
    "Taunt", // TM12
    "Ice Beam", // TM13
    "Blizzard", // TM14
    "Hyper Beam", // TM15
    "Light Screen", // TM16
    "Protect", // TM17
    "Rain Dance", // TM18
    "Giga Drain", // TM19
    "Safeguard", // TM20
    "Frustration", // TM21
    "Solarbeam", // TM22
    "Iron Tail", // TM23
    "Thunderbolt", // TM24
    "Thunder", // TM25
    "Earthquake", // TM26
    "Return", // TM27
    "Dig", // TM28
    "Psychic", // TM29
    "Shadow Ball", // TM30
    "Brick Break", // TM31
    "Draco Meteor", // TM32
    "Reflect", // TM33
    "Shock Wave", // TM34
    "Flamethrower", // TM35
    "Sludge Bomb", // TM36
    "Sandstorm", // TM37
    "Fire Blast", // TM38
    "Rock Tomb", // TM39
    "Aerial Ace", // TM40
    "Torment", // TM41
    "Facade", // TM42
    "Secret Power", // TM43
    "Rest", // TM44
    "Attract", // TM45
    "Thief", // TM46
    "Steel Wing", // TM47
    "Skill Swap", // TM48
    "Snatch", // TM49
    "Overheat", // TM50
    "Cut", // HM01
    "Fly", // HM02
    "Surf", // HM03
    "Strength", // HM04
    "Flash", // HM05
    "Rock Smash", // HM06
    "Waterfall", // HM07
    "Dive", // HM08
];

function hexToUnsignedInt(hex) {
    let intArray = [];
    for (let n = 0; n < hex.length; n += 2) {
        intArray.push(parseInt(hex.substr(n, 2), 16));
    }
    return intArray;
}

// This could be done in Python, but I decided to do it when the user loads the page
// otherwise pkmn.json would be bloated by many copies of the move name strings
function getTMHMLearnset(pokemon) {
    if (!pokemon.TMHM || pokemon.TMHM === "0000000000000000") {
        pokemon.TMHM = [];
        return;
    }

    const rawBytes = hexToUnsignedInt(pokemon.TMHM);

    pokemon.TMHM = [];
    for (let byte = 0; byte < 8; byte++) {
        for (let bit = 0; bit < 8; bit++) {
            if (rawBytes[byte] & (1 << bit)) {
                pokemon.TMHM.push(TMHMBitfieldLookup[byte * 8 + bit]);
            }
        }
    }
}
POKEMON.forEach(getTMHMLearnset);

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
    const pokemonData = pokemonByName[pokemon.name];
    const pokemonLevel = pokemon?.level || pokemon?.maxLevel || 100;
    if (pokemonData.learnset && !pokemon.moves) {
        pokemon.moves = [];
        for (const move of pokemonData.learnset) {
            if (move.level > pokemonLevel) {
                break;
            }
            if (!pokemon.moves.includes(move.move)) {
                if (pokemon.moves.length < 4) {
                    // Happy path, the pokemon doesn't know the move and has an empty slot
                    pokemon.moves.push(move.move);
                } else {
                    // The pokemon doesn't know the move, but doesn't have any free slots
                    // The game deletes the move in the first slot and teaches the new move in the fourth slot in this case
                    pokemon.moves = [
                        pokemon.moves[1],
                        pokemon.moves[2],
                        pokemon.moves[3],
                        move.move,
                    ];
                }
            }
        }
    }
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