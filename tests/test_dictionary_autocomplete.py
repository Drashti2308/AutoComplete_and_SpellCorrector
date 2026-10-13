from core.trie import Trie
from core.autocomplete import Autocomplete
from core.dictionary_loader import load_dictionary


def test_dictionary_autocomplete():
    print("Loading dictionary...")

    dictionary = load_dictionary()
    trie = Trie()

    print(f"Loaded {len(dictionary)} words.")

    print("Building Trie...")

    for word, frequency in dictionary:
        trie.insert(word, frequency)

    autocomplete = Autocomplete(trie)

    print("Testing autocomplete...")

    suggestions = autocomplete.get_suggestions("app", limit=5)

    print("\nSuggestions for 'app':")

    for word in suggestions:
        print(word)

    assert len(suggestions) <= 5

    for word in suggestions:
        assert word.startswith("app")
        assert trie.search(word)

    assert autocomplete.get_suggestions("xyzabc") == []

    print("\nDictionary autocomplete test passed!")


if __name__ == "__main__":
    test_dictionary_autocomplete()