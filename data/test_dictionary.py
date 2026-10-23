# test_dictionary.py
from dictionary_loader import contains_word, get_frequency, load_dictionary


def test_dictionary():
    data = load_dictionary()
    assert len(data) > 0, "Dictionary should not be empty"

    # Known words
    assert contains_word("apple") is True
    assert contains_word("Apple") is True  # case-insensitive check
    assert get_frequency("apple") > 0

    # Non-existent words
    assert contains_word("aple") is False
    assert get_frequency("aple") == 0

    # Edge cases
    assert contains_word("") is False
    assert get_frequency("") == 0
    assert contains_word("12345") is False

    print("All B3 dictionary tests passed successfully!")


if __name__ == "__main__":
    test_dictionary()