const searchInput = document.getElementById("searchInput");
const suggestionsBox = document.getElementById("suggestions");

let currentRequest = null;

searchInput.addEventListener("input", async function () {
    const prefix = searchInput.value.trim();

    // Clear suggestions when the input is empty
    if (!prefix) {
        suggestionsBox.innerHTML = "";
        return;
    }

    // Cancel the previous request if it is still running
    if (currentRequest) {
        currentRequest.abort();
    }

    currentRequest = new AbortController();

    try {
        const response = await fetch(
            `/api/autocomplete?q=${encodeURIComponent(prefix)}&limit=5`,
            { signal: currentRequest.signal }
        );

        if (!response.ok) {
            throw new Error("Failed to fetch autocomplete suggestions.");
        }

        const data = await response.json();

        // Display the returned suggestions
        suggestionsBox.innerHTML = "";

        data.suggestions.forEach(function (word) {
            const item = document.createElement("div");

            item.textContent = word;
            item.className = "suggestion-item";

            item.addEventListener("click", function () {
                searchInput.value = word;
                suggestionsBox.innerHTML = "";
            });

            suggestionsBox.appendChild(item);
        });

    } catch (error) {
        if (error.name !== "AbortError") {
            console.error("Autocomplete error:", error);
        }
    }
});