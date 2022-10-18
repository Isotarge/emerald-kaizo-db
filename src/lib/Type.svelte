<script>
    import { typeData } from "../state";

    export let whichType;
    export let specialDefenseBias;

    $: whichType, specialDefenseBias, updateClasses();
    let classes = "sentiment-neutral";

    function getSentiment() {
        if (specialDefenseBias === 0) {
            return "neutral";
        }
        if (typeData[whichType].contact === "Physical") {
            return specialDefenseBias > 0 ? "positive" : "negative";
        } else {
            return specialDefenseBias < 0 ? "positive" : "negative";
        }
    }

    function updateClasses() {
        classes = `sentiment-${getSentiment()}`;
    }
</script>

<div style="background: {typeData[whichType].color}" class={classes}>
    <b>{whichType}</b>
</div>

<style>
    div {
        display: inline-block;
        --shadow-colour: #333;
        border: 3px var(--shadow-colour) solid;
        border-radius: 7px;
        text-align: center;
        padding: 5px;
        min-width: 50px;
        text-shadow: -1px -1px 0 var(--shadow-colour),
            1px -1px 0 var(--shadow-colour), -1px 1px 0 var(--shadow-colour),
            1px 1px 0 var(--shadow-colour);
    }
    .sentiment-positive {
        outline: 3px #393 solid;
    }
    .sentiment-negative {
        outline: 3px #933 solid;
    }
    .sentiment-neutral {
        outline: 3px #333 solid;
    }
</style>
