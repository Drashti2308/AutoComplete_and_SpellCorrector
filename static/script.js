
const searchInput = document.getElementById("searchInput");
const suggestionsBox = document.getElementById("suggestions");
const correctionsBox = document.getElementById("corrections");

let typingTimer;

searchInput.addEventListener("input", () => {
    clearTimeout(typingTimer);

    const word = searchInput.value.trim();

    suggestionsBox.innerHTML = "";
    correctionsBox.innerHTML = "";

    if (!word) {
        return;
    }

    // Wait briefly so we do not send a request for every keystroke.
    typingTimer = setTimeout(() => {
        if (/\s/.test(word) || !/^[a-zA-Z]+$/.test(word)) {
            return;
        }

        if (word.length >= 2) {
            loadAutocomplete(word);
        }

        // Check spelling when the user has entered at least 3 characters.
        if (word.length >= 3) {
            loadCorrections(word);
        }
    }, 250);
});


async function loadAutocomplete(prefix) {
    try {
        const response = await fetch(
            `/api/autocomplete?q=${encodeURIComponent(prefix)}&limit=5`
        );

        if (!response.ok) {
            throw new Error("Autocomplete request failed");
        }

        const data = await response.json();

        // Ignore stale results if the user has changed the input.
        if (searchInput.value.trim() !== prefix) {
            return;
        }

        suggestionsBox.innerHTML = "";

        data.suggestions.forEach((word) => {
            const item = document.createElement("div");
            item.className = "suggestion-item";
            item.textContent = word;

            item.addEventListener("click", () => {
                searchInput.value = word;
                suggestionsBox.innerHTML = "";
                correctionsBox.innerHTML = "";
                searchInput.focus();
            });

            suggestionsBox.appendChild(item);
        });
    } catch (error) {
        console.error("Autocomplete error:", error);
    }
}


async function loadCorrections(word) {
    try {
        const response = await fetch(
            `/api/correct?q=${encodeURIComponent(word)}&limit=5`
        );

        if (!response.ok) {
            throw new Error("Spell-correction request failed");
        }

        const data = await response.json();

        // Ignore stale results if the user has changed the input.
        if (searchInput.value.trim() !== word) {
            return;
        }

        correctionsBox.innerHTML = "";

        // Do not show corrections when the input is already a valid word.
        if (
            data.suggestions.length === 1 &&
            data.suggestions[0].toLowerCase() === word.toLowerCase()
        ) {
            return;
        }

        if (data.suggestions.length === 0) {
            return;
        }

        const heading = document.createElement("h3");
        heading.textContent = "Spelling suggestions";
        correctionsBox.appendChild(heading);

        data.suggestions.forEach((correctedWord) => {
            const item = document.createElement("div");
            item.className = "correction-item";
            item.textContent = correctedWord;

            item.addEventListener("click", () => {
                searchInput.value = correctedWord;
                suggestionsBox.innerHTML = "";
                correctionsBox.innerHTML = "";
                searchInput.focus();
            });

            correctionsBox.appendChild(item);
        });
    } catch (error) {
        console.error("Spell-correction error:", error);
    }
}

