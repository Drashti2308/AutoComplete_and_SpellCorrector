from core.trie import Trie
from core.autocomplete import Autocomplete


def test_autocomplete():
    trie = Trie()

    # Insert sample words with frequencies
    trie.insert("apple", 100)
    trie.insert("application", 300)
    trie.insert("apply", 200)
    trie.insert("appreciate", 150)
    trie.insert("approach", 250)
    trie.insert("banana", 500)

    autocomplete = Autocomplete(trie)

    # Test prefix matching and frequency ranking
    suggestions = autocomplete.get_suggestions("app", limit=5)

    expected = [
        "application",
        "approach",
        "apply",
        "appreciate",
        "apple"
    ]

    assert suggestions == expected

    # Test a prefix matching only one word
    assert autocomplete.get_suggestions("ban") == ["banana"]

    # Test a prefix with no matches
    assert autocomplete.get_suggestions("xyz") == []

    # Test case-insensitive input
    assert autocomplete.get_suggestions("APP", limit=3) == [
        "application",
        "approach",
        "apply"
    ]

    # Test the limit
    assert len(autocomplete.get_suggestions("app", limit=2)) == 2

    print("All autocomplete tests passed!")


if __name__ == "__main__":
    test_autocomplete()