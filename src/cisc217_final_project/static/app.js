"use strict";

const APP_ROOT = window.APP_ROOT || "";

const form =
    document.querySelector("#character-form");

const classSelect =
    document.querySelector("#class-id");

const list =
    document.querySelector("#character-list");

const status =
    document.querySelector("#status");

const summary =
    document.querySelector("#summary");

const history =
    document.querySelector("#history");


function show(message) {
    status.textContent = message;
}


async function loadClasses() {
    const response = await fetch(
        `${APP_ROOT}/classes`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load character classes."
        );
    }

    const data = await response.json();

    classSelect.innerHTML = "";

    for (const characterClass of data) {
        const option =
            document.createElement("option");

        option.value = characterClass.id;

        option.textContent =
            `${characterClass.name} - ` +
            `${characterClass.description}`;

        classSelect.appendChild(option);
    }
}


async function fight(id, enemy) {
    const response = await fetch(
        `${APP_ROOT}/characters/${id}/battle/` +
        `${encodeURIComponent(enemy)}`,
        {
            method: "POST",
        }
    );

    const body = await response.json();

    show(
        response.ok
            ? `${body.attacker} fought ${body.enemy} ` +
              `and gained ${body.experience_gained} XP`
            : body.detail
    );

    if (response.ok) {
        await loadAll();
    }
}


function render(characters) {
    list.innerHTML = "";

    for (const character of characters) {
        const item =
            document.createElement("li");

        item.className = "character-card";

        item.append(
            `${character.name} ` +
            `L${character.level} ` +
            `HP${character.health} ` +
            `P${character.power} ` +
            `XP${character.experience} `
        );

        for (
            const enemy of [
                "Slime",
                "Goblin",
                "Dragon",
            ]
        ) {
            const button =
                document.createElement("button");

            button.type = "button";
            button.textContent =
                `Fight ${enemy}`;

            button.addEventListener(
                "click",
                () => fight(
                    character.id,
                    enemy
                )
            );

            item.appendChild(button);
        }

        list.appendChild(item);
    }
}


async function loadAll() {
    const [
        charactersResponse,
        summaryResponse,
        historyResponse,
    ] = await Promise.all([
        fetch(`${APP_ROOT}/characters`),
        fetch(`${APP_ROOT}/party-summary`),
        fetch(`${APP_ROOT}/battle-history`),
    ]);

    if (
        !charactersResponse.ok ||
        !summaryResponse.ok ||
        !historyResponse.ok
    ) {
        throw new Error(
            "Unable to load application data."
        );
    }

    render(
        await charactersResponse.json()
    );

    summary.textContent =
        JSON.stringify(
            await summaryResponse.json(),
            null,
            2
        );

    history.innerHTML = "";

    for (
        const row of
        await historyResponse.json()
    ) {
        const item =
            document.createElement("li");

        item.textContent =
            `Character ${row.character_id} ` +
            `vs ${row.enemy_name}: ` +
            `+${row.experience_gained} XP`;

        history.appendChild(item);
    }
}


form.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const payload = {
            name:
                document
                    .querySelector("#name")
                    .value,

            class_id:
                Number(
                    classSelect.value
                ),

            health:
                Number(
                    document
                        .querySelector("#health")
                        .value
                ),

            power:
                Number(
                    document
                        .querySelector("#power")
                        .value
                ),
        };

        const response = await fetch(
            `${APP_ROOT}/characters`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",
                },

                body:
                    JSON.stringify(payload),
            }
        );

        const body =
            await response.json();

        show(
            response.ok
                ? `Created ${body.name}`
                : body.detail
        );

        if (response.ok) {
            form.reset();

            document
                .querySelector("#health")
                .value = "100";

            document
                .querySelector("#power")
                .value = "10";

            await loadAll();
        }
    }
);


document
    .querySelector("#refresh")
    .addEventListener(
        "click",
        loadAll
    );


Promise.all([
    loadClasses(),
    loadAll(),
]).catch((error) => {
    show(error.message);
});