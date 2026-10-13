from core.trie import Trie


def test_trie():
    trie = Trie()

    # Insert sample words
    trie.insert("apple", 100)
    trie.insert("app", 200)
    trie.insert("apply", 80)
    trie.insert("bat", 50)

    # Test exact word search
    assert trie.search("apple") is True
    assert trie.search("app") is True
    assert trie.search("bat") is True
    assert trie.search("appl") is False
    assert trie.search("banana") is False

    # Test prefix search
    assert trie.starts_with("app") is True
    assert trie.starts_with("appl") is True
    assert trie.starts_with("bat") is True
    assert trie.starts_with("xyz") is False

    # Test case-insensitive search
    assert trie.search("APPLE") is True

    print("All Trie tests passed!")


if __name__ == "__main__":
    test_trie()