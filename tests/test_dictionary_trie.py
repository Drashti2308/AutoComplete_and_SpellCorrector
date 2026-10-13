from core.trie import Trie
from core.dictionary_loader import load_dictionary


def test_dictionary_trie():
    print("Loading dictionary...")

    dictionary = load_dictionary()
    trie = Trie()

    print(f"Dictionary contains {len(dictionary)} words.")

    print("Inserting words into Trie...")

    for word, frequency in dictionary:
        trie.insert(word, frequency)

    print("Testing dictionary words...")

    assert trie.search("the") is True
    assert trie.search("apple") is True
    assert trie.search("computer") is True

    print("Testing invalid words...")

    assert trie.search("xyzabc123") is False
    assert trie.search("notawordxyz") is False

    print("Testing prefixes...")

    assert trie.starts_with("app") is True
    assert trie.starts_with("comp") is True
    assert trie.starts_with("xyzabc") is False

    print("All dictionary-Trie tests passed!")


if __name__ == "__main__":
    test_dictionary_trie()