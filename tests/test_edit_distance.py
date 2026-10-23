from core.edit_distance import levenshtein_distance


def test_edit_distance():
    assert levenshtein_distance("apple", "apple") == 0
    assert levenshtein_distance("cat", "cut") == 1
    assert levenshtein_distance("aple", "apple") == 1
    assert levenshtein_distance("book", "back") == 2
    assert levenshtein_distance("", "cat") == 3
    assert levenshtein_distance("CAT", "cat") == 0

    print("All edit distance tests passed!")


if __name__ == "__main__":
    test_edit_distance()