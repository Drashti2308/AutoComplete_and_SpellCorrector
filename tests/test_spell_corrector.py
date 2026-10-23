from core.spell_corrector import SpellCorrector


def test_spell_corrector():
    dictionary = [
        ("apple", 100),
        ("ample", 80),
        ("apples", 60),
        ("banana", 90),
        ("computer", 120),
        ("hello", 200),
    ]

    corrector = SpellCorrector(dictionary, max_distance=2)

    assert "apple" in corrector.correct("aple")
    assert corrector.correct("hello") == ["hello"]
    assert corrector.correct("xyzabc") == []
    assert corrector.correct("") == []

    print("All spell corrector tests passed!")


if __name__ == "__main__":
    test_spell_corrector()
