
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const suggestionsContainer = document.getElementById("suggestions");
    const correctionsContainer = document.getElementById("corrections");
    const clearButton = document.getElementById("clearButton");

    let requestNumber = 0;
    let debounceTimer;

    // Display a message inside a results section.
    function showMessage(container, message, isError = false) {
        container.replaceChildren();

        const paragraph = document.createElement("p");
        paragraph.className = isError ? "error-message" : "empty-state";
        paragraph.textContent = message;

        container.appendChild(paragraph);
    }

    // Select a suggestion and place it in the search input.
    function selectSuggestion(word) {
        searchInput.value = word;
        clearButton.hidden = false;

        requestNumber++;
        clearTimeout(debounceTimer);

        showMessage(
            suggestionsContainer,
            "Enter a prefix to explore more words."
        );

        showMessage(
            correctionsContainer,
            "Your selected word is ready."
        );

        searchInput.focus();
    }

    // Create a suggestion button.
    function createSuggestion(word, container, className) {
        const button = document.createElement("button");

        button.type = "button";
        button.className = className;
        button.textContent = word;
        button.setAttribute("aria-label", `Select ${word}`);
        button.setAttribute("role", "option");
        button.setAttribute("tabindex", "0");

        button.addEventListener("click", () => {
            selectSuggestion(word);
        });

        container.appendChild(button);
    }

    // Fetch suggestions from the Flask API.
    async function fetchSuggestions(
        url,
        container,
        className,
        emptyMessage
    ) {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(
                `Request failed with status ${response.status}`
            );
        }

        const data = await response.json();

        container.replaceChildren();

        if (
            !Array.isArray(data.suggestions) ||
            data.suggestions.length === 0
        ) {
            showMessage(container, emptyMessage);
            return;
        }

        data.suggestions.forEach((word) => {
            createSuggestion(word, container, className);
        });
    }

    // Search autocomplete and spelling-correction APIs.
    async function searchWords(query, currentRequest) {
        const encodedQuery = encodeURIComponent(query);

        showMessage(
            suggestionsContainer,
            "Finding matching words..."
        );

        showMessage(
            correctionsContainer,
            "Checking possible corrections..."
        );

        const autocompleteRequest = fetchSuggestions(
            `/api/autocomplete?q=${encodedQuery}&limit=5`,
            suggestionsContainer,
            "suggestion-item",
            "No autocomplete suggestions found."
        );

        const correctionRequest = fetchSuggestions(
            `/api/correct?q=${encodedQuery}&limit=5`,
            correctionsContainer,
            "correction-item",
            "No spelling corrections found."
        );

        const results = await Promise.allSettled([
            autocompleteRequest,
            correctionRequest
        ]);

        // Ignore results from an earlier search.
        if (currentRequest !== requestNumber) {
            return;
        }

        if (results[0].status === "rejected") {
            showMessage(
                suggestionsContainer,
                "Could not load autocomplete suggestions. Please try again.",
                true
            );
        }

        if (results[1].status === "rejected") {
            showMessage(
                correctionsContainer,
                "Could not load spelling corrections. Please try again.",
                true
            );
        }
    }

    // Get all currently displayed suggestion buttons.
    function getAllSuggestions() {
        return [
            ...suggestionsContainer.querySelectorAll("button"),
            ...correctionsContainer.querySelectorAll("button")
        ];
    }

    // Handle keyboard controls in the search input.
    searchInput.addEventListener("keydown", (event) => {
        const buttons = getAllSuggestions();

        if (event.key === "Escape") {
            requestNumber++;
            clearTimeout(debounceTimer);

            showMessage(
                suggestionsContainer,
                "Suggestions closed."
            );

            showMessage(
                correctionsContainer,
                "Spelling suggestions closed."
            );

            return;
        }

        if (buttons.length === 0) {
            return;
        }

        if (event.key === "ArrowDown") {
            event.preventDefault();
            buttons[0].focus();
        }

        if (event.key === "Enter") {
            event.preventDefault();
            buttons[0].click();
        }
    });

    // Enable keyboard navigation across both suggestion sections.
    function enableSuggestionNavigation(container) {
        container.addEventListener("keydown", (event) => {
            const buttons = getAllSuggestions();
            const currentIndex = buttons.indexOf(
                document.activeElement
            );

            if (currentIndex === -1) {
                return;
            }

            if (event.key === "ArrowDown") {
                event.preventDefault();

                const nextIndex =
                    (currentIndex + 1) % buttons.length;

                buttons[nextIndex].focus();
            }

            if (event.key === "ArrowUp") {
                event.preventDefault();

                const previousIndex =
                    (currentIndex - 1 + buttons.length) %
                    buttons.length;

                buttons[previousIndex].focus();
            }

            if (event.key === "Enter") {
                event.preventDefault();
                buttons[currentIndex].click();
            }

            if (event.key === "Escape") {
                event.preventDefault();
                searchInput.focus();
            }
        });
    }

    enableSuggestionNavigation(suggestionsContainer);
    enableSuggestionNavigation(correctionsContainer);

    // Search as the user types.
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim();

        clearButton.hidden = query.length === 0;

        requestNumber++;
        const currentRequest = requestNumber;

        clearTimeout(debounceTimer);

        if (!query) {
            showMessage(
                suggestionsContainer,
                "Suggestions will appear here."
            );

            showMessage(
                correctionsContainer,
                "Spelling suggestions will appear here."
            );

            return;
        }

        // Wait 250 milliseconds after typing before searching.
        debounceTimer = setTimeout(() => {
            searchWords(query, currentRequest);
        }, 250);
    });

    // Clear the input and reset both result sections.
    clearButton.addEventListener("click", () => {
        clearTimeout(debounceTimer);
        requestNumber++;

        searchInput.value = "";
        clearButton.hidden = true;

        showMessage(
            suggestionsContainer,
            "Suggestions will appear here."
        );

        showMessage(
            correctionsContainer,
            "Spelling suggestions will appear here."
        );

        searchInput.focus();
    });
});

